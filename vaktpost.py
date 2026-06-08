"""
vaktpost.py – Simulerad backend-arbetare som bevakar Systembolaget
och skriver aktuell vinstatus till vin-status.json.
"""

import json
import os
import sys
from datetime import datetime

# Tvinga UTF-8 på stdout så att grafiska tecken fungerar i Windows-terminalen
sys.stdout.reconfigure(encoding="utf-8")

# Sökvägar till in- och utdatafilerna
ROT       = os.path.dirname(os.path.abspath(__file__))
VINER_FIL = os.path.join(ROT, "data", "viner.json")
UTDATA    = os.path.join(ROT, "vin-status.json")
JS_UTDATA = os.path.join(ROT, "vin-data.js")

# Butikens namn och plats
BUTIK = "Systembolaget Djurgården, Linköping"


def ladda_viner():
    """Läser vinlistan från data/viner.json – redigera den filen för att ändra sortimentet."""
    with open(VINER_FIL, encoding="utf-8") as f:
        return json.load(f)


# Hårdkodad lista används inte längre – kvar som referens vid behov
_VINER_EXEMPEL = [
    {
        "namn":   "Château Solstice Réserve 2019",
        "typ":    "Rött vin",
        "druva":  "Cabernet Sauvignon, Petit Verdot",
        "land":   "Frankrike – Bordeaux",
        "pris":   "349 kr",
        "antal":  3,
        "status": "I lager",
    },
    {
        "namn":   "Côte-Rôtie Les Grandes Places 2019",
        "typ":    "Rött vin",
        "druva":  "Syrah",
        "land":   "Frankrike – Norra Rhône",
        "pris":   "589 kr",
        "antal":  1,
        "status": "Sista flaskorna",
    },
    {
        "namn":   "Barolo del Vecchio Maestro 2018",
        "typ":    "Rött vin",
        "druva":  "Nebbiolo",
        "land":   "Italien – Piemonte",
        "pris":   "495 kr",
        "antal":  2,
        "status": "Sista flaskorna",
    },
    {
        "namn":   "Amarone della Valpolicella Classico 2017",
        "typ":    "Rött vin",
        "druva":  "Corvina, Rondinella, Molinara",
        "land":   "Italien – Veneto",
        "pris":   "649 kr",
        "antal":  1,
        "status": "Sista flaskorna",
    },
    {
        "namn":   "Priorat Camí Pessebre 2018",
        "typ":    "Rött vin",
        "druva":  "Garnacha, Cariñena",
        "land":   "Spanien – Priorat",
        "pris":   "445 kr",
        "antal":  4,
        "status": "Begränsat antal",
    },
    {
        "namn":   "Quinta da Pedra Negra Reserva 2020",
        "typ":    "Rött vin",
        "druva":  "Touriga Nacional, Tinta Roriz",
        "land":   "Portugal – Douro",
        "pris":   "265 kr",
        "antal":  6,
        "status": "I lager",
    },
    {
        "namn":   "Penfolds Bin 389 Cabernet Shiraz 2020",
        "typ":    "Rött vin",
        "druva":  "Cabernet Sauvignon, Shiraz",
        "land":   "Australien – South Australia",
        "pris":   "379 kr",
        "antal":  5,
        "status": "I lager",
    },
    {
        "namn":   "Domaine de la Lune Noire 2021",
        "typ":    "Vitt vin",
        "druva":  "Chardonnay",
        "land":   "Frankrike – Bourgogne",
        "pris":   "289 kr",
        "antal":  5,
        "status": "I lager",
    },
    {
        "namn":   "Chablis Premier Cru Montée de Tonnerre 2022",
        "typ":    "Vitt vin",
        "druva":  "Chardonnay",
        "land":   "Frankrike – Chablis",
        "pris":   "319 kr",
        "antal":  3,
        "status": "Begränsat antal",
    },
    {
        "namn":   "Sancerre La Croix du Roy 2022",
        "typ":    "Vitt vin",
        "druva":  "Sauvignon Blanc",
        "land":   "Frankrike – Loire",
        "pris":   "259 kr",
        "antal":  7,
        "status": "I lager",
    },
    {
        "namn":   "Grüner Veltliner Smaragd Stein am Rain 2022",
        "typ":    "Vitt vin",
        "druva":  "Grüner Veltliner",
        "land":   "Österrike – Wachau",
        "pris":   "229 kr",
        "antal":  4,
        "status": "I lager",
    },
    {
        "namn":   "Weingut Wieninger Nussberg Grande Reserve 2021",
        "typ":    "Vitt vin",
        "druva":  "Grüner Veltliner, Riesling",
        "land":   "Österrike – Wien",
        "pris":   "209 kr",
        "antal":  8,
        "status": "I lager",
    },
]


def bygg_status():
    """Bygger det fullständiga statusobjektet som ska sparas i JSON-filen."""
    viner = ladda_viner()
    return {
        "kord_av":       "vaktpost.py",
        "butik":         BUTIK,
        "uppdaterad":    datetime.now().isoformat(timespec="seconds"),
        "uppdaterad_sv": datetime.now().strftime("%d %B %Y kl. %H:%M:%S"),
        "antal_viner":   len(viner),
        "viner":         viner,
    }


def spara_json(data):
    """Skriver data till vin-status.json med UTF-8-kodning och snygg formattering."""
    with open(UTDATA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def skriv_js_fil(data):
    """Skriver vindata som window.VIN_STATUS i en JS-fil som sousvide.html laddar in direkt."""
    innehall = (
        "// Autogenererad av vaktpost.py – redigera inte manuellt\n"
        f"window.VIN_STATUS = {json.dumps(data, ensure_ascii=False, indent=2)};\n"
    )
    with open(JS_UTDATA, "w", encoding="utf-8") as f:
        f.write(innehall)


def skriv_ut_rapport(data):
    """Skriver ett snyggt terminalmeddelande när jobbet är klart."""
    bred = 58
    linje = "─" * bred

    print()
    print(f"  ┌{linje}┐")
    print(f"  │{'VAKTPOST – RAPPORT':^{bred}}│")
    print(f"  ├{linje}┤")
    print(f"  │  {'Butik:':<14}{data['butik']:<{bred - 16}}│")
    print(f"  │  {'Uppdaterad:':<14}{data['uppdaterad_sv']:<{bred - 16}}│")
    print(f"  │  {'Viner hittade:':<14}{data['antal_viner']} st{'':<{bred - 19}}│")
    print(f"  ├{linje}┤")

    # Skriv ut varje vin i rapporten
    for i, vin in enumerate(data["viner"], start=1):
        statusrad = f"  [{vin['status']}]  {vin['antal']} fl.  {vin['pris']}"
        print(f"  │  {i}. {vin['namn']:<{bred - 6}}│")
        print(f"  │     {vin['druva']} – {vin['land']:<{bred - 7 - len(vin['druva'])}}│")
        print(f"  │     {statusrad:<{bred - 5}}│")
        if i < data["antal_viner"]:
            print(f"  │{'':^{bred}}│")

    print(f"  ├{linje}┤")
    print(f"  │  ✓ vin-status.json uppdaterad{'':<{bred - 32}}│")
    print(f"  │  ✓ vin-data.js genererad{'':<{bred - 26}}│")
    print(f"  └{linje}┘")
    print()


if __name__ == "__main__":
    status = bygg_status()
    spara_json(status)
    skriv_js_fil(status)   # Genererar JS-filen som webbsidan läser in
    skriv_ut_rapport(status)
