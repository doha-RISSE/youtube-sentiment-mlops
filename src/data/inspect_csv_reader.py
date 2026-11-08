import csv
from collections import Counter
from pathlib import Path

file_path = Path("data/raw/reddit.csv")

rows = []

with file_path.open("r", encoding="utf-8", newline="") as file:
    reader = csv.reader(file)

    header = next(reader)

    for row in reader:
        rows.append(row)

print("===== INSPECTION CSV AVEC CSV.READER =====")
print("Colonnes :", header)
print("Nombre d'enregistrements :", len(rows))

column_counts = Counter(len(row) for row in rows)

print("\nNombre de champs par enregistrement :")
print(dict(column_counts))

valid_rows = [row for row in rows if len(row) == 2]

class_counts = Counter()
invalid_labels = []
empty_comments = []

for index, row in enumerate(valid_rows, start=1):
    comment, label = row
    label = label.strip()

    if label not in {"-1", "0", "1"}:
        invalid_labels.append((index, label))
        continue

    class_counts[label] += 1

    if not comment.strip():
        empty_comments.append(index)

print("\n===== QUALITE DES DONNEES =====")
print("Enregistrements avec exactement 2 champs :", len(valid_rows))
print("Répartition des classes :", dict(class_counts))
print("Labels invalides :", len(invalid_labels))
print("Commentaires vides :", len(empty_comments))

print("\nPremiers enregistrements :")
for row in rows[:3]:
    print(repr(row))

print("\n===== FIN =====")
