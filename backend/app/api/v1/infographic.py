from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

router = APIRouter()

class InfographicSpec(BaseModel):
    title: str
    date: str
    summary: str
    highlights: List[str]
    citations: List[str]

@router.post("/generate", response_model=InfographicSpec)
async def generate_infographic(prompt: str):
    spec = InfographicSpec(
        title="Research Infographic",
        date="2026-03-09",
        summary=f"Prompt received: {prompt}",
        highlights=["Key insight 1", "Key insight 2"],
        citations=["[1] Source A", "[2] Source B"],
    )

    image = Image.new("RGBA", (800, 1200), "white")
    draw = ImageDraw.Draw(image)
    draw.text((40, 40), spec.title, fill="black")
    draw.text((40, 80), spec.date, fill="gray")
    draw.text((40, 140), spec.summary, fill="black")
    highlight_y = 200
    for highlight in spec.highlights:
        draw.text((40, highlight_y), f"• {highlight}", fill="black")
        highlight_y += 40
    citation_y = highlight_y + 40
    for citation in spec.citations:
        draw.text((40, citation_y), citation, fill="gray")
        citation_y += 30

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")
