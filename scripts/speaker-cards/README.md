# Speaker-Card Renderer

Rendert die Speaker-Cards der Website (`data/speakers.yaml` + echtes HTML/CSS der Seite)
als PNG-Dateien — z.B. fürs Mediakit oder andere Projekte.

**Output:** `static/mediakit/speaker-cards/<slug>.png` (960px breit, 3x-Auflösung, ein Bild pro Speaker)

Alle Cards werden auf einer einheitlichen Höhe gerendert: Das Skript misst im ersten
Durchlauf die natürliche Höhe jeder Karte und fixiert im zweiten Durchlauf alle auf das
Maximum. So haben alle Bilder identische Maße — auch Speaker ohne Bio — und keine Karte
wird kleiner als die bisher größte. Bei neuen Speakern mit längeren Texten wachsen alle
Karten gemeinsam mit.

## Voraussetzungen (einmalig)

```bash
python3 -m venv .venv
.venv/bin/pip install playwright pyyaml
```

Benötigt Chromium unter `/snap/bin/chromium` (auf Ubuntu Standard via Snap; sonst Pfad
in `render.py` anpassen).

## Nutzung

Das Skript wechselt automatisch ins `.venv`, wenn es mit einem anderen Python
gestartet wird — `python3 render.py` genügt also:

```bash
python3 render.py
python3 render.py --background page
python3 render.py --card-bg "#1a1c1f" --accent "#00b4d8"
```

| Option | Effekt |
| --- | --- |
| `--background transparent` (default) | Transparenter Hintergrund, nur die Card |
| `--background page` | Hintergrund in Website-Farbe (`#011023`, dunkelblau) |
| `--background #RRGGBB` | Beliebige Hintergrundfarbe |
| `--card-bg #RRGGBB` | Hintergrund der Card (default: dunkles Grau `#121314`) |
| `--accent #RRGGBB` | Akzentfarbe für Rollen-Text und Foto-Gradient (default: Grün `#9acd32`) |
| `--accent-secondary #RRGGBB` | Zweite Akzentfarbe des Foto-Gradienten (default: Orange `#eb3812`) |
| `--text #RRGGBB` | Textfarbe (default: Weiß) — bei hellen Cards setzen, z.B. `--text "#011023"` |
| `--logo light\|dark` | Logo-Variante: `light` (weiß, default) oder `dark` (schwarz, für helle Cards) |
| `--format portrait\|id1\|id1-portrait` | `portrait` (default, 320px breit), `id1`: Kreditkarten-Format ISO/IEC 7810 ID-1 (CR80) quer, 85.60 × 54.00 mm, kompaktes Layout (Foto links, Text rechts, Logo unten rechts), 1284×810px, Dateiname `<slug>-id1.png` — oder `id1-portrait`: dasselbe ID-1-Verhältnis hochkant, 54.00 × 85.60 mm, 810×1284px, Dateiname `<slug>-id1-portrait.png` |
| `--samples` | Generiert alle Farbmuster (13 Stück) nach `static/mediakit/speaker-cards/tests/` |
| `--all-samples` | Generiert jeden Speaker in allen 13 Template-Varianten nach `static/mediakit/speaker-cards/` (Namensschema `<slug>-<sample>.png`) |
| `--bio-text TEXT` | Blendet die Bio aus und zeigt stattdessen den Text, z.B. `--bio-text "September 10, 2026"` |
| `--output DIR` | Ausgabeordner (default: `static/mediakit/speaker-cards/`); `--samples` schreibt nach `<DIR>/tests/` |
| `--version` | Zeigt Version, Build-Datum und Autor |

Beispiel für eine helle Card:

```bash
python3 render.py --card-bg "#ffffff" --text "#011023" --logo dark
```

Alle Samples auf einmal (die in `SAMPLES` in `render.py` definierten Varianten):

```bash
python3 render.py --samples
```

Jeden Speaker in allen Template-Varianten (z.B. für Auswahl/Archiv):

```bash
python3 render.py --all-samples
```

Bio durch statischen Text ersetzen (z.B. Datum des Talks):

```bash
python3 render.py --bio-text "September 10, 2026"
```

Karten im Kreditkarten-Format (ID-1 / CR80, 85.60 × 54.00 mm) — quer und hochkant:

```bash
python3 render.py --format id1
python3 render.py --format id1-portrait
```

Ausgabe in einen anderen Ordner (z.B. für ein anderes Projekt):

```bash
python3 render.py --output /pfad/zum/projekt/images
```

---

**BSides Frankfurt Speaker-Card Renderer v1.0.0 (build 2026-08-14) by Alexander Georgiev + DeepSeek V4**

Nach Änderungen an `data/speakers.yaml` einfach erneut ausführen — jeder Speaker
bekommt dann wieder ein frisches Bild.
