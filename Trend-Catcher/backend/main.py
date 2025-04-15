from fastapi import FastAPI
from trend_analyzer import get_trends, compare_trends

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Trend Catchers Backend Running"}

@app.get("/trends")
def trends():
    return get_trends()

@app.get("/compare")
def compare():
    return compare_trends()



from fastapi import FastAPI
from trend_analyzer import get_trends, compare_trends

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- or list specific frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Trend Catchers Backend Running"}

@app.get("/trends")
def trends():
    return get_trends()

@app.get("/compare")
def compare():
    return compare_trends()


from trend_predictor import predict_trend_growth


@app.post("/predict")
def predict_growth(data: dict):
    view_counts = data.get("views", [])
    if not view_counts or len(view_counts) < 7:
        return {"error": "Need at least 7 days of view data"}
    
    prediction = predict_trend_growth(view_counts)
    return {"predicted_day_21_views": prediction}
