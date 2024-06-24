import random
import os
randomauslassen = 5

# Funktion zur Auswahl eines zufälligen Gerichts aus vergangenen Infos
def wähle(vergangene_info):
    # Bestimmen Sie die Wahrscheinlichkeit für jedes vergangene Info
    wahrscheinlichkeiten = {info: random.uniform(0, 1) for info in vergangene_info}
    
    if wahrscheinlichkeiten:
        # Wählen Sie das Info mit der höchsten Wahrscheinlichkeit
        gewähltes_info = max(wahrscheinlichkeiten, key=wahrscheinlichkeiten.get)
        # Überprüfen, ob das gewählte Info in den letzten 10 Tagen ausgewählt wurde
        if gewähltes_info in vergangene_info[-randomauslassen:]: 
            gewähltes_info = "Das ausgewählte Gericht wurde in den letzten 10 Tagen nicht gespielt."
    else:
        gewähltes_info = "Es liegen keine vergangenen Info vor."
    
    return gewähltes_info

# Funktion zum Lesen vergangener Infos aus einer Datei
def lese_vergangene(dateipfad):
    vergangene_info = []
    
    if os.path.exists(dateipfad):
        # Datei existiert, lese Inhalte
        with open(dateipfad, 'r') as file:
            for line in file:
                vergangene_info.append(line.strip())
                
            # Wenn weniger als 15 Einträge vorhanden sind, fordere Benutzer zur Eingabe auf
            if len(vergangene_info) < randomauslassen + 5:
                print("Es liegen nicht genügend vergangene Info vor. Bitte geben Sie ein, was Sie in den letzten Tagen gegessen haben.")
                vergangene_info = eingabe_vergangene()
                speichere_vergangene(vergangene_info, dateipfad)
    else:
        # Datei existiert nicht, fordere Benutzer zur Eingabe auf
        print("Es liegen keine vergangenen Info vor. Bitte geben Sie ein, was Sie in den letzten Tagen gegessen haben.")
        vergangene_info = eingabe_vergangene()
        speichere_vergangene(vergangene_info, dateipfad)
        
    return vergangene_info

# Funktion zum Speichern vergangener Infos in eine Datei
def speichere_vergangene(vergangene_info, dateipfad):
    with open(dateipfad, 'w') as file:
        for info in vergangene_info:
            file.write(info + '\n')

# Funktion zur Eingabe vergangener Infos durch den Benutzer
def eingabe_vergangene():
    vergangene_info = []
    print("Gib ein Gericht ein, das du in den letzten Tagen gegessen hast, zuerst das was am längsten her ist")
    print("Man kann es auch in der Text Datei bearbeiten, eine Zeille ein Gericht.")
    print(f"(Enter zum Bestätigen oder zum Beenden) bitte mindestens {randomauslassen + 5} eingeben! Desto mehr desto zufälliger!")
    print("Als erstes was am längsten her ist.")
    
    while len(vergangene_info) < randomauslassen + 5:
        # Fordere den Benutzer auf, Gerichte einzugeben
        info = input(f"({len(vergangene_info) + 1} > {randomauslassen + 5}): ")
        if info:
            vergangene_info.append(info)
        else:
            print(f"Bitte mindestens {randomauslassen + 5} Eingaben machen.")
    
    return vergangene_info

# Dateipfad für vergangene Infos
dateipfad = 'vergangene_info.txt'
# Lese vergangene Infos aus der Datei
vergangene_info = lese_vergangene(dateipfad)

# Wähle ein zufälliges Gericht aus vergangenen Infos
heutiges_info = wähle(vergangene_info)
# Wiederhole die Auswahl, falls das gewählte Gericht in den letzten 10 Tagen ausgewählt wurde
while heutiges_info == "Das ausgewählte Gericht wurde in den letzten 10 Tagen nicht gespielt.":
    heutiges_info = wähle(vergangene_info)

# Zeige das heutige Gericht an
print("Heutiges Gericht:", heutiges_info)

if heutiges_info != "Es liegen keine vergangenen Info vor.":
    # Füge das heutige Gericht zu den vergangenen Infos hinzu
    vergangene_info.append(heutiges_info)
    # Speichere die aktualisierten vergangenen Infos in der Datei
    speichere_vergangene(vergangene_info, dateipfad)

if heutiges_info == "Es liegen keine vergangenen Info vor.":
    # Fordere den Benutzer zur Eingabe neuer vergangener Infos auf
    vergangene_info = eingabe_vergangene()
    # Speichere die neuen vergangenen Infos in der Datei
    speichere_vergangene(vergangene_info, dateipfad)
