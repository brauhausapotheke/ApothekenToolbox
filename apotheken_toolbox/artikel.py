from dataclasses import dataclass, field


@dataclass
class Artikel:

    # Originaldaten
    name: str
    bezeichnung: str = ""
    packung: str = ""

    # Normalisierte Daten
    normalisiert: str = ""
    normalisierte_bezeichnung: str = ""
    normalisierte_packung: str = ""

    # Zerlegte Daten für intelligentes Matching
    marke: str = ""
    darreichungsform: str = ""
    packung_groesse: int | None = None
    staerken: list = field(default_factory=list)

    # Preise
    normalpreis: float | None = None
    lieferpreis: float | None = None

    avp: str | None = None
    aep: str | None = None

    # Identifikation
    pzn: str | None = None

    quelle: str = ""
    tabelle: str = ""

    treffer: bool = False
    trefferart: str = ""
    fuzzy_score: float = 0.0

    # gefundener AVS-Artikel
    avs_name: str = ""

    kandidaten: list = field(default_factory=list)