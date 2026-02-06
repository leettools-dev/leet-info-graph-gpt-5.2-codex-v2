"""Compatibility package for local execution.

This allows `python -m infograph.svc.main` to work when running from the
backend directory without installing the package. It extends the package
path to include the src/infograph implementation.
"""

from __future__ import annotations

from pkgutil import extend_path
from pathlib import Path

__path__ = extend_path(__path__, __name__)  # type: ignore[name-defined]

SRC_PACKAGE = Path(__file__).resolve().parents[1] / "src" / "infograph"
if SRC_PACKAGE.exists():
    __path__.append(str(SRC_PACKAGE))
