from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
INDEX = DIST / "index.html"


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.references: list[tuple[str, str]] = []
        self.anchors: list[str] = []
        self.images: list[dict[str, str | None]] = []
        self.title_count = 0
        self.h1_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(str(values["id"]))
        if tag == "title":
            self.title_count += 1
        if tag == "h1":
            self.h1_count += 1
        if tag == "a" and values.get("href"):
            self.anchors.append(str(values["href"]))
        if tag in {"img", "script", "link"}:
            attribute = "src" if tag in {"img", "script"} else "href"
            value = values.get(attribute)
            if value:
                self.references.append((tag, str(value)))
        if tag == "img":
            self.images.append(values)


def main() -> None:
    failures: list[str] = []
    html = INDEX.read_text(encoding="utf-8")
    parser = SiteParser()
    parser.feed(html)

    if parser.title_count != 1:
        failures.append(f"Expected one title element, found {parser.title_count}")
    if parser.h1_count != 1:
        failures.append(f"Expected one h1, found {parser.h1_count}")

    for href in parser.anchors:
        if href.startswith("#") and href[1:] not in parser.ids:
            failures.append(f"Missing anchor target: {href}")

    local_references: set[Path] = set()
    for _, reference in parser.references:
        parsed = urlparse(reference)
        if parsed.scheme or reference.startswith("//") or reference.startswith("#"):
            continue
        target = (DIST / parsed.path).resolve()
        local_references.add(target)
        if not target.exists():
            failures.append(f"Missing referenced file: {reference}")

    for image in parser.images:
        if image.get("alt") is None:
            failures.append(f"Image missing alt text: {image.get('src')}")
        src = image.get("src")
        if src and src.endswith((".webp", ".png", ".jpg", ".jpeg")):
            path = DIST / src
            with Image.open(path) as asset:
                if asset.width < 1000:
                    failures.append(f"Image is unexpectedly narrow: {src} ({asset.width}px)")

    required = [DIST / "robots.txt", DIST / "sitemap.xml", DIST / "assets" / "favicon.svg"]
    for path in required:
        if not path.exists():
            failures.append(f"Missing required deployment file: {path.relative_to(DIST)}")

    private_tokens = ["HIUPM5553H", "4154101001281", "CNRB0004154"]
    for token in private_tokens:
        if token in html:
            failures.append(f"Private source-document token leaked into public HTML: {token}")

    if failures:
        raise SystemExit("VALIDATION FAILED\n- " + "\n- ".join(failures))

    print("VALIDATION PASSED")
    print(f"HTML: {INDEX.relative_to(ROOT)}")
    print(f"Internal anchor links: {sum(h.startswith('#') for h in parser.anchors)}")
    print(f"Local referenced assets: {len(local_references)}")
    print(f"Content images checked: {len(parser.images)}")
    print("Private certificate identifiers checked: 3")


if __name__ == "__main__":
    main()
