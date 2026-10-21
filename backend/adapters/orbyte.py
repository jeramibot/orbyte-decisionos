"""Own interface assumptions; this is not an official Orbyte integration."""
import hashlib
import json
from sqlalchemy import select
from backend.models.entities import InventoryItem, Supplier, SupplierOffer


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class MockOrbyteConnector:
    def __init__(self, db, business_id):
        self.db, self.business_id = db, business_id

    def procurement_context(self, item_id):
        item = self.db.scalar(select(InventoryItem).where(InventoryItem.id == item_id, InventoryItem.business_id == self.business_id))
        if not item:
            raise LookupError("Inventory item not found")
        offers = self.db.execute(select(SupplierOffer, Supplier).join(Supplier).where(
            SupplierOffer.item_id == item.id, Supplier.business_id == self.business_id).order_by(SupplierOffer.id)).all()
        return {"connector": "mock-orbyte-v1", "synthetic": True, "business_id": self.business_id,
            "item": {"id": item.id, "name": item.name, "unit": item.unit, "version": item.version,
                **{k: str(getattr(item, k)) for k in ("quantity", "daily_usage", "threshold_days", "purchase_quantity")}},
            "offers": [{"id": o.id, "supplier_id": s.id, "supplier_name": s.name, "established": s.established,
                "unit_price_sen": o.unit_price_sen, "lead_days": float(o.lead_days), "version": o.version} for o, s in offers]}
