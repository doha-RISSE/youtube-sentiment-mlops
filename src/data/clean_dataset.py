import csv
from collections import Counter
from pathlib import Path

input_path = Path("data/raw/reddit.csv")
output_path = Path("data/processed/reddit_clean.csv")

valid_labels = {"-1", "0", "1"}
invalid_comment_values = {"nan"}

clean_records = []
seen_comments = set()

empty_removed = 0
placeholder_removed = 0
duplicates_removed = 0
invalid_records = 0

with input_path.open("r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        comment = row["clean_comment"].strip()
        label = row["category"].strip()

        if label not in valid_labels:
            invalid_records += 1
            continue

        if not comment:
            empty_removed += 1
            continue

        if comment.casefold() in invalid_comment_values:
            placeholder_removed += 1
            continue

        if comment in seen_comments:
            duplicates_removed += 1
            continue

        seen_comments.add(comment)

        clean_records.append({
            "clean_comment": comment,
            "category": label
        })

if invalid_records:
    raise ValueError(
        f"Nettoyage interrompu : {invalid_records} labels invalides."
    )

with output_path.open("w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["clean_comment", "category"]
    )
    writer.writeheader()
    writer.writerows(clean_records)

class_counts = Counter(
    record["category"] for record in clean_records
)

print("===== RAPPORT DE NETTOYAGE =====")
print("Enregistrements initiaux : 37249")
print("Commentaires vides supprimes :", empty_removed)
print("Valeurs placeholder supprimees :", placeholder_removed)
print("Doublons supprimes :", duplicates_removed)
print("Labels invalides :", invalid_records)
print("Nombre final de commentaires :", len(clean_records))

print("\n===== REPARTITION FINALE =====")

for label in ["-1", "0", "1"]:
    count = class_counts[label]
    percentage = count / len(clean_records) * 100
    print(f"Classe {label} : {count} ({percentage:.2f} %)")

print("\nFichier cree :", output_path.exists())
print("NETTOYAGE TERMINE")
