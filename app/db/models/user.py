import uuid
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class User(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,  # generate UUID automatically
        primary_key=True,
        index=True
    )
    email: str = Field(index=True, nullable=False, unique=True)
    name: Optional[str]
    is_active: bool = Field(default=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))