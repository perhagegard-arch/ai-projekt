# AI-Projekt – Pers Sous Vide & Vin-labb

En personlig webbapp byggd steg för steg med HTML, CSS, JavaScript och Python.

---

## Vad är det här?

Tre sammankopplade sidor plus en Python-backend:

| Fil | Beskrivning |
|-----|-------------|
| `index.html` | Färgaruletten – ett litet interaktivt experiment |
| `sousvide.html` | Pers sous vide-dagbok med statistik, temperaturguide, vinrekommendationer och live-sortiment |
| `recept.html` | Recept och tips för sous vide-entrecôte |
| `vaktpost.py` | Python-skript som läser `data/viner.json` och genererar `vin-data.js` |

---

## Komma igång

### Krav
- En modern webbläsare (Chrome, Firefox, Edge)
- Python 3.10+ (för att köra vaktpost.py)

### 1. Öppna webbsidorna
Dubbelklicka på valfri HTML-fil. Ingen server behövs – de öppnas direkt i webbläsaren.

### 2. Uppdatera vinlistan på sidan
```bash
python vaktpost.py
```
Ladda sedan om `sousvide.html`. Skriptet genererar två filer automatiskt:
- `vin-status.json` – rådata (läsbar av människor)
- `vin-data.js` – laddas in av webbsidan

### 3. Redigera vinlistan
Öppna `data/viner.json` i valfri textredigerare. Lägg till, ta bort eller ändra viner.
Kör sedan `python vaktpost.py` igen för att publicera ändringarna till sidan.

---

## Projektstruktur

```
AI-Projekt/
│
├── index.html          # Färgaruletten
├── sousvide.html       # Sous vide-dagbok (huvudsida, ~1 200 rader)
├── recept.html         # Entrecôte-recept med inspiration
├── vaktpost.py         # Backend-skript – läser data/, skriver vin-data.js
│
├── data/
│   └── viner.json      # Vinlistan – redigera den här filen
│
├── CLAUDE.md           # Projektregler för Claude Code
├── README.md           # Den här filen
│
└── (autogenererat – checka inte in dessa)
    ├── vin-status.json
    └── vin-data.js
```

---

## Arbetsflöde – lägga till en sous vide-körning

1. Öppna `sousvide.html` i webbläsaren
2. Klicka **＋ Lägg till ny körning** (knappen nere till höger)
3. Fyll i kött, metod, temperatur, tid, betyg och omdöme
4. Klicka **Spara körning**

> **Obs:** Nya körningar sparas i webbläsarens **localStorage** – de är kopplade
> till just den webbläsaren på den datorn. En riktig databas planeras i Fas 2.

---

## Vinrekommendationer

Sommelier-funktionen i temperaturguiden matchar varje köttkategori med en
vinrekommendation och öppnar en färdig söklänk på Systembolaget.

Live-vinlistan (sektionen "🍾 Live från Systembolaget") hämtar sina data från
`vin-data.js` som genereras av `vaktpost.py`. Varje vinkort är en klickbar länk.

---

## Roadmap

| Fas | Status | Innehåll |
|-----|--------|----------|
| **Fas 1** | ✅ Klar | Grundstruktur, design, dagbok, vinrekommendationer, README, datafiler |
| **Fas 2** | 🔜 Nästa | Flask-server, JSON-API, spara körningar till fil istället för localStorage |
| **Fas 3** | 💡 Framtid | SQLite-databas, inloggning, deploy på server (Railway / Raspberry Pi) |

---

## Tekniker som används

- **HTML5 / CSS3** – struktur och mörk design (dark mode som standard)
- **JavaScript (vanilla)** – all interaktivitet, localStorage, Chart.js
- **Chart.js** – stapel- och cirkeldiagram i dagboken
- **Python 3** – vaktpost.py för datagenerering
- **JSON** – datautbyte mellan Python och webbsidan
