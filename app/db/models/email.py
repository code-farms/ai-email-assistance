from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
import uuid

class Email(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    sender: str
    recipient: str
    subject: str
    body: str
    summary: str = ""
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))