from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://verbose-waffle-v6q6wjpxg5x4fxwgw-8080.app.github.dev"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mocked trends data
def get_trends():
    return {
        "trends": [
            {"hashtag": "#springfashion", "views": 1200000},
            {"hashtag": "#viralrecipe", "views": 800000},
            {"hashtag": "#summerfood", "views": 1100000},
            {"hashtag": "#fastfood", "views": 950000},
            {"hashtag": "#foodie", "views": 1050000},
            {"hashtag": "#fashiontips", "views": 600000},
            {"hashtag": "#vintagefashion", "views": 540000},
            {"hashtag": "#healthyeats", "views": 740000},
            {"hashtag": "#kitchenhacks", "views": 680000},
            {"hashtag": "#trendwatch", "views": 910000}
        ]
    }

# Root endpoint
@app.get("/")
def root():
    return {"message": "Trend Catchers Backend Running"}

# Return all trends
@app.get("/trends")
def trends():
    return get_trends()

# Search trends based on a topic
@app.get("/search")
def search(topic: str = Query(..., min_length=1)):
    all_trends = get_trends()["trends"]
    filtered = [t for t in all_trends if topic.lower() in t["hashtag"].lower()]
    sorted_filtered = sorted(filtered, key=lambda x: x["views"], reverse=True)
    return {"results": sorted_filtered[:5]}  # top 5
