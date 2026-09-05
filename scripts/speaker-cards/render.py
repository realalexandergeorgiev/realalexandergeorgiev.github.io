#!/usr/bin/env python3
"""Render BSides Frankfurt speaker cards as PNGs.

Usage: python3 scripts/speaker-cards/render.py [--background OPTION]
Options for --background: "transparent" (default), "page" (site bg color),
                          or a hex color like "#1a1c1f".
Output: static/mediakit/speaker-cards/<slug>.png (960px wide, uniform height,
        3x scale). All cards share one fixed height (tallest card) so every
        image has identical dimensions.
"""

import argparse
import functools
import html
import http.server
import math
import os
import pathlib
import re
import shutil
import socketserver
import sys
import threading
import time
import unicodedata
from urllib.parse import unquote

VENV_DIR = pathlib.Path(__file__).resolve().parent / ".venv"
VENV_PYTHON = VENV_DIR / "bin" / "python"
if VENV_PYTHON.exists() and pathlib.Path(sys.prefix).resolve() != VENV_DIR.resolve():
    os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), __file__, *sys.argv[1:]])

import yaml
from playwright.sync_api import sync_playwright

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
TMP_DIR = SCRIPT_DIR / ".tmp"
OUT_DIR = REPO_ROOT / "static" / "mediakit" / "speaker-cards"
PORT = 8765
ORIGIN = f"http://127.0.0.1:{PORT}"
CARD_WIDTH = 320
SCALE = 3

# ISO/IEC 7810 ID-1 (CR80) credit-card format: 85.60 x 54.00 mm.
# 428:270 == 85.6:54 exactly (both x5), so 3x scale yields a ratio-exact PNG.
ID1_WIDTH = 428
ID1_HEIGHT = 270
ID1P_WIDTH = 270
ID1P_HEIGHT = 428

_CLAMP_2_LINES = """    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }"""

ID1_CSS = f"""
  .speaker-card--id1 {{
    position: relative;
    flex-direction: row;
    align-items: center;
    gap: 14px;
    padding: 20px;
    min-height: 0;
    text-align: left;
    overflow: hidden;
  }}
  .speaker-card--id1 .speaker-card__photo {{
    width: 96px;
    height: 96px;
  }}
  .speaker-card--id1 .speaker-card__initials {{
    font-size: 1.6rem;
  }}
  .speaker-card--id1 .speaker-card__body {{
    flex: 1;
    min-width: 0;
    align-items: flex-start;
    gap: 5px;
    padding-bottom: 30px;
  }}
  .speaker-card--id1 .speaker-card__name {{ font-size: 1.15rem; }}
  .speaker-card--id1 .speaker-card__role,
  .speaker-card--id1 .speaker-card__talk {{
{_CLAMP_2_LINES}
  .speaker-card--id1 .speaker-card__role {{ font-size: 0.6rem; }}
  .speaker-card--id1 .speaker-card__talk {{ font-size: 0.78rem; margin: 0; }}
  .speaker-card--id1 .speaker-card__bio {{ font-size: 0.72rem; }}
  .speaker-card--id1 .speaker-card__logo {{
    position: absolute;
    right: 16px;
    bottom: 12px;
    width: 104px;
    margin-top: 0;
    opacity: 0.9;
  }}
"""

ID1P_CSS = f"""
  .speaker-card--id1p {{
    gap: 8px;
    padding: 18px;
    min-height: 0;
    overflow: hidden;
  }}
  .speaker-card--id1p .speaker-card__photo {{
    width: 88px;
    height: 88px;
    flex: 0 0 auto;
  }}
  .speaker-card--id1p .speaker-card__initials {{
    font-size: 1.5rem;
  }}
  .speaker-card--id1p .speaker-card__body {{
    gap: 5px;
  }}
  .speaker-card--id1p .speaker-card__name {{ font-size: 1.1rem; }}
  .speaker-card--id1p .speaker-card__role,
  .speaker-card--id1p .speaker-card__talk {{
{_CLAMP_2_LINES}
  .speaker-card--id1p .speaker-card__role {{ font-size: 0.58rem; }}
  .speaker-card--id1p .speaker-card__talk {{ font-size: 0.75rem; margin: 0; }}
  .speaker-card--id1p .speaker-card__bio {{ font-size: 0.7rem; }}
  .speaker-card--id1p .speaker-card__logo {{
    width: 110px;
    opacity: 0.9;
  }}
"""

# fmt name -> (card width px, fixed height px or None for auto, extra CSS class, extra CSS)
FORMATS = {
    "portrait": (CARD_WIDTH, None, None, ""),
    "id1": (ID1_WIDTH, ID1_HEIGHT, "speaker-card--id1", ID1_CSS),
    "id1-portrait": (ID1P_WIDTH, ID1P_HEIGHT, "speaker-card--id1p", ID1P_CSS),
}

_HEIGHT_CACHE: dict[tuple[str, str | None], float] = {}

VERSION = "1.0.0"
BUILD_DATE = "2026-08-14"
AUTHOR = "Alexander Georgiev + DeepSeek V4"
TOOL_INFO = f"BSides Frankfurt Speaker-Card Renderer v{VERSION} (build {BUILD_DATE}) by {AUTHOR}"


class InfoArgumentParser(argparse.ArgumentParser):
    """ArgumentParser that shows the tool info banner above the help text."""

    def format_help(self):
        return f"{TOOL_INFO}\n\n{super().format_help()}"


SAMPLES = {
    "gold-auf-dunkelblau": {"card_bg": "#011023", "accent": "#d4af37", "accent_secondary": "#b8941f"},
    "gold-auf-navy": {"card_bg": "#0a1930", "accent": "#d4af37", "accent_secondary": "#e09c31"},
    "bronze": {"card_bg": "#121314", "accent": "#cd7f32", "accent_secondary": "#b8732a"},
    "kupfer": {"card_bg": "#121314", "accent": "#a06523", "accent_secondary": "#b8732a"},
    "rot-auf-navy": {"card_bg": "#0a1930", "accent": "#eb3812", "accent_secondary": "#a06523"},
    "rot-auf-dunkelblau": {"card_bg": "#011023", "accent": "#eb3812", "accent_secondary": "#a06523"},
    "silber": {"card_bg": "#1a1c1f", "accent": "#c0c0c0", "accent_secondary": "#7a7a7a"},
    "anthrazit": {"card_bg": "#2a2d31", "accent": "#c0c0c0", "accent_secondary": "#7a7a7a"},
    "gold-gruen": {"card_bg": "#121314", "accent": "#d4af37", "accent_secondary": "#9acd32"},
    "gelb-gold": {"card_bg": "#121314", "accent": "#e09c31", "accent_secondary": "#b8941f"},
    "gruen": {"card_bg": "#9acd32", "text": "#011023", "accent": "#011023",
              "accent_secondary": "#eb3812", "logo": "dark"},
    "weiss": {"card_bg": "#ffffff", "text": "#011023", "accent": "#9acd32",
              "accent_secondary": "#eb3812", "logo": "dark"},
    "hellgrau": {"card_bg": "#f5f5f5", "text": "#121314", "accent": "#7a7a7a",
                 "accent_secondary": "#c0c0c0", "logo": "dark"},
}


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """Serve repo root, falling back to static/ for Hugo's web-root URLs."""

    def log_message(self, *args):
        pass

    def translate_path(self, path):
        rel = unquote(path).lstrip("/")
        root = pathlib.Path(self.directory)
        target = root / rel
        if not target.exists():
            fallback = root / "static" / rel
            if fallback.exists():
                target = fallback
        return str(target)


def slugify(name: str) -> str:
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "-", name)
    return name.strip("-")


def card_html(s: dict, logo: str, bio_text: str | None = None,
              card_height: int | None = None, fmt: str = "portrait") -> str:
    if s.get("photo"):
        photo = (
            '<div class="speaker-card__photo">'
            f'<img src="{html.escape(s["photo"])}" alt="{html.escape(s["name"])}" loading="eager">'
            "</div>"
        )
    else:
        initials = "".join(p[:1] for p in s["name"].split()[:2]).upper()
        photo = (
            '<div class="speaker-card__photo">'
            f'<span class="speaker-card__initials" aria-hidden="true">{html.escape(initials)}</span>'
            "</div>"
        )

    talk = s.get("talk") or s.get("workshop")
    parts = [f'<h3 class="speaker-card__name">{html.escape(s["name"])}</h3>']
    if s.get("role"):
        parts.append(f'<p class="speaker-card__role">{html.escape(s["role"])}</p>')
    if talk:
        parts.append(f'<p class="speaker-card__talk">"{html.escape(talk)}"</p>')
    if s.get("bio"):
        if bio_text is not None:
            parts.append(f'<p class="speaker-card__bio">{html.escape(bio_text)}</p>')
        else:
            parts.append(
                f'<p class="speaker-card__bio" title="{html.escape(s["bio"])}">{html.escape(s["bio"])}</p>'
            )

    logo_file = "bsides_logo_white.png" if logo == "light" else "bsides_logo_black.png"
    logo = (
        f'<img class="speaker-card__logo" src="/mediakit/logos/{logo_file}" '
        'alt="BSides Frankfurt" loading="eager">'
    )

    fmt_width, _, fmt_class, _ = FORMATS[fmt]
    size = f"width:{fmt_width}px"
    if card_height is not None:
        size += f";height:{card_height}px"

    card_class = "speaker-card" + (f" {fmt_class}" if fmt_class else "")
    return (
        f'<article class="{card_class}" style="{size}">{photo}'
        f'<div class="speaker-card__body">{"".join(parts)}</div>{logo}</article>'
    )


def parse_args() -> argparse.Namespace:
    parser = InfoArgumentParser(
        description="Render BSides Frankfurt speaker cards from data/speakers.yaml as PNGs."
    )
    parser.add_argument(
        "--background",
        default="transparent",
        metavar="transparent|page|#RRGGBB",
        help='Background around the card: "transparent" (default, alpha channel), '
        '"page" (website background color #011023), or a hex color like "#1a1c1f".',
    )
    parser.add_argument(
        "--card-bg",
        metavar="#RRGGBB",
        help='Card background color (default: dark gray #121314). Example: "#1a1c1f".',
    )
    parser.add_argument(
        "--accent",
        metavar="#RRGGBB",
        help='Accent color for role text and photo gradient (default: green #9acd32).',
    )
    parser.add_argument(
        "--accent-secondary",
        metavar="#RRGGBB",
        help="Second accent for the photo gradient (default: orange #eb3812).",
    )
    parser.add_argument(
        "--text",
        metavar="#RRGGBB",
        help='Text color for name, talk and bio (default: white). Use with light card '
        'backgrounds, e.g. "#011023".',
    )
    parser.add_argument(
        "--logo",
        choices=["light", "dark"],
        default="light",
        help='BSides logo variant: "light" (white, default, for dark cards) or "dark" '
        "(black, for light cards).",
    )
    parser.add_argument(
        "--samples",
        action="store_true",
        help="Render all predefined color samples (see SAMPLES) to "
        "static/mediakit/speaker-cards/tests/.",
    )
    parser.add_argument(
        "--all-samples",
        action="store_true",
        help="Render every speaker in all sample templates (named <slug>-<sample>.png).",
    )
    parser.add_argument(
        "--output",
        metavar="DIR",
        help="Output directory (default: static/mediakit/speaker-cards/). "
        "--samples writes to <DIR>/tests/.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=TOOL_INFO,
    )
    parser.add_argument(
        "--format",
        choices=list(FORMATS),
        default="portrait",
        help='Card format: "portrait" (default, 320px wide, uniform height), '
        '"id1" (credit card ISO/IEC 7810 ID-1 / CR80, landscape, 85.60 x 54.00 mm) '
        "or \"id1-portrait\" (same card ratio in portrait, 54.00 x 85.60 mm). "
        "ID-1 files are named <slug>-id1.png / <slug>-id1-portrait.png.",
    )
    parser.add_argument(
        "--bio-text",
        metavar="TEXT",
        help='Hide the speaker bio and show this static text instead, e.g. '
        '"September 10, 2026".',
    )
    return parser.parse_args()


def parse_color(value: str, option: str) -> str:
    if re.fullmatch(r"#[0-9a-fA-F]{3,8}", value):
        return value
    raise SystemExit(f'Invalid value for --{option}: "{value}" (use a hex color like "#1a1c1f")')


def card_style_overrides(opts: dict) -> str:
    overrides = [
        ("--color-surface", opts.get("card_bg"), "card-bg"),
        ("--color-primary", opts.get("accent"), "accent"),
        ("--color-secondary", opts.get("accent_secondary"), "accent-secondary"),
        ("--color-text", opts.get("text"), "text"),
        ("--color-text-muted", opts.get("text"), "text"),
    ]
    lines = []
    for var, value, option in overrides:
        if value:
            lines.append(f"  {var}: {parse_color(value, option)};")
    return "\n".join(lines)


def background_css(value: str) -> str:
    if value == "transparent":
        return "transparent"
    if value == "page":
        return "var(--color-bg)"
    return parse_color(value, "background")


def page_html(s: dict, background: str, card_overrides: str, logo: str,
              bio_text: str | None = None, card_height: int | None = None,
              fmt: str = "portrait") -> str:
    card_css = f".speaker-card {{\n{card_overrides}\n}}\n" if card_overrides else ""
    fmt_css = FORMATS[fmt][3]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="{ORIGIN}/assets/css/main.css">
<style>
  html, body {{ background: {background} !important; }}
  body {{ margin: 0; padding: 0; }}
{card_css}{fmt_css}  .speaker-card__logo {{
    margin-top: auto;
    width: 170px;
    height: auto;
    opacity: 0.95;
  }}
</style>
</head>
<body>
{card_html(s, logo, bio_text, card_height, fmt)}
</body>
</html>"""


def open_card_page(browser, s: dict, background: str, card_overrides: str, logo: str,
                   bio_text: str | None, card_height: int | None = None,
                   fmt: str = "portrait"):
    slug = slugify(s["name"])
    tmp_file = TMP_DIR / f"{slug}.html"
    tmp_file.write_text(
        page_html(s, background, card_overrides, logo, bio_text, card_height, fmt),
        encoding="utf-8",
    )

    card_width = FORMATS[fmt][0]
    context = browser.new_context(
        device_scale_factor=SCALE,
        viewport={"width": card_width + 80, "height": 800},
    )
    page = context.new_page()
    page.goto(
        f"{ORIGIN}/scripts/speaker-cards/.tmp/{slug}.html",
        wait_until="networkidle",
    )
    page.evaluate("document.fonts.ready.then(() => true)")
    return context, page


def uniform_card_height(browser, speakers: list, background: str, card_overrides: str,
                        logo: str, bio_text: str | None) -> int:
    """Measure every card's natural height and return one fixed height for all.

    Heights depend only on speaker content and --bio-text (not on colors or the
    logo variant), so they are cached across sample-template batches.
    """
    for s in speakers:
        key = (slugify(s["name"]), bio_text)
        if key in _HEIGHT_CACHE:
            continue
        context, page = open_card_page(browser, s, background, card_overrides, logo, bio_text)
        _HEIGHT_CACHE[key] = page.locator(".speaker-card").bounding_box()["height"]
        context.close()
    return math.ceil(max(_HEIGHT_CACHE[(slugify(s["name"]), bio_text)] for s in speakers))


def render_cards(browser, speakers: list, opts: dict, out_dir: pathlib.Path, prefix: str = "") -> None:
    background = background_css(opts["background"])
    card_overrides = card_style_overrides(opts)
    logo = opts["logo"]
    bio_text = opts.get("bio_text")
    fmt = opts.get("format") or "portrait"
    out_dir.mkdir(parents=True, exist_ok=True)

    if fmt != "portrait":
        _, card_height, _, _ = FORMATS[fmt]
        prefix = f"{prefix}-{fmt}" if prefix else fmt
        print(f"{fmt} format: {FORMATS[fmt][0]}x{card_height}px "
              f"({FORMATS[fmt][0] * SCALE}x{card_height * SCALE}px at {SCALE}x)")
    else:
        card_height = uniform_card_height(browser, speakers, background, card_overrides, logo, bio_text)
        print(f"Uniform card height: {card_height}px ({card_height * SCALE}px at {SCALE}x)")

    for s in speakers:
        slug = slugify(s["name"])
        context, page = open_card_page(browser, s, background, card_overrides, logo,
                                       bio_text, card_height, fmt)
        box = page.locator(".speaker-card").bounding_box()
        name = f"{slug}-{prefix}.png" if prefix else f"{slug}.png"
        out_file = out_dir / name
        page.locator(".speaker-card").screenshot(path=str(out_file), omit_background=True)
        context.close()

        try:
            shown = out_file.relative_to(REPO_ROOT)
        except ValueError:
            shown = out_file
        print(f"{s['name']:<28} {shown}  {int(box['width'])}x{int(box['height'])}px")


def main() -> None:
    args = parse_args()
    print(TOOL_INFO)
    out_dir = pathlib.Path(args.output) if args.output else OUT_DIR
    speakers = yaml.safe_load((REPO_ROOT / "data" / "speakers.yaml").read_text(encoding="utf-8"))

    socketserver.TCPServer.allow_reuse_address = True
    handler = functools.partial(QuietHandler, directory=str(REPO_ROOT))
    with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        time.sleep(0.3)

        TMP_DIR.mkdir(parents=True, exist_ok=True)
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    executable_path="/snap/bin/chromium",
                    headless=True,
                    args=["--no-sandbox", "--disable-gpu"],
                )
                try:
                    if args.samples:
                        print(f"Rendering {len(SAMPLES)} color samples ...")
                        for name, sample in SAMPLES.items():
                            render_cards(browser, speakers, {**vars(args), **sample}, out_dir / "tests", prefix=name)
                    if args.all_samples:
                        print(f"Rendering all speakers in {len(SAMPLES)} sample templates ...")
                        for name, sample in SAMPLES.items():
                            render_cards(browser, speakers, {**vars(args), **sample}, out_dir, prefix=name)
                    if not args.samples and not args.all_samples:
                        render_cards(browser, speakers, vars(args), out_dir)
                finally:
                    browser.close()
        finally:
            shutil.rmtree(TMP_DIR, ignore_errors=True)
            httpd.shutdown()
            httpd.server_close()


if __name__ == "__main__":
    main()
