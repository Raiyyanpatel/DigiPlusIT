
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.database import get_db
from app.models.knowledge import KnowledgeDocument
from app.models.user import User
from app.schemas.knowledge import KnowledgeDocCreate, KnowledgeDocResponse

router = APIRouter()

@router.post("/", response_model=KnowledgeDocResponse, status_code=status.HTTP_201_CREATED)
async def create_knowledge_doc(
    doc_in: KnowledgeDocCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
         raise HTTPException(status_code=403, detail="Only admins can create knowledge docs")
         
    # TODO: generate embeddings before saving
    doc = KnowledgeDocument(**doc_in.model_dump())
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc

@router.get("/", response_model=list[KnowledgeDocResponse])
async def list_knowledge_docs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(KnowledgeDocument).offset(skip).limit(limit))
    return list(result.scalars().all())
