from __future__ import annotations

import base64
import hashlib
import mimetypes
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = Path("/Users/andyduan26/Desktop/html_clean_py")
PAGES = {
    "首页clean.html": "index.html",
    "分类页clean.html": "category.html",
    "播放页clean.html": "play.html",
}
ASSETS_DIR = ROOT / "assets"
PLACEHOLDER = ASSETS_DIR / "placeholder.png"


def ensure_placeholder() -> None:
    ASSETS_DIR.mkdir(exist_ok=True)
    if not PLACEHOLDER.exists():
        PLACEHOLDER.write_bytes(
            base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
            )
        )


def ext_for_mime(mime: str) -> str:
    if mime == "image/webp":
        return ".webp"
    if mime == "image/svg+xml":
        return ".svg"
    return mimetypes.guess_extension(mime) or ".bin"


def save_data_asset(data_uri: str, prefix: str, manifest: list[str]) -> str:
    match = re.match(r"data:([^;,]+)(;base64)?,(.*)", data_uri, re.S)
    if not match:
        return "./assets/placeholder.png"
    mime, is_base64, payload = match.groups()
    raw = base64.b64decode(payload) if is_base64 else payload.encode()
    digest = hashlib.sha1(raw).hexdigest()[:12]
    filename = f"{prefix}_{digest}{ext_for_mime(mime)}"
    target = ASSETS_DIR / filename
    if not target.exists():
        target.write_bytes(raw)
    manifest.append(f"{filename}\t{prefix}\t从 data URI/base64 外提")
    return f"./assets/{filename}"


def strip_noisy_attrs(html: str) -> str:
    noisy = (
        r"\sdata-aplus-[\w-]+(?:=(\"[^\"]*\"|'[^']*'|[^\s>]+))?",
        r"\sdata-spm(?:-[\w-]+)?(?:=(\"[^\"]*\"|'[^']*'|[^\s>]+))?",
        r"\sdata-trackinfo=(\"[^\"]*\"|'[^']*'|[^\s>]+)",
        r"\sdata-utparam=(\"[^\"]*\"|'[^']*'|[^\s>]+)",
        r"\sdata-scm(?:=(\"[^\"]*\"|'[^']*'|[^\s>]+))?",
        r"\sdata-expose_id(?:=(\"[^\"]*\"|'[^']*'|[^\s>]+))?",
        r"\sdata-trackinfo(?:=(\"[^\"]*\"|'[^']*'|[^\s>]+))?",
    )
    for pattern in noisy:
        html = re.sub(pattern, "", html)
    return html


def strip_tag_blocks(html: str, tag: str) -> tuple[str, list[str]]:
    pattern = re.compile(rf"<{tag}\b[^>]*>(.*?)</{tag}>", re.I | re.S)
    blocks = [match.group(1) for match in pattern.finditer(html)]
    return pattern.sub("", html), blocks


def process_page(source: Path, output_name: str, styles: list[str], manifest: list[str]) -> None:
    html = source.read_text(encoding="utf-8", errors="ignore")
    html, _ = strip_tag_blocks(html, "script")
    html, page_styles = strip_tag_blocks(html, "style")
    styles.extend(page_styles)
    html = re.sub(r"<meta\b[^>]*(?:aplus|tencent-site-verification|content-security-policy|name=(?:data-spm|site))[^>]*>", "", html, flags=re.I)
    html = strip_noisy_attrs(html)

    page_prefix = output_name.replace(".html", "")

    html = re.sub(
        r"url\((data:[^)]+)\)",
        lambda match: f"url({save_data_asset(match.group(1), page_prefix, manifest)})",
        html,
    )
    html = re.sub(
        r"(<link\b[^>]*\bhref=)(\"|')(data:[^\"']+)(\2)",
        lambda match: match.group(1) + match.group(2) + save_data_asset(match.group(3), page_prefix, manifest) + match.group(4),
        html,
        flags=re.I,
    )

    def replace_img(match: re.Match[str]) -> str:
        tag = match.group(0)
        src_match = re.search(r"\ssrc=(\"[^\"]*\"|'[^']*'|[^\s>]+)", tag, re.I)
        data_src_match = re.search(r"\sdata-src=(\"[^\"]*\"|'[^']*'|[^\s>]+)", tag, re.I)
        src = src_match.group(1).strip("\"'") if src_match else ""
        data_src = data_src_match.group(1).strip("\"'") if data_src_match else ""
        new_src = src
        if data_src.startswith(("http://", "https://")):
            new_src = data_src
            manifest.append(f"{data_src}\t{output_name}\t图片 data-src")
        elif src.startswith("data:"):
            new_src = save_data_asset(src, page_prefix, manifest)
        elif src in {"[REMOVED_BASE64_IMG]", "[BASE64_ASSET]", "data:,"} or not src:
            new_src = "./assets/placeholder.png"
            manifest.append(f"placeholder.png\t{output_name}\t原占位图片")
        elif src.startswith(("http://", "https://", "./assets/")):
            manifest.append(f"{src}\t{output_name}\t图片 src")
        if src_match:
            return tag[: src_match.start(1)] + f'"{new_src}"' + tag[src_match.end(1) :]
        return tag[:-1] + f' src="{new_src}">'

    html = re.sub(r"<img\b[^>]*>", replace_img, html, flags=re.I)

    if output_name == "play.html":
        container = '<div class="video-player-container" data-vid="XNTIwMDU4NzU2MA=="></div>'
        player_pattern = re.compile(r"<div\b(?=[^>]*(?:id|class)=(?:\"[^\"]*youku-player[^\"]*\"|'[^']*youku-player[^']*'|[^\s>]*youku-player[^\s>]*))[^>]*>.*?</div>", re.I | re.S)
        html, count = player_pattern.subn(container, html, count=1)
        html = re.sub(r"\sposter=(\"data:[^\"]*\"|'data:[^']*'|data:[^\s>]+)", "", html, flags=re.I)
        if count == 0:
            html = re.sub(r"(<body\b[^>]*>)", r"\1" + container, html, count=1, flags=re.I)

    includes = '<link rel="stylesheet" href="./style.css"><script src="./base.js" defer></script>'
    if re.search(r"</head>", html, re.I):
        html = re.sub(r"</head>", includes + "</head>", html, count=1, flags=re.I)
    else:
        html = re.sub(r"(<html\b[^>]*>)", r"\1<head>" + includes + "</head>", html, count=1, flags=re.I)

    (ROOT / output_name).write_text(html, encoding="utf-8")


def normalize_css(styles: list[str], manifest: list[str]) -> str:
    css = "\n".join(dict.fromkeys(s.strip() for s in styles if s.strip()))

    def repl_data(match: re.Match[str]) -> str:
        return f"url({save_data_asset(match.group(1), 'style', manifest)})"

    css = re.sub(r"url\((data:[^)]+)\)", repl_data, css)
    vars_seen: dict[str, str] = {}

    def repl_placeholder(match: re.Match[str]) -> str:
        token = match.group(1)
        vars_seen.setdefault(token, "./assets/placeholder.png")
        return f'{token}: url("./assets/placeholder.png")'

    css = re.sub(r"(--sf-img-[\w-]+):\s*url\([\"']?\[BASE64_ASSET\][\"']?\)", repl_placeholder, css)
    css = css.replace("[REMOVED_BASE64_IMG]", "./assets/placeholder.png")
    css = css.replace("[BASE64_ASSET]", "./assets/placeholder.png")
    for token in vars_seen:
        manifest.append(f"placeholder.png\tstyle.css\t{token} 原 BASE64_ASSET")
    return css


def write_base_js() -> None:
    (ROOT / "base.js").write_text(
        """(() => {
  document.addEventListener('click', (event) => {
    const episode = event.target.closest('[data-episode], .episode, .episode_item, .anthology_item');
    if (episode && episode.parentElement) {
      episode.parentElement.querySelectorAll('.active, .current, .selected').forEach((item) => {
        if (item !== episode) item.classList.remove('active', 'current', 'selected');
      });
      episode.classList.add('active');
    }

    const modalClose = event.target.closest('[data-close], .close, .icon-close, .iconclose');
    if (modalClose) {
      const modal = modalClose.closest('.modal, .dialog, .popup, .loginnew_login_mask, [role=\"dialog\"]');
      if (modal) modal.style.display = 'none';
    }

    const pageItem = event.target.closest('.pagination a, .pagination button, [data-page]');
    if (pageItem) {
      pageItem.parentElement?.querySelectorAll('.active, .current, .selected').forEach((item) => {
        if (item !== pageItem) item.classList.remove('active', 'current', 'selected');
      });
      pageItem.classList.add('active');
    }
  });

  document.querySelectorAll('.video-player-container').forEach((player) => {
    player.setAttribute('aria-label', `Youku video player ${player.dataset.vid || ''}`.trim());
  });
})();\n""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_placeholder()
    styles: list[str] = []
    manifest: list[str] = ["资源\t页面/文件\t位置说明"]
    for source_name, output_name in PAGES.items():
        process_page(SOURCE_DIR / source_name, output_name, styles, manifest)
    (ROOT / "style.css").write_text(normalize_css(styles, manifest), encoding="utf-8")
    write_base_js()
    (ROOT / "assets清单.txt").write_text("\n".join(dict.fromkeys(manifest)) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
