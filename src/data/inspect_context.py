from pathlib import Path

file_path = Path("data/raw/reddit.csv")

with file_path.open("r", encoding="utf-8") as file:
    lines = file.readlines()

problem_lines = [108, 220, 321, 453, 501]

print("===== CONTEXTE DES LIGNES PROBLEMATIQUES =====")

for number in problem_lines:
    print(f"\n\n========== AUTOUR DE LA LIGNE {number} ==========")

    start = max(1, number - 3)
    end = min(len(lines), number + 3)

    for i in range(start, end + 1):
        content = lines[i - 1].rstrip("\r\n")

        print(f"\nLigne {i}:")
        print(repr(content))
        print("Nombre de virgules :", content.count(","))
        print("Commence par guillemet :", content.startswith('"'))
        print("Termine par guillemet :", content.endswith('"'))

print("\n===== FIN DU DIAGNOSTIC =====")
