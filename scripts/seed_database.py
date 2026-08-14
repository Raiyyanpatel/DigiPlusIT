import asyncio
import os
import sys

# Add backend to path so we can import from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session, engine
from app.models.knowledge import KnowledgeDocument
from app.models.user import User, UserRole
from app.services.auth_service import get_password_hash
from app.services.embedding_service import get_embedding


async def seed_users(db: AsyncSession):
    # Check if admin exists
    admin_result = await db.execute(select(User).where(User.email == "admin@resolveai.internal"))
    if not admin_result.scalars().first():
        admin = User(
            name="Admin User",
            email="admin@resolveai.internal",
            password_hash=get_password_hash("admin123"),
            role=UserRole.admin
        )
        db.add(admin)
        print("Created admin user (admin@resolveai.internal / admin123)")

    # Check if engineer exists
    eng_result = await db.execute(select(User).where(User.email == "engineer@resolveai.internal"))
    if not eng_result.scalars().first():
        engineer = User(
            name="Support Engineer",
            email="engineer@resolveai.internal",
            password_hash=get_password_hash("engineer123"),
            role=UserRole.engineer
        )
        db.add(engineer)
        print("Created engineer user (engineer@resolveai.internal / engineer123)")
        
    await db.commit()

async def seed_knowledge(db: AsyncSession):
    knowledge_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../knowledge'))
    if not os.path.exists(knowledge_dir):
        print(f"Knowledge directory {knowledge_dir} not found. Skipping.")
        return

    # Check if we already seeded
    result = await db.execute(select(KnowledgeDocument).limit(1))
    if result.scalars().first():
        print("Knowledge base already seeded. Skipping.")
        return

    for filename in os.listdir(knowledge_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(knowledge_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            title = filename.replace(".md", "").title() + " Troubleshooting"
            
            # Try to extract title from markdown H1
            lines = content.split("\n")
            if lines and lines[0].startswith("# "):
                title = lines[0][2:].strip()
                
            print(f"Embedding and saving KB doc: {title}...")
            embedding = await get_embedding(content)
            
            doc = KnowledgeDocument(
                title=title,
                content=content,
                category=filename.replace(".md", ""),
                source="internal_kb",
                embedding=embedding
            )
            db.add(doc)
            
    await db.commit()
    print("Knowledge base seeding complete.")

async def main():
    print("Starting database seeding...")
    async with async_session() as db:
        await seed_users(db)
        await seed_knowledge(db)
    
    # Close engine
    await engine.dispose()
    print("Seeding finished successfully.")

if __name__ == "__main__":
    asyncio.run(main())
