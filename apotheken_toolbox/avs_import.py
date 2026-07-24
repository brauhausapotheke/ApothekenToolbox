import pandas as pd

from apotheken_toolbox.artikel import Artikel
from apotheken_toolbox.normalizer import normalisiere
from apotheken_toolbox.parser import parse_artikel


def lese_avs(csv_datei):

    print()
    print("Öffne AVS-CSV...")

    df = pd.read_csv(
        csv_datei,
        encoding="cp1252",
        sep=";",
        low_memory=False
    )

    artikel_liste = []

    for _, zeile in df.iterrows():

        bezeichnung = str(zeile["BEZEICH"]).strip()
        packung = str(zeile["PACKUNG"]).strip()

        kompletter_name = f"{bezeichnung} {packung}"
        normalisiert = normalisiere(kompletter_name)

        parsergebnis = parse_artikel(normalisiert)

        artikel_liste.append(
            Artikel(
                name=kompletter_name,
                bezeichnung=bezeichnung,
                packung=packung,

                normalisiert=normalisiert,
                normalisierte_bezeichnung=normalisiere(bezeichnung),
                normalisierte_packung=normalisiere(packung),

                marke=parsergebnis["marke"],
                darreichungsform=parsergebnis["form"],
                packung_groesse=parsergebnis["packung"],
                staerken=parsergebnis["staerken"],

                avp=zeile["AVP"],
                aep=zeile["AEP"],
                pzn=str(zeile["PHZNR"]),
                quelle="AVS"
            )
        )

    print(f"{len(artikel_liste)} AVS-Artikel eingelesen.")

    print()
    print("Erste 5 AVS-Artikel:")

    for artikel in artikel_liste[:5]:
        print(artikel)

    return artikel_liste