import re


DARREICHUNGSFORMEN = {
    "TBL",
    "FTBL",
    "KPS",
    "HKPS",
    "WKPS",
    "PAS",
    "SPR",
    "SLB",
    "CR",
    "GEL",
    "SIR",
    "PLV",
    "BTL",
}


def parse_artikel(text):

    if not text:
        return {
            "marke": "",
            "form": "",
            "packung": None,
            "staerken": []
        }

    woerter = text.split()

    marke = woerter[0]

    form = ""
    packung = None
    staerken = []

    i = 0

    while i < len(woerter):

        wort = woerter[i]

        # Darreichungsform
        if wort in DARREICHUNGSFORMEN:
            form = wort

        # Zahlen + Einheiten (400 MG, 0,5 MG, 1000 IE ...)
        if re.fullmatch(r"\d+(?:[.,]\d+)?", wort):

            wert = float(wort.replace(",", "."))

            if i + 1 < len(woerter):

                einheit = woerter[i + 1]

                if einheit in {
                    "MG",
                    "MCG",
                    "G",
                    "ML",
                    "IE"
                }:
                    staerken.append((wert, einheit))
                    i += 2
                    continue

            # Packungsgröße (nur wenn keine Stärke)
            if wert.is_integer():

                zahl = int(wert)

                if 1 <= zahl <= 200:
                    packung = zahl

        i += 1

    return {
        "marke": marke,
        "form": form,
        "packung": packung,
        "staerken": staerken
    }