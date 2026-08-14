import asyncio
import hashlib
import os
import sys

from datasets import load_dataset

# Add backend to path so we can import from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from sqlalchemy import select

from app.database import async_session, engine
from app.models.embedding import IncidentEmbedding
from app.models.incident import Incident, IncidentPriority, IncidentStatus
from app.models.resolution import Resolution
from app.services.embedding_service import get_embedding

# We'll ingest a subset to keep embedding time/cost low for the demo
MAX_TICKETS = 100

async def ingest_dataset():
    print("Loading dataset from HuggingFace (mindweave/help-desk-tickets)...")
    dataset = load_dataset("mindweave/help-desk-tickets", split="train")
    
    # Take a subset
    df = dataset.to_pandas()
    subset = df.head(MAX_TICKETS)
    print(f"Loaded {len(subset)} tickets.")

    async with async_session() as db:
        # Check if already ingested
        result = await db.execute(select(Incident).limit(1))
        if result.scalars().first():
            print("Database already contains incidents. Skipping ingestion to avoid duplicates.")
            return

        for index, row in subset.iterrows():
            external_id = row.get("Ticket ID", f"INC-{1000 + index}")
            title = row.get("Subject", "Untitled Incident")
            description = row.get("Description", "")
            priority_raw = str(row.get("Priority", "UNASSIGNED")).upper()
            status_raw = str(row.get("Status", "OPEN")).upper()
            resolution_text = row.get("Resolution", "")
            
            # Map Priority
            priority = IncidentPriority.UNASSIGNED
            if "CRITICAL" in priority_raw or "1" in priority_raw or "HIGH" in priority_raw:
                priority = IncidentPriority.P1
            elif "2" in priority_raw or "MEDIUM" in priority_raw:
                priority = IncidentPriority.P2
            elif "LOW" in priority_raw or "3" in priority_raw:
                priority = IncidentPriority.P3

            # Map Status
            status = IncidentStatus.OPEN
            if "CLOSED" in status_raw or "RESOLVED" in status_raw:
                status = IncidentStatus.RESOLVED

            incident = Incident(
                external_id=external_id,
                title=title,
                description=description,
                priority=priority,
                category=row.get("Category", "General"),
                status=status
            )
            db.add(incident)
            await db.flush() # get ID
            
            # Combine text for embedding
            embedding_text = f"Title: {title}\nDescription: {description}\nCategory: {incident.category}"
            if resolution_text:
                embedding_text += f"\nResolution: {resolution_text}"
                
            text_hash = hashlib.md5(embedding_text.encode()).hexdigest()
            
            print(f"Embedding ticket {external_id}...")
            vector = await get_embedding(embedding_text)
            
            embedding = IncidentEmbedding(
                incident_id=incident.id,
                embedding=vector,
                text_hash=text_hash
            )
            db.add(embedding)
            
            # If resolved, add a resolution record
            if status == IncidentStatus.RESOLVED and resolution_text:
                resolution = Resolution(
                    incident_id=incident.id,
                    root_cause="Derived from historical data",
                    actions_taken=resolution_text,
                    summary="Historical resolution"
                )
                db.add(resolution)
                
            # Commit every 10 records
            if (index + 1) % 10 == 0:
                await db.commit()
                print(f"Committed {index + 1} records.")
                
        # Final commit
        await db.commit()
        
    print("Dataset ingestion complete.")

async def main():
    await ingest_dataset()
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
