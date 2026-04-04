# recommender.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# ─────────────────────────────
# LOAD DATA
# ─────────────────────────────
BASE = os.path.dirname(__file__)

movies_df  = pd.read_csv(os.path.join(BASE, "data", "movies.csv"))
ratings_df = pd.read_csv(os.path.join(BASE, "data", "ratings.csv"))
tags_df    = pd.read_csv(os.path.join(BASE, "data", "tags.csv"))

# Clean genres
movies_df["genres"] = movies_df["genres"].str.replace("|", " ", regex=False)

# Merge tags with movies
tags_grouped = tags_df.groupby("movieId")["tag"].apply(lambda x: " ".join(x)).reset_index()
movies_df = movies_df.merge(tags_grouped, on="movieId", how="left")
movies_df["tag"] = movies_df["tag"].fillna("")

# Combine genres + tags for content analysis
movies_df["content"] = movies_df["genres"] + " " + movies_df["tag"]

# ─────────────────────────────
# CONTENT-BASED FILTERING
# ─────────────────────────────
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(movies_df["content"])
content_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

def content_based_recommend(movie_ids, n=6):
    indices = movies_df[movies_df["movieId"].isin(movie_ids)].index.tolist()
    if not indices:
        return []
    
    sim_scores = content_sim_matrix[indices].mean(axis=0)
    
    # Exclude already selected movies
    for idx in indices:
        sim_scores[idx] = -1
    
    top_indices = sim_scores.argsort()[::-1][:n]
    result = movies_df.iloc[top_indices][["movieId", "title", "genres"]].copy()
    result["genres"] = result["genres"].str.split()
    return result.to_dict(orient="records")

# ─────────────────────────────
# COLLABORATIVE FILTERING
# ─────────────────────────────
# Use top 500 most-rated movies to keep it fast
top_movies = ratings_df["movieId"].value_counts().head(500).index
ratings_filtered = ratings_df[ratings_df["movieId"].isin(top_movies)]

user_movie_matrix = ratings_filtered.pivot_table(
    index="userId", columns="movieId", values="rating"
).fillna(0)

movie_user_matrix = user_movie_matrix.T
collab_sim_matrix = cosine_similarity(movie_user_matrix)
collab_sim_df = pd.DataFrame(
    collab_sim_matrix,
    index=movie_user_matrix.index,
    columns=movie_user_matrix.index
)

def collaborative_recommend(movie_ids, n=6):
    valid_ids = [mid for mid in movie_ids if mid in collab_sim_df.index]
    if not valid_ids:
        return []

    sim_scores = collab_sim_df[valid_ids].mean(axis=1)
    sim_scores = sim_scores.drop(index=valid_ids, errors="ignore")
    top_ids = sim_scores.nlargest(n).index.tolist()

    result = movies_df[movies_df["movieId"].isin(top_ids)][["movieId", "title", "genres"]].copy()
    result["genres"] = result["genres"].str.split()
    return result.to_dict(orient="records")

# ─────────────────────────────
# HYBRID RECOMMENDER
# ─────────────────────────────
def hybrid_recommend(movie_ids, n=6):
    content_recs = content_based_recommend(movie_ids, n=n)
    collab_recs  = collaborative_recommend(movie_ids, n=n)

    seen = set(movie_ids)
    final = []

    for movie in content_recs + collab_recs:
        mid = movie["movieId"]
        if mid not in seen:
            seen.add(mid)
            final.append(movie)
        if len(final) >= n:
            break

    return final