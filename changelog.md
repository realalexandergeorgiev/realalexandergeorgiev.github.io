# Changelog

## 2026-07-14 — working tree (uncommitted)

### Added
- **Keynote auf der `/schedule/`-Seite (datengetrieben)** — der Schedule-Layout (`layouts/schedule/list.html`) liest `data/speakers.yaml` und rendert jeden Eintrag mit `keynote: true` als hervorgehobene Keynote-Karte (Foto/Initialen-Avatar, Role, Talk-Titel, volle Bio, LinkedIn).
- **`keynote`-Flag in `data/speakers.yaml`** — markiert einen Speaker als Keynote; erscheint dann sowohl im Homepage-Karussell als auch als Keynote-Karte auf `/schedule/`.
- **Homepage: "Featured Speakers"-Karussell reaktiviert** — neue Section in `layouts/index.html` (nach der Stats-Strip) über das `speakers-carousel.html`-Partial; war zuvor entfernt.
- **Beispiel-Timetable im Schedule-Layout** — vollständiger Platzhalter-Stundenplan (Registrierung, Keynote, Talk-Slots, Kaffee-/Mittagspausen, Closing, Social) als Hugo-Template-Kommentar (`{{/* ... */}}`) inkl. `<style>`-Block; zum Freischalten nur die Kommentar-Marker entfernen und Platzhalter füllen.
- **CSS-Modifier `.speaker-card__bio--full`** — zeigt eine Speaker-Bio ungekürzt statt auf 3 Zeilen; genutzt von der Keynote-Karte.

### Changed
- **`data/speakers.yaml`**: Name normalisiert `"Joern"` → `"Jörn"` (konsistent zur Bio); `keynote: true` am Eintrag gesetzt.
- **Bio-Mouseover-Tooltip (Carousel)** — `layouts/partials/speakers-carousel.html` setzt ein `title`-Attribut mit dem vollen Bio-Text; optische Truncierung bleibt auf 3 Zeilen, voller Text per Hover.
- **`MANUAL.md` §5.8 (Schedule)** umgeschrieben: klargestellt, dass der `_index.md`-Body nicht gerendert wird (nur Frontmatter); Keynote ist datengetrieben; Anleitung zur Beispiel-Timetable ergänzt.
- **`MANUAL.md` §5.12 (Speakers)** aktualisiert: Karussell ist live; `keynote`-Flag, Bio-Truncierung/-Tooltip und `--full`-Modifier dokumentiert; Heading "(when ready)" inkl. TOC-Anker bereinigt.
- **`layouts/index.html`**: veralteten Sponsoren-Kommentar ("speaker section hidden until lineup confirmed") korrigiert.

### Fixed
- **`.Site.Data` → `hugo.Data` (13 Layout-Dateien, 17 Vorkommen)** — Hugo ≥0.156 deprecates `.Site.Data`; alle Vorkommen migriert, die entsprechende Deprecation-Warning ist damit beseitigt (betrifft u.a. `index`, `schedule`, `women`, `team`, `faq`, `workshops`, `partials/{footer,about-grid,sponsor-carousel,seo,seo-jsonld-data,speakers-carousel,sponsors-grid}`).
- **Redundantes Title-Tooltip an der Keynote-Bio entfernt** — die `--full`-Variante zeigt die Bio bereits vollständig, das doppelte `title`-Attribut wurde gestrichen (nur die truncierte Carousel-Variante behält es).

## 2026-07-06 22:38 — `85ad16e` → `88502e3`

### Fixed
- **CSS-Reihenfolge-Fix: `sponsor-card--light` wurde von `.sponsor-card` Basisregel überschrieben** — die pro-Card-Hintergrund-Varianten (`sponsor-card--dark/medium/light`) standen vor der `.sponsor-card` Basisregel und wurden dadurch überschrieben. Die Varianten wurden nach der Basisregel verschoben, sodass sie nun korrekt greifen.

## 2026-07-06 22:33 — `caea30e` → `66718eb`

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