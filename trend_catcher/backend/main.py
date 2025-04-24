from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from trend_catcher.backend.trend_analyzer import get_trends, compare_trends
from trend_catcher.backend.trend_predictor import predict_trend_growth

app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://verbose-waffle-v6q6wjpxg5x4fxwgw-8080.app.github.dev"
    ],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root health check
@app.get("/")
def root():
    return {"message": "Trend Catchers Backend Running"}

# GET: /trends
@app.get("/trends")
def trends():
    return get_trends()

# GET: /compare
@app.get("/compare")
def compare():
    return compare_trends()

# POST: /predict
@app.post("/predict")
def predict_growth(data: dict):
    view_counts = data.get("views", [])
    if not view_counts or len(view_counts) < 7:
        return {"error": "Need at least 7 days of view data"}
    
    prediction = predict_trend_growth(view_counts)
    return {"predicted_day_21_views": prediction}
