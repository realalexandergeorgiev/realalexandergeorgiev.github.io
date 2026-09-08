#!/usr/bin/env python3
"""Render BSides Frankfurt speaker/team cards as PNGs.

Usage: python3 scripts/speaker-cards/render.py [--source speakers|team] [--background OPTION]
Options for --background: "transparent" (default), "page" (site bg color),
                           or a hex color like "#1a1c1f".
Output: static/mediakit/speaker-cards/<slug>.png or
        static/mediakit/team-cards/<slug>.png (960px wide, uniform height,
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
OUT_DIRS = {
    "speakers": REPO_ROOT / "static" / "mediakit" / "speaker-cards",
    "team": REPO_ROOT / "static" / "mediakit" / "team-cards",
}
OUT_DIR = OUT_DIRS["speakers"]  # default, kept for backwards compatibility
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
  .speaker-card--id1 .speaker-card__badge {{ font-size: 0.5rem; padding: 2px 9px 2px 11px; }}
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
  .speaker-card--id1p .speaker-card__badge {{ font-size: 0.5rem; padding: 2px 9px 2px 11px; }}
  .speaker-card--id1p .speaker-card__logo {{
    width: 110px;
    opacity: 0.9;
  }}
"""

DEFAULT_ACCENT = "#9acd32"

GLOW_INNER_CSS = """
  .speaker-card--glow-inner {
    box-shadow: inset 0 0 25px 6px __G1__, inset 0 0 70px 20px __G2__;
  }
"""


def glow_shadows(color: str) -> tuple[str, str]:
    """Derive two translucent shadow colors from the glow color (tight/wide)."""
    if re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        return color + "66", color + "30"
    return color, color

BADGE_CSS = """
  .speaker-card__badge {
    display: inline-block;
    font-family: var(--font-heading);
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--color-primary);
    border: 1px solid var(--color-primary);
    border-radius: 999px;
    padding: 3px 12px 3px 14px;
    margin: 0;
  }
"""

# fmt name -> (card width px, fixed height px or None for auto, extra CSS class, extra CSS)
FORMATS = {
    "portrait": (CARD_WIDTH, None, None, ""),
    "id1": (ID1_WIDTH, ID1_HEIGHT, "speaker-card--id1", ID1_CSS),
    "id1-portrait": (ID1P_WIDTH, ID1P_HEIGHT, "speaker-card--id1p", ID1P_CSS),
}

_HEIGHT_CACHE: dict[tuple[str, str, str | None, str | None], float] = {}

VERSION = "1.7.0"
BUILD_DATE = "2026-09-07"
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


def load_people(source: str) -> list:
    """Load card data for the given source.

    "speakers" returns the list from data/speakers.yaml directly.
    "team" flattens data/team.yaml (organisers + team) and maps the
    team's "image" field onto "photo" so card_html() works unchanged.
    Team entries have no talk/workshop/bio, so their cards show only
    photo, name, role, an optional --bio-text line, and the logo.
    """
    if source == "team":
        team_data = yaml.safe_load((REPO_ROOT / "data" / "team.yaml").read_text(encoding="utf-8"))
        people = list(team_data.get("organisers", [])) + list(team_data.get("team", []))
        normalized = []
        for person in people:
            entry = dict(person)
            if "photo" not in entry and entry.get("image"):
                entry["photo"] = entry["image"]
            normalized.append(entry)
        return normalized
    return yaml.safe_load((REPO_ROOT / "data" / "speakers.yaml").read_text(encoding="utf-8"))


def badge_for(source: str, s: dict, override: str | None) -> str | None:
    """Resolve the badge pill text for a card.

    An explicit --badge value wins (empty string hides the badge).
    Otherwise: "TEAM" for team cards, "TRAINER" for speakers with a
    workshop, "SPEAKER" for the rest.
    """
    if override is not None:
        return override or None
    if source == "team":
        return "TEAM"
    if s.get("workshop"):
        return "TRAINER"
    return "SPEAKER"


def card_html(s: dict, logo: str, bio_text: str | None = None,
              card_height: int | None = None, fmt: str = "portrait",
              source: str = "speakers", badge: str | None = None,
              glow_inner: str | None = None) -> str:
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
    parts = []
    badge_text = badge_for(source, s, badge)
    if badge_text:
        parts.append(f'<span class="speaker-card__badge">{html.escape(badge_text)}</span>')
    parts.append(f'<h3 class="speaker-card__name">{html.escape(s["name"])}</h3>')
    if s.get("role"):
        parts.append(f'<p class="speaker-card__role">{html.escape(s["role"])}</p>')
    if talk:
        parts.append(f'<p class="speaker-card__talk">"{html.escape(talk)}"</p>')
    if bio_text is not None:
        parts.append(f'<p class="speaker-card__bio">{html.escape(bio_text)}</p>')
    elif s.get("bio"):
        parts.append(
            f'<p class="speaker-card__bio" title="{html.escape(s["bio"])}">{html.escape(s["bio"])}</p>'
        )

    # Current website hero logo (SVG on transparent). Team cards always use
    # the gold variant; speaker cards use white ("light") or white rendered
    # black via CSS filter ("dark", for light cards), since no separate dark
    # asset of the new design exists.
    if source == "team":
        logo_src = "/images/bsides-frankfurt-logo-gold.svg"
        logo_filter = ""
    else:
        logo_src = "/images/bsides-frankfurt-logo-white.svg"
        logo_filter = "" if logo == "light" else ' style="filter:brightness(0);"'
    logo = (
        f'<img class="speaker-card__logo" src="{logo_src}"{logo_filter} '
        'alt="BSides Frankfurt" loading="eager">'
    )

    fmt_width, _, fmt_class, _ = FORMATS[fmt]
    size = f"width:{fmt_width}px"
    if card_height is not None:
        size += f";height:{card_height}px"

    card_class = "speaker-card" + (f" {fmt_class}" if fmt_class else "")
    if glow_inner:
        card_class += " speaker-card--glow-inner"
    return (
        f'<article class="{card_class}" style="{size}">{photo}'
        f'<div class="speaker-card__body">{"".join(parts)}</div>{logo}</article>'
    )


def parse_args() -> argparse.Namespace:
    parser = InfoArgumentParser(
        description="Render BSides Frankfurt speaker/team cards as PNGs "
        "(data/speakers.yaml or data/team.yaml).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""manual single card (renders one card instead of the whole list):

  --name NAME --role ROLE [--photo PATH] [--talk TITLE]
  [--workshop TITLE] [--bio TEXT]

  PATH is a repo web path (e.g. /images/team/max-mustermann.jpg) or an
  http(s) URL. Without --photo the card shows initials instead.

examples:
  team member card
    python3 render.py --source team --name "Erika Mustermann" \\
        --role "Volunteer" --photo "/images/team/erika-mustermann.jpg" \\
        --bio-text "BSidesFrankfurt Team 2026"

  speaker card
    python3 render.py --name "Dr. Evil" \\
        --role "Security Researcher, ACME Corp" \\
        --photo "/images/speakers/dr-evil.jpg" \\
        --talk "Hacking Everything" \\
        --bio "Dr. Evil has been hacking everything since 1999."
""",
    )
    parser.add_argument(
        "--source",
        choices=["speakers", "team"],
        default="speakers",
        help='Card source: "speakers" (default, data/speakers.yaml) or "team" '
        '(data/team.yaml, organisers + team, output to static/mediakit/team-cards/).',
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
        help='BSides logo variant (website hero SVG): "light" (white, default, '
        'for dark cards) or "dark" (black via CSS filter, for light cards).',
    )
    parser.add_argument(
        "--samples",
        action="store_true",
        help="Render all predefined color samples (see SAMPLES) to "
        "<output-dir>/tests/.",
    )
    parser.add_argument(
        "--all-samples",
        action="store_true",
        help="Render every person in all sample templates (named <slug>-<sample>.png).",
    )
    parser.add_argument(
        "--output",
        metavar="DIR",
        help="Output directory (default: static/mediakit/speaker-cards/ or "
        "static/mediakit/team-cards/ with --source team). "
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
        help='Hide the bio and show this static text instead, e.g. '
        '"September 10, 2026". With --source team (no bios) it adds '
        'a text line to every card.',
    )
    parser.add_argument(
        "--badge",
        metavar="TEXT",
        default=None,
        help='Badge pill above the name. Default is automatic: "TEAM" for '
        '--source team, "TRAINER" for speakers with a workshop, "SPEAKER" '
        'for the rest. Use --badge "" to hide the badge.',
    )
    parser.add_argument(
        "--glow-inner",
        metavar="#RRGGBB",
        nargs="?",
        const="accent",
        default=None,
        help='Inner glow inside the card edges, fading from the border '
        'toward the center (print-safe: nothing extends past the card, '
        'image size unchanged). Bare --glow-inner uses the accent color; '
        'otherwise pass a hex color, e.g. --glow-inner "#eb3812". '
        'Ideal for printed ID-1 badges.',
    )
    group = parser.add_argument_group(
        "manual single card",
        "Render one card from command-line values instead of the YAML list "
        "(requires --name; see examples below).",
    )
    group.add_argument(
        "--name",
        metavar="NAME",
        help='Full name for a manual single card, e.g. "Erika Mustermann".',
    )
    group.add_argument(
        "--role",
        metavar="ROLE",
        default=None,
        help='Role/job title line, e.g. "Volunteer" or '
        '"Security Researcher, ACME Corp".',
    )
    group.add_argument(
        "--photo",
        metavar="PATH",
        default=None,
        help='Photo: repo web path (e.g. "/images/team/erika-mustermann.jpg") '
        "or http(s) URL. Without --photo the card shows initials.",
    )
    group.add_argument(
        "--talk",
        metavar="TITLE",
        default=None,
        help='Talk title (speakers), e.g. "Hacking Everything".',
    )
    group.add_argument(
        "--workshop",
        metavar="TITLE",
        default=None,
        help='Workshop title (marks the card with a TRAINER badge).',
    )
    group.add_argument(
        "--bio",
        metavar="TEXT",
        default=None,
        help="Bio text line (speakers).",
    )
    return parser.parse_args()


def manual_person(args: argparse.Namespace) -> dict:
    """Build a single card entry from the manual --name/--role/... flags."""
    person = {"name": args.name}
    if args.role:
        person["role"] = args.role
    if args.photo:
        person["photo"] = args.photo
    if args.talk:
        person["talk"] = args.talk
    if args.workshop:
        person["workshop"] = args.workshop
    if args.bio:
        person["bio"] = args.bio
    return person


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


def resolve_glow(opts: dict, key: str = "glow_inner") -> str | None:
    """Resolve the --glow-inner option to a CSS color, or None when disabled.

    A bare flag uses the accent color (--accent or the default green).
    """
    glow = opts.get(key)
    if glow is None:
        return None
    if glow == "accent":
        return opts.get("accent") or DEFAULT_ACCENT
    return parse_color(glow, key.replace("_", "-"))


def page_html(s: dict, background: str, card_overrides: str, logo: str,
              bio_text: str | None = None, card_height: int | None = None,
              fmt: str = "portrait", source: str = "speakers",
              badge: str | None = None,
              glow_inner: str | None = None) -> str:
    card_css = f".speaker-card {{\n{card_overrides}\n}}\n" if card_overrides else ""
    fmt_css = FORMATS[fmt][3]
    glow_css = ""
    if glow_inner:
        g1, g2 = glow_shadows(glow_inner)
        glow_css += GLOW_INNER_CSS.replace("__G1__", g1).replace("__G2__", g2)
    card = card_html(s, logo, bio_text, card_height, fmt, source, badge, glow_inner)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="{ORIGIN}/assets/css/main.css">
<style>
  html, body {{ background: {background} !important; }}
  body {{ margin: 0; padding: 0; }}
{card_css}{fmt_css}{BADGE_CSS}{glow_css}  .speaker-card__logo {{
    margin-top: auto;
    width: 170px;
    height: auto;
    opacity: 0.95;
  }}
</style>
</head>
<body>
{card}
</body>
</html>"""


def open_card_page(browser, s: dict, background: str, card_overrides: str, logo: str,
                   bio_text: str | None, card_height: int | None = None,
                   fmt: str = "portrait", source: str = "speakers",
                   badge: str | None = None,
                   glow_inner: str | None = None):
    slug = slugify(s["name"])
    tmp_file = TMP_DIR / f"{slug}.html"
    tmp_file.write_text(
        page_html(s, background, card_overrides, logo, bio_text, card_height,
                  fmt, source, badge, glow_inner),
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
                        logo: str, bio_text: str | None, source: str = "speakers",
                        badge: str | None = None,
                        glow_inner: str | None = None) -> int:
    """Measure every card's natural height and return one fixed height for all.

    Heights depend only on card content, the source, --bio-text and --badge
    (not on colors, the inner glow or the logo variant), so they are cached
    across sample-template batches.
    """
    for s in speakers:
        key = (source, slugify(s["name"]), bio_text, badge)
        if key in _HEIGHT_CACHE:
            continue
        context, page = open_card_page(browser, s, background, card_overrides, logo,
                                       bio_text, None, "portrait", source, badge,
                                       glow_inner)
        _HEIGHT_CACHE[key] = page.locator(".speaker-card").bounding_box()["height"]
        context.close()
    return math.ceil(max(_HEIGHT_CACHE[(source, slugify(s["name"]), bio_text, badge)]
                         for s in speakers))


def render_cards(browser, speakers: list, opts: dict, out_dir: pathlib.Path, prefix: str = "") -> None:
    background = background_css(opts["background"])
    card_overrides = card_style_overrides(opts)
    logo = opts["logo"]
    bio_text = opts.get("bio_text")
    fmt = opts.get("format") or "portrait"
    source = opts.get("source") or "speakers"
    badge = opts.get("badge")
    glow_inner = resolve_glow(opts, "glow_inner")
    out_dir.mkdir(parents=True, exist_ok=True)
    if glow_inner:
        print(f"Inner glow: {glow_inner} (inset, edge fading inward, print-safe)")

    if fmt != "portrait":
        _, card_height, _, _ = FORMATS[fmt]
        prefix = f"{prefix}-{fmt}" if prefix else fmt
        print(f"{fmt} format: {FORMATS[fmt][0]}x{card_height}px "
              f"({FORMATS[fmt][0] * SCALE}x{card_height * SCALE}px at {SCALE}x)")
    else:
        card_height = uniform_card_height(browser, speakers, background, card_overrides,
                                          logo, bio_text, source, badge, glow_inner)
        print(f"Uniform card height: {card_height}px ({card_height * SCALE}px at {SCALE}x)")

    for s in speakers:
        slug = slugify(s["name"])
        context, page = open_card_page(browser, s, background, card_overrides, logo,
                                       bio_text, card_height, fmt, source, badge,
                                       glow_inner)
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
    out_dir = pathlib.Path(args.output) if args.output else OUT_DIRS[args.source]
    if args.name:
        speakers = [manual_person(args)]
        print(f"Manual card: {args.name} ({args.source} style) -> {out_dir}")
    else:
        speakers = load_people(args.source)
        print(f"Source: {args.source} ({len(speakers)} cards) -> {out_dir}")

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
                        print(f"Rendering all {args.source} in {len(SAMPLES)} sample templates ...")
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
