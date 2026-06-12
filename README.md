# Pers Kök & Vinkällare

En personlig hemmaköksplattform som samlar frys, vinkällare och kök i en enda app – med en inbyggd AI-kock som hjälper till att planera måltider utifrån vad som faktiskt finns hemma.

---

## Startsida

**[https://perhagegard-arch.github.io/ai-projekt/hub.html](https://perhagegard-arch.github.io/ai-projekt/hub.html)**

---

## Vision

Plattformen löser ett konkret vardagsproblem: vad ska man laga till middag med det man har?

- **Frysen** – inventering av vad som ligger i frysen, med datum och mängd
- **Vinkällaren** – live-sortiment och vinrekommendationer kopplade till måltider
- **Köket** – sous vide-dagbok, recept och matlagningshistorik
- **AI-kocken** – föreslår recept och menyer baserat på frysinnehåll, preferenser och säsong

> Detaljer om funktioner och tekniska val finns i [SPEC-PERS-KOK.md](SPEC-PERS-KOK.md).  
> Planerade faser och prioriteringar finns i [ROADMAP-PERS-KOK.md](ROADMAP-PERS-KOK.md).

---

## Projektprinciper

| Princip | Regel |
|---------|-------|
| **Språk** | Alla kommentarer i koden skrivs på **svenska** |
| **Design** | **Mörkt tema (dark mode)** som standard på alla sidor |
| **Teknik** | HTML/CSS/JS i frontend, Python i backend – enkelt och utan onödiga beroenden |

Basinställningar för dark mode:
```css
body {
  background-color: #121212;
  color: #e0e0e0;
  font-family: sans-serif;
}
```

---

## Komma igång

### Krav
- En modern webbläsare (Chrome, Firefox, Edge)
- Python 3.10+ (för backend-skript)

### Öppna appen
Dubbelklicka på valfri HTML-fil – ingen server behövs för frontenden.

### Uppdatera vinlistan
```bash
python vaktpost.py
```
Ladda sedan om `sousvide.html`. Skriptet genererar `vin-status.json` och `vin-data.js`.

---

## Nuvarande filer

```
ai-projekt/
│
├── sousvide.html       # Sous vide-dagbok med statistik och vinrekommendationer
├── recept.html         # Recept och tips för sous vide-entrecôte
├── vaktpost.py         # Backend-skript – läser data/viner.json, skriver vin-data.js
│
├── data/
│   └── viner.json      # Vinlistan – redigera den här filen
│
├── CLAUDE.md           # Projektregler för Claude Code
├── SPEC-PERS-KOK.md    # Funktionsspecifikation för hela plattformen
├── ROADMAP-PERS-KOK.md # Fasplan och prioriteringar
└── README.md           # Den här filen
```
