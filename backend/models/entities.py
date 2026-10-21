"""Business-owned records. Money is stored in integer sen, never floating point."""
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def uid():
    return str(uuid4())


def now():
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Business(Base):
    __tablename__ = "businesses"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    currency: Mapped[str] = mapped_column(String(3), default="MYR")


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[str] = mapped_column(String(30), primary_key=True)


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"))
    name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(ForeignKey("roles.id"))


class InventoryItem(Base):
    __tablename__ = "inventory_items"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"))
    name: Mapped[str] = mapped_column(String(120))
    unit: Mapped[str] = mapped_column(String(30))
    quantity: Mapped[float] = mapped_column(Numeric(12, 3))
    daily_usage: Mapped[float] = mapped_column(Numeric(12, 3))
    threshold_days: Mapped[float] = mapped_column(Numeric(8, 3))
    purchase_quantity: Mapped[float] = mapped_column(Numeric(12, 3))
    version: Mapped[int] = mapped_column(Integer, default=1)


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"
    id: Mapped[str] = mapped_column(String(40), primary_key=True, default=uid)
    item_id: Mapped[str] = mapped_column(ForeignKey("inventory_items.id"))
    actor_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    delta: Mapped[float] = mapped_column(Numeric(12, 3))
    reason: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Supplier(Base):
    __tablename__ = "suppliers"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"))
    name: Mapped[str] = mapped_column(String(120))
    established: Mapped[bool] = mapped_column(Boolean, default=True)


class SupplierOffer(Base):
    __tablename__ = "supplier_offers"
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    supplier_id: Mapped[str] = mapped_column(ForeignKey("suppliers.id"))
    item_id: Mapped[str] = mapped_column(ForeignKey("inventory_items.id"))
    unit_price_sen: Mapped[int] = mapped_column(Integer)
    lead_days: Mapped[float] = mapped_column(Numeric(8, 3))
    version: Mapped[int] = mapped_column(Integer, default=1)


class Decision(Base):
    __tablename__ = "decisions"
    id: Mapped[str] = mapped_column(String(40), primary_key=True, default=uid)
    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"), index=True)
    item_id: Mapped[str] = mapped_column(ForeignKey("inventory_items.id"))
    # NULL on terminal decisions; a unique value protects concurrent monitoring.
    active_key: Mapped[str | None] = mapped_column(String(100), unique=True)
    status: Mapped[str] = mapped_column(String(30), default="DETECTED")
    snapshot: Mapped[dict] = mapped_column(JSON, default=dict)
    fingerprint: Mapped[str] = mapped_column(String(64), default="")
    evaluation: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class DecisionOption(Base):
    __tablename__ = "decision_options"
    id: Mapped[str] = mapped_column(String(40), primary_key=True, default=uid)
    decision_id: Mapped[str] = mapped_column(ForeignKey("decisions.id"), index=True)
    offer_id: Mapped[str] = mapped_column(ForeignKey("supplier_offers.id"))
    details: Mapped[dict] = mapped_column(JSON)


class OperationalAlert(Base):
    __tablename__ = "operational_alerts"
    id: Mapped[str] = mapped_column(String(40), primary_key=True, default=uid)
    decision_id: Mapped[str] = mapped_column(ForeignKey("decisions.id"), unique=True)
    message: Mapped[str] = mapped_column(Text)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False)


class Approval(Base):
    __tablename__ = "approvals"
    id: Mapped[str] = mapped_column(String(40), primary_key=True, default=uid)
    decision_id: Mapped[str] = mapped_column(ForeignKey("decisions.id"), unique=True)
    actor_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    outcome: Mapped[str] = mapped_column(String(30))
    reason: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class PurchaseOrder(Base):
    __tablename__ = "purchase_order_drafts"
    id: Mapped[str] = mapped_column(String(40), primary_key=True, default=uid)
    decision_id: Mapped[str] = mapped_column(ForeignKey("decisions.id"), unique=True)
    supplier_id: Mapped[str] = mapped_column(ForeignKey("suppliers.id"))
    details: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[str] = mapped_column(String(40), primary_key=True, default=uid)
    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"), index=True)
    actor_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    decision_id: Mapped[str | None] = mapped_column(ForeignKey("decisions.id"))
    action: Mapped[str] = mapped_column(String(80))
    before: Mapped[dict] = mapped_column(JSON, default=dict)
    after: Mapped[dict] = mapped_column(JSON, default=dict)
    reason: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class IdempotencyRecord(Base):
    __tablename__ = "idempotency_records"
    __table_args__ = (UniqueConstraint("actor_id", "key"),)
    id: Mapped[str] = mapped_column(String(40), primary_key=True, default=uid)
    actor_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    key: Mapped[str] = mapped_column(String(100))
    fingerprint: Mapped[str] = mapped_column(String(64))
    result: Mapped[dict] = mapped_column(JSON)


class SimulationRun(Base):
    __tablename__ = "simulation_runs"
    id: Mapped[str] = mapped_column(String(40), primary_key=True, default=uid)
    business_id: Mapped[str] = mapped_column(ForeignKey("businesses.id"), index=True)
    actor_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(40), default="QUEUED")
    scenario: Mapped[dict] = mapped_column(JSON)
    provenance: Mapped[dict] = mapped_column(JSON, default=dict)
    report: Mapped[dict | None] = mapped_column(JSON)
    error: Mapped[str | None] = mapped_column(Text)
    cancel_requested: Mapped[bool] = mapped_column(Boolean, default=False)
    elapsed_seconds: Mapped[int | None] = mapped_column(Integer)
    token_usage: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
