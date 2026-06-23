# 🚀 Roadmap: Från personlig app till delad plattform (multiuser)

*Pers målbild: appen ska ut i verkligheten. Fler ska kunna använda den – varje användare med sina egna frysar och sin egen vinkällare, inloggning med Google, gratis. Per vill se vilka som registrerat sig, kunna fråga en vän om att se deras vinkällare och dela recept.*

*Benchmarkat mot etablerad praxis för onboarding (NN/g, Stripe) och delad data (Supabase Row Level Security). Inget av detta byggs nu – men målbilden och vägen dit ska finnas dokumenterad.*

---

## Var vi står idag

Statiska filer på GitHub Pages, data i localStorage per enhet. **Etapp 1 (nedan) är i praktiken klar:** frysen och vinkällaren är gjorda konfigurerbara – en ny användare kan sätta upp sina egna frysar/platser, och Pers uppsättning bevaras automatiskt (silent migration).

Att nå målbilden kräver tre fundamentala skiften:
1. **Från hårdkodad till konfigurerbar** – varje användare sätter upp sitt eget kök ✅ *(klart för frys + vinkällare)*
2. **Från localStorage till moln** – data följer användaren, inte enheten
3. **Från ensam till social** – användare kan se varandra och dela

Detta är inte "fler funktioner" – det är en ny grund under huset. Bygg i ordning, med en fungerande app i varje steg.

---

## ETAPP 1 — Gör appen konfigurerbar (utan inloggning) ✅ i stort sett klar

Appen slutar vara "Pers app" och blir "vem som helsts app" – men fortfarande lokalt.

- ✅ **Frysen konfigurerbar** – setup-wizard, Pers uppsättning bevarad, hantera-frysar
- ✅ **Vinkällaren konfigurerbar** – setup-wizard, Pers Temptech-SVG bevarad för hans uppsättning, nya platser ritas generellt, hantera-platser
- ⏳ Återstår ev: skafferiet och köket för fullständig "ny användare"-upplevelse

**Värdefullt oavsett moln, och förbereder marken.** Mät på riktiga användare innan nästa stora steg.

---

## ETAPP 2 — Inloggning + molnlagring (det stora steget)

Data följer användaren mellan enheter, och vi vet vem som är vem. Rekommenderat verktyg: **Supabase** (inloggning + databas i ett, gratisnivå räcker långt).

- **Google-inloggning** via Supabase Auth (nästan färdigt out of the box)
- **Flytta data från localStorage till molnet** – frysar, viner, recept, skafferi, sous vide kopplas till användarens konto
- **Row Level Security (RLS)** – kritiskt: varje användare når bara sin egen data. Inte valfritt; det är detta som gör att en användares viner inte syns för någon annan förrän de tillåter det.
- **AI-nyckeln** kan nu gå genom servern (dold) – alla slipper egen nyckel. Detta är AI-proxyn, fast naturligt inbyggd. Sätt kostnadstak.

⚠️ **Migrering:** Pers (och andras) befintliga data måste flyttas från localStorage utan förlust. Backas upp först, testas stegvis. Veckor av arbete – rör varje del som idag läser/skriver localStorage. Pers bror (erfaren Claude-utvecklare) kan vara ovärderlig här.

**Tekniska tips som blir RELEVANTA först här** (se LOGGBOK.md):
- Miljövariabler/.env för hemligheter (server-nyckeln) + .gitignore
- Felhantering (try/catch) på varje databasoperation
- Input-validering/sanering innan data sparas i delad databas
- Ev. cachning av sällan ändrad data

---

## ETAPP 3 — Det sociala (se varandra, dela)

Byggs på etapp 2:s grund. Ordning från minst till mest känsligt:

- **Användarkatalog** – "vilka använder appen?". Per ser att en vän är registrerad. (Visa bara namn/användarnamn.)
- **Vänförfrågningar** – skicka → godkänn. Inget syns om varandra utan ömsesidigt godkännande.
- **Dela vinkällare (läs-vy)** – vänner kan be att SE varandras källare, med godkännande. RLS: vänner får läsa, aldrig ändra.
- **Dela recept** – skicka ur receptbanken till en vän eller gemensam pool.

⚠️ **Integritet är HELA spelet här.** Grundregel: inget delas förrän ägaren aktivt sagt ja. Standard = privat. Varje delning ett medvetet, ångerbart val. Bygg det fel en gång och förtroendet är borta.

---

## ETAPP 4 — Community (om visionen växer)

Bredare idéer från testarna – recept-community, chatta/FaceTime medan man lagar. Se IDEBANK-BACKLOGG.md. Bygg bara om/när etapp 3 visat att folk faktiskt delar och vill ha mer.

---

## Tre råd som bär resan

1. **Ta etapperna i ordning.** Hoppa inte till moln på en hårdkodad grund. Etapp 1 ger värde direkt och förbereder marken.
2. **Mät på riktiga användare mellan etapperna.** Per gjorde redan rätt en gång – visade appen live, fick feedback, slapp bygga proxyn i onödan.
3. **Integritet är grunden, inte en funktion.** Särskilt etapp 3. Standard privat, allt delande aktivt och ångerbart.

*Samma princip som burit hela bygget: bygg lagom, lär av verkligheten, bygg stort när du vet. Skillnaden nu: Per vet redan att kompisarna vill ha det här.*
