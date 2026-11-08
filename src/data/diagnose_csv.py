import csv
from pathlib import Path

file_path = Path("data/raw/reddit.csv")

with file_path.open("r", encoding="utf-8", newline="") as file:
    lines = file.readlines()

# Lignes signalées par le premier script
problem_lines = [108, 220, 321, 453, 501]

print("===== DIAGNOSTIC DES LIGNES =====")

for line_number in problem_lines:
    raw_line = lines[line_number - 1].rstrip("\r\n")

    print(f"\n--- Ligne {line_number} ---")
    print("Contenu brut :")
    print(repr(raw_line))

    print("Nombre de virgules :", raw_line.count(","))
    print("Nombre de guillemets :", raw_line.count('"'))

    try:
        parsed = next(csv.reader([raw_line]))
        print("Champs détectés par csv.reader :", len(parsed))
        print("Champs :", parsed)
    except csv.Error as error:
        print("Erreur CSV :", error)

print("\n===== FIN DU DIAGNOSTIC =====")
