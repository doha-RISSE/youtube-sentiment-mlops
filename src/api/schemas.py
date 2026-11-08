from typing import Annotated

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    comments: list[
        Annotated[str, Field(min_length=1, max_length=10000)]
    ] = Field(min_length=1, max_length=100)


class SentimentResult(BaseModel):
    comment: str
    sentiment: int
    label: str
    confidence: float
    probabilities: dict[str, float]


class PredictionResponse(BaseModel):
    total_comments: int
    predictions: list[SentimentResult]
    statistics: dict[str, dict[str, float | int]]
