from backend.models.entities import Business, Role, User, InventoryItem, Supplier, SupplierOffer


def seed(db):
    if db.get(Business, "cafe-demo"):
        return
    db.add(Business(id="cafe-demo", name="Kopi & Co. · Synthetic café", currency="MYR"))
    db.add_all([Role(id=r) for r in ("owner", "manager", "viewer")]); db.flush()
    db.add_all([User(id=f"{r}-demo", business_id="cafe-demo", name=n, role=r) for r, n in [
        ("owner", "Demo owner"), ("manager", "Demo purchasing manager"), ("viewer", "Demo observer")]])
    db.add_all([InventoryItem(id=id, business_id="cafe-demo", name=name, unit=unit, quantity=q,
        daily_usage=u, threshold_days=t, purchase_quantity=p) for id, name, unit, q, u, t, p in [
        ("milk", "Fresh milk", "litres", 18, 12, 3, 60), ("coffee", "Coffee beans", "kg", 16, 2, 3, 10),
        ("oat", "Oat milk", "litres", 24, 4, 3, 24), ("cups", "Takeaway cups", "units", 500, 80, 3, 500)]])
    db.add_all([Supplier(id="supplier-a", business_id="cafe-demo", name="Supplier A · Valley Dairy", established=True),
        Supplier(id="supplier-b", business_id="cafe-demo", name="Supplier B · Metro Fresh", established=True)])
    db.flush()
    db.add_all([SupplierOffer(id="offer-a", supplier_id="supplier-a", item_id="milk", unit_price_sen=950, lead_days=4),
        SupplierOffer(id="offer-b", supplier_id="supplier-b", item_id="milk", unit_price_sen=1100, lead_days=1)])
    db.commit()
