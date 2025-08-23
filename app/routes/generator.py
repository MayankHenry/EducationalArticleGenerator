# app/routes/generator.py
from fastapi import APIRouter, HTTPException, status, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Literal
from app.services.llm_service import generate_article_content
from app.utils.helpers import convert_markdown_to_pdf, convert_markdown_to_docx
from app.models import ArticleRequest
import time

router = APIRouter(
    prefix="/api/v1",
    tags=["generator"],
)

# In-memory storage for generated articles, now with more data
# {
#   "article_id": {
#     "timestamp": "2023-10-27T10:00:00Z",
#     "topic": "...",
#     "difficulty": "...",
#     "audience": "...",
#     "content": "..."
#   }
# }
articles_cache = {}

@router.get("/status")
def get_status():
    return {"status": "The generator API is running successfully!"}

@router.post("/generate_article")
async def generate_article(request: ArticleRequest):
    """
    Generates a structured educational article based on a given topic,
    difficulty, and target audience.
    """
    try:
        # Call the LLM service to generate the article
        article_data = generate_article_content(
            topic=request.topic,
            difficulty=request.difficulty,
            audience=request.audience
        )

        if "error" in article_data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=article_data["error"]
            )

        # Generate a unique ID and store all the data
        # Using a timestamp as a simple unique ID for demonstration
        article_id = int(time.time() * 1000)
        articles_cache[article_id] = {
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
            "topic": request.topic,
            "difficulty": request.difficulty,
            "audience": request.audience,
            "content": article_data["article"]
        }

        return {"article_id": article_id, "article_content": article_data["article"]}

    except Exception as e:
        print(f"An error occurred during article generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during article generation."
        )

@router.get("/download_article/{article_id}")
async def download_article(article_id: int, format: Literal["pdf", "docx"]):
    """
    Returns a previously generated article as a downloadable PDF or DOCX file.
    """
    article_entry = articles_cache.get(article_id)
    if not article_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found. Please generate it first."
        )

    article_content = article_entry["content"]
    # (Existing conversion and response logic remains the same)
    if format == "pdf":
        file_buffer = convert_markdown_to_pdf(article_content)
        return StreamingResponse(
            content=file_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=article.pdf"}
        )

    elif format == "docx":
        file_buffer = convert_markdown_to_docx(article_content)
        return StreamingResponse(
            content=file_buffer,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=article.docx"}
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid format specified. Must be 'pdf' or 'docx'."
    )
# (Add this to the end of your generator.py file)
@router.get("/history")
def get_history():
    """
    Returns a list of all generated articles with their IDs and metadata.
    Does not return the full article content to keep the response light.
    """
    history_list = []
    for article_id, data in articles_cache.items():
        history_list.append({
            "article_id": article_id,
            "timestamp": data["timestamp"],
            "topic": data["topic"],
            "difficulty": data["difficulty"],
            "audience": data["audience"]
        })
    # Return the history in reverse chronological order
    return sorted(history_list, key=lambda x: x["timestamp"], reverse=True)