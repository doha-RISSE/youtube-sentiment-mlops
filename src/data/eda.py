import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Chemins
input_path = Path("data/processed/reddit_clean.csv")
output_path = Path("data/processed/class_distribution.png")

# Charger le dataset nettoyé
df = pd.read_csv(input_path, dtype={"category": str})

print("===== 1. INFORMATIONS GENERALES =====")
print("Dimensions :", df.shape)
print("\nColonnes :")
print(df.columns.tolist())
print("\nTypes de donnees :")
print(df.dtypes)

print("\n===== 2. VALEURS MANQUANTES =====")
print(df.isnull().sum())

print("\n===== 3. REPARTITION DES SENTIMENTS =====")
counts = df["category"].value_counts().reindex(["-1", "0", "1"], fill_value=0)
percentages = df["category"].value_counts(normalize=True).reindex(
    ["-1", "0", "1"], fill_value=0
) * 100

for label in ["-1", "0", "1"]:
    print(
        f"Classe {label} : "
        f"{counts[label]} commentaires "
        f"({percentages[label]:.2f} %)"
    )

print("\n===== 4. LONGUEUR DES COMMENTAIRES =====")

df["character_count"] = df["clean_comment"].str.len()
df["word_count"] = df["clean_comment"].str.split().str.len()

print("\nStatistiques du nombre de caracteres :")
print(df["character_count"].describe().round(2))

print("\nStatistiques du nombre de mots :")
print(df["word_count"].describe().round(2))

print("\n===== 5. LONGUEUR PAR CLASSE =====")
print(
    df.groupby("category")[["character_count", "word_count"]]
    .agg(["mean", "median", "min", "max"])
    .round(2)
)

print("\n===== 6. COMMENTAIRES LES PLUS COURTS =====")
shortest = df.nsmallest(5, "word_count")

for _, row in shortest.iterrows():
    print(
        f"Label={row['category']} | "
        f"Mots={row['word_count']} | "
        f"Texte={row['clean_comment'][:150]}"
    )

print("\n===== 7. COMMENTAIRES LES PLUS LONGS =====")
longest = df.nlargest(5, "word_count")

for _, row in longest.iterrows():
    print(
        f"Label={row['category']} | "
        f"Mots={row['word_count']} | "
        f"Texte={row['clean_comment'][:150]}"
    )

# Graphique de distribution des classes
plt.figure(figsize=(8, 5))
counts.plot(kind="bar")
plt.title("Distribution des classes de sentiment")
plt.xlabel("Classe de sentiment")
plt.ylabel("Nombre de commentaires")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(output_path, dpi=150)
plt.close()

print("\n===== 8. GRAPHIQUE =====")
print("Graphique enregistre :", output_path)
print("Fichier existe :", output_path.exists())

print("\n===== FIN DE L'EDA =====")
