from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import settings

# Initialize the Gemini embeddings client
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-2",
    google_api_key=settings.GEMINI_API_KEY
)

async def get_embedding(text: str) -> list[float]:
    """Get a single embedding vector for a piece of text."""
    if not text or not text.strip():
        return [0.0] * 3072
        
    try:
        result = await embeddings.aembed_query(text)
        return result
    except Exception as e:
        print(f"Error generating embedding: {e}")
        # Return a zero vector as fallback if API fails
        return [0.0] * 3072

async def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Get embeddings for a batch of texts."""
    valid_texts = [t.replace("\n", " ") if t and t.strip() else "empty" for t in texts]
    if not valid_texts:
        return []
        
    try:
        results = await embeddings.aembed_documents(texts)
        return results
    except Exception as e:
        print(f"Error generating batch embeddings: {e}")
        return [[0.0] * 3072 for _ in texts]
