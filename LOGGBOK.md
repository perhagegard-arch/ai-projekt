# 📓 Loggbok – Pers Kök & Vinkällare

*Beslutslogg: dokumenterar VARFÖR saker ser ut som de gör, så att Per (och brodern, och framtida testare) förstår resonemangen vid återbesök. Senast uppdaterad: 2026-06-23.*

---

## Större beslut (nyast först)

**2026-06-23 · Vinkällaren gjord konfigurerbar**
Hårdkodad `PLATSKONFIG` (Pers Vinkyl + Garaget) ersatt med konfiguration i localStorage (`vinkallare_platskonfig_v1`). Silent migration: befintliga användare med viner får Pers uppsättning automatiskt. Setup-wizard för nya användare (börjar med tom plats de döper själva). Pers Temptech-SVG bevaras endast för hans exakta Vinkyl; nya platser ritas med generella rack-vyn (SVG:n är ritad för just hans modell). *Varför enkel vinzon: en ny användare ska inte tvingas in i Pers struktur.*

**2026-06-23 · Frysen gjord konfigurerbar + uppstädning**
Frysuppsättningen konfigurerbar via setup-wizard (samma mönster som vinkällaren). Tog även bort kvarlevor: gamla "Laga mat"/Recept-vyn och "Sparade recept"-vyn. *Varför: all matlagning och alla recept sker numera i Köket – frysen ska bara hålla koll på råvaror.*

**2026-06-23 · Arbetssätt: chatt + direkt repo-åtkomst**
Per gick från att köra Claude Code i PowerShell till att jobba helt i chatten, där hela kodbasen läses in och Claude committar/pushar direkt. *Varför: allt på ett ställe, en sammanhållen konversation. Kräver en GitHub-token; den återkallas efter användning.*

**Tidigare (från CHANGELOG/historik):**
- Frysappen flyttad in i ai-projekt under `frys/` – allt samlat i ett repo
- Skafferiet byggt (har/har-inte, förkryssad grundlista) och inkopplat i Kökets motor
- AI-proxy (Cloudflare Worker) planerad men PARKERAD – Per löste feedback-behovet genom live-demo för kompisar istället
- Statisk plattform på GitHub Pages, Anthropic ersätter Gemini (en nyckel, vision+text)

---

## Utvecklingsprinciper & när de gäller

*Genomgång av "20 tips för webb-app". Flera gäller inte den nuvarande statiska appen men blir viktiga vid multiuser/databas (etapp 2–3, se ROADMAP-DELAD-PLATTFORM.md). Dokumenterat så de inte glöms.*

**Gäller redan nu (på plats eller löpande):**
- Kommentera syfte, inte kod (CLAUDE.md kräver svenska kommentarer)
- Mobile-first (viewport, testas alltid på iPad/iPhone)
- Commit ofta med beskrivande meddelanden
- Plan innan kod; testa i webbläsaren direkt efter ändring
- Tomma tillstånd med vänliga meddelanden
- En funktion = ett ansvar (små namngivna funktioner)

**Snabba vinster värda att göra nu (statisk app):**
- ✅ `loading="lazy"` tillagt på etikett-thumbnails (2026-06-23). NOT: vinsten mindre än väntat – de stora stämningsbilderna är CSS-bakgrunder (inte `<img>`) och redan hyfsat komprimerade. Logotyper i headers lämnades utan lazy (syns direkt).
- ✅ Ladda-tillstånd på AI-knappar – REDAN VÄLGJORT i hela appen (kontrollerat 2026-06-23): etikettmagin "⏳ Analyserar…", Köket spinner + "AI-kocken tänker… 30–60 sek", Kockens viskning, receptbanken "Skriver om receptet…". Alla med inaktiv knapp under anropet. Inget att göra.
- Genomgång att HTML-escape (`h()`) används konsekvent – se teknisk skuld nedan (skjuts till multiuser-steget).
- Stärka try/catch där localStorage/API läses (löpande).

**Blir RELEVANTA först vid multiuser + databas (etapp 2–3):**
- **Miljövariabler/.env för hemligheter** – gäller INTE nu (ingen server, API-nyckeln matas in av användaren i deras localStorage). Blir kritiskt när en server med Pers nyckel finns: nyckeln i `.env`, aldrig i koden, `.env` i `.gitignore`.
- **Felhantering på varje databasoperation** – idag mest localStorage; vid moln blir try/catch på varje DB-anrop ett måste.
- **Input-validering/sanering (HTML-escape)** – KONKRET TEKNISK SKULD funnen 2026-06-23: `h()`-escapefunktionen finns bara i vinkallare.html. De andra fyra sidorna (kok, frys, skafferi, receptbank) sätter användardata (varunamn, anteckningar) via innerHTML utan escape. Risk LÅG idag (Per är ende användaren – skadar inte sig själv), men MÅSTE åtgärdas vid multiuser, då andras input visas. Görs naturligt när datalagret byggs om mot databasen i etapp 2 – att escape-säkra localStorage-versionen nu vore att putsa något som snart ersätts. *Inte glömt – det står här.*
- **Cachning av API-svar** – marginellt nu (anropen är unika); kan bli relevant för sällan ändrad delad data.
- **Paginering** – inte nu (45 viner). Aktuellt om en användare får hundratals.

**Gäller inte / passar inte appens arkitektur:**
- "Håll filer under 300 rader" – appen är medvetet fristående HTML-filer (en sida = en fil med inbäddad CSS/JS) för GitHub Pages. Modularisering skulle vara stort arbete med liten vinst. Omvärderas om ett bygg-steg (t.ex. ramverk) införs vid moln.

---

## Hur vi använder den här filen

Claude uppdaterar loggboken när ett större beslut tas eller en etapp avslutas. Syftet är inte en komplett ändringshistorik (det är CHANGELOG) utan att fånga *resonemangen* bakom vägval – det som annars glöms.
