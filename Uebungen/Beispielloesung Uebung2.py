# -*- coding: utf-8 -*-
"""
Created on Sat May 12 14:30:52 2018

#############################
# Übungsblatt 2
# Anpassung eines Netzmodells
#############################
"""


# Import der benötigten Module
import pandapower as pp
import os


#############################
# Vorbereitung des Netzmodells:
# Dieser Abschnitt zeigt, wie das Netzmodell vorbereitet wurde, damit es
# verschiedene Problemstellungen aufweist

# Bestimme den Pfad dieses Pythonscripts
path = os.path.dirname(os.path.realpath(__file__))
# Hänge den Namen der Pickle-Datei an den Pfad
net_path = os.path.join(path, "advanced_network.p")

# Lade das Netz aus der Pickle-Datei
net = pp.from_pickle(net_path)


# Erzeuge Überlastung durch zu große Lasten
net.load.p_kw.loc[18] = 10000
#net.load.p_kw.loc[4] = 100000

# Entferne zwei Leitungen
net.line.drop(20, inplace=True)
net.line.drop(13, inplace=True)

# Tausche Primär- und Sekundärknoten eines Transformators
net.trafo.hv_bus.loc[1] = 45
net.trafo.lv_bus.loc[1] = 41

# Speichere das vorbereitete Netz in eine Pickle-Datei
pp.to_pickle(net, os.path.join(path, "net_uebung_2.p"))
#############################



#############################
# Eigentlicher Beginn der Übung
# Aufgabe 1
# a)

# Bestimme den Pfad dieses Pythonscripts
path = os.path.dirname(os.path.realpath(__file__))
# Hänge den Namen der Pickle-Datei an den Pfad
net_path = os.path.join(path, "net_uebung_2.p")

# Lade das Netz aus der Pickle-Datei
net = pp.from_pickle(net_path)

# Führe die Diagnostik-Funktion aus
pp.diagnostic(net)

# Die Diagnose zeigt, dass zwei Netzabschnitte nicht angeschlossen sind und die
# Anschlüsse eines Transformators vertauscht wurden.


# b)

# Zur Identifikation der nicht angeschlossenen Abschnitte können die
# Knoteninformationen der Diagnostik-Funktion benutzt werden.

# Speichere das Rückgabe-Dictionary der Diagnostik-Funktion in der Variable diag
diag = pp.diagnostic(net)

# Mit dem Key "disconnected_elements" können die nicht angeschlossenen Elemente
# aus dem Dictionary ausgelesen und mit dem Index 0 oder 1 die beiden
# Abschnitte ausgewählt werden. Mit dem Key "buses" kann auf die Liste der
# nicht angeschlossenen Knoten zugegriffen werden.
disc_buses_1 = diag["disconnected_elements"][0]["buses"]
disc_buses_2 = diag["disconnected_elements"][1]["buses"]

disc_bus_names_1 = net.bus.name.loc[disc_buses_1]
disc_bus_names_2 = net.bus.name.loc[disc_buses_2]

print("Nicht angeschlossene Knoten, Abschnitt 1:")
print(disc_bus_names_1)
print()
print("Nicht angeschlossene Knoten, Abschnitt 2:")
print(disc_bus_names_2)
print()

# Durch Zuhilfenahme der Strukturdarstellung aus dem Übungsblatt können die
# Knoten "MV7" und "MV0" als Verbindungsknoten für den Abschnitt 1 und die
# Knoten "LV2.2" und "LV2.1" für den Abschnitt 2 identifiziert werden

# Knotenindizes der Knoten "MV0" und "MV7" bestimmen
bus_1_sec_1 = net.bus.index[net.bus.name == "Bus MV0"][0]
bus_2_sec_1 = net.bus.index[net.bus.name == "Bus MV7"][0]

# Knotenindizes der Knoten "LV2.1" und "LV2.2" bestimmen
bus_1_sec_2 = net.bus.index[net.bus.name == "Bus LV2.1"][0]
bus_2_sec_2 = net.bus.index[net.bus.name == "Bus LV2.2"][0]

# Zur Auswahl der Standardtypen der Wiederversorgungsleitungen können z. B. die
# benachbarten Leitungen "MV Line7" für Abschnitt 1 und "LV Line2.1" für
# Abschnitt 2 zur Orientierung benutzt werden:
print("Standardtyp 'MV Line7': %s" % net.line.std_type[net.line.name == "MV Line7"].values)
print("Standardtyp 'LV Line2.1': %s" % net.line.std_type[net.line.name == "LV Line2.1"].values)
print()

# Standardtyp "MV Line7": NA2XS2Y 1x185 RM/25 12/20 kV
# Standardtyp "LV Line2.1": NAYY 4x120 SE

# Wiederversorgungsleitungen erstellen
pp.create_line(net, bus_1_sec_1, bus_2_sec_1, length_km=1, std_type="NA2XS2Y 1x185 RM/25 12/20 kV")
pp.create_line(net, bus_1_sec_2, bus_2_sec_2, length_km=1, std_type="NAYY 4x120 SE")

# Ein weiterer durchlauf der Diagnostik-Funktion zeigt, dass nun alle
# Netzabschnitte angeschlossen sind
pp.diagnostic(net)


# c)

# Die Diagnose hat zusätzlich gezeigt, dass die Anschlussknoten des
# Transformators mit dem Index 1 vertauscht sind.

# Tausche die Anschlussknoten des Transformators mit Index 1
hv_bus, lv_bus = net.trafo.loc[1, ["hv_bus", "lv_bus"]]
net.trafo.loc[1, ["hv_bus", "lv_bus"]] = lv_bus, hv_bus

# Die Diagnostik zeigt nun keine Probleme mehr mit falsch angeschlossenen Elementen
pp.diagnostic(net)


# d)

# Nachdem nun alle Elemente richtig angeschlossen sind, zeigt die Diagnose,
# dass eine zu große Belastung eine Konvergenz des Lastfluss verhindern könnte

# Die Lasttabelle zeigt, dass die Lasten "MV Net 4" (Index 4) und "Residential
# Load(5)" (Index 18) im Vergleich zu den umliegenden Lasten sehr hohe
# Wirkleistungen "p_kw" aufweisen.
print(net.load)
print()

# Angleichen der Wirkleistungen
net.load.p_kw.loc[4] = 38000.0
net.load.p_kw.loc[18] = 10.0

# Die Diagnose zeigt nun, dass alle Probleme im Netzwerk beseitigt wurden
pp.diagnostic(net)

# Überprüfung, ob Leitungen oder Transformatoren überlastet sind:
# Lastfluss ausführen
pp.runpp(net)

# Möglichkeit 1: "loading_percent" in Tabellen überprüfen
print("Lastflussergebnisse Leitungen:")
print(net.res_line)
print()
print("Lastflussergebnisse Transformatoren:")
print(net.res_trafo)
print()

# Möglichkeit 2: Maximale Auslastungen bestimmen
print("Maximale Leitungsauslastung: ", net.res_line.loading_percent.max())
print("Maximale Transformatorauslastung: ", net.res_trafo.loading_percent.max())
print()

# Möglichkeit 3: Filter anwenden
print("Überlastete Leitungen")
print(net.res_line[net.res_line.loading_percent > 100])
print()
print("Überlastete Transformatoren")
print(net.res_trafo[net.res_trafo.loading_percent > 100])
#############################