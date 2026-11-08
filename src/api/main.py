from contextlib import asynccontextmanager
from pathlib import Path

import joblib

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.api.schemas import PredictionRequest, PredictionResponse, SentimentResult


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "sentiment_pipeline.joblib"

LABELS = {
    -1: "Negatif",
    0: "Neutre",
    1: "Positif"
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modele introuvable : {MODEL_PATH}"
        )

    app.state.model = joblib.load(MODEL_PATH)
    print(f"Modele charge : {MODEL_PATH}")

    yield

    app.state.model = None
    print("Modele decharge.")


app = FastAPI(
    title="YouTube Sentiment Analysis API",
    description="API de classification des sentiments des commentaires.",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1"
    ],
    allow_origin_regex=r"chrome-extension://.*",
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"]
)


@app.get("/health")
def health():
    model_loaded = getattr(app.state, "model", None) is not None

    return {
        "status": "healthy" if model_loaded else "unavailable",
        "model_loaded": model_loaded
    }


@app.post("/predict_batch", response_model=PredictionResponse)
def predict_batch(request: PredictionRequest):

    model = getattr(app.state, "model", None)

    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Modele non disponible."
        )

    try:
        comments = request.comments

        predicted_classes = model.predict(comments)
        probabilities = model.predict_proba(comments)
        model_classes = model.classes_

        predictions = []

        counts = {
            "Negatif": 0,
            "Neutre": 0,
            "Positif": 0
        }

        for comment, predicted_class, probability_row in zip(
            comments,
            predicted_classes,
            probabilities
        ):

            sentiment = int(predicted_class)
            label = LABELS[sentiment]

            probability_dict = {
                LABELS[int(class_id)]: round(float(probability), 4)
                for class_id, probability in zip(
                    model_classes,
                    probability_row
                )
            }

            confidence = max(probability_dict.values())

            predictions.append(
                SentimentResult(
                    comment=comment,
                    sentiment=sentiment,
                    label=label,
                    confidence=confidence,
                    probabilities=probability_dict
                )
            )

            counts[label] += 1

        total = len(comments)

        statistics = {
            label: {
                "count": count,
                "percentage": round(count / total * 100, 2)
            }
            for label, count in counts.items()
        }

        return PredictionResponse(
            total_comments=total,
            predictions=predictions,
            statistics=statistics
        )

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant la prediction : {str(error)}"
        )
