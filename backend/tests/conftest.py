import os

import pytest

from infograph.settings import settings
from infograph.stores.duckdb.duckdb_client import DuckDBClient


@pytest.fixture(autouse=True)
def use_test_settings(tmp_path):
    settings.is_test = True
    settings.database_path = str(tmp_path)
    settings.infographic_path = str(tmp_path / "infographics")
    yield
    settings.is_test = False


@pytest.fixture
def duckdb_client() -> DuckDBClient:
    return DuckDBClient(db_name="infograph")
