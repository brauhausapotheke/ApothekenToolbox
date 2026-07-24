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

    for wort in woerter:

        if wort in DARREICHUNGSFORMEN:
            form = wort

        if re.fullmatch(r"\d+", wort):
            zahl = int(wort)

            if zahl <= 200:
                packung = zahl

        if re.fullmatch(r"\d+MG", wort):
            staerken.append(int(wort[:-2]))

        if re.fullmatch(r"\d+MCG", wort):
            staerken.append(int(wort[:-3]))

    return {
        "marke": marke,
        "form": form,
        "packung": packung,
        "staerken": staerken
    }