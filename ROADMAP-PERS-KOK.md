# 🗺️ Roadmap – Pers Kök & Vinkällare (plattformen)

*Bygger vidare på frysregistrets roadmap. Varje etapp ger något användbart – inget "stort släpp" på slutet.*

## Etapp 1 – Startsidan och skalet
Startsida med emblemet, dagens överblick och tre ingångar (Frysen, Vinkällaren, Köket). Frysregistret flyttar in oförändrat. Gemensam navigation och gemensam säkerhetskopia förberedd.
*Klart när: man kan navigera mellan startsidan och frysen på iPaden.*

## Etapp 2 – Vinkällaren grundversion
Flasklista med befintliga fält + hyllplats + drickfönster, ＋/− med historik, sök/filter, statistik. **Datamigrering**: skript som läser gamla repots vinkällare-data och sous vide-databas och skapar en importfil till plattformen.
*Klart när: alla befintliga flaskor syns i nya vinkällaren utan manuell ominmatning.*

## Etapp 3 – Köket
Sous vide-dagboken migrerad (45 körningar) med betyg och omdömen, temperaturguiden, sammanslagen receptvy (AI-recept + körningar). Möjlighet att logga ny körning.
*Klart när: dagboken är komplett på plattformen och gamla Flask-sidan kan pensioneras.*

## Etapp 4 – Den stora kopplingen 🍷🧊🍳
Middagskomponören och AI-kocken får se allt: vinval hämtas ur den egna källaren (med hyllplats och antal), tidigare lyckade körningar påverkar tillagningsförslagen, inköpslistan vet vad som finns. Detta är plattformens hjärta och unika värde.
*Klart när: kärnscenariot fungerar – trerätters med viner ur egen källare och historikbaserade tillagningstips.*

## Etapp 5 – Etikettmagi
Fota en vinetikett → Claude Vision läser den, förifyller fälten (namn, druva, årgång, region) och skriver smaknot (ersätter Gemini-funktionen). Snabbaste sättet att lägga in nya flaskor.
*Klart när: en ny flaska läggs in på under 30 sekunder med foto.*

## Etapp 6 – Molnsynk ☁️
När plattformen bevisat sig i vardagen: Supabase (gratis nivå) ersätter localStorage. iPad, iPhone och dator ser samma data i realtid; hela hushållet kan använda den; risken för rensad webbdata försvinner. Befintlig data följer med via säkerhetskopian.
*Klart när: en flaska som öppnas på mobilen försvinner ur listan på iPaden.*

## Idébank (senare)
QR-koder på fryspåsar och vinhyllor · notiser (drickfönster, frystider) · Systembolaget-integration för inköpslistan · säsongsrapport för jaktåret · gästläge ("visa källaren" utan redigering) · vinprovningsanteckningar med betyg per flaska som öppnats

## Arbetssätt
- En etapp i taget, testad på iPad innan nästa påbörjas
- Claude Code rekommenderas som verktyg från och med detta projekt (repo finns, datorn behövs ändå för migreringen) – chatten för design och beslut
- CHANGELOG uppdateras per etapp; incidenter loggas direkt
- Säkerhetskopia före varje migrering – alltid en väg tillbaka

## Beslut som tagits (se SPEC för motivering)
| Beslut | Innebörd |
|---|---|
| Statisk plattform på GitHub Pages | Flask-versionen blir arkiv/labb, vidareutvecklas inte |
| Anthropic ersätter Gemini | En AI-tjänst, en nyckel, vision + text i samma API |
| Migrering före nybyggnation | Befintliga 45 körningar och alla flaskor följer med |
| Moln i etapp 6, inte tidigare | Bevisa vardagsvärdet först, precis som med frysen |
