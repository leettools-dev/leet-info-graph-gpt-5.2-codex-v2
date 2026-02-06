from __future__ import annotations

from pathlib import Path

from infograph.core.schemas.research_session import ResearchSession
from infograph.core.schemas.source import SourceCreate
from infograph.services.infographic_service import InfographicService
from infograph.stores.duckdb.duckdb_client import DuckDBClient
from infograph.stores.duckdb.infographic_store_duckdb import InfographicStoreDuckDB
from infograph.stores.duckdb.source_store_duckdb import SourceStoreDuckDB


def _session() -> ResearchSession:
    return ResearchSession(
        session_id="session-123",
        user_id="user-1",
        prompt="Test prompt",
        status="generating",
        created_at=1,
        updated_at=1,
    )


def test_generate_infographic_creates_metadata_and_image(tmp_path: Path) -> None:
    client = DuckDBClient(db_name="infograph")
    infographic_store = InfographicStoreDuckDB(client=client)
    source_store = SourceStoreDuckDB(client=client)
    service = InfographicService(
        infographic_store=infographic_store,
        output_dir=tmp_path / "infographics",
    )

    source_store.create_source(
        SourceCreate(
            session_id="session-123",
            title="Alpha Source",
            url="https://example.com",
            snippet="Snippet",
            confidence=0.9,
        )
    )
    sources = source_store.list_sources("session-123")

    infographic = service.generate_infographic(session=_session(), sources=sources)

    assert infographic.session_id == "session-123"
    assert infographic.template_type == "basic"
    assert infographic.layout_data["source_count"] == 1
    assert "Alpha Source" in infographic.layout_data["bullets"][0]

    image_path = Path(infographic.image_path)
    assert image_path.exists()
    assert image_path.suffix == ".png"

    stored = infographic_store.get_infographic("session-123")
    assert stored is not None
    assert stored.image_path == str(image_path)
