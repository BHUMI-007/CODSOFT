from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import movies_df, hybrid_recommend

app = Flask(__name__)
CORS(app)

@app.route("/movies", methods=["GET"])
def get_movies():
    # Return top 50 popular movies for UI
    from recommender import ratings_df
    popular = ratings_df["movieId"].value_counts().head(50).index
    result = movies_df[movies_df["movieId"].isin(popular)][["movieId","title","genres"]].copy()
    result["genres"] = result["genres"].str.split()
    return result.to_dict(orient="records")

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").lower()
    if not query:
        return []
    mask = movies_df["title"].str.lower().str.contains(query)
    result = movies_df[mask].head(10)[["movieId","title","genres"]].copy()
    result["genres"] = result["genres"].str.split()
    return result.to_dict(orient="records")

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    liked_ids = data.get("liked_movie_ids", [])
    if not liked_ids:
        return {"error": "No movies selected"}, 400
    recs = hybrid_recommend(liked_ids, n=6)
    return recs

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)