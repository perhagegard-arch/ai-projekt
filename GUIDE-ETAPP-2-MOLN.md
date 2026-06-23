# 🎓 Guide: Etapp 2 – Inloggning & moln (för nybörjare)

*En lugn, visuell genomgång av nästa stora steg för Pers Kök & Vinkällare: att gå från en app som sparar data lokalt på varje enhet, till en app med inloggning och molnlagring där flera användare kan ha var sin källare – och så småningom dela med varandra.*

*Skriven för dig som är ny. Inga förkunskaper antas. Läs i lugn och ro, och ta den gärna med när du bygger tillsammans med din bror.*

---

## Innehåll

1. Var vi står idag (och varför vi vill vidare)
2. Supabase – "bakrummet" till appen
3. De tre begreppen: Auth, Databas, RLS
4. Google-inloggning steg för steg
5. Vad händer med min data? (migreringen)
6. Hur multiuser fungerar
7. Det sociala steget (etapp 3)
8. Hela vägen – delstegen i ordning
9. Ordlista (ta med till din bror)
10. Frågor att ställa din bror

---

## 1. Var vi står idag

Din app är byggd som **statiska filer på GitHub Pages**. All data sparas i webbläsarens **localStorage** – ett litet utrymme i webbläsaren, på just den enheten.

```
   DIN IPAD             DIN TELEFON          KOMPIS TELEFON
 ┌────────────┐       ┌────────────┐       ┌────────────┐
 │localStorage│       │localStorage│       │localStorage│
 │  45 viner  │       │    tom     │       │    tom     │
 │ dina frysar│       │  (separat) │       │  (separat) │
 └────────────┘       └────────────┘       └────────────┘
       │                    │                    │
   isolerad             isolerad             isolerad
```

Det fungerar bra – men har tre begränsningar:

- **Bunden till enheten.** Öppnar du appen på en ny enhet är den tom. Din data finns bara där du skapade den.
- **Ingen vet vem du är.** Det finns ingen inloggning. Appen känner igen "dig" bara genom att det råkar finnas data på enheten.
- **Ingen kan dela.** Du och en kompis lever i varsin bubbla. Ni kan inte se varandras källare även om ni vill.

Din målbild är att appen ska ut i verkligheten: flera användare, var och en med sin egen frys och vinkyl, inloggning med Google, och möjlighet att be en vän få se deras vinkällare. Det kräver tre skiften – och alla tre löses i etapp 2 och 3.

---

## 2. Supabase – "bakrummet" till appen

**Supabase** är en färdig tjänst på nätet som ger din app ett "bakrum" – allt det du inte har idag. Istället för att bygga inloggning, databas och säkerhet från grunden (månader av arbete) får du det på köpet.

```
 ┌──────────────────── SUPABASE ────────────────────┐
 │                                                   │
 │    AUTH             DATABAS          RLS-REGLER    │
 │  (inloggning)      (lagring)        (säkerhet)    │
 │                                                   │
 │  "Logga in         Sparar alla      Var och en    │
 │   med Google"      viner, frysar,   når bara SIN  │
 │  Vet vem du är     recept centralt  egen data     │
 └───────────────────────────────────────────────────┘
```

Bra att veta:
- Supabase har en **gratisnivå** som räcker långt för ett projekt som ditt.
- Det är ett av de vanligaste valen för precis den här typen av app, så din bror känner troligen till det.
- Du skapar ett konto, ett "projekt", och får nycklar som din app använder för att prata med bakrummet.

---

## 3. De tre begreppen: Auth, Databas, RLS

Det här är de tre orden du kommer höra och själv säga. Lär dig dem, så förstår du hela steget.

### Auth (uttalas "ååth", av *authentication* = autentisering)
Betyder helt enkelt **inloggning**. När du klickar "Logga in med Google" är det Auth som sköter det. Google bekräftar att du är du, och du får ett digitalt "armband" (en **token**) som bevisar din identitet resten av besöket. **Du behöver aldrig skapa eller lagra lösenord** – Google sköter den biten. Det är både enklare och säkrare.

### Databas
Där all data bor – **centralt på nätet** istället för på din enhet. En databas är som ett gäng mycket strukturerade Excel-ark som pratar med varandra:

```
  ARK: anvandare        ARK: viner             ARK: frysar
  ┌──────────────┐      ┌──────────────────┐   ┌──────────────┐
  │ id           │      │ id               │   │ id           │
  │ namn         │      │ ägare (vem?)     │   │ ägare (vem?) │
  │ epost        │      │ namn, druva, år  │   │ namn, fack   │
  └──────────────┘      │ hyllplats        │   └──────────────┘
                        └──────────────────┘
```

Varje **rad** (ett vin, en frys) har en kolumn som säger **vem den tillhör**. Det är nyckeln till nästa begrepp.

### RLS (Row Level Security = säkerhet på radnivå)
Den viktigaste och mest geniala delen. RLS betyder att **varje rad vet vem den tillhör**, och en regel säger: *"du får bara se rader som är dina."*

Det är detta som gör att en kompis viner är **osynliga för alla andra** – tills han aktivt väljer att dela. Utan RLS skulle vem som helst kunna se allas data. Med RLS är allt **privat som standard**. Du bygger delning ovanpå, som ett medvetet val.

> Tumregel att minnas: **Privat som standard. Delning är ett aktivt, ångerbart val.**

---

## 4. Google-inloggning steg för steg

Så här går "Logga in med Google" till, från insidan:

```
 1. Du klickar          2. Google              3. Supabase           4. Appen visar
 ┌─────────────┐        ┌─────────────┐        ┌─────────────┐       ┌─────────────┐
 │ "Logga in   │   →    │ bekräftar:  │   →    │ ger dig en  │   →   │   DIN       │
 │  med Google"│        │ "det är Per"│        │ token       │       │   data      │
 └─────────────┘        └─────────────┘        │ (armband)   │       └─────────────┘
                                               └─────────────┘
```

**Armbandet (token)** följer sedan med varje gång appen pratar med databasen. Så databasen vet hela tiden att det är du – och RLS ser till att du bara får tillbaka dina egna rader.

Det fina: du loggar in en gång, och sen "kommer appen ihåg dig" oavsett vilken enhet du sitter vid. Det löser problemet med att data var bunden till enheten.

---

## 5. Vad händer med min data? (migreringen)

Det här är den känsligaste delen – dina 45 viner och dina frysar ska flyttas från localStorage till molnet **utan att något tappas**. Vi gör det varsamt, i en bestämd ordning:

```
 1. Säkerhetskopia  →  2. Läs lokalt    →  3. Skriv till moln  →  4. Verifiera
 ┌──────────────┐      ┌──────────────┐    ┌──────────────┐      ┌──────────────┐
 │ Exportera    │      │ Hämta data   │    │ Spara i      │      │ Kom allt     │
 │ allt till    │      │ ur local-    │    │ Supabase,    │      │ fram? ✓      │
 │ en fil först │      │ Storage      │    │ kopplat      │      │              │
 │              │      │              │    │ till dig     │      │              │
 └──────────────┘      └──────────────┘    └──────────────┘      └──────────────┘
```

**Den gyllene regeln:** Säkerhetskopian (steg 1) är din väg tillbaka. Originaldatan i localStorage rörs inte under tiden. Vi **litar inte på molnet förrän steg 4 är grönt** – tills vi sett att precis alla viner och frysar kom fram, korrekt.

Det här är samma princip vi följt hela projektet ("alltid en väg tillbaka"), bara i lite större skala. Det är därför vi inte stressar – migreringen görs en gång, och den görs rätt.

---

## 6. Hur multiuser fungerar

När flera är inloggade ligger allas data i **samma databas** – men RLS gör att var och en bara ser sitt. Tänk databasen som ett stort arkiv där varje mapp är märkt med en ägare, och en vakt (RLS) bara släpper fram dig till dina egna mappar:

```
  Per      ─┐
  Kompis A ─┼─→  [ RLS-vakten ]  ─→   GEMENSAM DATABAS
  Kompis B ─┘    "Vems data            ┌────────────────────────┐
                  är du?"               │ Pers viner   → bara Per│
                                        │ A:s data     → bara A  │
                                        │ B:s data     → bara B  │
                                        └────────────────────────┘
```

Alla använder samma app och samma databas, men upplevelsen är att var och en har sin **egen privata källare**. Ingen ser någon annans – förrän de väljer att dela. Vilket leder oss till nästa steg.

---

## 7. Det sociala steget (etapp 3)

När inloggning och moln är på plats (etapp 2) kan vi bygga det du drömmer om: att se varandra och dela. Vi tar det från **minst till mest känsligt**, så integriteten alltid är skyddad:

```
  1. Användarkatalog   →  "vilka använder appen?" (visar bara namn)
  2. Vänförfrågningar  →  skicka → godkänn (inget syns utan ja från båda)
  3. Dela vinkällare   →  en vän får SE din källare (läs-vy, aldrig ändra)
  4. Dela recept       →  skicka ett recept ur banken till en vän
```

**Integritet är hela spelet här.** Grundregeln, hela vägen:
- Standard = **privat**.
- Varje delning är ett **aktivt val** du gör.
- Allt går att **ångra** (sluta dela).
- En vän som får se din källare kan bara **läsa**, aldrig ändra.

Bygger man det här fel en gång är förtroendet borta. Därför bygger vi det sist, noggrant, på en stabil grund.

---

## 8. Hela vägen – delstegen i ordning

Etapp 2 är inte en eftermiddag – det är flera sittningar. Så här delar vi upp den i trygga bitar. **En sak i taget, testa mellan varje.**

```
  ETAPP 2 – moln & inloggning
  ─────────────────────────────────────────────────────────
  Steg A:  Skapa Supabase-konto + projekt          (uppsättning)
  Steg B:  Få "Logga in med Google" att fungera     (bara inloggning)
  Steg C:  Skapa databastabeller (viner, frysar…)   (en i taget)
  Steg D:  Sätt RLS-regler (privat som standard)    (säkerheten)
  Steg E:  Koppla EN sida till molnet (t.ex. vinkällaren)
  Steg F:  Migrera din data – backup, flytta, verifiera
  Steg G:  Koppla resten av sidorna, en i taget
  Steg H:  Flytta AI-nyckeln till servern (dold för användare)
  ─────────────────────────────────────────────────────────
  ETAPP 3 – det sociala (efter att etapp 2 är stabil)
  ─────────────────────────────────────────────────────────
  Användarkatalog → vänförfrågningar → dela källare → dela recept
```

Vi börjar inte koda förrän du känner dig redo. Mellan varje steg stannar vi, testar, och går vidare först när det fungerar.

---

## 9. Ordlista (ta med till din bror)

| Ord | Betyder | I klartext |
|-----|---------|-----------|
| **Supabase** | Tjänst för inloggning + databas + säkerhet | "Bakrummet" till appen |
| **Auth** | Authentication = autentisering | Inloggning |
| **Token** | Tillfälligt identitetsbevis | Ett "armband" som visar vem du är |
| **Databas** | Strukturerad central lagring | Excel-ark som pratar med varandra |
| **Tabell** | Ett "ark" i databasen | T.ex. ett ark för viner |
| **Rad** | En post i en tabell | Ett enskilt vin |
| **RLS** | Row Level Security | "Du ser bara dina egna rader" |
| **Migrering** | Flytta data mellan system | Flytta vinerna från localStorage till molnet |
| **localStorage** | Lagring i webbläsaren | Där datan bor idag (per enhet) |
| **Backend** | Serverdelen av en app | Det som händer "bakom" – databasen, inloggningen |

---

## 10. Frågor att ställa din bror

När ni sätter er tillsammans kan dessa frågor vara bra att utgå från:

1. Har du jobbat med Supabase förut – eller föredrar du något annat (t.ex. Firebase)? Varför?
2. Hur vill du lägga upp tabellerna? En tabell per sak (viner, frysar, recept), eller annorlunda?
3. Hur testar vi RLS ordentligt så vi vet att ingen kan se någon annans data?
4. Hur gör vi migreringen säkrast? Kör vi den för en testanvändare först?
5. Var lägger vi AI-nyckeln när den flyttar till servern? Hur sätter vi ett kostnadstak?
6. Hur hanterar vi en användare som loggar in på en ny enhet – ska gammal localStorage-data erbjudas att "flyttas upp"?

---

## En sista uppmuntran

Det här är ett stort steg, men det är samma arbetssätt som burit hela projektet: **bygg lagom, en sak i taget, testa, och ha alltid en väg tillbaka.** Du behöver inte kunna allt själv – poängen med den här guiden är att du ska förstå *helheten* och *orden*, så att du och din bror kan bygga tillsammans på lika villkor.

När du läst klart och känner dig redo: säg bara till, så börjar vi med **Steg A**. 🍷

*Dokumentet hör till Pers Kök & Vinkällare. Se även ROADMAP-DELAD-PLATTFORM.md för den övergripande planen och LOGGBOK.md för beslut.*
