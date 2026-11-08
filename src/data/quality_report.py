import csv
from collections import Counter, defaultdict
from pathlib import Path

file_path = Path("data/raw/reddit.csv")

records = []

with file_path.open("r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        records.append({
            "comment": row["clean_comment"].strip(),
            "label": row["category"].strip()
        })

print("===== QUALITE DETAILLEE DU DATASET =====")

# 1. Commentaires vides
empty_records = [r for r in records if not r["comment"]]

# 2. Commentaires non vides
non_empty = [r for r in records if r["comment"]]

# 3. Répartition des classes après exclusion des commentaires vides
class_counts = Counter(r["label"] for r in non_empty)

# 4. Fréquence des commentaires identiques
comment_counts = Counter(r["comment"] for r in non_empty)

duplicate_groups = {
    comment: count
    for comment, count in comment_counts.items()
    if count > 1
}

duplicate_excess = sum(count - 1 for count in duplicate_groups.values())

# 5. Vérifier les commentaires identiques avec plusieurs labels
comment_labels = defaultdict(set)

for record in non_empty:
    comment_labels[record["comment"]].add(record["label"])

conflicting_duplicates = {
    comment: labels
    for comment, labels in comment_labels.items()
    if len(labels) > 1
}

print("Nombre total d'enregistrements :", len(records))
print("Commentaires vides :", len(empty_records))
print("Commentaires non vides :", len(non_empty))

print("\n===== REPARTITION APRES EXCLUSION DES VIDES =====")
for label in ["-1", "0", "1"]:
    count = class_counts[label]
    percentage = count / len(non_empty) * 100
    print(f"Classe {label} : {count} ({percentage:.2f} %)")

print("\n===== DOUBLONS =====")
print("Groupes de commentaires dupliques :", len(duplicate_groups))
print("Nombre de lignes dupliquees en exces :", duplicate_excess)
print("Commentaires identiques avec labels differents :", len(conflicting_duplicates))

print("\n===== EXEMPLES DE DOUBLONS CONTRADICTOIRES =====")
for comment, labels in list(conflicting_duplicates.items())[:5]:
    print("Commentaire :", comment[:150])
    print("Labels :", sorted(labels))
    print("---")

print("\n===== FIN =====")
