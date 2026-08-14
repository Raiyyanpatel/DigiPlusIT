from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.embedding_service import get_embedding


async def search_similar_incidents(db: AsyncSession, query: str, limit: int = 5) -> list[dict]:
    """Search for similar historical incidents based on semantic similarity."""
    query_vector = await get_embedding(query)
    
    # We use pgvector's <=> operator for cosine distance
    stmt = text("""
        SELECT i.external_id, i.title, i.description, i.status, 
               1 - (ie.embedding <=> :vector) as similarity
        FROM incidents i
        JOIN incident_embeddings ie ON i.id = ie.incident_id
        WHERE i.status = 'RESOLVED' OR i.status = 'CLOSED'
        ORDER BY ie.embedding <=> :vector
        LIMIT :limit
    """)
    
    result = await db.execute(stmt, {"vector": str(query_vector), "limit": limit})
    rows = result.fetchall()
    
    return [
        {
            "incident_id": row.external_id,
            "title": row.title,
            "description": row.description,
            "status": row.status,
            "similarity": round(row.similarity, 2)
        }
        for row in rows
    ]

async def search_knowledge_base(db: AsyncSession, query: str, limit: int = 3) -> list[dict]:
    """Search the knowledge base documents."""
    query_vector = await get_embedding(query)
    
    stmt = text("""
        SELECT title, content, category, 
               1 - (embedding <=> :vector) as similarity
        FROM knowledge_documents
        ORDER BY embedding <=> :vector
        LIMIT :limit
    """)
    
    result = await db.execute(stmt, {"vector": str(query_vector), "limit": limit})
    rows = result.fetchall()
    
    return [
        {
            "title": row.title,
            "content": row.content,
            "category": row.category,
            "similarity": round(row.similarity, 2)
        }
        for row in rows
    ]

async def search_resolutions(db: AsyncSession, query: str, limit: int = 3) -> list[dict]:
    """Search historical resolutions directly."""
    query_vector = await get_embedding(query)
    
    # Search by embedding the incident, but returning the resolution data
    stmt = text("""
        SELECT i.external_id, i.title, r.root_cause, r.actions_taken, r.summary,
               1 - (ie.embedding <=> :vector) as similarity
        FROM resolutions r
        JOIN incidents i ON r.incident_id = i.id
        JOIN incident_embeddings ie ON i.id = ie.incident_id
        ORDER BY ie.embedding <=> :vector
        LIMIT :limit
    """)
    
    result = await db.execute(stmt, {"vector": str(query_vector), "limit": limit})
    rows = result.fetchall()
    
    return [
        {
            "incident_id": row.external_id,
            "incident_title": row.title,
            "root_cause": row.root_cause,
            "actions_taken": row.actions_taken,
            "resolution_summary": row.summary,
            "similarity": round(row.similarity, 2)
        }
        for row in rows
    ]
