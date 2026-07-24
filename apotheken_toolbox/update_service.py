from apotheken_toolbox.ods_reader import lese_tabellen
from apotheken_toolbox.avs_import import lese_avs
from apotheken_toolbox.matcher import (
    baue_index,
    finde_treffer,
    finde_kandidaten,
    fuzzy_match
)
from apotheken_toolbox.report import erstelle_trefferanalyse
from apotheken_toolbox.ods_writer import schreibe_preise

import os


def aktualisieren(ods_datei, csv_datei):

    print()
    print("========================================")
    print("ApothekenToolbox startet")
    print("----------------------------------------")
    print("ODS :", ods_datei)
    print("CSV :", csv_datei)
    print("========================================")

    ornamentum = lese_tabellen(ods_datei)

    print()
    print(f"{len(ornamentum)} Ornamentum-Artikel eingelesen.")

    avs = lese_avs(csv_datei)

    print()
    print(f"{len(avs)} AVS-Artikel eingelesen.")

    index = baue_index(avs)

    treffer_exakt = 0
    treffer_fuzzy = 0
    offen = 0

    print()
    print("Suche Treffer...")

    for artikel in ornamentum:

        # ---------------------------
        # 1. Exakter Treffer
        # ---------------------------
        avs_artikel = finde_treffer(artikel, index)

        if avs_artikel is not None:

            artikel.avp = avs_artikel.avp
            artikel.aep = avs_artikel.aep
            artikel.pzn = avs_artikel.pzn
            artikel.avs_name = avs_artikel.name

            artikel.treffer = True
            artikel.trefferart = "EXAKT"
            artikel.fuzzy_score = 100.0

            if artikel.name.startswith("Grippostad C"):
                print()
                print("========== DEBUG GRIPPOSTAD ==========")
                print("Trefferart :", "EXAKT")
                print("Ornamentum :", artikel.name)
                print("AVS        :", avs_artikel.name)
                print("AVP        :", avs_artikel.avp)
                print("AEP        :", avs_artikel.aep)
                print("======================================")
                print()

            treffer_exakt += 1
            continue

        # ---------------------------
        # 2. Fuzzy-Match
        # ---------------------------
        avs_artikel, score = fuzzy_match(artikel, avs)

        if avs_artikel is not None:

            artikel.avp = avs_artikel.avp
            artikel.aep = avs_artikel.aep
            artikel.pzn = avs_artikel.pzn
            artikel.avs_name = avs_artikel.name

            artikel.treffer = True
            artikel.trefferart = "FUZZY"
            artikel.fuzzy_score = round(score * 100, 1)

            if artikel.name.startswith("Grippostad C"):
                print()
                print("========== DEBUG GRIPPOSTAD ==========")
                print("Trefferart :", "FUZZY")
                print("Score      :", round(score * 100, 1))
                print("Ornamentum :", artikel.name)
                print("AVS        :", avs_artikel.name)
                print("AVP        :", avs_artikel.avp)
                print("AEP        :", avs_artikel.aep)
                print("======================================")
                print()

            treffer_fuzzy += 1
            continue

        # ---------------------------
        # 3. Kein Treffer
        # ---------------------------
        artikel.kandidaten = finde_kandidaten(
            artikel,
            avs,
            anzahl=3
        )

        artikel.treffer = False
        artikel.trefferart = "OFFEN"

        offen += 1

    print()
    print("========================================")
    print(f"Exakte Treffer : {treffer_exakt}")
    print(f"Fuzzy Treffer  : {treffer_fuzzy}")
    print(f"Offen          : {offen}")
    print("========================================")

    print()
    print("Erstelle Trefferanalyse...")
    erstelle_trefferanalyse(ornamentum)

    print()

    # ---------------------------
    # Aktualisierte ODS schreiben
    # ---------------------------
    basis, ext = os.path.splitext(ods_datei)
    ziel_datei = basis + "_aktualisiert" + ext

    schreibe_preise(
        ods_datei,
        ziel_datei,
        ornamentum
    )

    print()
    print("Fertig.")