from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from infograph.core.schemas.infographic import Infographic, InfographicCreate
from infograph.core.schemas.research_session import ResearchSession
from infograph.core.schemas.source import Source
from infograph.settings import settings
from infograph.stores.duckdb.infographic_store_duckdb import InfographicStoreDuckDB


class InfographicServiceError(RuntimeError):
    """Raised when infographic generation fails."""


@dataclass
class InfographicService:
    """Service for generating infographic assets."""

    infographic_store: InfographicStoreDuckDB
    output_dir: Path = field(default_factory=lambda: Path(settings.infographic_path))
    image_size: tuple[int, int] = (960, 540)
    default_bullets_limit: int = 3
    background_color: str = "white"
    text_color: str = "black"

    def generate_infographic(
        self,
        session: ResearchSession,
        sources: list[Source],
        template_type: str = "basic",
    ) -> Infographic:
        """Generate an infographic and persist metadata."""
        if template_type != "basic":
            raise InfographicServiceError("Unsupported template type")

        layout_data = self._build_basic_layout(session, sources)
        output_path = self._render_basic(layout_data, session.session_id)
        self.infographic_store.delete_infographic(session.session_id)
        return self.infographic_store.create_infographic(
            InfographicCreate(
                session_id=session.session_id,
                template_type=template_type,
                layout_data={
                    **layout_data,
                    "image_path": str(output_path),
                },
            )
        )

    def get_infographic(self, session_id: str) -> Infographic | None:
        """Return infographic metadata for a session."""
        return self.infographic_store.get_infographic(session_id)

    def _build_basic_layout(
        self, session: ResearchSession, sources: list[Source]
    ) -> dict:
        bullet_points = [source.title for source in sources if source.title][
            : self.default_bullets_limit
        ]
        if not bullet_points:
            bullet_points = ["No sources available yet."]
        return {
            "title": session.prompt,
            "bullets": bullet_points,
            "source_count": len(sources),
        }

    def _render_basic(self, layout_data: dict, session_id: str) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir / f"{session_id}_basic.png"

        image = Image.new("RGB", self.image_size, self.background_color)
        draw = ImageDraw.Draw(image)
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

        margin_x = 32
        max_width = self.image_size[0] - margin_x * 2
        y = 24

        y = self._draw_wrapped_text(
            draw,
            f"Research: {layout_data.get('title', '')}",
            title_font,
            margin_x,
            y,
            max_width,
        )
        y += 12

        y = self._draw_wrapped_text(
            draw,
            "Key Points:",
            body_font,
            margin_x,
            y,
            max_width,
        )
        for bullet in layout_data.get("bullets", []):
            y = self._draw_wrapped_text(
                draw,
                f"• {bullet}",
                body_font,
                margin_x + 8,
                y,
                max_width - 8,
            )

        y += 8
        self._draw_wrapped_text(
            draw,
            f"Sources: {layout_data.get('source_count', 0)}",
            body_font,
            margin_x,
            y,
            max_width,
        )

        image.save(output_path, format="PNG")
        return output_path

    def _draw_wrapped_text(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        font: ImageFont.ImageFont,
        x: int,
        y: int,
        max_width: int,
    ) -> int:
        lines: list[str] = []
        for paragraph in text.splitlines():
            words = paragraph.split()
            if not words:
                lines.append("")
                continue
            current = words[0]
            for word in words[1:]:
                candidate = f"{current} {word}"
                if draw.textlength(candidate, font=font) <= max_width:
                    current = candidate
                else:
                    lines.append(current)
                    current = word
            lines.append(current)

        for line in lines:
            draw.text((x, y), line, font=font, fill=self.text_color)
            bbox = font.getbbox(line)
            line_height = max(1, bbox[3] - bbox[1])
            y += line_height + 6
        return y
