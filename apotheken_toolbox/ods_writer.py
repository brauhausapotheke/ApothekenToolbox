import shutil
import ezodf


def schreibe_preise(original_datei, ziel_datei, artikel_liste):

    print("Schreibe aktualisierte ODS-Datei...")

    # Originaldatei kopieren
    shutil.copy2(original_datei, ziel_datei)

    # Kopie öffnen
    doc = ezodf.opendoc(ziel_datei)

    aktualisiert = 0

    for artikel in artikel_liste:

        if not artikel.treffer:
            continue

        if artikel.avp is None or artikel.aep is None:
            continue

        try:
            sheet = doc.sheets[artikel.blatt]

            avp = float(str(artikel.avp).replace(",", "."))
            aep = float(str(artikel.aep).replace(",", "."))

            # Spalte C = Normalpreis
            sheet[(artikel.zeile - 1, 2)].set_value(avp)

            # Spalte D = Lieferpreis
            sheet[(artikel.zeile - 1, 3)].set_value(aep)

            aktualisiert += 1

        except Exception as e:
            print(f"Fehler bei {artikel.name}: {e}")

    doc.save()

    print()
    print(f"{aktualisiert} Preise aktualisiert.")
    print(f"Datei gespeichert: {ziel_datei}")