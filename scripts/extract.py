#!/usr/bin/env python3
"""Extract the Simply Static WordPress tree into Hugo content.

Reads HTML from the repository root and writes content/, data/comments/,
and the upload files Hugo should publish under static/wp-content/.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml
from bs4 import BeautifulSoup, NavigableString, Tag
from markdownify import markdownify

ROOT = Path(__file__).resolve().parents[1]
SITE_HOSTS = {
    "virtjunkie.com",
    "www.virtjunkie.com",
    "new.virtjunkie.com",
    "dev.virtjunkie.com",
}
LANG_MAP = {
    "shell": "bash",
    "bash": "bash",
    "sh": "bash",
    "powershell": "powershell",
    "ps1": "powershell",
    "posh": "powershell",
    "pgsql": "sql",
    "postgres": "sql",
    "postgresql": "sql",
    "sql": "sql",
    "mysql": "sql",
    "php": "php",
    "python": "python",
    "py": "python",
    "javascript": "js",
    "js": "js",
    "html": "html",
    "xml": "xml",
    "css": "css",
    "json": "json",
    "yaml": "yaml",
    "yml": "yaml",
    "go": "go",
    "ruby": "ruby",
    "text": "text",
    "plaintext": "text",
    "plain": "text",
    "ini": "ini",
    "conf": "ini",
    "apache": "apache",
    "nginx": "nginx",
    "dockerfile": "dockerfile",
    "hcl": "hcl",
    "terraform": "hcl",
    "tf": "hcl",
    "dos": "bat",
    "batch": "bat",
    "cmd": "bat",
}
FAVICONS = [
    "wp-content/uploads/2020/04/cropped-vj4-150x150.png",
    "wp-content/uploads/2020/04/cropped-vj4-300x300.png",
]
SIZE_SUFFIX = re.compile(r"^(?P<stem>.*)-\d+x\d+(?P<ext>\.[^.]+)$")


def q(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def local_path(url: str | None) -> str | None:
    if not url:
        return None
    url = url.strip()
    if url.startswith(("mailto:", "javascript:", "#", "data:")):
        return None
    if url.startswith("//"):
        url = "https:" + url
    if url.startswith("/"):
        path = url
    else:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return None
        host = parsed.netloc.lower().split(":")[0]
        if host not in SITE_HOSTS:
            return None
        path = parsed.path or "/"
    path = unquote(path.split("?", 1)[0].split("#", 1)[0])
    if not path.startswith("/"):
        path = "/" + path
    if " " in path or "https:" in path:
        return None
    if path.endswith("/index.html"):
        path = path[: -len("index.html")]
    return path


ASSET_PREFIXES = ("/wp-content/", "/images/", "/blog/", "/wp-includes/", "/wp-admin/")
DOMAIN_TLDS = {"com", "org", "net", "ca", "io", "edu", "gov", "uk", "de", "info", "us", "me"}


def unglue_external(path: str) -> str | None:
    """Turn crawler-joined hosts and mailto= paths back into real URLs."""
    parts = [part for part in path.split("/") if part]
    for index, part in enumerate(parts):
        if part.lower().startswith("mailto="):
            return "mailto:" + unquote(part.split("=", 1)[1])
        low = part.lower()
        if "_" in low or not re.fullmatch(r"(?:[a-z0-9-]+\.)+[a-z]{2,}", low):
            continue
        if low.rsplit(".", 1)[-1] not in DOMAIN_TLDS:
            continue
        rest = "/".join(parts[index + 1 :])
        return "https://" + part + ("/" + rest if rest else "/")
    return None


def repo_file(path: str) -> Path | None:
    rel = path.lstrip("/")
    if not rel or ".." in Path(rel).parts:
        return None
    candidate = ROOT / rel
    if candidate.is_file():
        return candidate
    return None


def original_path(path: str) -> str:
    name = Path(path).name
    match = SIZE_SUFFIX.match(name)
    if not match:
        return path
    return str(Path(path).with_name(match.group("stem") + match.group("ext")))


class Extractor:
    def __init__(self) -> None:
        self.copies: dict[str, Path] = {}
        self.missing_images: list[str] = []
        self.languages: set[str] = set()
        self.categories: dict[str, dict[str, str]] = {}
        self.tags: dict[str, dict[str, str]] = {}
        self.category_titles: dict[str, str] = {}
        self.years: set[str] = set()
        self.months: set[str] = set()
        self.aliases: dict[str, list[str]] = {}
        self.posts: list[dict] = []
        self.comment_count = 0
        self.comment_ids: list[int] = []

    def choose_image(self, img: Tag) -> str | None:
        raw_urls = []
        if img.get("src"):
            raw_urls.append(img["src"])
        srcset = img.get("srcset") or ""
        for part in srcset.split(","):
            bit = part.strip().split(" ")[0] if part.strip() else ""
            if bit:
                raw_urls.append(bit)
        found: list[tuple[int, str]] = []
        for raw in raw_urls:
            path = local_path(raw)
            if not path or not path.startswith("/wp-content/"):
                continue
            for cand in (original_path(path), path):
                source = repo_file(cand)
                if source:
                    found.append((source.stat().st_size, cand))
        if not found:
            src = img.get("src") or ""
            if local_path(src):
                self.missing_images.append(src)
            return None
        found.sort(reverse=True)
        path = found[0][1]
        source = repo_file(path)
        if source:
            self.copies[path] = source
        return path

    def rewrite_links(self, scope: Tag) -> None:
        for anchor in scope.select("a[href]"):
            original = anchor.get("href") or ""
            rewritten = local_path(original)
            if not rewritten:
                continue
            external = unglue_external(rewritten)
            if external:
                anchor["href"] = external
                continue
            if rewritten.startswith(ASSET_PREFIXES):
                source = repo_file(rewritten)
                if source is None:
                    continue
                if rewritten.startswith("/wp-content/"):
                    self.copies[rewritten] = source
            anchor["href"] = rewritten

    def rewrite_images(self, scope: Tag) -> None:
        for img in scope.select("img"):
            chosen = self.choose_image(img)
            if not chosen:
                continue
            img["src"] = chosen
            for attr in ("srcset", "sizes", "width", "height", "fetchpriority", "decoding", "loading"):
                if img.has_attr(attr):
                    del img[attr]

    def fence(self, language: str, code: str) -> str:
        key = re.sub(r"[^a-z0-9]+", "", language.lower())
        mapped = LANG_MAP.get(key)
        if mapped is None:
            mapped = "text"
            if language.strip():
                self.languages.add(language.strip())
        else:
            self.languages.add(f"{language.strip()} -> {mapped}")
        code = code.replace("\u00a0", " ").replace("\r\n", "\n").replace("\r", "\n")
        code = code.strip("\n")
        ticks = "```"
        while ticks in code:
            ticks += "`"
        return f"\n\n{ticks}{mapped}\n{code}\n{ticks}\n\n"

    def body_to_markdown(self, entry: Tag) -> str:
        self.rewrite_images(entry)
        self.rewrite_links(entry)
        fences: list[tuple[str, str]] = []
        raws: list[tuple[str, str]] = []

        for block in entry.select("div.urvanov-syntax-highlighter-syntax"):
            label = ""
            label_el = block.select_one(".crayon-language")
            if label_el:
                label = label_el.get_text(strip=True)
            area = block.select_one("textarea.urvanov-syntax-highlighter-plain")
            code = area.get_text() if area else block.get_text("\n")
            token = f"URVANOVBLOCK{len(fences):04d}"
            fences.append((token, self.fence(label, code)))
            replacement = entry.new_tag("p")
            replacement.string = token
            block.replace_with(replacement)

        for pre in entry.select("pre"):
            token = f"URVANOVBLOCK{len(fences):04d}"
            fences.append((token, self.fence("", pre.get_text())))
            replacement = entry.new_tag("p")
            replacement.string = token
            pre.replace_with(replacement)

        for node in entry.select("script, iframe"):
            token = f"RAWHTMLBLOCK{len(raws):04d}"
            raws.append((token, str(node)))
            replacement = entry.new_tag("p")
            replacement.string = token
            node.replace_with(replacement)

        for span in list(entry.select("span[id]")):
            span_id = span.get("id") or ""
            if span_id.startswith("more-"):
                marker = entry.new_tag("p")
                marker.string = "HUGOMORESPLIT"
                span.replace_with(marker)

        for meta in entry.select(".entry-meta"):
            meta.decompose()

        html = entry.decode_contents()
        text = markdownify(html, heading_style="ATX", bullets="-")
        text = text.replace("HUGOMORESPLIT", "<!--more-->")
        for token, fence in fences:
            text = text.replace(token, fence)
        for token, raw in raws:
            text = text.replace(token, "\n\n" + raw + "\n\n")
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        return text + "\n"

    def body_to_html(self, entry: Tag) -> str:
        self.rewrite_images(entry)
        self.rewrite_links(entry)
        for meta in entry.select(".entry-meta"):
            meta.decompose()
        return entry.decode_contents().strip() + "\n"

    def remember_term(self, bucket: dict[str, dict[str, str]], href: str, title: str, prefix: str) -> None:
        path = local_path(href) or href
        if not path.startswith(prefix):
            return
        leaf = path.strip("/").split("/")[-1]
        current = bucket.get(leaf)
        if current and current["url"] != path:
            raise SystemExit(f"term leaf collision for {leaf}: {current['url']} vs {path}")
        bucket[leaf] = {"title": title.strip(), "url": path if path.endswith("/") else path + "/"}

    def parse_comments(self, article_root: BeautifulSoup, slug: str) -> None:
        listing = article_root.select_one("ol.comment-list")
        if listing is None:
            return
        records = []

        def walk(node: Tag, parent: int) -> None:
            for item in node.find_all("li", recursive=False):
                item_id = item.get("id") or ""
                if not item_id.startswith("comment-"):
                    continue
                cid = int(item_id.split("-", 1)[1])
                author_el = item.select_one("b.fn")
                author = author_el.get_text(" ", strip=True) if author_el else ""
                author_url = ""
                if author_el and author_el.find("a"):
                    author_url = author_el.find("a").get("href") or ""
                time_el = item.select_one("time[datetime]")
                when = time_el.get("datetime") if time_el else ""
                content = item.select_one(".comment-content")
                html = content.decode_contents().strip() if content else ""
                classes = item.get("class") or []
                records.append(
                    {
                        "id": cid,
                        "parent": parent,
                        "author": author,
                        "author_url": author_url,
                        "date": when,
                        "by_post_author": "bypostauthor" in classes,
                        "html": html,
                    }
                )
                self.comment_ids.append(cid)
                child_list = item.find("ol", class_="children", recursive=False)
                if child_list:
                    walk(child_list, cid)

        walk(listing, 0)
        if not records:
            return
        self.comment_count += len(records)
        dest = ROOT / "data" / "comments" / f"{slug}.yaml"
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(records, handle, allow_unicode=True, sort_keys=False, width=10000)

    def write_post(self, slug: str, fields: dict, body: str) -> None:
        lines = ["---", f"title: {q(fields['title'])}", f"date: {fields['date']}"]
        if fields.get("lastmod") and fields["lastmod"] != fields["date"]:
            lines.append(f"lastmod: {fields['lastmod']}")
        lines.append(f"slug: {q(slug)}")
        lines.append(f"url: {fields['url']}")
        lines.append("author:")
        lines.append('  - "jhowe"')
        lines.append(f"year: [{q(fields['year'])}]")
        lines.append(f"month: [{q(fields['month'])}]")
        lines.append("categories:" if fields["categories"] else "categories: []")
        for name in fields["categories"]:
            lines.append(f"  - {q(name)}")
        lines.append("tags:" if fields["tags"] else "tags: []")
        for name in fields["tags"]:
            lines.append(f"  - {q(name)}")
        aliases = self.aliases.get(fields["url"], [])
        aliases = list(dict.fromkeys(aliases + [fields["url"].rstrip("/") + "/feed/"]))
        lines.append("aliases:")
        for alias in aliases:
            lines.append(f"  - {q(alias)}")
        lines.append("---")
        dest = ROOT / "content" / "posts" / f"{slug}.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text("\n".join(lines) + "\n\n" + body, encoding="utf-8")

    def parse_dates(self, article: Tag) -> tuple[str, str]:
        meta = article.select_one(".entry-meta")
        published = ""
        updated = ""
        if meta:
            for stamp in meta.select("time[datetime]"):
                classes = stamp.get("class") or []
                if "published" in classes or ("entry-date" in classes and not published):
                    if "published" in classes or not published:
                        published = stamp["datetime"]
                if "updated" in classes and "published" not in classes:
                    updated = stamp["datetime"]
        if not published:
            raise SystemExit(f"missing published time in {article.get('id')}")
        return published, updated or published

    def extract_post(self, path: Path) -> None:
        slug = path.parent.name
        url = "/" + "/".join(path.relative_to(ROOT).parts[:-1]) + "/"
        if not re.fullmatch(r"/\d{4}/\d{2}/\d{2}/[^/]+/", url):
            raise SystemExit(f"bad post url {url} for {path}")
        soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="replace"), "lxml")
        article = soup.select_one("article")
        if article is None:
            raise SystemExit(f"no article in {path}")
        title_el = article.select_one("h3.overlay-h-title")
        title = title_el.get_text(" ", strip=True) if title_el else ""
        if not title and soup.title:
            title = re.sub(r"\s+-\s+VirtJunkie\s*$", "", soup.title.get_text(strip=True))
        published, updated = self.parse_dates(article)
        day = published[:10]
        categories = []
        tags = []
        footer = article.select_one("footer.entry-footer")
        if footer:
            seen_cats = set()
            for link in footer.select(".cat-links a[href]"):
                for cat_url in self.expand_category(link["href"]):
                    if cat_url in seen_cats:
                        continue
                    seen_cats.add(cat_url)
                    name = self.category_titles.get(cat_url) or link.get_text(" ", strip=True)
                    # Term files are keyed by the URL leaf. Front matter must use that
                    # leaf so Hugo does not invent a second term from the display title
                    # ("Windows Stuff" would become /categories/windows-stuff/).
                    categories.append(cat_url.strip("/").split("/")[-1])
                    self.remember_term(self.categories, cat_url, name, "/category/")
            for link in footer.select(".tags-links a[href]"):
                name = link.get_text(" ", strip=True)
                href = local_path(link["href"]) or link["href"]
                tags.append(href.strip("/").split("/")[-1])
                self.remember_term(self.tags, link["href"], name, "/tag/")
        entry = article.select_one(".entry-content")
        if entry is None:
            raise SystemExit(f"no entry-content in {path}")
        self.parse_comments(soup, slug)
        body = self.body_to_markdown(entry)
        year, month = day[:4], day[:7]
        self.years.add(year)
        self.months.add(month)
        self.write_post(
            slug,
            {
                "title": title or slug,
                "date": published,
                "lastmod": updated,
                "url": url,
                "year": year,
                "month": month,
                "categories": categories,
                "tags": tags,
            },
            body,
        )
        self.posts.append({"slug": slug, "url": url, "date": published})

    def extract_page(self, path: Path, dest: Path, *, html: bool, title: str | None = None, aliases: list[str] | None = None) -> None:
        soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="replace"), "lxml")
        article = soup.select_one("article") or soup
        entry = article.select_one(".entry-content")
        if entry is None:
            raise SystemExit(f"no entry-content in {path}")
        if title is None:
            title_el = article.select_one("h3.overlay-h-title")
            title = title_el.get_text(" ", strip=True) if title_el else ""
            if not title and soup.title:
                title = re.sub(r"\s+-\s+VirtJunkie\s*$", "", soup.title.get_text(strip=True))
        body = self.body_to_html(entry) if html else self.body_to_markdown(entry)
        dest.parent.mkdir(parents=True, exist_ok=True)
        alias_yaml = ""
        if aliases:
            alias_yaml = "aliases:\n" + "".join(f"  - {q(alias)}\n" for alias in aliases)
        dest.write_text(f"---\ntitle: {q(title or dest.stem)}\n{alias_yaml}---\n\n{body}", encoding="utf-8")

    def load_category_titles(self) -> None:
        for path in (ROOT / "category").rglob("index.html"):
            parts = path.relative_to(ROOT).parts
            if "page" in parts or "feed" in parts:
                continue
            url = "/" + "/".join(parts[:-1]) + "/"
            soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="replace"), "lxml")
            label = soup.select_one("h3.overlay-h-title span")
            title = label.get_text(" ", strip=True) if label else parts[-2].replace("-", " ")
            self.category_titles[url] = title

    def expand_category(self, href: str) -> list[str]:
        path = local_path(href) or ""
        if not path.startswith("/category/"):
            return []
        if not path.endswith("/"):
            path += "/"
        found = []
        current = path
        while current.startswith("/category/") and current != "/category/":
            if current in self.category_titles:
                found.append(current)
            parent = current.rstrip("/").rsplit("/", 1)[0] + "/"
            if parent == current:
                break
            current = parent
        return found

    def load_redirects(self) -> None:
        for path in ROOT.iterdir():
            index = path / "index.html"
            if not path.is_dir() or not index.is_file():
                continue
            head = index.read_text(encoding="utf-8", errors="replace")[:400]
            if "Redirecting" not in head:
                continue
            match = re.search(r'url=(/[^"\']+)', head)
            if not match:
                raise SystemExit(f"redirect without target: {index}")
            target = match.group(1)
            if not target.endswith("/"):
                target += "/"
            source = "/" + path.name + "/"
            self.aliases.setdefault(target, []).append(source)

    def write_terms(self) -> None:
        for leaf, info in sorted(self.categories.items()):
            self.write_term(ROOT / "content" / "categories" / leaf / "_index.md", info["title"], info["url"])
        for leaf, info in sorted(self.tags.items()):
            self.write_term(ROOT / "content" / "tags" / leaf / "_index.md", info["title"], info["url"])
        for year in sorted(self.years):
            self.write_term(ROOT / "content" / "year" / year / "_index.md", year, f"/{year}/", alias_feed=False)
        for month in sorted(self.months):
            year, mm = month.split("-")
            self.write_term(ROOT / "content" / "month" / month / "_index.md", month, f"/{year}/{mm}/", alias_feed=False)
        self.write_term(ROOT / "content" / "author" / "jhowe" / "_index.md", "Jon", "/author/jhowe/")

    def write_term(self, path: Path, title: str, url: str, *, alias_feed: bool = True) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = ["---", f"title: {q(title)}", f"url: {url}"]
        if alias_feed:
            lines.append("aliases:")
            lines.append(f"  - {q(url.rstrip('/') + '/feed/')}")
        lines.append("---")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_static_redirect(self, rel: str, target: str) -> None:
        dest = ROOT / "static" / rel / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(
            "<!DOCTYPE html>\n<html><head>"
            f'<meta http-equiv="refresh" content="0; url={target}">'
            f'<link rel="canonical" href="{target}">'
            "<title>Redirecting...</title></head>"
            f'<body><p><a href="{target}">Redirecting...</a></p></body></html>\n',
            encoding="utf-8",
        )

    def copy_uploads(self) -> None:
        for rel in FAVICONS:
            source = ROOT / rel
            if source.is_file():
                self.copies["/" + rel] = source
        for web_path, source in self.copies.items():
            dest = ROOT / "static" / web_path.lstrip("/")
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists() or dest.stat().st_size != source.stat().st_size:
                shutil.copy2(source, dest)

    def reset_outputs(self) -> None:
        for path in [
            ROOT / "content" / "posts",
            ROOT / "content" / "categories",
            ROOT / "content" / "tags",
            ROOT / "content" / "year",
            ROOT / "content" / "month",
            ROOT / "content" / "author",
            ROOT / "data" / "comments",
            ROOT / "static" / "wp-content",
        ]:
            if path.exists():
                shutil.rmtree(path)

    def check_comments(self) -> None:
        expected = []
        for path in ROOT.glob("[0-9][0-9][0-9][0-9]/*/*/*/index.html"):
            text = path.read_text(encoding="utf-8", errors="replace")
            expected.extend(int(n) for n in re.findall(r'<li id="comment-(\d+)"', text))
        if sorted(expected) != sorted(self.comment_ids):
            missing = sorted(set(expected) - set(self.comment_ids))
            extra = sorted(set(self.comment_ids) - set(expected))
            raise SystemExit(f"comment mismatch missing={missing[:10]} extra={extra[:10]} expected={len(expected)} got={len(self.comment_ids)}")
        vrops = ROOT / "data" / "comments" / "vrops-opsgenie-production-setup.yaml"
        records = yaml.safe_load(vrops.read_text(encoding="utf-8"))
        by_id = {item["id"]: item for item in records}
        if by_id[262]["parent"] != 261:
            raise SystemExit("comment 262 is not a reply to 261")
        if by_id[261]["author"] != "sz" or by_id[262]["author"] != "Jon":
            raise SystemExit("unexpected vROps comment authors")

    def run(self) -> None:
        self.load_redirects()
        self.load_category_titles()
        self.reset_outputs()
        posts = []
        for path in sorted(ROOT.glob("[0-9][0-9][0-9][0-9]/*/*/*/index.html")):
            parts = path.relative_to(ROOT).parts
            if parts[1].isdigit() and parts[2].isdigit() and parts[3] not in {"page", "feed"}:
                posts.append(path)
        print(f"posts: {len(posts)}", file=sys.stderr)
        seen = set()
        for path in posts:
            slug = path.parent.name
            if slug in seen:
                raise SystemExit(f"duplicate slug {slug}")
            seen.add(slug)
            self.extract_post(path)
        self.extract_page(ROOT / "index.html", ROOT / "content" / "_index.md", html=True, title="About Jon", aliases=["/about-jon/feed/"])
        self.extract_page(ROOT / "privacy-policy-2" / "index.html", ROOT / "content" / "privacy-policy-2.md", html=False)
        self.extract_page(ROOT / "sample-page" / "index.html", ROOT / "content" / "sample-page.md", html=False, aliases=["/sample-page/feed/"])
        self.extract_page(ROOT / "thank-you" / "index.html", ROOT / "content" / "thank-you.md", html=False)
        posts_index = ROOT / "content" / "posts" / "_index.md"
        posts_index.write_text('---\ntitle: "Posts"\n---\n', encoding="utf-8")
        search = ROOT / "content" / "search" / "_index.md"
        search.parent.mkdir(parents=True, exist_ok=True)
        search.write_text(
            '---\ntitle: "Search"\nurl: /search/\nlayout: search\n_build:\n  list: false\n  render: true\n---\n',
            encoding="utf-8",
        )
        self.write_terms()
        self.write_static_redirect("feed/atom", "/feed/")
        self.write_static_redirect("feed/rdf", "/feed/")
        self.write_static_redirect("comments/feed", "/feed/")
        self.copy_uploads()
        self.check_comments()
        summary = {
            "posts": len(self.posts),
            "comments": self.comment_count,
            "categories": len(self.categories),
            "tags": len(self.tags),
            "years": sorted(self.years),
            "months": len(self.months),
            "images": len(self.copies),
            "missing_images": self.missing_images,
            "languages": sorted(self.languages),
            "aliases": {k: v for k, v in self.aliases.items()},
        }
        (ROOT / "scripts" / "extract-manifest.json").write_text(
            json.dumps(summary, indent=2), encoding="utf-8"
        )
        print(json.dumps({k: summary[k] for k in ("posts", "comments", "categories", "tags", "images")}, indent=2))
        if self.missing_images:
            print(f"missing images: {len(self.missing_images)}", file=sys.stderr)
            for item in self.missing_images[:20]:
                print(" ", item, file=sys.stderr)


if __name__ == "__main__":
    Extractor().run()
