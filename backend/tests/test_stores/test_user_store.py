from infograph.core.schemas.user import UserCreate
from infograph.stores.duckdb.user_store_duckdb import UserStoreDuckDB


def test_user_store_crud(duckdb_client) -> None:
    store = UserStoreDuckDB(client=duckdb_client)
    user = store.create_user(
        UserCreate(email="user@example.com", name="Test User", google_id="google-1")
    )

    fetched = store.get_user_by_id(user.user_id)
    assert fetched is not None
    assert fetched.email == user.email

    fetched_by_google = store.get_user_by_google_id("google-1")
    assert fetched_by_google is not None
    assert fetched_by_google.user_id == user.user_id

    updated = store.update_user(
        user.model_copy(update={"name": "Updated User"})
    )
    assert updated.name == "Updated User"

    store.delete_user(user.user_id)
    assert store.get_user_by_id(user.user_id) is None
