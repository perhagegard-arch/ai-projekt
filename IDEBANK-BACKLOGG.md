# 💡 Idébank & Backlogg – Pers Kök & Vinkällare

*Här samlas allt vi medvetet skjutit på framtiden, så inget glöms bort. Plockas härifrån när vi är redo. Senast uppdaterad: 2026-06-14.*

## Parkerat under bygget (att plocka upp)

**Streckkodsskanning av vinflaskor** – Fota streckkoden på en flaska köpt på Systembolaget för att snabbt lägga in den (autofylla namn, druva, årgång m.m.). Komplement till etikettfotot. Tekniskt: streckkodsläsning i webbläsaren (kameran + ett JS-bibliotek), sedan uppslag mot en produktdatabas – möter samma Systembolags-API-fråga som nedan, så de hör ihop.

**Fota kvitto från Systembolaget** – Fota hela kvittot efter ett inköp så läses alla viner in på en gång (Claude Vision tolkar kvittoraderna → flera flaskor läggs till samtidigt). Smidigt vid storhandling. Tekniskt: samma vision-flöde som etikettanalysen, men prompten tolkar en kvittolista istället för en etikett.

**Röstinmatning ("prata in tankar")** – När man vill laga en rätt, kunna trycka på en mick och prata in sina önskemål ("jag är sugen på nåt med rådjuret och svamp, lite höstigt") istället för att skriva. Tekniskt: webbläsarens inbyggda taligenkänning (Web Speech API) som fyller önskemålsfältet, eller ljud till en transkriberingstjänst. Gör Köket enklare när man står med händerna i matlagningen.

**AI-genererade köksknuffar**
Förslagsrutan ("Köksanden") börjar med enkel datalogik (råvaror nära frysgräns, vin nära drickfönster, kategori man inte ätit på länge). Senare: låt AI:n formulera mer kreativa, personliga tips ("det var ett tag sedan fisk – vad sägs om en pocherad röding med brynt smör?"). Bygg ovanpå den datadrivna grunden.

**Systembolaget-integration**
Hämta riktiga, aktuella vinpriser och produktinfo automatiskt istället för AI-uppskattning. Status: deras öppna API är nedlagt/begränsat – kräver utvärdering av tredjepartsalternativ och beslut om det är värt risken (inofficiella vägar kan sluta fungera). Prisfältet i vinkällaren är redan förberett för detta.

**Pris via nätsökning (på begäran)**
Knapp vid prisfältet som söker aktuellt marknadspris på nätet för en specifik flaska (web_search), som komplement till AI-uppskattningen. Avvägt bort tills vidare – AI-uppskattningen räcker för nuvarande behov.

## Från frysregistrets ursprungliga roadmap (ej gjort än)

**QR-etiketter** – Skriv ut QR-koder att fästa på fryspåsar och vinhyllor; skanna med kameran för att se innehåll/datum eller bocka ut direkt.

**Notiser/påminnelser** – När varor närmar sig frysgräns eller vin närmar sig drickfönstrets slut. Kräver att appen görs till PWA med service worker, eller molnlösning.

**Säsongsstatistik för jakten** – Jämför år för år: kg älg/rådjur in 2026 vs 2027, förbrukningstakt.

**Foton på varor** – Bild per frysvara, praktiskt för udda styckdetaljer.

## Plattformsidéer (längre fram)

**Molnsynk (Etapp 6)** – Supabase eller liknande så iPad, iPhone och dator ser samma data i realtid; hela hushållet kan använda den; ingen risk att webbdata rensas. Beslut: byggs när plattformen bevisat sitt vardagsvärde.

**Gästläge** – "Visa källaren/menyn" utan redigeringsmöjlighet, för att visa upp för gäster.

**Vinprovningsanteckningar** – Betyg och noteringar per flaska man öppnat, kopplat till vinarkivet.

**Visuell hyllvy för Garaget** – Samma kärleksfulla SVG-behandling som Vinkylen fått (träställ, synliga hyllplan), så de två skåpen känns som ett par.

**Måltidshistorik** – Logg över komponerade och lagade middagar, så Köket-motorn kan lära sig ännu mer av vad som faktiskt lagats och uppskattats.

## Hur vi använder den här filen

- När ett "det gör vi senare"-förslag dyker upp under bygget → läggs här direkt
- När vi är redo för nästa större grej → vi tittar här och väljer
- Inget byggs härifrån utan eget beslut och egen plan först
