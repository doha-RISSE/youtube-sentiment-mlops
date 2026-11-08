from pathlib import Path
from collections import Counter

file_path = Path("data/raw/reddit.csv")

with file_path.open("r", encoding="utf-8") as file:
    lines = file.readlines()

print("===== INSPECTION DU DATASET =====")
print(f"Nombre total de lignes avec en-tete : {len(lines)}")
print(f"En-tete : {lines[0].strip()}")

class_counts = Counter()
invalid_labels = []
empty_comments = []
valid_rows = 0
duplicate_comments = Counter()

for line_number, line in enumerate(lines[1:], start=2):
    line = line.rstrip("\r\n")

    if "," not in line:
        invalid_labels.append((line_number, line))
        continue

    comment, label = line.rsplit(",", 1)
    label = label.strip()

    if label not in {"-1", "0", "1"}:
        invalid_labels.append((line_number, label))
        continue

    valid_rows += 1
    class_counts[label] += 1
    duplicate_comments[comment.strip()] += 1

    if not comment.strip():
        empty_comments.append(line_number)

print("\n===== RESULTATS =====")
print(f"Lignes de donnees valides : {valid_rows}")
print(f"Repartition des classes : {dict(class_counts)}")
print(f"Labels invalides : {len(invalid_labels)}")
print(f"Commentaires vides : {len(empty_comments)}")
print(f"Commentaires dupliques : {sum(n - 1 for n in duplicate_comments.values() if n > 1)}")

if invalid_labels:
    print("\nPremieres lignes avec label invalide :")
    print(invalid_labels[:5])

if empty_comments:
    print("\nNumeros des premieres lignes vides :")
    print(empty_comments[:10])

print("\n===== FIN DE L'INSPECTION =====")
