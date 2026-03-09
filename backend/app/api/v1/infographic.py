from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from io import BytesIO
from PIL import Image, ImageDraw
import base64
from datetime import datetime

router = APIRouter()


def _current_timestamp() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


class InfographicSpec(BaseModel):
    title: str
    date: str
    summary: str
    highlights: List[str]
    citations: List[str]


class SourceMetadata(BaseModel):
    title: str
    publisher: str
    url: str
    publish_date: str
    accessed_at: str
    snippet: str
    reliability: str


class Provenance(BaseModel):
    sources_fetched_at: str
    last_accessed_at: str
    provider: str
    retrieval_method: str
    source_count: int


class InfographicResult(BaseModel):
    spec: InfographicSpec
    sources: List[SourceMetadata]
    confidence_note: str
    provenance: Provenance
    image_url: str


@router.post("/generate", response_model=InfographicResult)
async def generate_infographic(prompt: str):
    timestamp = _current_timestamp()
    sources = [
        SourceMetadata(
            title="State of AI Research",
            publisher="ResearchPulse",
            url="https://researchpulse.example.com/state-of-ai",
            publish_date="2026-03-07",
            accessed_at=timestamp,
            snippet="Latest advances show a surge in multimodal reasoning models.",
            reliability="High",
        ),
        SourceMetadata(
            title="Ethical AI Landscape",
            publisher="PolicyLab",
            url="https://policylab.example.com/ai-ethics",
            publish_date="2026-01-21",
            accessed_at=timestamp,
            snippet="Policy teams prioritize transparent reporting and citations.",
            reliability="Medium",
        ),
        SourceMetadata(
            title="Innovation in Visual Storytelling",
            publisher="DesignChronicle",
            url="https://designchronicle.example.com/visual-storytelling",
            publish_date="2026-02-10",
            accessed_at=timestamp,
            snippet="Visual summaries accelerate stakeholder adoption of research findings.",
            reliability="High",
        ),
    ]

    citations = [f"[{i + 1}] {source.title}" for i, source in enumerate(sources)]

    spec = InfographicSpec(
        title="Research Infographic",
        date=datetime.utcnow().strftime("%Y-%m-%d"),
        summary=f"Prompt received: {prompt}",
        highlights=[
            "Generative AI models now weave narratives across text, image, and sound",
            "Citations and provenance provide accountability for every claim",
        ],
        citations=citations,
    )

    image = Image.new("RGBA", (800, 1200), "white")
    draw = ImageDraw.Draw(image)
    draw.text((40, 40), spec.title, fill="black")
    draw.text((40, 80), spec.date, fill="gray")
    draw.text((40, 140), spec.summary, fill="black")
    highlight_y = 220
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
    encoded_image = base64.b64encode(buffer.getvalue()).decode("ascii")
    image_url = f"data:image/png;base64,{encoded_image}"

    provenance = Provenance(
        sources_fetched_at=timestamp,
        last_accessed_at=timestamp,
        provider="Research Infographic Studio",
        retrieval_method="Mocked curated search",
        source_count=len(sources),
    )

    result = InfographicResult(
        spec=spec,
        sources=sources,
        confidence_note="Confidence: Medium-high (derived from curated sources with explicit provenance).",
        provenance=provenance,
        image_url=image_url,
    )

    return result
