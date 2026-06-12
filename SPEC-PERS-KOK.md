# 📋 Specifikation – Pers Kök & Vinkällare (plattformen)

*Version 1.0 · 2026-06-12 · Underlag inför utvecklingsstart*

## 1. Vision

En samlad digital plattform för hela matlivet på gården: **vad som finns** (frys + vinkällare), **vad som lagats** (sous vide-dagboken) och **vad som ska lagas** (AI-kock med menyer, vinval ur egen källare och inköpslistor). En startsida under emblemet Pers Kök & Vinkällare förgrenar sig till de tre delarna, och AI:n ser allt samtidigt.

**Kärnscenariot som allt ska stödja:** *"Komponera en trerätters för 6 på lördag"* → AI:n tittar i frysen (rådjursytterlår finns), i sous vide-dagboken (ytterlår 56° i 8h fick betyg Toppen i januari), i vinkällaren (Barolo del Vecchio Maestro 2018, 2 flaskor) – och levererar meny, tillagning, vinval per rätt och inköpslista på det som saknas.

## 2. Nuläge – två världar som ska bli en

| | Frysregister | AI-Projekt (befintligt) |
|---|---|---|
| Teknik | En statisk HTML-fil | Flask-server + SQLite + flera HTML-sidor |
| Hosting | GitHub Pages (nås överallt) | localhost:5000 (kräver PC igång) |
| Data | localStorage per enhet | sousvide.db: 45 körningar, vinkällare-tabell, viner.json |
| AI | Anthropic API (AI-kocken, menyer) | Gemini Vision (etikettanalys) |
| Primär enhet | iPad/iPhone | Datorn |

**Styrkor att bevara från AI-Projektet:** datamodellen för vinkällaren (namn, druva, land, region, årgång, typ, anteckningar, etikettbilder fram/bak, AI-smaknoter), sous vide-dagbokens struktur (temp, tid, betyg, omdöme, taggar) och idén med etikettfotografering + AI-analys.

**Styrkor att bevara från Frysregistret:** nås från alla enheter utan server, noll driftskostnad, beprövat AI-flöde med Anthropic, etablerade rutiner (uppdatering, säkerhetskopia, API-nyckel).

## 3. Arkitekturbeslut (förslag)

**Plattformen byggs som statisk app på GitHub Pages, i frysregistrets modell.** Flask-versionen behålls som labb/arkiv men vidareutvecklas inte.

Motivering: kärnvärdet är att allt nås från iPaden i köket och mobilen i butiken – det klarar inte en localhost-server. Statiskt på Pages är gratis, beprövat i hushållet och AI-integrationen finns redan. Det som "förloras" hanteras så här:

- *Bilduppladdning (etiketter):* bilder lagras som komprimerad base64 i localStorage (max ~300 px, fungerar för etiketter) – eller skjuts till molnfasen
- *Etikettanalys med Gemini:* ersätts av Anthropic Vision via samma API-nyckel som AI-kocken (Claude kan läsa bilder) – en tjänst färre att hantera
- *Riktig databas/synk:* medvetet senarelagt till molnfasen (se roadmap), precis som frysregistrets beslutslogg redan slagit fast

**Datamigrering ingår:** ett skript konverterar befintliga sousvide.db/recept.json/vinkällare-data till plattformens format, så inget av de 45 dokumenterade körningarna eller inlagda vinerna går förlorat.

## 4. Funktionell specifikation

### 4.1 Startsidan (huvet)
Emblemet, dagens överblick ("142 förp i frysarna · 38 flaskor i källaren · 45 loggade körningar") och tre stora ingångar: 🧊 Frysen · 🍷 Vinkällaren · 🍳 Köket. Plus snabbknapp till "Komponera middag". Designspråk: nuvarande mörka tema (per projektreglerna i CLAUDE.md), med emblemets vinröda/guld som accenter.

### 4.2 Frysen
Befintliga frysregistret oförändrat i funktion – flyttar in under startsidan.

### 4.3 Vinkällaren
- Flasklista med fält från befintlig datamodell: namn, typ (rött/vitt/mousserande/sött), druva, land, region, årgång, antal, anteckningar
- **Nytt:** hyllplats (enkel text, t.ex. "B3") – benchmarken visar att "var står flaskan?" är killer-funktionen hos InVintory/CellarTracker (de gör 3D-vyer; vi börjar med text)
- **Nytt:** drickfönster (från–till år) med "drick snart"-markering, motsvarande frysens "ät detta först"
- ＋/− per flaska som i frysen, med historik ("öppnade Barolon 14 feb")
- Etikettfoto + AI-smaknot via Anthropic Vision (doft, smak, passar till, karaktär – samma format som befintliga Gemini-prompten)
- Statistik: flaskor per typ/land/druva, totalvärde, äldsta årgång
- Sök + filter (typ, land, druva, drickfönster)

### 4.4 Köket
- **Sous vide-dagboken:** de 45 migrerade körningarna + nya. Fält som idag: namn, kategori, metod, temp, tid, antal gånger, betyg, omdöme, taggar. Temperaturguiden följer med.
- **Receptbanken:** AI-sparade recept (finns redan) + sous vide-körningarna i samma vy
- **AI-kocken & Middagskomponören:** som idag, MEN med tre nya datakällor i prompten:
  1. Vinkällaren → "VINVAL UR KÄLLAREN: [flaska] (hylla B3, 2 kvar)" istället för generiska vintips; generiskt tips endast om inget passande finns hemma
  2. Sous vide-dagboken → AI:n vet vad som lyckats förr ("din 56°/8h på ytterlår fick Toppen – kör samma")
  3. Möjlighet att markera en sous vide-rätt i frysen som färdiglagad komponent

### 4.5 Gemensamt
- En gemensam säkerhetskopia (JSON) för allt: frys + vin + kök + sparade recept + historik
- All data i localStorage med samma nyckelprefix; API-nyckeln delas av alla AI-funktioner
- Utskrift/PDF per del (finns i frysen, byggs för vin och kök)

## 5. Benchmark-slutsatser

Jämfört med CellarTracker, InVintory, Vivino och VinoCell:

**Vi matchar redan/lätt:** inventering, antal, sök, statistik, AI-sommelier (InVintorys premium-säljpunkt – vår AI-kock gör redan mer eftersom den ser maten också).

**Värt att låna:** hyllplats/lokalisering (deras viktigaste funktion), drickfönster, etikettskanning för snabb inläggning (vi: foto + Claude Vision som läser etiketten och förifyller fälten), import från kalkylark (vi: migrering från befintlig data).

**Vi hoppar medvetet över:** 3D-cellarvyer, NFC-stickers, investeringsvärdering, social delning – fel komplexitet för ett hushåll.

**Vår unika fördel ingen av dem har:** kopplingen mat ↔ vin ↔ egen lagringshistorik. InVintory kan rekommendera vin till "lammstek"; vi rekommenderar vin till *rådjuret som ligger i garagefrysen*, lagat på *sättet som fick toppbetyg sist*. Det är plattformens identitet.

## 6. Avgränsningar v1

Ingen molnsynk (data per enhet, export/import som brygga). Ingen inloggning. Inga notiser. Ingen Systembolaget-integration utöver befintliga söklänkar. Färgaruletten (index.html i gamla repot) pensioneras med heder.

## 7. Tekniska krav

En eller få statiska filer, vanilla JS, inga ramverk. Hostas i befintligt GitHub Pages-repo (frysregister byter skepnad till plattformen, alternativt nytt repo "pers-kok"). Mörkt tema enligt CLAUDE.md. Kommentarer på svenska. Allt testbart på iPad Safari som primär miljö.
