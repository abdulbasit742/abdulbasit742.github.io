#!/usr/bin/env python3
"""Dependency-free validation for the static portfolio."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "pakentrepreneur.me"
REQUIRED_FILES = (
    "index.html",
    "styles.css",
    "script.js",
    "404.html",
    "CNAME",
    "robots.txt",
    "sitemap.xml",
    "assets/favicon.svg",
    "README.md",
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"),
    re.compile(
        r"\b(?:api[_-]?key|secret|token|password)\b\s*[:=]\s*[\"'][^\"'\n]{12,}[\"']",
        re.IGNORECASE,
    ),
)


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.references: list[tuple[str, str]] = []
        self.title_seen = False
        self.description_seen = False
        self.canonical_seen = False
        self.lang_seen = False
        self.viewport_seen = False
        self.main_seen = False
        self.h1_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html" and values.get("lang"):
            self.lang_seen = True
        if tag == "title":
            self.title_seen = True
        if tag == "main":
            self.main_seen = True
        if tag == "h1":
            self.h1_count += 1
        if element_id := values.get("id"):
            self.ids.add(element_id)
        if tag == "meta" and values.get("name") == "description" and values.get("content"):
            self.description_seen = True
        if tag == "meta" and values.get("name") == "viewport" and values.get("content"):
            self.viewport_seen = True
        if tag == "link" and values.get("rel") == "canonical" and values.get("href"):
            self.canonical_seen = values["href"].startswith(f"https://{DOMAIN}/")
        for attribute in ("href", "src"):
            if value := values.get(attribute):
                self.references.append((attribute, value))


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def validate_html(path: Path, errors: list[str]) -> None:
    parser = SiteParser()
    parser.feed(path.read_text(encoding="utf-8"))

    checks = {
        "document language": parser.lang_seen,
        "title": parser.title_seen,
        "meta description": parser.description_seen,
        "viewport metadata": parser.viewport_seen,
        "canonical URL": parser.canonical_seen,
        "main landmark": parser.main_seen,
        "exactly one h1": parser.h1_count == 1,
    }
    for label, passed in checks.items():
        if not passed:
            fail(f"{path.name}: missing or invalid {label}", errors)

    for attribute, reference in parser.references:
        parsed = urlparse(reference)
        if parsed.scheme in {"http", "https", "mailto", "tel"} or reference.startswith("//"):
            continue
        if reference.startswith("#"):
            target = reference[1:]
            if target and target not in parser.ids:
                fail(f"{path.name}: unresolved fragment {reference}", errors)
            continue

        clean = reference.split("#", 1)[0].split("?", 1)[0]
        if not clean:
            continue
        target = ROOT / clean.lstrip("/")
        if not target.exists():
            fail(f"{path.name}: {attribute} points to missing file {reference}", errors)


def validate_domain(errors: list[str]) -> None:
    cname = (ROOT / "CNAME").read_text(encoding="utf-8").strip()
    if cname != DOMAIN:
        fail(f"CNAME must contain only {DOMAIN!r}", errors)

    expected = f"https://{DOMAIN}/"
    for relative in ("index.html", "robots.txt", "sitemap.xml"):
        content = (ROOT / relative).read_text(encoding="utf-8")
        if expected not in content:
            fail(f"{relative}: missing canonical domain {expected}", errors)


def scan_secrets(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.stat().st_size > 1_000_000:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                fail(f"{path.relative_to(ROOT)}: possible committed secret", errors)


def main() -> int:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            fail(f"Missing required file: {relative}", errors)

    if not errors:
        validate_html(ROOT / "index.html", errors)
        validate_domain(errors)
        scan_secrets(errors)

    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        print(f"\nStatic-site validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print("[OK] Static-site structure, metadata, links, domain, and secret checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
