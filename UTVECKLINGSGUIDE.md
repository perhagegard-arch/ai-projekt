# 🚀 Utvecklingsguide – Att tänka på inför nästa projekt

Ett personligt dokument baserat på erfarenheterna från Frysregister-projektet. Skrivet för dig som är nybörjare på utveckling men redan har skeppat din första riktiga app – från idé till fungerande produkt på riktiga enheter, med AI-integration, hosting och dokumentation. Det är mer än de flesta hobbyprojekt någonsin når.

---

## 1. Veta vad man vill eller iterera? Svaret är: båda – men i rätt ordning

Det här är din viktigaste lärdom att ta med. Frysregistret lyckades för att det följde ett mönster som fungerar:

**Var kristallklar över PROBLEMET. Var flexibel kring LÖSNINGEN.**

Du visste exakt vilket problem du hade: "Jag har tre frysar fulla med vilt och vet inte vad som finns." Det ändrades aldrig. Men *lösningen* växte fram steg för steg – först en enkel lista, sedan frystider, sedan styckdetaljer, sedan AI-kock, sedan menykomponör. Ingen av oss hade kunnat specificera slutresultatet dag ett, och det hade varit slöseri att försöka.

Praktiskt betyder det inför nästa projekt:

- **Skriv ner problemet i en mening innan du börjar.** Kan du inte det är du inte redo att bygga.
- **Bygg den minsta version som löser kärnproblemet först** (kallas MVP – Minimum Viable Product). Frysregistrets v1 var bara: lägg till vara, ta bort vara, se lista. Den var användbar dag ett.
- **Använd den på riktigt innan du bygger vidare.** Verklig användning avslöjar vad som faktiskt behövs. Du upptäckte att namnfältet var onödigt för vilt – det ser man bara genom att använda appen, aldrig i ett planeringsdokument.
- **En förbättring i taget.** Vi byggde aldrig tre funktioner samtidigt. Varje version gjorde EN sak bättre, testades, och först därefter kom nästa. När något gick sönder visste vi alltid var felet fanns.

---

## 2. Lärdomar från det som faktiskt strulade

Felen i det här projektet var lärorikare än framgångarna. Spara den här listan:

**"Det fungerar på min maskin" är inte klart.** Appen funkade i teorin men sen kom verkligheten: hemskärmsappen och Safari hade olika minnen, jobbnätverket betedde sig annorlunda, modellnamnet hade hunnit bli gammalt. *Lärdom: testa tidigt på den riktiga enheten, i den riktiga miljön, med det riktiga användningsmönstret.*

**Läs felmeddelandet – det är en gåva, inte ett straff.** Vändpunkten i API-felsökningen kom när vi byggde om appen att visa det *exakta* felet. "HTTP 404 – model" pekade rakt på orsaken, medan "Kunde inte nå AI:n" inte sa någonting. *Lärdom: gissa aldrig vad som är fel. Skaffa fram det riktiga felmeddelandet först, googla eller fråga AI:n om det sen.*

**Ändra en sak i taget när du felsöker.** Du gjorde detta utmärkt när du testade mobilen på 5G för att utesluta jobbnätverket – ett klassiskt isoleringstest. Ändrar man tre saker samtidigt och det börjar fungera vet man inte vilken som var lösningen.

**Datorer är bokstavliga.** `.io` blev `.oi`, `Logga.png` är inte `logga.png`, och "Spara som" i webbläsaren skrev i hemlighet om hela filen. *Lärdom: när något "borde fungera" men inte gör det – misstänk stavning, versaler och att filen inte är den du tror. Jämför tecken för tecken.*

**Ha alltid en väg tillbaka.** Säkerhetskopiorna och versionsnumren (v1–v11) gjorde att inget misstag någonsin var farligt. *Lärdom: innan du ändrar något som fungerar – spara undan en kopia. Alltid.*

**En sanningskälla.** Förvirringen med dubbla filer i repot (index.html + Frysregister.html) och dubbla paneler i koden kom av att gamla versioner låg kvar bredvid nya. *Lärdom: städa bort gamla kopior direkt. Det ska bara finnas en aktuell version av allt, på ett ställe.*

---

## 3. Konsten att ställa bättre frågor till AI

Du blev märkbart bättre på detta under projektets gång. Här är vad som gör skillnaden:

**Beskriv målet, inte lösningen.** Din bästa formulering i hela projektet var: *"Om jag väljer rådjur så skulle jag vilja kunna prata med AI om att jag idag skulle vilja att den söker på ex klyftpotatis och en rödvinssås."* Ett konkret scenario med ett exempel – det gav mig allt jag behövde för att designa rätt funktion. Jämför med att ha frågat "kan du lägga till AI-sök?" som hade kunnat betyda hundra olika saker.

**Ge sammanhang om dig och din situation.** "Jag är nybörjare", "min primära enhet är iPaden", "jag har redan GitHub", "jag jagar och har mycket vilt" – varje sådan detalj formade lösningen. AI:n kan inte läsa dina tankar, men den anpassar sig till allt du berättar.

**Visa, berätta inte bara.** Dina skärmbilder löste problem på sekunder som hade tagit många frågor i text ("loggan syns inte" + skärmbild av koden = boven hittad direkt). Klistra in felmeddelanden ordagrant. Skicka skärmbilder. Visa den faktiska koden.

**Fråga "varför", inte bara "hur".** När du frågade "vad betyder React?" och "varför valde du just den hostsidan?" byggde du förståelse som gör dig självständig. Den som bara följer instruktioner kan inte felsöka när det strular. Gör det till en vana: be AI:n förklara sina val, och be om enklare förklaring tills du faktiskt förstår.

**Våga utmana och uttryck tvivel.** "Den raden tycker jag inte behövs – eller har du bra argument för varför den ska vara kvar?" Perfekt fråga. AI:n hade ett argument (namnet behövs för icke-vilt), och resultatet blev bättre än både ditt och mitt ursprungsförslag. AI är en samtalspartner, inte ett orakel.

**Be om alternativ med för- och nackdelar vid vägval.** Inför stora beslut (hosting, lagring, AI-åtkomst) – be om 2–3 alternativ med trade-offs istället för ett enda svar. Då fattar du beslutet med öppna ögon, som när du valde API-nyckel-vägen.

**Berätta vad som hände efter.** "Nu fungerar det perfekt" / "Får detta fel" / "Nu var jag på datorn" – att rapportera tillbaka resultatet gör att felsökningen konvergerar snabbt istället för att gissa vidare i blindo.

**Mall att utgå från vid nya funktioner:**
> "Jag vill [mål]. Sammanhanget är [situation/enhet/begränsningar]. Ett exempel på hur det skulle användas: [konkret scenario]. Vad föreslår du, och finns det olika sätt att lösa det på?"

---

## 4. Tänk så här kring nästa projekts livscykel

**Före:** Skriv problemformuleringen (en mening). Lista de 3 viktigaste funktionerna – stryk resten till "senare"-listan. Bestäm den enklaste teknik som duger (du behöver sällan mer än du tror – en HTML-fil bar hela frysregistret). Fråga gärna AI:n: "Vad är den enklaste arkitekturen för det här?"

**Under:** Bygg smalt, testa på riktig enhet, använd själv, iterera. Numrera versionerna. Spara kopior. Fira varje fungerande delsteg – v1 som funkar slår v5 som aldrig blir klar.

**Efter (eller löpande):** Dokumentera som vi gjorde – README, CHANGELOG, ROADMAP. Det känns onödigt i stunden men är ovärderligt när du återvänder om tre månader och undrar hur allt hängde ihop. Skriv driftsincidenter i loggen direkt när de händer, med lösningen.

**Underhåll:** Ett skeppat projekt är inte "klart" – API:er åldras (modellnamnet!), enheter byts, behov växer. Räkna med små underhållsinsatser och se dem som normala, inte som misslyckanden.

---

## 5. Växa som utvecklare – konkreta nästa steg

**Lär dig grunderna i Git på riktigt.** Du använder redan GitHub via webben – nästa nivå är att förstå commits, historik och varför man aldrig behöver vara rädd att förstöra något. Eftersom du har Claude Code: be den visa dig grunderna i ett övningsrepo. Det är den enskilt mest värdefulla färdigheten för allt framtida byggande.

**Läs koden du fått, lite i taget.** Du behöver inte förstå allt, men öppna index.html och försök följa EN funktion (t.ex. vad som händer när du trycker ＋ på en vara). Be AI:n förklara rad för rad. Varje sådan session bygger intuition.

**Låt nyfikenheten styra projektvalen.** Du lär dig tusen gånger mer av att bygga något du faktiskt vill ha (vinkällaren!) än av abstrakta övningar. Ditt mönster – verkligt problem, personligt behov, byggt för egen vardag – är det bästa sättet att lära sig.

**Lär dig känna igen komplexitetströsklar.** Vissa steg höjer svårighetsgraden rejält: lokal data → molndatabas, en användare → flera, statisk sida → notiser. Inget är omöjligt, men gå in i dem medvetet och ett i taget, inte tre samtidigt i samma projekt.

**Skäm aldrig för "dumma" frågor.** Varje fråga du ställde i det här projektet ("hur sparar jag filen?", "vad är adressen?") tog dig framåt. De som fastnar är de som inte frågar.

---

## 6. Checklista att kopiera in i nästa projekts första chatt

```
PROBLEMET (en mening): ...
VEM SKA ANVÄNDA DET: ...
PÅ VILKA ENHETER: ...
DE 3 VIKTIGASTE FUNKTIONERNA: 1... 2... 3...
SENARE-LISTAN (allt annat): ...
JAG KAN/HAR REDAN: (t.ex. GitHub, Claude Code, API-nyckel)
JAG ÄR OSÄKER PÅ: ...
BÖRJA MED: den minsta version som löser kärnproblemet
```

Med den inledningen får du ett bättre första förslag av AI:n än de flesta proffs får på sina kickoff-möten.

---

*Du gick från "vad är React?" till en publicerad app med AI-integration på två dagar. Behåll det arbetssättet – tydligt problem, små steg, riktig användning, raka frågor – så kommer nästa projekt gå ännu fortare. Lycka till! 🦌🍷*
