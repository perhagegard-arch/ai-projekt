"""
tools/migrera_sousvide.py – Konverterar data/recept.json till
data/sousvide_import.json, redo att importeras i sousvide-dagbok.html.

Kör från projektmappen: python tools/migrera_sousvide.py
"""

import json
import os
import random
import string
import sys
import time
from datetime import date

sys.stdout.reconfigure(encoding="utf-8")

ROT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KALLA = os.path.join(ROT, "data", "recept.json")
MAL   = os.path.join(ROT, "data", "sousvide_import.json")

# Basid ökas med index för att garantera unika strängar
_BASE_TS = int(time.time() * 1000)


def ny_id(index: int) -> str:
    """Genererar ett unikt ID i samma format som nyId() i JavaScript."""
    t = _BASE_TS + index
    charset = "0123456789abcdefghijklmnopqrstuvwxyz"
    b36 = ""
    while t:
        b36 = charset[t % 36] + b36
        t //= 36
    rnd = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return b36 + rnd


def konvertera(post: dict, index: int) -> dict:
    return {
        "id":     ny_id(index),
        "namn":   post.get("namn", ""),
        "kat":    post.get("kat"),
        "metod":  post.get("metod"),
        "temp":   post.get("temp"),
        "tid":    post.get("tid"),
        "n":      post.get("n", 0),
        "betyg":  post.get("betyg"),
        "omdome": post.get("omdome", ""),
        "datum":  post.get("datum"),
        "hl":     post.get("hl"),
        "tags":   post.get("tags", ""),
        "eget":   False,   # false = migrerat, true = lagt till i appen
        "bild":   None,
    }


if __name__ == "__main__":
    if not os.path.exists(KALLA):
        print(f"  ✗ Hittar inte källfilen: {KALLA}")
        sys.exit(1)

    with open(KALLA, encoding="utf-8") as f:
        recept = json.load(f)

    koningar = [konvertera(r, i) for i, r in enumerate(recept)]

    payload = {
        "version":     1,
        "exportdatum": date.today().isoformat(),
        "koningar":    koningar,
    }

    with open(MAL, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print()
    print(f"  ✓ Klart! {len(koningar)} körningar exporterade.")
    print(f"  Fil:    {MAL}")
    print()
    print("  Importera i sousvide-dagbok.html via knappen '↑ Importera'.")
    print()
