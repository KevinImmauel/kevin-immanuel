import json
import os
import time
import random
import requests
from letterboxdpy import user
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_tmdb_poster(title, year=None):
    if not TMDB_API_KEY:
        return None
    
    session = requests.Session()
    # Retry 3 times on specific errors, with a "backoff" (waits longer each time)
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        params = {
            "api_key": TMDB_API_KEY,
            "query": title,
            "year": year or "",
        }
        # Increased timeout to 10 seconds
        r = session.get(
            "https://api.themoviedb.org/3/search/movie",
            params=params, timeout=10
        )
        r.raise_for_status() # Check for HTTP errors
        
        results = r.json().get("results", [])
        if results and results[0].get("poster_path"):
            return f"https://image.tmdb.org/t/p/w342{results[0]['poster_path']}"
    except Exception as e:
        print(f"  TMDB lookup failed for '{title}': {e}")
    return None

LETTERBOXD_USER = "kevinvcx"  # your Letterboxd username
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

def get_tmdb_poster(title, year=None):
    if not TMDB_API_KEY:
        return None
    
    session = requests.Session()
    # Retry 3 times on specific errors, with a "backoff" (waits longer each time)
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        params = {
            "api_key": TMDB_API_KEY,
            "query": title,
            "year": year or "",
        }
        # Increased timeout to 10 seconds
        r = session.get(
            "https://api.themoviedb.org/3/search/movie",
            params=params, timeout=10
        )
        r.raise_for_status() # Check for HTTP errors
        
        results = r.json().get("results", [])
        if results and results[0].get("poster_path"):
            return f"https://image.tmdb.org/t/p/w342{results[0]['poster_path']}"
    except Exception as e:
        print(f"  TMDB lookup failed for '{title}': {e}")
    return None

def main():
    print(f"Fetching Letterboxd data for: {LETTERBOXD_USER}")
    u = user.User(LETTERBOXD_USER)

    website_data = {"recent_likes": [], "random_five_stars": []}

    # ── Recent Likes ──
    liked_movies = list(u.get_liked_films().get("movies", {}).values())
    for movie in liked_movies[:8]:
        time.sleep(2)
        title = movie.get("name", "")
        year  = movie.get("year")
        poster = get_tmdb_poster(title, year)
        print(f"  liked: {title} ({year}) → poster: {'ok' if poster else 'none'}")
        website_data["recent_likes"].append({
            "title":  title,
            "year":   year,
            "poster": poster,
        })

    # ── Random 5-Star Picks ──
    five_star_movies = list(u.get_films_by_rating(5).get("movies", {}).values())
    picks = random.sample(five_star_movies, 8) if len(five_star_movies) >= 8 else five_star_movies
    for movie in picks:
        title  = movie.get("name", "")
        year   = movie.get("year")
        poster = get_tmdb_poster(title, year)
        print(f"  5star: {title} ({year}) → poster: {'ok' if poster else 'none'}")
        website_data["random_five_stars"].append({
            "title":  title,
            "year":   year,
            "poster": poster,
        })

    with open("movies.json", "w", encoding="utf-8") as f:
        json.dump(website_data, f, ensure_ascii=False, indent=2)

    print("Done. movies.json written.")

if __name__ == "__main__":
    main()