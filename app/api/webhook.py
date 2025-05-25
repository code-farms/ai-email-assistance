from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from datetime import datetime, timezone

from app.db.db import engine
from app.db.models import Email
from app.core.summarizer import summarize_email
from app.core.embeddings import email_embedder
from app.db.qdrant import add_email_embedding
from uuid import uuid4

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
        # Step 1: Summarize the email
        summary = await summarize_email(payload.TextBody)
        print("✅ Email summarized successfully!")

        # Step 2: Store email in SQL DB
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
        
        print("✅ Email stored in SQL DB successfully!")

        # Step 3: Get embedding
        embedding = email_embedder(payload.TextBody)
        print("✅ Email embedding generated successfully!")

        # Step 4: Add to Qdrant
        metadata = {
            "id": str(uuid4()),
            "email_id": email.id,
            "from": payload.From,
            "to": payload.To,
            "subject": payload.Subject,
            "summary": summary,
            "date": payload.Date,
        }

        add_email_embedding(embedding, metadata)
        print("✅ Email added to Qdrant successfully!")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing email: {e}")

    return {"message": "Email received, summarized, and stored successfully"}