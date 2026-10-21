import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from decimal import Decimal
from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from backend.db import make_engine, session_factory
from backend.models.entities import (Business, User, InventoryItem, InventoryMovement, Supplier, SupplierOffer,
    Decision, DecisionOption, OperationalAlert, PurchaseOrder, Approval, AuditEvent, SimulationRun)
from backend.schemas.contracts import MonitorRequest, InventoryUpdate, OfferUpdate, Resolution, ScenarioRequest
from backend.services.procurement import audit, get_decision, monitor, require, resolve, transition
from backend.services.rules import coverage
from backend.services.seed import seed
from backend.adapters.orbyte import MockOrbyteConnector


def row(obj):
    if obj is None:
        return None
    result = {}
    for c in obj.__table__.columns:
        v = getattr(obj, c.name)
        if isinstance(v, Decimal):
            v = float(v)
        elif isinstance(v, datetime):
            v = v.replace(tzinfo=v.tzinfo or timezone.utc).isoformat()
        result[c.name] = v
    return result


def simulation_connection():
    enabled = os.getenv("MIROFISH_ALLOW_EXTERNAL", "false").lower() == "true"
    configured = bool(os.getenv("MIROFISH_BASE_URL"))
    return {"enabled": enabled and configured, "status": "CONFIGURED_UNVERIFIED" if enabled and configured else "UNAVAILABLE",
        "reason": "External execution configured; worker and upstream credentials must be verified." if enabled and configured else
            "MiroFish is unavailable. External execution is disabled; no LLM or Zep credentials have been verified.",
        "commit": "7657031ac01184afe2cb220f5ee3545573b5e843", "verified_live_run": False}


def create_app(database_url=None):
    engine = make_engine(database_url)
    factory = session_factory(engine)

    @asynccontextmanager
    async def lifespan(app):
        with factory() as db:
            seed(db)
        yield

    app = FastAPI(title="Orbyte DecisionOS — synthetic-data API", version="0.1.0", lifespan=lifespan)
    app.state.engine, app.state.sessions = engine, factory

    def db_session():
        with factory() as db:
            try:
                yield db
            except Exception:
                db.rollback()
                raise

    def actor(db=Depends(db_session), x_demo_user: str = Header(default="viewer-demo")):
        user = db.get(User, x_demo_user)
        if not user:
            raise HTTPException(401, "Unknown simulated user")
        return user

    @app.exception_handler(LookupError)
    async def not_found(request, exc):
        return JSONResponse(status_code=404, content={"detail": "Requested business record not found"})

    @app.exception_handler(IntegrityError)
    async def conflict(request, exc):
        return JSONResponse(status_code=409, content={"detail": "Concurrent or duplicate operation. Reload and retry with the same request key."})

    @app.exception_handler(SQLAlchemyError)
    async def database_failure(request, exc):
        return JSONResponse(status_code=503, content={"detail": "Database operation failed; no partial action was committed. Retry safely."})

    @app.get("/api/health")
    def health():
        return {"status": "ok", "synthetic": True, "authentication": "simulated roles only"}

    @app.get("/api/bootstrap")
    def bootstrap(db=Depends(db_session), user=Depends(actor)):
        def scoped(model):
            return [row(o) for o in db.scalars(select(model).where(model.business_id == user.business_id))]
        items = scoped(InventoryItem)
        for item in items:
            c = coverage(item["quantity"], item["daily_usage"])
            item["coverage_days"] = float(c) if c is not None else None
            item["at_risk"] = c is not None and c < Decimal(str(item["threshold_days"]))
        ds = scoped(Decision)
        ds.sort(key=lambda x: x["created_at"], reverse=True)
        audit_rows = [row(x) for x in db.scalars(select(AuditEvent).where(AuditEvent.business_id == user.business_id).order_by(AuditEvent.created_at.desc()).limit(100))]
        offers = [row(o) for o in db.scalars(select(SupplierOffer).join(Supplier).where(Supplier.business_id == user.business_id))]
        return {"business": row(db.get(Business, user.business_id)), "user": row(user), "users": scoped(User),
            "inventory": items, "suppliers": scoped(Supplier), "offers": offers, "decisions": ds,
            "audit": audit_rows, "simulations": sorted(scoped(SimulationRun), key=lambda x: x["created_at"], reverse=True),
            "connection": simulation_connection(), "synthetic": True}

    @app.post("/api/monitor")
    def run_monitor(body: MonitorRequest, db=Depends(db_session), user=Depends(actor)):
        d = monitor(db, user, body.item_id)
        db.commit()
        return row(d)

    @app.get("/api/decisions/{id}")
    def detail(id: str, db=Depends(db_session), user=Depends(actor)):
        d = get_decision(db, user, id)
        return {**row(d), "options": [row(o) for o in db.scalars(select(DecisionOption).where(DecisionOption.decision_id == id))],
            "approval": row(db.scalar(select(Approval).where(Approval.decision_id == id))),
            "purchase_order": row(db.scalar(select(PurchaseOrder).where(PurchaseOrder.decision_id == id))),
            "audit": [row(a) for a in db.scalars(select(AuditEvent).where(AuditEvent.decision_id == id).order_by(AuditEvent.created_at))]}

    @app.post("/api/decisions/{id}/resolve")
    def resolve_decision(id: str, body: Resolution, idempotency_key: Annotated[str, Header(min_length=8, max_length=100)],
                         db=Depends(db_session), user=Depends(actor)):
        result = resolve(db, user, id, body, idempotency_key)
        db.commit()
        return result

    @app.post("/api/decisions/{id}/refresh")
    def refresh_decision(id: str, db=Depends(db_session), user=Depends(actor)):
        require(user, {"owner", "manager"})
        d = get_decision(db, user, id)
        transition(db, user, d, "CANCELLED", "Superseded by a fresh evaluation")
        db.execute(update(OperationalAlert).where(OperationalAlert.decision_id == id).values(resolved=True))
        db.flush()
        fresh = monitor(db, user, d.item_id)
        db.commit()
        return row(fresh)

    @app.patch("/api/inventory/{id}")
    def inventory_update(id: str, body: InventoryUpdate, db=Depends(db_session), user=Depends(actor)):
        require(user, {"owner"})
        item = db.scalar(select(InventoryItem).where(InventoryItem.id == id, InventoryItem.business_id == user.business_id))
        if not item:
            raise HTTPException(404, "Item not found")
        before = row(item)
        values = body.model_dump(exclude={"reason", "expected_version"})
        changed = db.execute(update(InventoryItem).where(InventoryItem.id == id, InventoryItem.version == body.expected_version).values(
            **values, version=body.expected_version + 1))
        if changed.rowcount != 1:
            raise HTTPException(409, "Inventory changed; reload before editing")
        db.add(InventoryMovement(item_id=id, actor_id=user.id, delta=body.quantity - Decimal(str(before["quantity"])), reason=body.reason))
        db.flush(); db.refresh(item)
        audit(db, user, "INVENTORY_UPDATED", body.reason, before=before, after=row(item))
        db.commit()
        return row(item)

    @app.patch("/api/offers/{id}")
    def offer_update(id: str, body: OfferUpdate, db=Depends(db_session), user=Depends(actor)):
        require(user, {"owner"})
        offer = db.scalar(select(SupplierOffer).join(Supplier).where(SupplierOffer.id == id, Supplier.business_id == user.business_id))
        if not offer:
            raise HTTPException(404, "Offer not found")
        before = row(offer)
        changed = db.execute(update(SupplierOffer).where(SupplierOffer.id == id, SupplierOffer.version == body.expected_version).values(
            unit_price_sen=body.unit_price_sen, lead_days=body.lead_days, version=body.expected_version + 1))
        if changed.rowcount != 1:
            raise HTTPException(409, "Offer changed; reload before editing")
        db.flush(); db.refresh(offer)
        audit(db, user, "SUPPLIER_OFFER_UPDATED", body.reason, before=before, after=row(offer))
        db.commit()
        return row(offer)

    @app.post("/api/simulations", status_code=202)
    def queue_simulation(body: ScenarioRequest, db=Depends(db_session), user=Depends(actor)):
        require(user, {"owner"})
        from backend.services.scenarios import build_scenario
        scenario = build_scenario(body, MockOrbyteConnector(db, user.business_id).procurement_context(body.item_id))
        connection = simulation_connection()
        run = SimulationRun(business_id=user.business_id, actor_id=user.id, scenario=scenario,
            status="QUEUED" if connection["enabled"] else "UNAVAILABLE",
            error=None if connection["enabled"] else connection["reason"],
            provenance={"upstream_commit": connection["commit"], "genuine_completed_run": False})
        db.add(run); db.flush()
        audit(db, user, "SIMULATION_REQUESTED", "Hypothetical stakeholder scenario; no operational action", after={"run_id": run.id, "status": run.status})
        db.commit()
        return row(run)

    @app.get("/api/simulations/{id}")
    def simulation_detail(id: str, db=Depends(db_session), user=Depends(actor)):
        run = db.scalar(select(SimulationRun).where(SimulationRun.id == id, SimulationRun.business_id == user.business_id))
        if not run:
            raise HTTPException(404, "Simulation not found")
        return row(run)

    @app.post("/api/simulations/{id}/cancel")
    def cancel_simulation(id: str, db=Depends(db_session), user=Depends(actor)):
        require(user, {"owner"})
        run = db.scalar(select(SimulationRun).where(SimulationRun.id == id, SimulationRun.business_id == user.business_id))
        if not run:
            raise HTTPException(404, "Simulation not found")
        if run.status not in {"QUEUED", "RUNNING", "CANCEL_REQUESTED"}:
            raise HTTPException(409, "Run is already terminal")
        run.cancel_requested = True
        run.status = "CANCELLED" if run.status == "QUEUED" else "CANCEL_REQUESTED"
        audit(db, user, "SIMULATION_CANCELLATION_REQUESTED", "Owner requested cancellation", after={"run_id": id})
        db.commit()
        return row(run)

    return app


app = create_app()
