# Changelog – Pers Kök & Vinkällare

## [Opublicerad] – 2026-06-13

### Vinkällaren – bulk-prisuppskattning via AI
- Ny knapp "🤖 Uppskatta pris för viner utan pris" i statistiksektionen
- Loopar sekventiellt genom alla viner utan pris och frågar Claude Haiku om ungefärligt marknadspris i SEK (avrundat till närmaste 10-tal)
- Live-progressindikator: "Uppskattar 3 av 12: Château Margaux…"
- Sparar och uppdaterar UI efter varje vin – inget tappas om sidan stängs halvvägs
- Fel per vin visas i rött men avbryter inte körningen – nästa vin testas ändå
- Avbryt-knapp syns under pågående körning
- Sammanfattning när klart: "✓ Klart – 8 priser ifyllda, 2 misslyckades"
- Befintliga priser rörs aldrig

---

### Vinkällaren – prisfält och källarvärde
- Nytt fält "Pris (kr/flaska)" i lägg till/redigera-modalen
- Etikettanalysen föreslår nu ett ungefärligt marknadspris i SEK (Systembolaget-nivå, avrundat till närmaste 10-tal) och förifylls automatiskt
- Priset visas som etikett (💰 189 kr/fl) på vinkorten i listvyn
- Ny knapp "💰 Visa källarens värde" under statistikraden togglar en panel med:
  - Totalt uppskattat källarvärde (i guld)
  - Delsummor per plats (Vinkylen / Garaget)
  - Delsummor per vintyp (rött / vitt / mousserande etc.)
  - Disclaimer med antal viner som saknar pris och därmed inte räknas in

---

## [Opublicerad] – 2026-06-13

### Vinkällaren – visuell källarvy
- Ny vy "🏠 Källarvy" (toggle i filterraden bredvid "☰ Lista")
- **Vinkylen** visas med två tydliga zoner: VITT (H1–3, blå ton) och RÖTT (H1–8, röd ton) – totalt 11 hyllor
- **Garaget** visas neutralt med H1–10 utan zonindelning
- Kompakt läge: varje hylla är en rad med färgkodade prickar per vin (rött/vitt/mousserande/rosé/sött)
- Expanderat läge (▼ Öppna): pills med vinnamn, årgång och antal per hylla
- Felzon-markering `↕` (guld) om vintypen inte stämmer med zonens avsedda typ
- Den gemensamma sökrutan markerar matchande flaskor och tonar ned övriga – i båda lägena
- Hyllplats-väljaren i modalen har nu optgroups per zon för Vinkylen (t.ex. "Vitt-zonen · Hylla 2") och spara som `"Vinkylen · Vitt · Hylla 2"`
- Bakåtkompatibelt: viner sparade i gammalt format visas korrekt

---

## [v0.5] – 2026-06-12

### Vinkällaren – tre förbättringar
- Platsstats (flaskor per plats) visas som extra rad under statistikraden
- Sökning filtrerar på druva och region, inte bara namn och land
- Typfilterknappar får visuell aktiv-stil per vintyp (röd/gul/grön/rosa/orange)

---

## [v0.4] – 2026-06-11

### Vinkällaren – etikettmagi utökad
- Analysresultatet visar doft, smak, passar till, lagringspotential och drickfönster som förhandsvisning i modalen
- Drickfönster (drinkfran/dricktill) läggs till i datamodellen med "drick snart"-markering på vinkortet
- AI-prompten begär strukturerade smaknoter (doft, smak, passar till, lagring)

---

## [v0.3] – 2026-06-10

### Vinkällaren – etikettmagi
- Foto av framsida (och valfri baksida) av vinlabel via kameran
- Claude Vision analyserar etiketten och förifyller namn, typ, druva, land, region och årgång
- API-nyckeln delas med övriga AI-funktioner via localStorage

---

## [v0.2] – 2026-06-09

### Vinkällaren – statisk källarsida
- Flasklista med kort (namn, typ, druva, land, region, årgång, antal, anteckningar)
- Hyllplats per vin med dynamiska selects (plats → hylla)
- ＋/− per flaska med historiklogg
- Sök, typfilter och landsfilter
- Export/import som JSON-säkerhetskopia
- Mörkt tema, FAB-knapp, slide-up modal

---

## [v0.1] – 2026-06-08

### Plattformen
- Startsida `hub.html` med tre ingångskort: 🧊 Frysen · 🍷 Vinkällaren · 🍽️ Köket
- Emblem (Logga.png) och vinrött/guld designspråk
- README och SPEC-PERS-KOK.md dokumenterar vision och arkitektur
