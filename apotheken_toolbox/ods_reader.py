import pandas as pd

from apotheken_toolbox.artikel import Artikel
from apotheken_toolbox.normalizer import normalisiere
from apotheken_toolbox.parser import parse_artikel


def lese_tabellen(ods_datei):

    print("Öffne ODS-Datei...", flush=True)

    artikel_liste = []

    excel = pd.ExcelFile(ods_datei, engine="odf")

    relevante_tabellen = [
        "Aktuell",
        "Kosmetik",
        "Maniküre,_Pediküre",
        "Nahrungsergänzung",
        "Lagersortiment_gesamt"
    ]

    for tabelle in relevante_tabellen:

        print(f"Lese Tabelle: {tabelle}")

        df = pd.read_excel(
            ods_datei,
            sheet_name=tabelle,
            engine="odf"
        )

        for _, zeile in df.iterrows():

            artikelname = zeile.iloc[1]

            if pd.isna(artikelname):
                continue

            artikelname = str(artikelname).strip()

            normalisiert = normalisiere(artikelname)
            parsergebnis = parse_artikel(normalisiert)

            artikel_liste.append(
                Artikel(
                    name=artikelname,
                    bezeichnung=artikelname,
                    packung="",

                    normalisiert=normalisiert,
                    normalisierte_bezeichnung=normalisiert,
                    normalisierte_packung="",

                    marke=parsergebnis["marke"],
                    darreichungsform=parsergebnis["form"],
                    packung_groesse=parsergebnis["packung"],
                    staerken=parsergebnis["staerken"],

                    normalpreis=zeile.iloc[2],
                    lieferpreis=zeile.iloc[3],

                    quelle="Ornamentum",
                    tabelle=tabelle
                )
            )

    print()
    print(f"Insgesamt {len(artikel_liste)} Artikel eingelesen.")

    return artikel_liste