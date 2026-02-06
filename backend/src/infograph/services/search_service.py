from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Callable, Iterable
from urllib.parse import urljoin

import httpx

from infograph.core.schemas.source import SourceCreate


class SearchServiceError(RuntimeError):
    """Raised when web search fails."""


@dataclass(frozen=True)
class ParsedResult:
    """Parsed search result fields."""

    title: str
    url: str
    snippet: str


@dataclass(frozen=True)
class SearchResult:
    """Search result with confidence score."""

    title: str
    url: str
    snippet: str
    confidence: float


class _DuckDuckGoParser(HTMLParser):
    """Lightweight HTML parser for DuckDuckGo search results."""

    def __init__(self) -> None:
        super().__init__()
        self._results: list[ParsedResult] = []
        self._current: dict[str, str] = {}
        self._capture_title = False
        self._capture_snippet = False

    @property
    def results(self) -> list[ParsedResult]:
        return self._results

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key: value or "" for key, value in attrs}
        classes = set(attrs_dict.get("class", "").split())

        if tag == "a" and {"result__a", "result-link", "result__url"}.intersection(classes):
            self._flush_current()
            self._current = {
                "title": "",
                "url": attrs_dict.get("href", ""),
                "snippet": "",
            }
            self._capture_title = True
            return

        if tag in {"div", "span", "a"} and {
            "result__snippet",
            "result-snippet",
        }.intersection(classes):
            self._capture_snippet = True

    def handle_data(self, data: str) -> None:
        if self._capture_title:
            self._current["title"] = f"{self._current.get('title', '')}{data}".strip()
        if self._capture_snippet:
            self._current["snippet"] = (
                f"{self._current.get('snippet', '')}{data}".strip()
            )

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._capture_title:
            self._capture_title = False
        if tag in {"div", "span", "a"} and self._capture_snippet:
            self._capture_snippet = False
            self._flush_current(require_snippet=False)

    def close(self) -> None:
        self._flush_current()
        super().close()

    def _flush_current(self, require_snippet: bool = True) -> None:
        if not self._current:
            return
        title = self._current.get("title", "").strip()
        url = self._current.get("url", "").strip()
        snippet = self._current.get("snippet", "").strip()
        if title and url and (snippet or not require_snippet):
            self._results.append(
                ParsedResult(title=title, url=url, snippet=snippet or "")
            )
        self._current = {}
        self._capture_title = False
        self._capture_snippet = False


@dataclass
class SearchService:
    """Service for performing web searches and extracting sources."""

    base_url: str = "https://duckduckgo.com/html/"
    timeout_seconds: float = 10.0
    max_results_default: int = 5
    fetcher: Callable[[str], str] | None = None
    http_client: httpx.Client | None = None

    def __post_init__(self) -> None:
        if self.http_client is None:
            self.http_client = httpx.Client(
                headers={"User-Agent": "infograph-search/1.0"}
            )

    def close(self) -> None:
        if self.http_client is not None:
            self.http_client.close()

    def search(self, query: str, max_results: int | None = None) -> list[SearchResult]:
        """Run a web search and return ranked results."""
        if not query or not query.strip():
            raise SearchServiceError("Query cannot be empty")
        html = self.fetcher(query) if self.fetcher else self._fetch_html(query)
        parsed = self.parse_results(html)
        limit = max_results or self.max_results_default
        return self._assign_confidence(parsed[:limit])

    def search_sources(
        self, session_id: str, query: str, max_results: int | None = None
    ) -> list[SourceCreate]:
        """Run a search and return SourceCreate entries."""
        results = self.search(query, max_results=max_results)
        return self.results_to_sources(session_id, results)

    def results_to_sources(
        self, session_id: str, results: Iterable[SearchResult]
    ) -> list[SourceCreate]:
        """Convert search results to SourceCreate models."""
        return [
            SourceCreate(
                session_id=session_id,
                title=result.title,
                url=result.url,
                snippet=result.snippet,
                confidence=result.confidence,
            )
            for result in results
        ]

    def parse_results(self, html: str) -> list[ParsedResult]:
        """Parse HTML search results into structured data."""
        parser = _DuckDuckGoParser()
        parser.feed(html)
        parser.close()
        results = [
            ParsedResult(
                title=result.title.strip(),
                url=self._normalize_url(result.url),
                snippet=result.snippet.strip(),
            )
            for result in parser.results
            if result.title.strip() and result.url.strip()
        ]
        return results

    def _fetch_html(self, query: str) -> str:
        if self.http_client is None:
            raise SearchServiceError("HTTP client not initialized")
        try:
            response = self.http_client.get(
                self.base_url,
                params={"q": query},
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as exc:
            raise SearchServiceError("Search request failed") from exc

    def _assign_confidence(self, results: list[ParsedResult]) -> list[SearchResult]:
        ranked: list[SearchResult] = []
        for index, result in enumerate(results):
            confidence = max(0.1, round(1.0 - index * 0.1, 2))
            ranked.append(
                SearchResult(
                    title=result.title,
                    url=result.url,
                    snippet=result.snippet,
                    confidence=confidence,
                )
            )
        return ranked

    def _normalize_url(self, url: str) -> str:
        if url.startswith("http://") or url.startswith("https://"):
            return url
        return urljoin(self.base_url, url)
