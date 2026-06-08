"""
server.py – Flask-backend för AI-Projekt med SQLite-databas (Fas 3).

Före första start:  python tools/migrera_db.py
Kör sedan:          python server.py
Öppna:              http://localhost:5000
Stoppa:             Ctrl+C
"""

import base64
import os
import requests
import sqlite3
import sys
from datetime import datetime

# Tvinga UTF-8 i Windows-terminalen
sys.stdout.reconfigure(encoding="utf-8")

from flask import Flask, g, jsonify, request, send_from_directory

# ── KONFIGURATION ────────────────────────────────────────────────────

ROT          = os.path.dirname(os.path.abspath(__file__))
DB_FIL       = os.path.join(ROT, "data", "sousvide.db")
BILD_MAPP       = os.path.join(ROT, "static", "bilder")
VINKALLARE_MAPP = os.path.join(ROT, "static", "vinkallare")
BILDTYPER       = {"jpg", "jpeg", "png", "webp"}

# Svenska månadsförkortningar – locale-oberoende
MANADER = ["jan","feb","mar","apr","maj","jun","jul","aug","sep","okt","nov","dec"]

app = Flask(__name__)
app.secret_key = "byt-ut-mig-till-nagot-hemligt-i-fas-4"

# ── GEMINI AI ────────────────────────────────────────────────────────

# Prompt som skickas till Gemini Vision tillsammans med etikettbilden
GEMINI_PROMPT = (
    "Du är en erfaren sommelier. Titta noga på vinets etikett och ge en kort "
    "beskrivning på svenska. Svara exakt i detta format – en rad per punkt:\n\n"
    "🍷 Doft: [2–3 aromer, t.ex. körsbär, vanilj, tobak]\n"
    "👅 Smak: [2–3 egenskaper, t.ex. fyllig, len, lång eftersmak]\n"
    "🍽️ Passar till: [2 maträtter]\n"
    "⭐ Karaktär: [en kort mening om vinets stil och årgång]\n\n"
    "Håll varje rad kort (max 12 ord). Svara alltid på svenska."
)


def hamta_smaknot(bildvag):
    """Skickar etikettbild till Gemini Vision och returnerar smak- och doftnoter."""
    api_nyckel = os.environ.get("GEMINI_API_KEY", "")
    if not api_nyckel:
        return None  # Ingen nyckel konfigurerad – hoppa över analysen

    try:
        # Läs och base64-koda bildfilen
        ext  = bildvag.rsplit(".", 1)[1].lower()
        mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
                "png": "image/png",  "webp": "image/webp"}.get(ext, "image/jpeg")
        with open(bildvag, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()

        # Anropa Gemini 1.5 Flash (gratis tier)
        url  = (f"https://generativelanguage.googleapis.com/v1beta/"
                f"models/gemini-2.5-flash:generateContent?key={api_nyckel}")
        data = {
            "contents": [{
                "parts": [
                    {"text": GEMINI_PROMPT},
                    {"inlineData": {"mimeType": mime, "data": b64}}
                ]
            }],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 200}
        }
        svar = requests.post(url, json=data, timeout=20)
        svar.raise_for_status()
        text = svar.json()["candidates"][0]["content"]["parts"][0]["text"]
        print(f"  ✓ Gemini-analys klar ({len(text)} tecken)")
        return text.strip()
    except Exception as e:
        print(f"  ⚠️  Gemini-fel: {e}")
        return None


# ── DATABASHANTERING ─────────────────────────────────────────────────

def get_db():
    """Returnerar en databasanslutning kopplad till det aktiva anropet."""
    if "db" not in g:
        g.db = sqlite3.connect(DB_FIL)
        g.db.row_factory = sqlite3.Row   # Gör att rader beter sig som dict
    return g.db


@app.teardown_appcontext
def close_db(error):
    """Stänger databasanslutningen automatiskt när anropet är klart."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def datum_sv():
    """Returnerar dagens datum i svensk kortformat, t.ex. '3 jun'."""
    d = datetime.now()
    return f"{d.day} {MANADER[d.month - 1]}"


def tillaten_bildtyp(filnamn):
    """Returnerar True om filändelsen är en tillåten bildtyp."""
    return "." in filnamn and filnamn.rsplit(".", 1)[1].lower() in BILDTYPER


def migrera_bild_kolumn():
    """Lägger till bild-kolumnen i recept-tabellen om den saknas."""
    try:
        with sqlite3.connect(DB_FIL) as db:
            db.execute("ALTER TABLE recept ADD COLUMN bild TEXT")
    except sqlite3.OperationalError:
        pass  # Kolumnen finns redan


def init_vinkallare_tabell():
    """Skapar vinkallare-tabellen och dess index om de saknas."""
    with sqlite3.connect(DB_FIL) as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS vinkallare (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                namn         TEXT    NOT NULL,
                druva        TEXT,
                land         TEXT,
                region       TEXT,
                arsgang      INTEGER,
                typ          TEXT,
                anteckningar TEXT,
                bild_fram    TEXT,
                bild_bak     TEXT,
                smaknot      TEXT,
                inlagd       TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_vinkallare_typ ON vinkallare (typ);
        """)


def init_smaknot_kolumn():
    """Lägger till smaknot-kolumnen i vinkallare-tabellen om den saknas."""
    try:
        with sqlite3.connect(DB_FIL) as db:
            db.execute("ALTER TABLE vinkallare ADD COLUMN smaknot TEXT")
    except sqlite3.OperationalError:
        pass  # Kolumnen finns redan


# ── STATISKA FILER ───────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(ROT, "index.html")


@app.route("/<path:filnamn>")
def statisk_fil(filnamn):
    """Serverar alla HTML-, JS- och CSS-filer från projektmappen."""
    return send_from_directory(ROT, filnamn)


# ── API: RECEPT ──────────────────────────────────────────────────────

@app.route("/api/recept", methods=["GET"])
def hamta_recept():
    """Returnerar alla körningar från databasen."""
    rader = get_db().execute("SELECT * FROM recept ORDER BY id").fetchall()
    return jsonify([dict(r) for r in rader])


@app.route("/api/recept", methods=["POST"])
def lagg_till_recept():
    """Sparar en ny körning i databasen."""
    nytt = request.get_json(silent=True)
    if not nytt or not nytt.get("namn"):
        return jsonify({"fel": "Fältet 'namn' saknas"}), 400

    db = get_db()
    cursor = db.execute(
        """INSERT INTO recept (namn, kat, metod, temp, tid, n, betyg, omdome, datum, hl, tags, eget)
           VALUES (:namn, :kat, :metod, :temp, :tid, :n, :betyg, :omdome, :datum, :hl, :tags, :eget)""",
        {
            "namn":   nytt.get("namn", ""),
            "kat":    nytt.get("kat", "ovrigt"),
            "metod":  nytt.get("metod", "Sous vide"),
            "temp":   nytt.get("temp"),
            "tid":    nytt.get("tid"),
            "n":      nytt.get("n", 3),
            "betyg":  nytt.get("betyg", "Bra"),
            "omdome": nytt.get("omdome", ""),
            "datum":  datum_sv(),
            "hl":     nytt.get("hl"),
            "tags":   nytt.get("tags", nytt.get("namn", "").lower()),
            "eget":   1,
        },
    )
    db.commit()

    nytt["id"]    = cursor.lastrowid
    nytt["datum"] = datum_sv()
    nytt["eget"]  = True
    print(f"  ✓ Ny körning sparad: {nytt['namn']} (id={nytt['id']})")
    return jsonify(nytt), 201


@app.route("/api/recept/<int:recept_id>/bild", methods=["POST"])
def ladda_upp_bild(recept_id):
    """Tar emot en bildfil och kopplar den till en körning."""
    if "fil" not in request.files:
        return jsonify({"fel": "Ingen fil skickades"}), 400

    fil = request.files["fil"]
    if not fil.filename or not tillaten_bildtyp(fil.filename):
        return jsonify({"fel": "Tillåtna filtyper: jpg, png, webp"}), 400

    db  = get_db()
    rad = db.execute("SELECT id, bild FROM recept WHERE id = ?", (recept_id,)).fetchone()
    if not rad:
        return jsonify({"fel": "Körning hittades inte"}), 404

    # Ta bort eventuell gammal bild
    if rad["bild"]:
        gammal = os.path.join(BILD_MAPP, rad["bild"])
        if os.path.exists(gammal):
            os.remove(gammal)

    # Spara ny bild – filnamnet baseras på körningens id
    ext       = fil.filename.rsplit(".", 1)[1].lower()
    bildnamn  = f"recept_{recept_id}.{ext}"
    fil.save(os.path.join(BILD_MAPP, bildnamn))

    db.execute("UPDATE recept SET bild = ? WHERE id = ?", (bildnamn, recept_id))
    db.commit()

    print(f"  ✓ Bild sparad: {bildnamn}")
    return jsonify({"bild": bildnamn}), 200


@app.route("/api/recept/<int:recept_id>", methods=["DELETE"])
def ta_bort_recept(recept_id):
    """Tar bort en körning ur databasen."""
    db  = get_db()
    rad = db.execute("SELECT id FROM recept WHERE id = ?", (recept_id,)).fetchone()
    if not rad:
        return jsonify({"fel": "Körning hittades inte"}), 404
    db.execute("DELETE FROM recept WHERE id = ?", (recept_id,))
    db.commit()
    print(f"  ✓ Körning {recept_id} borttagen")
    return "", 204


# ── API: VINSTATUS ───────────────────────────────────────────────────

@app.route("/api/vinstatus", methods=["GET"])
def hamta_vinstatus():
    """Returnerar aktuellt vinsortiment från databasen."""
    viner = [dict(r) for r in get_db().execute("SELECT * FROM viner ORDER BY id").fetchall()]
    nu    = datetime.now()
    return jsonify({
        "kord_av":       "server.py",
        "butik":         "Systembolaget Djurgården, Linköping",
        "uppdaterad":    nu.isoformat(timespec="seconds"),
        "uppdaterad_sv": f"{nu.day} {MANADER[nu.month - 1]} {nu.year} kl. {nu.strftime('%H:%M:%S')}",
        "antal_viner":   len(viner),
        "viner":         viner,
    })


# ── API: BILDBIBLIOTEK ───────────────────────────────────────────────

@app.route("/api/bilder")
def lista_bilder():
    """Returnerar alla bilder i static/bilder/bibliotek/ som URL-lista."""
    bibliotek = os.path.join(ROT, "static", "bilder", "bibliotek")
    os.makedirs(bibliotek, exist_ok=True)
    ok_typer  = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    bilder    = [
        f"/static/bilder/bibliotek/{f}"
        for f in sorted(os.listdir(bibliotek))
        if os.path.splitext(f)[1].lower() in ok_typer
    ]
    return jsonify(bilder)


@app.route("/api/bilder/ladda-upp", methods=["POST"])
def ladda_upp_bibliotek_bild():
    """Laddar upp en bild till bildbiblioteket."""
    if "fil" not in request.files:
        return jsonify({"fel": "Ingen fil"}), 400
    fil = request.files["fil"]
    if not fil.filename or not tillaten_bildtyp(fil.filename):
        return jsonify({"fel": "Ogiltig filtyp"}), 400
    bibliotek = os.path.join(ROT, "static", "bilder", "bibliotek")
    os.makedirs(bibliotek, exist_ok=True)
    # Behåll originalnamnet men ersätt mellanslag
    sakert_namn = fil.filename.replace(" ", "_")
    fil.save(os.path.join(bibliotek, sakert_namn))
    return jsonify({"url": f"/static/bilder/bibliotek/{sakert_namn}"}), 201


# ── API: VINKÄLLARE ──────────────────────────────────────────────────

@app.route("/api/vinkallare", methods=["GET"])
def hamta_vinkallare():
    """Returnerar alla flaskor i vinkällaren, sorterade på typ och namn."""
    rader = get_db().execute(
        "SELECT * FROM vinkallare ORDER BY typ, namn"
    ).fetchall()
    return jsonify([dict(r) for r in rader])


@app.route("/api/vinkallare", methods=["POST"])
def lagg_till_vin():
    """Lägger till en ny flaska i vinkällaren."""
    nytt = request.get_json(silent=True)
    if not nytt or not nytt.get("namn"):
        return jsonify({"fel": "Fältet 'namn' saknas"}), 400

    db = get_db()
    cursor = db.execute(
        """INSERT INTO vinkallare (namn, druva, land, region, arsgang, typ, anteckningar, inlagd)
           VALUES (:namn, :druva, :land, :region, :arsgang, :typ, :anteckningar, :inlagd)""",
        {
            "namn":         nytt.get("namn", ""),
            "druva":        nytt.get("druva", ""),
            "land":         nytt.get("land", ""),
            "region":       nytt.get("region", ""),
            "arsgang":      nytt.get("arsgang"),
            "typ":          nytt.get("typ", "Rött"),
            "anteckningar": nytt.get("anteckningar", ""),
            "inlagd":       datum_sv(),
        },
    )
    db.commit()
    nytt["id"]     = cursor.lastrowid
    nytt["inlagd"] = datum_sv()
    print(f"  ✓ Nytt vin: {nytt['namn']} (id={nytt['id']})")
    return jsonify(nytt), 201


@app.route("/api/vinkallare/<int:vin_id>/bild/<sida>", methods=["POST"])
def ladda_upp_vin_bild(vin_id, sida):
    """Laddar upp etikettbild – sida är 'fram' eller 'bak'."""
    if sida not in ("fram", "bak"):
        return jsonify({"fel": "Ogiltig sida – använd fram eller bak"}), 400
    if "fil" not in request.files:
        return jsonify({"fel": "Ingen fil skickades"}), 400

    fil = request.files["fil"]
    if not fil.filename or not tillaten_bildtyp(fil.filename):
        return jsonify({"fel": "Tillåtna filtyper: jpg, png, webp"}), 400

    db  = get_db()
    rad = db.execute("SELECT id FROM vinkallare WHERE id = ?", (vin_id,)).fetchone()
    if not rad:
        return jsonify({"fel": "Flaska hittades inte"}), 404

    ext      = fil.filename.rsplit(".", 1)[1].lower()
    bildnamn = f"vin_{vin_id}_{sida}.{ext}"
    fil.save(os.path.join(VINKALLARE_MAPP, bildnamn))

    # Kolumnnamnet är antingen bild_fram eller bild_bak
    db.execute(f"UPDATE vinkallare SET bild_{sida} = ? WHERE id = ?", (bildnamn, vin_id))
    db.commit()
    print(f"  ✓ Vinkällare-bild: {bildnamn}")

    # Kör AI-analys med Gemini när framsidan laddas upp
    smaknot = None
    if sida == "fram":
        print(f"  🤖 Skickar etikett till Gemini för smakanalys…")
        smaknot = hamta_smaknot(os.path.join(VINKALLARE_MAPP, bildnamn))
        if smaknot:
            db.execute("UPDATE vinkallare SET smaknot = ? WHERE id = ?", (smaknot, vin_id))
            db.commit()

    return jsonify({"bild": bildnamn, "sida": sida, "smaknot": smaknot}), 200


@app.route("/api/vinkallare/<int:vin_id>", methods=["PATCH"])
def uppdatera_vin(vin_id):
    """Uppdaterar textfälten på en befintlig flaska."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"fel": "Ingen data skickades"}), 400

    db  = get_db()
    rad = db.execute("SELECT id FROM vinkallare WHERE id = ?", (vin_id,)).fetchone()
    if not rad:
        return jsonify({"fel": "Flaska hittades inte"}), 404

    db.execute(
        """UPDATE vinkallare
           SET namn=:namn, druva=:druva, land=:land, region=:region,
               arsgang=:arsgang, typ=:typ, anteckningar=:anteckningar
           WHERE id=:id""",
        {
            "id":           vin_id,
            "namn":         data.get("namn", ""),
            "druva":        data.get("druva", ""),
            "land":         data.get("land", ""),
            "region":       data.get("region", ""),
            "arsgang":      data.get("arsgang"),
            "typ":          data.get("typ", "Rött"),
            "anteckningar": data.get("anteckningar", ""),
        },
    )
    db.commit()
    uppdaterad = dict(db.execute(
        "SELECT * FROM vinkallare WHERE id = ?", (vin_id,)
    ).fetchone())
    print(f"  ✓ Vin {vin_id} uppdaterat: {uppdaterad['namn']}")
    return jsonify(uppdaterad), 200


@app.route("/api/vinkallare/<int:vin_id>", methods=["DELETE"])
def ta_bort_vin(vin_id):
    """Tar bort en drucken flaska och dess bilder."""
    db  = get_db()
    rad = db.execute(
        "SELECT bild_fram, bild_bak FROM vinkallare WHERE id = ?", (vin_id,)
    ).fetchone()
    if not rad:
        return jsonify({"fel": "Flaska hittades inte"}), 404

    # Ta bort eventuella bildfiler från disk
    for bildnamn in (rad["bild_fram"], rad["bild_bak"]):
        if bildnamn:
            stig = os.path.join(VINKALLARE_MAPP, bildnamn)
            if os.path.exists(stig):
                os.remove(stig)

    db.execute("DELETE FROM vinkallare WHERE id = ?", (vin_id,))
    db.commit()
    print(f"  ✓ Flaska {vin_id} borttagen (drucken!)")
    return "", 204


# ── START ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not os.path.exists(DB_FIL):
        print("\n  ⚠️  Databasen saknas – kör först: python tools/migrera_db.py\n")
    os.makedirs(BILD_MAPP, exist_ok=True)
    os.makedirs(VINKALLARE_MAPP, exist_ok=True)
    migrera_bild_kolumn()
    init_vinkallare_tabell()
    init_smaknot_kolumn()
    if not os.environ.get("GEMINI_API_KEY"):
        print("  ℹ️  Gemini ej konfigurerat – sätt GEMINI_API_KEY för AI-smakanalys")
    print()
    print("  ♨️  AI-Projekt – Flask + SQLite (Fas 3)")
    print("  ──────────────────────────────────────────")
    print("  Öppna:   http://localhost:5000")
    print("  API:     http://localhost:5000/api/recept")
    print("  Stoppa:  Ctrl+C")
    print()
    app.run(debug=True, port=5000)
