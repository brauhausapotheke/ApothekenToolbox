import re

ERSETZUNGEN = {

    # -------------------------
    # Darreichungsformen
    # -------------------------

    "TABLETTEN": "TBL",
    "TABLETTE": "TBL",
    "TABS": "TBL",

    "FILMTABLETTEN": "FTBL",
    "FILMTABLETTE": "FTBL",
    "FILMTBL": "FTBL",

    "KAPSELN": "KPS",
    "KAPSEL": "KPS",

    "WEICHKAPSELN": "WKPS",
    "WEICHKAPSEL": "WKPS",

    "HARTKAPSELN": "HKPS",
    "HARTKAPSEL": "HKPS",

    "LUTSCHTABLETTEN": "PAS",
    "LUTSCHTABLETTE": "PAS",

    "PASTILLEN": "PAS",
    "PASTILLE": "PAS",

    "SPRAY": "SPR",
    "SALBE": "SLB",
    "CREME": "CR",
    "SIRUP": "SIR",
    "ERKAELTUNGSSAFT": "ERKAELT SIR",
    "HEISSGETRAENK": "HEISSGETR",
    "PULVER": "PLV",

    # -------------------------
    # Verpackung
    # -------------------------

    "STUECK": "ST",
    "BEUTEL": "BTL",

    # -------------------------
    # Füllwörter
    # -------------------------

    "FUER": "",
}

# Diese Wörter unterscheiden Varianten,
# sind aber für den Produktabgleich meist nicht entscheidend.
# Wir entfernen sie komplett.
IGNORIEREN = {
    "CLASSIC",
    "KLASSIK",
    "CLASSIK",

    "ZITRONE",
    "LEMON",

    "HONIG",
    "ORANGE",
    "KIRSCHE",
    "KIRSCH",
    "WALDBEER",
    "WALDBEERE",

    "ZUCKERFREI",
    "ZUCKERFR",
    "ZUFR",

    "MINZE",
    "MENTHOL",
}


def normalisiere(text):

    if text is None:
        return ""

    text = str(text).upper()

    # Umlaute
    text = (
        text.replace("Ä", "AE")
            .replace("Ö", "OE")
            .replace("Ü", "UE")
            .replace("ß", "SS")
    )

    # Klammern entfernen
    text = re.sub(r"\(.*?\)", " ", text)

    # Satzzeichen vereinheitlichen
    text = re.sub(r"[,:;.+/()-]", " ", text)

    # Einheiten trennen
    text = re.sub(r"(\d)ML", r"\1 ML", text)
    text = re.sub(r"(\d)MG", r"\1 MG", text)
    text = re.sub(r"(\d)MCG", r"\1 MCG", text)
    text = re.sub(r"(\d)G", r"\1 G", text)

    text = re.sub(r"\s+", " ", text).strip()

    # Synonyme ersetzen
    for alt, neu in ERSETZUNGEN.items():
        text = re.sub(rf"\b{re.escape(alt)}\b", neu, text)

    # Irrelevante Begriffe entfernen
    for wort in IGNORIEREN:
        text = re.sub(rf"\b{re.escape(wort)}\b", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text