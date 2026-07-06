# Changelog

## 2026-07-06 22:32 — `caea30e` → *pending*

### Changed
- **`light_background` (bool) → `background` (3 Stufen: dark/medium/light)** — die bisherige Bool-Option wurde durch eine String-Option mit drei Stufen ersetzt. Wirkt global (`options.background`) und pro Eintrag (`background`).
  - `dark`: dunkler Section-Gradient + dunkle Karten (Standard, wie bisher)
  - `medium`: mittelgrauer Section-Gradient + mittelgraue Karten
  - `light`: heller Section-Gradient + weiße Karten
- `data/sponsors.yaml`: `options.light_background` → `options.background` (String); Kommentar-Dokumentation für pro-Eintrag-Override erweitert.
- `layouts/index.html`: Section-Klasse `sponsors--dark/medium/light` basierend auf `options.background`.
- `layouts/partials/sponsors-grid.html`: pro Card wird `sponsor-card--dark/medium/light` basierend auf `.background | default $globalBg` gesetzt.
- `assets/css/main.css`: Section-Level Regeln für `sponsors--dark/medium/light` und pro-Card Regeln für `sponsor-card--dark/medium/light`; alte `.sponsors--light .sponsor-card` Regeln durch pro-Card-Klassen ersetzt.

## 2026-07-06 22:24 — `e9ba422` → `d9983a7`

### Changed
- **`colored_logos` jetzt pro Eintrag möglich** — zusätzlich zum globalen `options.colored_logos` kann nun jeder Sponsor/Partner-Eintrag in `data/sponsors.yaml` ein optionales `colored: true` / `colored: false` Feld erhalten, das den globalen Default für diesen einen Eintrag überschreibt.
- `layouts/partials/sponsors-grid.html`: Logik von Grid-Level-Klasse (`sponsors__grid--colored`) auf pro-Card-Klasse (`sponsor-card--colored`) umgestellt; pro Eintrag wird `.colored | default $globalColored` ausgewertet.
- `assets/css/main.css`: CSS-Selektor von `.sponsors__grid--colored .sponsor-card img` zu `.sponsor-card--colored img` geändert (wirkt nun auf einzelne Cards).
- `data/sponsors.yaml`: Kommentar-Dokumentation für pro-Eintrag-Override hinzugefügt.

## 2026-07-06 22:16 — `dfc8957` → `81a66b2`

### Added
- **Sponsoren-Section: Option für hellen Hintergrund** — neue Bool-Option `options.light_background` in `data/sponsors.yaml`; wenn `true`, wird die CSS-Klasse `sponsors--light` auf die Section angewendet (heller Gradient, dunkle Textfarben, weiße Karten).
- **Sponsoren-Section: Option für farbige Logos** — neue Bool-Option `options.colored_logos` in `data/sponsors.yaml`; wenn `true`, werden die Logos immer farbig angezeigt (Klasse `sponsors__grid--colored`, kein Grayscale-Filter).

### Changed
- `data/sponsors.yaml`: Neuer Top-Level-Key `options` mit `light_background` und `colored_logos` (beide default `false`).
- `layouts/index.html`: Sponsors-Section liest `light_background` und setzt `sponsors--light`-Klasse.
- `layouts/partials/sponsors-grid.html`: liest `colored_logos` und setzt `sponsors__grid--colored`-Klasse auf alle Grid-Container.
- `assets/css/main.css`: Neue CSS-Regeln für `.sponsors--light` (heller Hintergrund, angepasste Tier-Titel- und Karten-Farben) und `.sponsors__grid--colored` (kein Grayscale-Filter auf Logos).