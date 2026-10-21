import pytest
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy import event, select, func
from backend.api.app import create_app
from backend.models.entities import PurchaseOrder, Approval, AuditEvent, Decision, InventoryItem
from backend.services.rules import coverage, evaluate

OWNER = {"X-Demo-User": "owner-demo"}
MANAGER = {"X-Demo-User": "manager-demo"}


@pytest.fixture
def app(tmp_path):
    return create_app(f"sqlite:///{tmp_path / 'test.db'}")


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


def pending(client):
    r = client.post("/api/monitor", json={"item_id": "milk"}, headers=MANAGER)
    assert r.status_code == 200, r.text
    return client.get(f"/api/decisions/{r.json()['id']}", headers=OWNER).json()


def approve(client, d, key="approval-0001", offer="offer-b", headers=None, **extra):
    option = next(o for o in d["options"] if o["offer_id"] == offer)
    return client.post(f"/api/decisions/{d['id']}/resolve", headers={**(headers or OWNER), "Idempotency-Key": key},
        json={"action": "approve", "option_id": option["id"], "reason": "Keep the café supplied", **extra})


def test_expected_arithmetic_and_journey(client):
    d = pending(client)
    assert d["evaluation"]["coverage_days"] == 1.5
    a, b = d["evaluation"]["options"]
    assert [a["total_sen"], b["total_sen"], b["premium_sen"]] == [57000, 66000, 9000]
    assert a["stockout_risk"] and a["stockout_gap_days"] == 2.5
    assert not b["stockout_risk"] and b["coverage_after_arrival_days"] == 5.5
    assert [a["action"] for a in d["audit"]] == ["DETECTED", "EVALUATED", "PENDING_APPROVAL"]
    r = approve(client, d)
    assert r.status_code == 200
    detail = client.get(f"/api/decisions/{d['id']}", headers=OWNER).json()
    assert detail["status"] == "APPROVED"
    assert detail["purchase_order"]["details"]["total_sen"] == 66000
    assert detail["audit"][-1]["action"] == "PURCHASE_ORDER_DRAFT_CREATED"
    assert client.get('/api/bootstrap', headers=OWNER).json()['inventory'][0]['quantity'] == 18


def test_permissions_and_unknown_actor(client):
    assert client.post('/api/monitor', json={'item_id': 'milk'}).status_code == 403
    assert client.get('/api/bootstrap', headers={'X-Demo-User': 'fake'}).status_code == 401
    d = pending(client)
    assert approve(client, d, headers=MANAGER).status_code == 403


def test_idempotency_and_no_duplicate_orders(client, app):
    d = pending(client)
    a = approve(client, d); b = approve(client, d)
    assert a.status_code == b.status_code == 200 and a.json() == b.json()
    assert approve(client, d, key="different-key").status_code == 409
    assert approve(client, d, offer="offer-a", acknowledge_risk=True).status_code == 409
    with app.state.sessions() as db:
        assert db.scalar(select(func.count()).select_from(PurchaseOrder)) == 1
        assert db.scalar(select(func.count()).select_from(Approval)) == 1


def test_parallel_approval_never_duplicates(client, app):
    d = pending(client)
    with ThreadPoolExecutor(2) as pool:
        responses = list(pool.map(lambda key: approve(client, d, key=key), ['parallel-01', 'parallel-02']))
    assert sum(r.status_code == 200 for r in responses) == 1
    assert all(r.status_code in {200, 409, 503} for r in responses)
    with app.state.sessions() as db:
        assert db.scalar(select(func.count()).select_from(PurchaseOrder)) == 1


@pytest.mark.parametrize('action', ['reject', 'cancel'])
def test_reject_cancel(client, action):
    d = pending(client)
    r = client.post(f"/api/decisions/{d['id']}/resolve", headers={**OWNER, 'Idempotency-Key': 'reject-or-cancel'}, json={'action': action, 'reason': 'Do not proceed'})
    assert r.status_code == 200
    assert r.json()['purchase_order_id'] is None
    assert approve(client, d).status_code == 409


def test_stockout_requires_acknowledgement(client):
    d = pending(client)
    assert approve(client, d, offer='offer-a').status_code == 422
    assert approve(client, d, offer='offer-a', acknowledge_risk=True).status_code == 200


@pytest.mark.parametrize('field,value', [('unit_price_sen', 1200), ('lead_days', 5)])
def test_stale_offer_requires_refresh(client, field, value):
    d = pending(client)
    payload = {'unit_price_sen': 1100, 'lead_days': 1, 'expected_version': 1, 'reason': 'Updated synthetic quotation', field: value}
    assert client.patch('/api/offers/offer-b', headers=OWNER, json=payload).status_code == 200
    assert approve(client, d).status_code == 409
    r = client.post(f"/api/decisions/{d['id']}/refresh", headers=MANAGER)
    assert r.status_code == 200 and r.json()['id'] != d['id']
    fresh = client.get(f"/api/decisions/{r.json()['id']}", headers=OWNER).json()
    assert approve(client, fresh, acknowledge_risk=True).status_code == 200


def test_inventory_update_and_validation(client):
    d = pending(client)
    payload = {'quantity': 12, 'daily_usage': 12, 'threshold_days': 3, 'purchase_quantity': 60, 'expected_version': 1, 'reason': 'Stock count correction'}
    assert client.patch('/api/inventory/milk', headers=MANAGER, json=payload).status_code == 403
    assert client.patch('/api/inventory/milk', headers=OWNER, json={**payload, 'quantity': -1}).status_code == 422
    assert client.patch('/api/inventory/milk', headers=OWNER, json={**payload, 'daily_usage': 'NaN'}).status_code == 422
    assert client.patch('/api/inventory/milk', headers=OWNER, json=payload).status_code == 200
    assert client.patch('/api/inventory/milk', headers=OWNER, json=payload).status_code == 409
    assert approve(client, d).status_code == 409


def test_monitor_deduplicates(client):
    assert pending(client)['id'] == pending(client)['id']


def test_missing_and_zero_usage(client, app):
    assert client.post('/api/monitor', headers=MANAGER, json={'item_id': 'absent'}).status_code == 404
    assert client.post('/api/monitor', headers=MANAGER, json={}).status_code == 422
    with app.state.sessions() as db:
        db.get(InventoryItem, 'milk').daily_usage = 0
        db.commit()
    r = client.post('/api/monitor', headers=MANAGER, json={'item_id': 'milk'})
    assert r.json()['status'] == 'FAILED' and 'zero' in r.json()['evaluation']['error']


def test_threshold_boundary(client):
    p = {'quantity': 36, 'daily_usage': 12, 'threshold_days': 3, 'purchase_quantity': 60, 'expected_version': 1, 'reason': 'Boundary test'}
    client.patch('/api/inventory/milk', headers=OWNER, json=p)
    assert client.post('/api/monitor', headers=MANAGER, json={'item_id': 'milk'}).status_code == 409
    assert coverage(18, 12) == Decimal('1.5') and coverage(10, 0) is None
    with pytest.raises(ValueError): coverage(-1, 12)


def test_transaction_failure_rolls_back_everything(client, app):
    d = pending(client)
    def fail(conn, cursor, statement, parameters, context, many):
        if statement.startswith('INSERT INTO purchase_order_drafts'):
            from sqlalchemy.exc import OperationalError
            raise OperationalError(statement, parameters, Exception('injected disk failure'))
    event.listen(app.state.engine, 'before_cursor_execute', fail)
    try:
        assert approve(client, d).status_code == 503
    finally:
        event.remove(app.state.engine, 'before_cursor_execute', fail)
    detail = client.get(f"/api/decisions/{d['id']}", headers=OWNER).json()
    assert detail['status'] == 'PENDING_APPROVAL' and detail['approval'] is None and detail['purchase_order'] is None
    assert len(detail['audit']) == 3
    assert approve(client, d).status_code == 200


def test_restart_persists(tmp_path):
    url = f"sqlite:///{tmp_path / 'persistent.db'}"
    with TestClient(create_app(url)) as c:
        d = pending(c); approve(c, d)
    with TestClient(create_app(url)) as c:
        r = c.get(f"/api/decisions/{d['id']}", headers=OWNER).json()
        assert r['status'] == 'APPROVED' and len(r['audit']) == 5


def test_unavailable_simulation_does_not_fake_report(client, monkeypatch):
    monkeypatch.setenv('MIROFISH_ALLOW_EXTERNAL', 'false')
    r = client.post('/api/simulations', headers=OWNER, json={})
    assert r.status_code == 202 and r.json()['status'] == 'UNAVAILABLE'
    assert r.json()['report'] is None and r.json()['token_usage'] is None
    assert pending(client)['status'] == 'PENDING_APPROVAL'
