'''from fastapi import FastAPI
from fastapi.responses import JSONResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import httpx
import asyncio

app = FastAPI()
scheduler = AsyncIOScheduler()


app = FastAPI()

# In-memory cache for trending posts
trending_posts = []

# URL for Reddit's popular posts
REDDIT_URL = "https://www.reddit.com/r/popular.json"
HEADERS = {"User-Agent": "TrendingFetcherBot/0.1"}
@app.get("/trends")
async def get_trends():
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL)
        data = response.json()
        return [
            {
                "description": item['text'],
                "video_url": item['videoUrl'],
                "author": item['authorMeta']['name']
            }
            for item in data
        ]
###    return {
   ###     "trends": [
      ###      {"hashtag": "#springfashion", "views": 1200000},
         ###   {"hashtag": "#viralrecipe", "views": 800000}
        ###]
   ### }

def compare_trends():
    trends = get_trends()["trends"]
    if len(trends) < 2:
        return {"comparison": "Not enough data to compare trends."}

    diff = trends[0]["views"] - trends[1]["views"]
    percentage = round((diff / trends[1]["views"]) * 100, 2)

    return {
        "comparison": f"Trend {trends[0]['hashtag']} is currently outperforming {trends[1]['hashtag']} by {percentage}% more engagement."
    }
'''
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, desc
from sqlalchemy.orm import sessionmaker
import httpx
from datetime import datetime

DATABASE_URL = "sqlite+aiosqlite:///./reddit.db"

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

app = FastAPI()
scheduler = AsyncIOScheduler()

REDDIT_TOP_URL = "https://www.reddit.com/r/popular/top.json?t=month&limit=50"
HEADERS = {"User-Agent": "TrendingFetcherBot/1.0"}


class RedditPost(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    subreddit = Column(String)
    url = Column(String)
    score = Column(Integer)
    num_comments = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


async def fetch_and_store_trending():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(REDDIT_TOP_URL, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            posts = data["data"]["children"]

            async with SessionLocal() as session:
                for post in posts:
                    p = post["data"]
                    reddit_post = RedditPost(
                        id=p["id"],
                        title=p["title"],
                        subreddit=p["subreddit"],
                        url=p["url"],
                        score=p["score"],
                        num_comments=p["num_comments"],
                        created_at=datetime.utcnow()
                    )
                    await session.merge(reddit_post)
                await session.commit()
                print(f"{len(posts)} posts updated.")

        except Exception as e:
            print(f"Failed to fetch posts: {e}")


@app.get("/trending")
async def get_trends():
    async with SessionLocal() as session:
        result = await session.execute(
            RedditPost.__table__.select().order_by(desc(RedditPost.score)).limit(10)
        )
        top_posts = result.fetchall()
        return JSONResponse(content={"top_trending": [
            {
                "title": post.title,
                "subreddit": post.subreddit,
                "url": post.url,
                "score": post.score,
                "comments": post.num_comments
            } for post in top_posts
        ]})


@app.on_event("startup")
async def on_startup():
    # Create DB schema
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Fetch once at startup
    await fetch_and_store_trending()

    # Schedule updates every 6 hours
    scheduler.add_job(fetch_and_store_trending, "interval", hours=6)
    scheduler.start()


@app.on_event("shutdown")
async def on_shutdown():
    scheduler.shutdown()
