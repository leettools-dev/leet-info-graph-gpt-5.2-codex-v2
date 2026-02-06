from infograph.core.schemas.source import SourceCreate
from infograph.stores.duckdb.source_store_duckdb import SourceStoreDuckDB


def test_source_store_crud(duckdb_client) -> None:
    store = SourceStoreDuckDB(client=duckdb_client)
    source = store.create_source(
        SourceCreate(
            session_id="session-1",
            title="Title",
            url="https://example.com",
            snippet="Snippet",
            confidence=0.9,
        )
    )

    sources = store.list_sources("session-1")
    assert len(sources) == 1
    assert sources[0].source_id == source.source_id

    store.delete_sources_for_session("session-1")
    assert store.list_sources("session-1") == []
