from flask import Flask, jsonify

app = Flask(__name__)

def get_trends():
    return {
        "trends": [
            {"hashtag": "#springfashion", "views": 1200000},
            {"hashtag": "#viralrecipe", "views": 800000}
        ]
    }

def compare_trends():
    return {
        "comparison": "Trend #springfashion is currently outperforming #viralrecipe by 40% more engagement."
    }

@app.route("/")
def home():
    return "Trend Catcher backend is running!"

@app.route("/api/trends", methods=["GET"])
def trends_route():
    return jsonify(get_trends())

@app.route("/api/compare", methods=["GET"])
def compare_route():
    return jsonify(compare_trends())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
