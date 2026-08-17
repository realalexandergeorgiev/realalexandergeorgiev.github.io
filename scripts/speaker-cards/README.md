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
| `--all-samples` | Generiert jeden Speaker in allen 13 Template-Varianten nach `static/mediakit/speaker-cards/` (Namensschema `<slug>-<sample>.png`) |
| `--bio-text TEXT` | Blendet die Bio aus und zeigt stattdessen den Text, z.B. `--bio-text "September 10, 2026"` |
| `--output DIR` | Ausgabeordner (default: `static/mediakit/speaker-cards/`); `--samples` schreibt nach `<DIR>/tests/` |
| `--version` | Zeigt Version, Build-Datum und Autor |

Beispiel für eine helle Card:

```bash
.venv/bin/python render.py --card-bg "#ffffff" --text "#011023" --logo dark
```

Alle Samples auf einmal (die in `SAMPLES` in `render.py` definierten Varianten):

```bash
.venv/bin/python render.py --samples
```

Jeden Speaker in allen Template-Varianten (z.B. für Auswahl/Archiv):

```bash
.venv/bin/python render.py --all-samples
```

Bio durch statischen Text ersetzen (z.B. Datum des Talks):

```bash
.venv/bin/python render.py --bio-text "September 10, 2026"
```

Ausgabe in einen anderen Ordner (z.B. für ein anderes Projekt):

```bash
.venv/bin/python render.py --output /pfad/zum/projekt/images
```

---

**BSides Frankfurt Speaker-Card Renderer v1.0.0 (build 2026-08-14) by Alexander Georgiev + DeepSeek V4**

Nach Änderungen an `data/speakers.yaml` einfach erneut ausführen — jeder Speaker
bekommt dann wieder ein frisches Bild.
