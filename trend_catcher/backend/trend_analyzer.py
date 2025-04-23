def get_trends():
    return {
        "trends": [
            {"hashtag": "#springfashion", "views": 1200000},
            {"hashtag": "#viralrecipe", "views": 800000}
        ]
    }

def compare_trends():
    trends = get_trends()["trends"]
    if len(trends) < 2:
        return {"comparison": "Not enough data to compare trends."}

    diff = trends[0]["views"] - trends[1]["views"]
    percentage = round((diff / trends[1]["views"]) * 100, 2)

    return {
        "comparison": f"Trend {trends[0]['hashtag']} is currently outperforming {trends[1]['hashtag']} by {percentage}% more engagement."
    }
