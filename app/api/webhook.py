from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from datetime import datetime, timezone

from app.db.db import engine
from app.db.models import Email
from app.core.summarizer import summarize_email

router = APIRouter()

class PostmarkInboundPayload(BaseModel):
    From: str
    To: str
    Subject: str
    TextBody: str
    Date: str


@router.post("/webhook/email")
async def receive_inbound_email(payload: PostmarkInboundPayload):
    try:
        summary = await summarize_email(payload.TextBody)
        email = Email(
            sender=payload.From,
            recipient=payload.To,
            subject=payload.Subject,
            body=payload.TextBody,
            summary=summary,
            received_at=datetime.now(timezone.utc),
        )
        with Session(engine) as session:
            session.add(email)
            session.commit()
            session.refresh(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        return {"message": "Email received and stored successfully"}