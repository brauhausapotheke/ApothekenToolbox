import pandas as pd

from apotheken_toolbox.artikel import Artikel
from apotheken_toolbox.normalizer import normalisiere
from apotheken_toolbox.parser import parse_artikel


def _spalte(df, *namen):
    """
    Liefert den ersten vorhandenen Spaltennamen zurück.
    Dadurch werden verschiedene AVS-Exportformate unterstützt.
    """
    for name in namen:
        if name in df.columns:
            return name

    raise KeyError(
        f"Keine der erwarteten Spalten gefunden: {', '.join(namen)}"
    )


def lese_avs(csv_datei):

    print()
    print("Öffne AVS-CSV...")

    df = pd.read_csv(
        csv_datei,
        encoding="cp1252",
        sep=";",
        low_memory=False
    )

    # Unterstützt sowohl den alten Export
    # als auch den vollständigen Lagerexport

    col_bezeichnung = _spalte(df, "BEZEICH", "Bezeichnung")
    col_packung = _spalte(df, "PACKUNG", "Packungsgröße")
    col_avp = _spalte(df, "AVP")
    col_aep = _spalte(df, "AEP")
    col_pzn = _spalte(df, "PHZNR", "PhZNr")

    artikel_liste = []

    for _, zeile in df.iterrows():

        bezeichnung = str(zeile[col_bezeichnung]).strip()

        packung = ""
        if not pd.isna(zeile[col_packung]):
            packung = str(zeile[col_packung]).strip()

        kompletter_name = f"{bezeichnung} {packung}".strip()

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

                avp=zeile[col_avp],
                aep=zeile[col_aep],
                pzn=str(zeile[col_pzn]),

                quelle="AVS"
            )
        )

    print(f"{len(artikel_liste)} AVS-Artikel eingelesen.")

    return artikel_liste