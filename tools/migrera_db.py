"""
tools/migrera_db.py – Engångsskript som importerar data från JSON-filerna
till SQLite-databasen data/sousvide.db.

Kör från projektmappen:  python tools/migrera_db.py
"""

import json
import os
import sqlite3
import sys

# Tvinga UTF-8 i Windows-terminalen
sys.stdout.reconfigure(encoding="utf-8")

# Sökvägar relativt projektmappen
ROT        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FIL     = os.path.join(ROT, "data", "sousvide.db")
RECEPT_FIL = os.path.join(ROT, "data", "recept.json")
VINER_FIL  = os.path.join(ROT, "data", "viner.json")


def skapa_tabeller(db):
    """Skapar databastabellerna och index om de inte redan finns."""
    db.executescript("""
        CREATE TABLE IF NOT EXISTS recept (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            namn   TEXT    NOT NULL,
            kat    TEXT,
            metod  TEXT,
            temp   REAL,
            tid    TEXT,
            n      INTEGER,
            betyg  TEXT,
            omdome TEXT,
            datum  TEXT,
            hl     TEXT,
            tags   TEXT,
            eget   INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS viner (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            namn   TEXT    NOT NULL,
            typ    TEXT,
            druva  TEXT,
            land   TEXT,
            pris   TEXT,
            antal  INTEGER,
            status TEXT
        );

        -- Index för snabbare sökningar i dagboken
        CREATE INDEX IF NOT EXISTS idx_recept_kat  ON recept (kat);
        CREATE INDEX IF NOT EXISTS idx_recept_eget ON recept (eget);
    """)


def importera_recept(db):
    """Läser recept.json och skriver alla körningar till databasen."""
    with open(RECEPT_FIL, encoding="utf-8") as f:
        recept = json.load(f)

    for r in recept:
        db.execute(
            """INSERT INTO recept
               (id, namn, kat, metod, temp, tid, n, betyg, omdome, datum, hl, tags, eget)
               VALUES
               (:id,:namn,:kat,:metod,:temp,:tid,:n,:betyg,:omdome,:datum,:hl,:tags,:eget)""",
            {
                "id":     r.get("id"),
                "namn":   r["namn"],
                "kat":    r.get("kat"),
                "metod":  r.get("metod"),
                "temp":   r.get("temp"),
                "tid":    r.get("tid"),
                "n":      r.get("n"),
                "betyg":  r.get("betyg"),
                "omdome": r.get("omdome", ""),
                "datum":  r.get("datum"),
                "hl":     r.get("hl"),
                "tags":   r.get("tags", ""),
                "eget":   int(bool(r.get("eget", False))),
            },
        )
    return len(recept)


def importera_viner(db):
    """Läser viner.json och skriver alla viner till databasen."""
    with open(VINER_FIL, encoding="utf-8") as f:
        viner = json.load(f)

    for v in viner:
        db.execute(
            """INSERT INTO viner (namn, typ, druva, land, pris, antal, status)
               VALUES (:namn,:typ,:druva,:land,:pris,:antal,:status)""",
            v,
        )
    return len(viner)


if __name__ == "__main__":
    # Börja alltid om från scratch för att undvika dubbletter
    if os.path.exists(DB_FIL):
        os.remove(DB_FIL)
        print("  – Befintlig databas borttagen.")

    with sqlite3.connect(DB_FIL) as db:
        skapa_tabeller(db)
        antal_recept = importera_recept(db)
        antal_viner  = importera_viner(db)

    storlek_kb = os.path.getsize(DB_FIL) // 1024

    print()
    print("  ✓ Migrering klar!")
    print(f"  Databas:  {DB_FIL}")
    print(f"  Recept:   {antal_recept} körningar importerade")
    print(f"  Viner:    {antal_viner} viner importerade")
    print(f"  Storlek:  {storlek_kb} KB")
    print()
    print("  Starta servern: python server.py")
    print()
