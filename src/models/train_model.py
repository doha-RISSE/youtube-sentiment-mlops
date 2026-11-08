import pandas as pd
import joblib

from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score
)

# Chemins des fichiers
train_path = Path("data/processed/train.csv")
test_path = Path("data/processed/test.csv")
model_path = Path("models/sentiment_pipeline.joblib")

# Charger les données
train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)

X_train = train_df["clean_comment"]
y_train = train_df["category"]

X_test = test_df["clean_comment"]
y_test = test_df["category"]

print("===== 1. DONNEES CHARGEES =====")
print("Entrainement :", len(X_train))
print("Test :", len(X_test))

# Construire le pipeline TF-IDF + Logistic Regression
pipeline = Pipeline([
    (
        "tfidf",
        TfidfVectorizer()
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            random_state=42
        )
    )
])

# Entraîner le modèle
print("\n===== 2. ENTRAINEMENT =====")

pipeline.fit(X_train, y_train)

print("Entrainement termine.")

# Prédictions sur les données de test
print("\n===== 3. EVALUATION =====")

y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
macro_f1 = f1_score(y_test, y_pred, average="macro")

print(f"Accuracy : {accuracy:.4f}")
print(f"Macro F1-score : {macro_f1:.4f}")

print("\n===== 4. RAPPORT DE CLASSIFICATION =====")

print(
    classification_report(
        y_test,
        y_pred,
        labels=[-1, 0, 1],
        target_names=["Negatif", "Neutre", "Positif"],
        digits=4
    )
)

print("\n===== 5. MATRICE DE CONFUSION =====")

matrix = confusion_matrix(
    y_test,
    y_pred,
    labels=[-1, 0, 1]
)

print("Ordre des classes : [-1, 0, 1]")
print(matrix)

# Enregistrer le pipeline complet
print("\n===== 6. SAUVEGARDE =====")

model_path.parent.mkdir(parents=True, exist_ok=True)

joblib.dump(pipeline, model_path)

print("Modele enregistre :", model_path)
print("Fichier existe :", model_path.exists())

print("\nENTRAINEMENT TERMINE")
