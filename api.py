
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal

from backend import calculate_footprint

app = FastAPI(
    title="Carbon Choices API",
    description="Calculate lifestyle carbon emissions.",
    version="1.0.0",
)

# Allows a separately running frontend to call this API.
# We can restrict this when we know the frontend's deployment URL.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Activity(BaseModel):
    category: str
    item: str
    amount: float = Field(ge=0, allow_inf_nan=False)
    activity_unit: str
    period: Literal["day", "month"]


class FootprintRequest(BaseModel):
    activities: list[Activity]


@app.get("/")
def home():
    return {
        "message": "Carbon Choices API is running!",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/calculate")
def calculate(request: FootprintRequest):
    activities = [
        activity.model_dump()
        for activity in request.activities
    ]

    return calculate_footprint(activities)
