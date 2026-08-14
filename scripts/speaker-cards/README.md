# Speaker-Card Renderer

Rendert die Speaker-Cards der Website (`data/speakers.yaml` + echtes HTML/CSS der Seite)
als PNG-Dateien — z.B. fürs Mediakit oder andere Projekte.

**Output:** `static/mediakit/speaker-cards/<slug>.png` (960px breit, 3x-Auflösung, ein Bild pro Speaker)

## Voraussetzungen (einmalig)

```bash
python3 -m venv .venv
.venv/bin/pip install playwright pyyaml
```

Benötigt Chromium unter `/snap/bin/chromium` (auf Ubuntu Standard via Snap; sonst Pfad
in `render.py` anpassen).

## Nutzung

```bash
.venv/bin/python render.py
.venv/bin/python render.py --background page
.venv/bin/python render.py --card-bg "#1a1c1f" --accent "#00b4d8"
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
| `--samples` | Generiert alle Farbmuster (13 Stück) nach `static/mediakit/speaker-cards/tests/` |

Beispiel für eine helle Card:

```bash
.venv/bin/python render.py --card-bg "#ffffff" --text "#011023" --logo dark
```

Alle Samples auf einmal (die in `SAMPLES` in `render.py` definierten Varianten):

```bash
.venv/bin/python render.py --samples
```

Nach Änderungen an `data/speakers.yaml` einfach erneut ausführen — jeder Speaker
bekommt dann wieder ein frisches Bild.
