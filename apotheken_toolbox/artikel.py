from dataclasses import dataclass, field


@dataclass
class Artikel:

    # Originaldaten
    name: str
    bezeichnung: str = ""
    packung: str = ""

    # Position in der Originaldatei
    blatt: str = ""
    zeile: int = 0

    # Originalwerte Ornamentum
    normalpreis: float | None = None
    lieferpreis: float | None = None

    # Normalisierte Daten
    normalisiert: str = ""
    normalisierte_bezeichnung: str = ""
    normalisierte_packung: str = ""

    # Parser
    marke: str = ""
    darreichungsform: str = ""
    packung_groesse: int | None = None
    staerken: list = field(default_factory=list)

    # AVS
    avp: str | None = None
    aep: str | None = None
    pzn: str | None = None

    quelle: str = ""
    tabelle: str = ""

    # Matcher
    treffer: bool = False
    trefferart: str = ""
    fuzzy_score: float = 0.0
    avs_name: str = ""

    kandidaten: list = field(default_factory=list)