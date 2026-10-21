from fastapi import HTTPException
from sqlalchemy import select, update
from backend.models.entities import Decision, DecisionOption, OperationalAlert, Approval, PurchaseOrder, AuditEvent, IdempotencyRecord
from backend.adapters.orbyte import MockOrbyteConnector, fingerprint
from backend.services.rules import evaluate


def audit(db, user, action, reason, decision_id=None, before=None, after=None):
    db.add(AuditEvent(business_id=user.business_id, actor_id=user.id, action=action, reason=reason,
        decision_id=decision_id, before=before or {}, after=after or {}))


def require(user, roles):
    if user.role not in roles:
        raise HTTPException(403, "This simulated role is not authorised for that action")


def get_decision(db, user, id):
    d = db.scalar(select(Decision).where(Decision.id == id, Decision.business_id == user.business_id))
    if not d:
        raise HTTPException(404, "Decision not found")
    return d


def transition(db, user, decision, status, reason):
    before = decision.status
    allowed = {"DETECTED": {"EVALUATED", "FAILED"}, "EVALUATED": {"PENDING_APPROVAL"},
        "PENDING_APPROVAL": {"APPROVED", "REJECTED", "CANCELLED"}}
    if status not in allowed.get(before, set()):
        raise HTTPException(409, "Invalid decision transition")
    decision.status = status
    if status in {"APPROVED", "REJECTED", "CANCELLED", "FAILED"}:
        decision.active_key = None
    audit(db, user, status, reason, decision.id, {"status": before}, {"status": status})


def monitor(db, user, item_id):
    require(user, {"owner", "manager"})
    context = MockOrbyteConnector(db, user.business_id).procurement_context(item_id)
    active = db.scalar(select(Decision).where(Decision.active_key == f"{user.business_id}:{item_id}"))
    if active:
        return active
    try:
        result = evaluate(context)
    except ValueError as exc:
        d = Decision(business_id=user.business_id, item_id=item_id, snapshot=context, fingerprint=fingerprint(context), status="DETECTED")
        db.add(d); db.flush()
        audit(db, user, "DETECTED", "Inventory check requested", d.id, after={"status": "DETECTED"})
        d.evaluation = {"error": str(exc)}
        transition(db, user, d, "FAILED", str(exc))
        return d
    if not result["triggered"]:
        raise HTTPException(409, "Stock coverage is at or above the threshold; no shortage decision is needed")
    d = Decision(business_id=user.business_id, item_id=item_id, active_key=f"{user.business_id}:{item_id}",
        snapshot=context, fingerprint=fingerprint(context), status="DETECTED", evaluation=result)
    db.add(d); db.flush()
    audit(db, user, "DETECTED", "Stock coverage fell below the configured threshold", d.id, after={"status": "DETECTED"})
    transition(db, user, d, "EVALUATED", "Deterministic supplier comparison completed")
    db.add_all([DecisionOption(decision_id=d.id, offer_id=o["id"], details=o) for o in result["options"]])
    db.add(OperationalAlert(decision_id=d.id, message=f"{context['item']['name']}: {result['coverage_days']:g} days of stock; owner decision required"))
    transition(db, user, d, "PENDING_APPROVAL", "Awaiting an authorised owner; no order has been placed")
    return d


def resolve(db, user, decision_id, request, key):
    require(user, {"owner"})
    payload_hash = fingerprint({"decision_id": decision_id, **request.model_dump()})
    previous = db.scalar(select(IdempotencyRecord).where(IdempotencyRecord.actor_id == user.id, IdempotencyRecord.key == key))
    if previous:
        if previous.fingerprint != payload_hash:
            raise HTTPException(409, "Idempotency key was already used for a different request")
        return previous.result
    d = get_decision(db, user, decision_id)
    if d.status != "PENDING_APPROVAL":
        raise HTTPException(409, "Decision is no longer pending")
    option = None
    if request.action == "approve":
        current = MockOrbyteConnector(db, user.business_id).procurement_context(d.item_id)
        if fingerprint(current) != d.fingerprint:
            raise HTTPException(409, "Inputs changed since evaluation. Refresh the decision before approving.")
        option = db.scalar(select(DecisionOption).where(DecisionOption.id == request.option_id, DecisionOption.decision_id == d.id))
        if not option:
            raise HTTPException(422, "Select a valid supplier option")
        if option.details["stockout_risk"] and not request.acknowledge_risk:
            raise HTTPException(422, "Acknowledge the stockout risk before approving this supplier")
    target = {"approve": "APPROVED", "reject": "REJECTED", "cancel": "CANCELLED"}[request.action]
    claim = db.execute(update(Decision).where(Decision.id == d.id, Decision.status == "PENDING_APPROVAL").values(
        status=target, active_key=None).execution_options(synchronize_session=False))
    if claim.rowcount != 1:
        raise HTTPException(409, "Another request already resolved this decision")
    db.add(Approval(decision_id=d.id, actor_id=user.id, outcome=target, reason=request.reason))
    po = None
    if option:
        po = PurchaseOrder(decision_id=d.id, supplier_id=option.details["supplier_id"], details={
            "status": "SYNTHETIC_DRAFT", "currency": "MYR", "item": d.snapshot["item"]["name"],
            "unit": d.snapshot["item"]["unit"], "quantity": d.evaluation["purchase_quantity"],
            "supplier": option.details["supplier_name"], "total_sen": option.details["total_sen"],
            "unit_price_sen": option.details["unit_price_sen"], "lead_days": option.details["lead_days"],
            "notice": "Simulation only. Not sent to a supplier. No payment or inventory receipt."})
        db.add(po); db.flush()
    db.execute(update(OperationalAlert).where(OperationalAlert.decision_id == d.id).values(resolved=True))
    result = {"decision_id": d.id, "status": target, "purchase_order_id": po.id if po else None}
    audit(db, user, target, request.reason, d.id, {"status": "PENDING_APPROVAL"}, result)
    if po:
        audit(db, user, "PURCHASE_ORDER_DRAFT_CREATED", "Synthetic draft generated after owner approval", d.id, after=po.details)
    db.add(IdempotencyRecord(actor_id=user.id, key=key, fingerprint=payload_hash, result=result))
    db.flush()
    return result
