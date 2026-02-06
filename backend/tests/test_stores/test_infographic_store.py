from infograph.core.schemas.infographic import InfographicCreate
from infograph.stores.duckdb.infographic_store_duckdb import InfographicStoreDuckDB


def test_infographic_store_crud(duckdb_client) -> None:
    store = InfographicStoreDuckDB(client=duckdb_client)
    infographic = store.create_infographic(
        InfographicCreate(
            session_id="session-1",
            template_type="basic",
            layout_data={"image_path": "/tmp/image.png", "title": "Test"},
        )
    )

    fetched = store.get_infographic("session-1")
    assert fetched is not None
    assert fetched.infographic_id == infographic.infographic_id

    store.delete_infographic("session-1")
    assert store.get_infographic("session-1") is None
