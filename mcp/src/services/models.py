from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone
from decimal import Decimal
import uuid

if TYPE_CHECKING:
    pass

__all__ = [
    "User", "Company", "Contact",
    "Lead", "LeadSource", "Deal", "PipelineStage", "DealStageHistory",
    "Meeting", "Activity", "Task",
    "Campaign", "CampaignMember", "EmailTemplate", "Sequence",
    "Product", "PriceBook", "PriceBookEntry", "Quote", "QuoteLineItem", "Order", "Invoice",
    "Webhook", "WebhookEvent", "Integration", "AutomationRule", "ApiKey",
]

def utcnow():
    return datetime.now(timezone.utc)


class TimestampMixin(SQLModel):
    created_at: datetime = Field(default_factory=utcnow, nullable=False, index=True)
    updated_at: datetime = Field(default_factory=utcnow, nullable=False, sa_column_kwargs={"onupdate": utcnow})
    deleted_at: Optional[datetime] = Field(default=None, index=True)


# ──────────────────────────────────────────────
# Phase 1: Core CRM
# ──────────────────────────────────────────────

class User(TimestampMixin, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str = Field(nullable=False, index=True)
    email: str = Field(unique=True, nullable=False, index=True)
    role: str = Field(nullable=False, index=True)  # admin, manager, rep
    team: Optional[str] = Field(default=None, index=True)
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool = Field(default=True, index=True)


class Company(TimestampMixin, table=True):
    __tablename__ = "companies"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    company_name: str = Field(nullable=False, index=True)
    industry: Optional[str] = Field(default=None, index=True)
    employee_count: Optional[int] = None
    location: Optional[str] = None
    domain: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    linkedin_url: Optional[str] = None
    annual_revenue: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    description: Optional[str] = None
    is_active: bool = Field(default=True, index=True)


class Contact(TimestampMixin, table=True):
    __tablename__ = "contacts"

    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: uuid.UUID = Field(foreign_key="companies.id", index=True)
    first_name: str = Field(nullable=False, index=True)
    last_name: str = Field(nullable=False, index=True)
    email: str = Field(nullable=False, index=True)
    phone: Optional[str] = None
    mobile: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    linkedin_url: Optional[str] = None
    is_primary_contact: bool = Field(default=False)
    is_active: bool = Field(default=True, index=True)


# ──────────────────────────────────────────────
# Phase 2: Leads & Pipeline
# ──────────────────────────────────────────────

class LeadSource(SQLModel, table=True):
    __tablename__ = "lead_sources"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False)
    description: Optional[str] = None


class Lead(TimestampMixin, table=True):
    __tablename__ = "leads"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    company_name: Optional[str] = None
    contact_name: str = Field(nullable=False)
    email: str = Field(nullable=False, index=True)
    phone: Optional[str] = None
    source_id: Optional[int] = Field(default=None, foreign_key="lead_sources.id", index=True)
    source_detail: Optional[str] = None
    status: str = Field(default="new", index=True)  # new, contacted, qualified, disqualified
    qualification_score: Optional[int] = Field(default=None, ge=0, le=100)
    notes: Optional[str] = None
    assigned_to: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id", index=True)
    converted_to_deal_id: Optional[uuid.UUID] = Field(default=None, foreign_key="deals.id")
    is_active: bool = Field(default=True, index=True)


class PipelineStage(SQLModel, table=True):
    __tablename__ = "pipeline_stages"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, index=True)
    display_order: int = Field(default=0)
    probability: int = Field(default=0, ge=0, le=100)
    category: str = Field(default="active")  # active, won, lost
    color_hex: Optional[str] = None


class Deal(TimestampMixin, table=True):
    __tablename__ = "deals"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str = Field(nullable=False, index=True)
    company_id: uuid.UUID = Field(foreign_key="companies.id", index=True, nullable=False)
    contact_id: Optional[int] = Field(default=None, foreign_key="contacts.id")
    stage_id: int = Field(foreign_key="pipeline_stages.id", index=True, nullable=False)
    owner_id: uuid.UUID = Field(foreign_key="users.id", index=True, nullable=False)
    value: Decimal = Field(default=Decimal("0.00"), max_digits=15, decimal_places=2)
    currency: str = Field(default="USD")
    expected_close_date: Optional[datetime] = None
    actual_close_date: Optional[datetime] = None
    loss_reason: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = Field(default=True, index=True)


class DealStageHistory(SQLModel, table=True):
    __tablename__ = "deal_stage_history"

    id: Optional[int] = Field(default=None, primary_key=True)
    deal_id: uuid.UUID = Field(foreign_key="deals.id", index=True, nullable=False)
    from_stage_id: Optional[int] = Field(default=None, foreign_key="pipeline_stages.id")
    to_stage_id: int = Field(foreign_key="pipeline_stages.id", nullable=False)
    changed_by: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    changed_at: datetime = Field(default_factory=utcnow)
    notes: Optional[str] = None


# ──────────────────────────────────────────────
# Phase 3: Activities, Meetings & Tasks
# ──────────────────────────────────────────────

class Meeting(TimestampMixin, table=True):
    __tablename__ = "meetings"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    description: Optional[str] = None
    scheduled_at: datetime = Field(nullable=False, index=True)
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    meeting_link: Optional[str] = None
    status: str = Field(default="scheduled", index=True)  # scheduled, completed, cancelled
    organizer_id: uuid.UUID = Field(foreign_key="users.id", nullable=False, index=True)
    contact_id: Optional[int] = Field(default=None, foreign_key="contacts.id")
    company_id: Optional[uuid.UUID] = Field(default=None, foreign_key="companies.id")
    deal_id: Optional[uuid.UUID] = Field(default=None, foreign_key="deals.id")
    outcome: Optional[str] = None


class Activity(TimestampMixin, table=True):
    __tablename__ = "activities"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    activity_type: str = Field(nullable=False, index=True)  # call, email, meeting, note, task
    subject: str = Field(nullable=False)
    description: Optional[str] = None
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False, index=True)
    contact_id: Optional[int] = Field(default=None, foreign_key="contacts.id", index=True)
    deal_id: Optional[uuid.UUID] = Field(default=None, foreign_key="deals.id", index=True)
    company_id: Optional[uuid.UUID] = Field(default=None, foreign_key="companies.id", index=True)
    duration_minutes: Optional[int] = None
    outcome: Optional[str] = None
    is_active: bool = Field(default=True, index=True)


class Task(TimestampMixin, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    description: Optional[str] = None
    assigned_to: uuid.UUID = Field(foreign_key="users.id", nullable=False, index=True)
    assigned_by: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    due_date: Optional[datetime] = Field(default=None, index=True)
    completed_at: Optional[datetime] = None
    priority: str = Field(default="medium", index=True)  # low, medium, high, urgent
    status: str = Field(default="pending", index=True)  # pending, in_progress, completed, cancelled
    related_to_type: Optional[str] = None  # contact, deal, company, lead
    related_to_id: Optional[str] = None
    is_active: bool = Field(default=True, index=True)


# ──────────────────────────────────────────────
# Phase 4: Campaigns & Marketing
# ──────────────────────────────────────────────

class Campaign(TimestampMixin, table=True):
    __tablename__ = "campaigns"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str = Field(nullable=False, index=True)
    description: Optional[str] = None
    type: str = Field(nullable=False, index=True)  # email, event, social, outbound, ads
    status: str = Field(default="draft", index=True)  # draft, active, paused, completed
    budget: Optional[float] = None
    actual_cost: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    company_id: Optional[uuid.UUID] = Field(default=None, foreign_key="companies.id")
    created_by: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    is_active: bool = Field(default=True, index=True)


class CampaignMember(SQLModel, table=True):
    __tablename__ = "campaign_members"

    id: Optional[int] = Field(default=None, primary_key=True)
    campaign_id: uuid.UUID = Field(foreign_key="campaigns.id", nullable=False, index=True)
    contact_id: int = Field(foreign_key="contacts.id", nullable=False, index=True)
    status: str = Field(default="sent", index=True)  # sent, opened, clicked, replied, bounced, opted_out
    engaged_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=utcnow)


class EmailTemplate(TimestampMixin, table=True):
    __tablename__ = "email_templates"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str = Field(nullable=False)
    subject: str = Field(nullable=False)
    body_html: str = Field(nullable=False)
    variables: Optional[str] = None  # JSON list of variable names
    category: Optional[str] = Field(default=None, index=True)
    created_by: uuid.UUID = Field(foreign_key="users.id", nullable=False)


class Sequence(TimestampMixin, table=True):
    __tablename__ = "sequences"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str = Field(nullable=False)
    description: Optional[str] = None
    steps: Optional[str] = None  # JSON array of step definitions
    trigger_condition: Optional[str] = None
    status: str = Field(default="draft", index=True)
    created_by: uuid.UUID = Field(foreign_key="users.id", nullable=False)


# ──────────────────────────────────────────────
# Phase 6: Products, Quotes & Orders
# ──────────────────────────────────────────────

class Product(TimestampMixin, table=True):
    __tablename__ = "products"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str = Field(nullable=False, index=True)
    description: Optional[str] = None
    sku: Optional[str] = Field(default=None, unique=True, index=True)
    unit_price: Decimal = Field(max_digits=12, decimal_places=2, nullable=False)
    cost_price: Optional[Decimal] = Field(default=None, max_digits=12, decimal_places=2)
    currency: str = Field(default="USD")
    category: Optional[str] = Field(default=None, index=True)
    tax_rate: Decimal = Field(default=Decimal("0.00"), max_digits=5, decimal_places=2)
    is_active: bool = Field(default=True, index=True)


class PriceBook(TimestampMixin, table=True):
    __tablename__ = "price_books"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str = Field(nullable=False)
    description: Optional[str] = None
    currency: str = Field(default="USD")
    is_active: bool = Field(default=True)


class PriceBookEntry(SQLModel, table=True):
    __tablename__ = "price_book_entries"

    id: Optional[int] = Field(default=None, primary_key=True)
    price_book_id: uuid.UUID = Field(foreign_key="price_books.id", nullable=False, index=True)
    product_id: uuid.UUID = Field(foreign_key="products.id", nullable=False, index=True)
    unit_price: Decimal = Field(max_digits=12, decimal_places=2, nullable=False)


class Quote(TimestampMixin, table=True):
    __tablename__ = "quotes"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    quote_number: Optional[str] = Field(default=None, unique=True, index=True)
    deal_id: uuid.UUID = Field(foreign_key="deals.id", nullable=False, index=True)
    company_id: uuid.UUID = Field(foreign_key="companies.id", nullable=False, index=True)
    contact_id: Optional[int] = Field(default=None, foreign_key="contacts.id")
    status: str = Field(default="draft", index=True)  # draft, sent, approved, rejected, converted
    valid_until: Optional[datetime] = None
    subtotal: Decimal = Field(default=Decimal("0.00"), max_digits=15, decimal_places=2)
    discount_percent: Decimal = Field(default=Decimal("0.00"), max_digits=5, decimal_places=2)
    discount_amount: Decimal = Field(default=Decimal("0.00"), max_digits=15, decimal_places=2)
    tax_total: Decimal = Field(default=Decimal("0.00"), max_digits=15, decimal_places=2)
    grand_total: Decimal = Field(default=Decimal("0.00"), max_digits=15, decimal_places=2)
    terms: Optional[str] = None
    notes: Optional[str] = None
    created_by: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    approved_by: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")


class QuoteLineItem(SQLModel, table=True):
    __tablename__ = "quote_line_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    quote_id: uuid.UUID = Field(foreign_key="quotes.id", nullable=False, index=True)
    product_id: uuid.UUID = Field(foreign_key="products.id", nullable=False)
    product_name: str = Field(nullable=False)
    quantity: int = Field(default=1, ge=1)
    unit_price: Decimal = Field(max_digits=12, decimal_places=2, nullable=False)
    discount_percent: Decimal = Field(default=Decimal("0.00"), max_digits=5, decimal_places=2)
    tax_rate: Decimal = Field(default=Decimal("0.00"), max_digits=5, decimal_places=2)
    line_total: Decimal = Field(max_digits=15, decimal_places=2, nullable=False)


class Order(TimestampMixin, table=True):
    __tablename__ = "orders"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    order_number: Optional[str] = Field(default=None, unique=True, index=True)
    quote_id: uuid.UUID = Field(foreign_key="quotes.id", nullable=False, index=True)
    company_id: uuid.UUID = Field(foreign_key="companies.id", nullable=False, index=True)
    contact_id: Optional[int] = Field(default=None, foreign_key="contacts.id")
    status: str = Field(default="pending", index=True)  # pending, confirmed, shipped, delivered, cancelled
    grand_total: Decimal = Field(max_digits=15, decimal_places=2, nullable=False)
    shipping_address: Optional[str] = None
    payment_terms: Optional[str] = None
    placed_by: uuid.UUID = Field(foreign_key="users.id", nullable=False)


class Invoice(TimestampMixin, table=True):
    __tablename__ = "invoices"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    invoice_number: Optional[str] = Field(default=None, unique=True, index=True)
    order_id: uuid.UUID = Field(foreign_key="orders.id", nullable=False, index=True)
    company_id: uuid.UUID = Field(foreign_key="companies.id", nullable=False, index=True)
    status: str = Field(default="unpaid", index=True)  # unpaid, paid, overdue, cancelled
    amount_due: Decimal = Field(max_digits=15, decimal_places=2, nullable=False)
    amount_paid: Decimal = Field(default=Decimal("0.00"), max_digits=15, decimal_places=2)
    due_date: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    payment_method: Optional[str] = None
    payment_reference: Optional[str] = None


# ──────────────────────────────────────────────
# Phase 7: Integrations & Automation
# ──────────────────────────────────────────────

class Webhook(SQLModel, table=True):
    __tablename__ = "webhooks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    url: str = Field(nullable=False)
    events: str = Field(nullable=False)  # JSON array of event names
    secret: Optional[str] = None
    is_active: bool = Field(default=True)
    created_by: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=utcnow)


class WebhookEvent(SQLModel, table=True):
    __tablename__ = "webhook_events"

    id: Optional[int] = Field(default=None, primary_key=True)
    webhook_id: uuid.UUID = Field(foreign_key="webhooks.id", nullable=False, index=True)
    event_type: str = Field(nullable=False)
    payload: str = Field(nullable=False)  # JSON
    status: str = Field(default="pending")  # pending, delivered, failed
    attempt_count: int = Field(default=0)
    last_attempt_at: Optional[datetime] = None
    response_status: Optional[int] = None
    created_at: datetime = Field(default_factory=utcnow)


class Integration(SQLModel, table=True):
    __tablename__ = "integrations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    provider: str = Field(nullable=False, index=True)  # gmail, google_calendar, outlook, twilio, slack
    label: Optional[str] = None
    credentials: Optional[str] = None  # encrypted JSON
    settings: Optional[str] = None  # JSON
    is_connected: bool = Field(default=False)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=utcnow)
    last_synced_at: Optional[datetime] = None


class AutomationRule(TimestampMixin, table=True):
    __tablename__ = "automation_rules"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str = Field(nullable=False)
    description: Optional[str] = None
    trigger_event: str = Field(nullable=False, index=True)
    conditions: Optional[str] = None  # JSON
    actions: str = Field(nullable=False)  # JSON
    is_active: bool = Field(default=True)
    created_by: uuid.UUID = Field(foreign_key="users.id", nullable=False)


class ApiKey(TimestampMixin, table=True):
    __tablename__ = "api_keys"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    name: str = Field(nullable=False)
    key_hash: str = Field(nullable=False, unique=True)
    scopes: Optional[str] = None  # JSON array
    expires_at: Optional[datetime] = None
    is_active: bool = Field(default=True)
    created_by: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    last_used_at: Optional[datetime] = None
