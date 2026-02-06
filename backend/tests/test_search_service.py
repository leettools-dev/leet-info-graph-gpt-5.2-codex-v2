from __future__ import annotations

import pytest

from infograph.services.search_service import SearchService, SearchServiceError


HTML_WITH_RESULTS = """
<html>
<body>
  <div class="results">
    <a class="result__a" href="https://example.com/alpha">Alpha Title</a>
    <span class="result__snippet">Alpha snippet text.</span>
  </div>
  <div class="results">
    <a class="result__a" href="/beta">Beta Title</a>
    <span class="result__snippet">Beta snippet text.</span>
  </div>
</body>
</html>
"""


class DummyFetcher:
    def __init__(self, html: str) -> None:
        self.html = html
        self.calls: list[str] = []

    def __call__(self, query: str) -> str:
        self.calls.append(query)
        return self.html


def test_search_returns_ranked_results() -> None:
    fetcher = DummyFetcher(HTML_WITH_RESULTS)
    service = SearchService(fetcher=fetcher)

    results = service.search("test query", max_results=2)

    assert fetcher.calls == ["test query"]
    assert len(results) == 2
    assert results[0].title == "Alpha Title"
    assert results[0].url == "https://example.com/alpha"
    assert results[0].snippet == "Alpha snippet text."
    assert results[0].confidence == 1.0
    assert results[1].title == "Beta Title"
    assert results[1].url == "https://duckduckgo.com/beta"
    assert results[1].confidence == 0.9


def test_search_rejects_empty_query() -> None:
    service = SearchService(fetcher=DummyFetcher(HTML_WITH_RESULTS))

    with pytest.raises(SearchServiceError):
        service.search("   ")


def test_search_sources_creates_source_models() -> None:
    fetcher = DummyFetcher(HTML_WITH_RESULTS)
    service = SearchService(fetcher=fetcher)

    sources = service.search_sources("session-123", "query", max_results=1)

    assert len(sources) == 1
    source = sources[0]
    assert source.session_id == "session-123"
    assert source.title == "Alpha Title"
    assert source.url == "https://example.com/alpha"
    assert source.snippet == "Alpha snippet text."
    assert source.confidence == 1.0
