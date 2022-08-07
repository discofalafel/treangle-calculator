import numpy as np

# gibt zuerst eine Nachricht <msg> aus (falls diese definiert ist)
# stellt anschließend eine Frage <text> und erwartet eine Eingabe
# gibt folgenden Wert zurück:
# - float-Wert der Eingabe falls eine Zahl im Bereich <dim_min> bis <dim_max>
# - np.nan falls Eingabe '-'
# fragt solange bis gültige Zahl oder '-' eingegeben wurde
def get_dim(text, msg=None, dim_min=0, dim_max=np.inf):
    # Audgabe der Nachricht
    if not msg==None:
        print(msg)
    # Eingabe der Zahl
    dim_str = input(text)
    try:
        # wandle Eingabe in float-Zahl (oder NaN falls '-')
        dim_test = np.nan if dim_str == '-' else float(dim_str)
        # Ausgabe falls Zahl im spezifizierten Bereich -> ansonsten neuer Versuch
        return dim_test if np.isnan(dim_test) or (not np.isnan(dim_test) and (dim_min < dim_test <= dim_max)) else get_dim(text, "Ungültige Zahl!")
    except:
        # Falls keine Zahl oder kein '-' -> neuer Versuch
        return get_dim(text, "Ungültige Eingabe!")

# berechnet den Radius des Inkreises eines Dreiecks
# gegeben müssen alle 3 Seiten (<a>, <b>, <c>) sein
# optional kann Fläche <A> gegeben sein.
# es wird nicht überprüft ob die Fläche stimmt!
# alle Werte sollten positiv sein
def calc_r1(a, b, c, A=np.nan):
    # Berechung des halben Umfangs
    s = (a+b+c)/2
    if np.isnan(A):
        # Wenn Fläche unbekannt -> Formal (2)
        return np.sqrt( ((s-a)*(s-b)*(s-c))/s )
    else:
        # Wenn Fläche bekannt -> Formel (1)
        return A/s

# berechnet den Radius des Inkreises eines Dreiecks
# gegeben sein müssen:
# - eine Seite <l>
# - und die beiden anliegenden Winkel <arc1> und <arc2> in Grad
# alle Werte sollten positiv sein und die Winkel kleiner 180
def calc_r2(l, arc1, arc2):
    # Formel (3)
    return l / ( (1/np.tan(np.deg2rad(arc1/2))) + (1/np.tan(np.deg2rad(arc2/2))) )

# gibt aus was das Programm macht und erwartet
print("Bestimmung Der Fläche und des Inhaltes einer Dreieckes:")
print("        +       ")
print("       / \      ")
print("      /   \     ")
print("     /     \    ")
print("  a /       \ c ")
print("   /         \  ")
print("  /           \ ")
print(" +-------------+")
print("        b          ")
print("Geben Sie die gefragten Werte ein!\n(Falls ein Wert unbekannt ist '-' eingeben)")

# Eingabe der drei Seitenlängen
a = get_dim("Länge [cm] a: ")
b = get_dim("Länge [cm] b: ")
c = get_dim("Länge [cm] c: ")

# Ermittlung der Anzahl der bekannten Seiten
cnt_nan_1 = np.sum(np.isnan([a, b, c]))
if cnt_nan_1 == 3:
    # Wenn keine Seite bekannt -> Problem nicht lösbar
    print("Nicht lösbar!\n(Mindestens eine Seite muss bekannt sein)")
elif cnt_nan_1 == 0:
    # Wenn alle Seiten bekannt -> Abfrage ob Fläche bekannt
    A = get_dim("Fläche [cm³] A: ")
    # Berechnung des Radius -> Funktionsaufruf
    r = calc_r1(a, b, c, A)
else:
    # ansonsten: Eingabe der drei Winkel
    alpha = get_dim("Winkel alpha [°] gegenüber Seite a: ", dim_max=180)
    beta  = get_dim("Winkel beta  [°] gegenüber Seite b: ", dim_max=180)
    gamma = get_dim("Winkel gamma [°] gegenüber Seite c: ", dim_max=180)
    # Ermittlung der Anzahl der bekannten Winkel
    cnt_nan_2 = np.sum(np.isnan([alpha, beta, gamma]))
    if cnt_nan_2 >= 2:
        # Wenn zwei oder mehr Winkel unbekannt -> Problem nicht lösbar
        # (zumindest nicht mit den gegebenen Formeln)
        # (unter bestimmten Bedingungen trotzdem lösbar aber hier nicht betrachtet)
        print("Nicht lösbar!\n(Mindestens zwei Winkel müssen bekannt sein!)")
    else:
        # Wenn mindestens zwei Winkel bekannt -> Funktionsaufruf
        # Es werden zunächst alle drei Optionen versucht zu berechnen
        r1 = calc_r2(a, beta, gamma)
        r2 = calc_r2(b, alpha, gamma)
        r3 = calc_r2(c, alpha, beta)
        # Auswahl des Radius welcher sich berechnen ließ
        # - r1 falls dieser nicht NaN
        # - ansonsten r2 falls dieser nicht NaN
        # - ansonsten r3 (dieser muss dann nicht NaN sein)
        r = r1 if not np.isnan(r1) else r2 if not np.isnan(r2) else r3

# Berechnung von Unfang (circ) und Fläche (area) des Inkreises 
circ = 2 * np.pi * r
area = np.pi * r**2

# Ausgabe von Umfang und Fläche des Inkreises
print("Der Umfang beträgt: " + "{:.3f}".format(circ) + "cm")
print("Die Fläche beträgt: " + "{:.3f}".format(area) + "cm³")
