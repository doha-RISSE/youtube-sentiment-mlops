import pandas as pd
from pathlib import Path

path = Path("data/processed/reddit_clean.csv")

# Lecture avec le comportement par défaut de Pandas
df_default = pd.read_csv(path)

# Lecture sans interprétation automatique des chaînes comme NaN
df_raw = pd.read_csv(path, keep_default_na=False)

print("===== COMPARAISON DES LECTURES PANDAS =====")
print("Dimensions lecture par défaut :", df_default.shape)
print("Dimensions sans NA automatique :", df_raw.shape)

print("\nValeurs manquantes avec lecture par défaut :")
print(df_default.isna().sum())

missing_indices = df_default.index[df_default["clean_comment"].isna()]

print("\n===== VALEURS CONCERNEES =====")

for index in missing_indices:
    print("Index Pandas :", index)
    print("Commentaire brut :", repr(df_raw.loc[index, "clean_comment"]))
    print("Label :", repr(df_raw.loc[index, "category"]))
    print("---")

print("\n===== VERIFICATION DES CHAINES VIDES =====")
empty_count = (
    df_raw["clean_comment"].str.strip().eq("").sum()
)
print("Commentaires réellement vides :", empty_count)

print("\n===== FIN =====")
