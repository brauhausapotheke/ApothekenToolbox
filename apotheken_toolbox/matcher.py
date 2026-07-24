from difflib import SequenceMatcher


IGNORIERTE_WOERTER = {
    "BIO",
    "DER",
    "DIE",
    "DAS",
    "DEN",
    "DEM",
    "DES",
    "UND",
    "MIT",
    "OHNE",
    "FUER",
    "IN",
    "VON",
    "ZU",
    "ZUM",
    "ZUR",
    "IM",
    "AM",
}


def baue_index(avs_artikel):

    index = {}

    for artikel in avs_artikel:
        index[artikel.normalisiert] = artikel

    print()
    print(f"Index erstellt: {len(index)} Einträge")

    return index


def finde_treffer(ornamentum_artikel, index):

    return index.get(ornamentum_artikel.normalisiert)


def ermittle_suchwort(text):

    woerter = text.split()

    for wort in woerter:

        if len(wort) <= 2:
            continue

        if wort in IGNORIERTE_WOERTER:
            continue

        return wort

    if woerter:
        return woerter[0]

    return ""


def finde_kandidaten(ornamentum_artikel, avs_artikel, anzahl=10):

    suchwort = ermittle_suchwort(
        ornamentum_artikel.normalisierte_bezeichnung
    )

    kandidaten = []

    for avs in avs_artikel:

        if suchwort and suchwort not in avs.normalisierte_bezeichnung:
            continue

        score = SequenceMatcher(
            None,
            ornamentum_artikel.normalisiert,
            avs.normalisiert
        ).ratio()

        kandidaten.append((score, avs))

    kandidaten.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return kandidaten[:anzahl]


def fuzzy_match(ornamentum_artikel, avs_artikel):

    kandidaten = finde_kandidaten(
        ornamentum_artikel,
        avs_artikel,
        anzahl=10
    )

    if not kandidaten:
        return None, 0.0

    # 1. Bester SequenceMatcher wie bisher
    bester_score, bester_kandidat = kandidaten[0]

    # 2. Versuche einen fachlich besseren Kandidaten zu finden
    for score, kandidat in kandidaten:

        if score < 0.80:
            continue

        gleiche_marke = (
            ornamentum_artikel.marke
            and kandidat.marke
            and ornamentum_artikel.marke == kandidat.marke
        )

        gleiche_packung = (
            ornamentum_artikel.packung_groesse
            and kandidat.packung_groesse
            and ornamentum_artikel.packung_groesse == kandidat.packung_groesse
        )

        if gleiche_marke and gleiche_packung:
            return kandidat, score

    # 3. Altes Verhalten beibehalten
    if bester_score >= 0.92:
        return bester_kandidat, bester_score

    if bester_score >= 0.80:

        if ornamentum_artikel.normalisierte_packung:

            if ornamentum_artikel.normalisierte_packung in bester_kandidat.normalisiert:
                return bester_kandidat, bester_score

    return None, bester_score