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
    "GEL": "GEL",
    "SIRUP": "SIR",
    "ERKAELTUNGSSAFT": "ERKAELT SIR",
    "HEISSGETRAENK": "HEISSGETR",
    "PULVER": "PLV",

    # Verpackung
    "STUECK": "ST",
    "STK": "ST",
    "BEUTEL": "BTL",

    # Schreibweisen
    "FUER": "",
}

IGNORIEREN = {

    # Geschmacksrichtungen
    "CLASSIC",
    "CLASSIK",
    "KLASSIK",
    "LEMON",
    "ZITRONE",
    "HONIG",
    "ORANGE",
    "KIRSCHE",
    "KIRSCH",
    "WALDBEER",
    "WALDBEERE",
    "MINZE",
    "MENTHOL",

    # Werbetexte
    "GEGEN",
    "FUER",
    "ZUR",
    "ZUM",
    "MIT",
    "OHNE",
    "GEEIGNET",
    "ERWACHSENE",
    "ERWACHSENER",
    "ERWACHSENEN",
    "KINDER",
    "KIND",
    "BABY",
    "BABIES",

    # Varianten
    "ODER",

    # Marketing
    "SONNENBRAND",
    "INSEKTENSTICHE",
    "INSEKTENSTICH",
    "JUCKREIZ",
    "SCHWELLUNG",
    "SCHWELLUNGEN",

    # Geräte
    "IPHONE",
    "ANDROID",
    "USB",
    "LIGHTNING",

    # Zuckerfrei
    "ZUCKERFREI",
    "ZUCKERFR",
    "ZUFR",
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

    # Klammerinhalte entfernen
    text = re.sub(r"\(.*?\)", " ", text)

    # Satzzeichen vereinheitlichen
    text = re.sub(r"[,:;.+/()\-]", " ", text)

    # Einheiten trennen
    text = re.sub(r"(\d)(MG|MCG|ML|G|KG|L|IE)", r"\1 \2", text)

    # Mehrfachleerzeichen
    text = re.sub(r"\s+", " ", text).strip()

    # Synonyme
    for alt, neu in ERSETZUNGEN.items():
        text = re.sub(rf"\b{re.escape(alt)}\b", neu, text)

    # Zu ignorierende Wörter entfernen
    for wort in IGNORIEREN:
        text = re.sub(rf"\b{re.escape(wort)}\b", " ", text)

    # Mehrfachleerzeichen erneut bereinigen
    text = re.sub(r"\s+", " ", text).strip()

    return text