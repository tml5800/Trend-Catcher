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
