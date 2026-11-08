import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# Chemins des fichiers
input_path = Path("data/processed/reddit_clean.csv")
train_path = Path("data/processed/train.csv")
test_path = Path("data/processed/test.csv")

# Charger le dataset nettoyé
df = pd.read_csv(input_path)

# Séparer les variables explicatives et la cible
X = df["clean_comment"]
y = df["category"]

# Séparation stratifiée : 80 % entraînement, 20 % test
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Reconstituer les DataFrames
train_df = pd.DataFrame({
    "clean_comment": X_train,
    "category": y_train
})

test_df = pd.DataFrame({
    "clean_comment": X_test,
    "category": y_test
})

# Enregistrer les fichiers
train_df.to_csv(train_path, index=False, encoding="utf-8")
test_df.to_csv(test_path, index=False, encoding="utf-8")

# Afficher le rapport
print("===== RAPPORT DE SEPARATION =====")

print("\nDimensions initiales :", df.shape)
print("Ensemble d'entrainement :", train_df.shape)
print("Ensemble de test :", test_df.shape)

print("\n===== REPARTITION DES CLASSES =====")

for label in ["-1", "0", "1"]:
    train_count = (y_train == label).sum()
    test_count = (y_test == label).sum()

    print(
        f"Classe {label} | "
        f"Train : {train_count} ({train_count / len(y_train) * 100:.2f} %) | "
        f"Test : {test_count} ({test_count / len(y_test) * 100:.2f} %)"
    )

print("\n===== VERIFICATIONS =====")
print("Valeurs manquantes train :", train_df.isna().sum().sum())
print("Valeurs manquantes test :", test_df.isna().sum().sum())
print("Total train + test :", len(train_df) + len(test_df))
print("Fichier train cree :", train_path.exists())
print("Fichier test cree :", test_path.exists())

print("\nSEPARATION TERMINEE")
