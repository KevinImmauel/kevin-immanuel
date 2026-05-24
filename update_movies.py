import json
import os
import time
import random
import requests
from letterboxdpy import user
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

LETTERBOXD_USER = "kevinvcx"
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

def get_tmdb_poster(title, year=None):
    """
    Tries to find a poster for a title from TMDB.
    Uses a robust 3-tier fallback strategy:
      1. Full title with and without year (movie/tv).
      2. Prefix title (split on colon ':') with year (movie/tv).
      3. Prefix title (split on colon ':') without year (movie/tv) — handles
         TV episodes rated on Letterboxd where the year is the episode's year
         but TMDB expects the show's original debut year (e.g., Black Mirror 2016 vs 2011).
    """
    if not TMDB_API_KEY:
        return None

    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    # Queue of search attempts: (query_string, search_type, year_to_use)
    attempts = []

    # 1. Full title with and without year
    attempts.append((title, 'movie', year))
    attempts.append((title, 'tv', year))
    attempts.append((title, 'movie', None))
    attempts.append((title, 'tv', None))

    # 2. Prefix queries if title has a colon (e.g., "Black Mirror: Shut Up and Dance" -> "Black Mirror")
    if ":" in title:
        prefix = title.split(":")[0].strip()
        attempts.append((prefix, 'movie', year))
        attempts.append((prefix, 'tv', year))
        attempts.append((prefix, 'movie', None))
        attempts.append((prefix, 'tv', None))

    for query, search_type, yr in attempts:
        try:
            if search_type == 'movie':
                params = {
                    "api_key": TMDB_API_KEY,
                    "query": query,
                    "year": yr or "",
                }
                r = session.get("https://api.themoviedb.org/3/search/movie", params=params, timeout=10)
                r.raise_for_status()
                results = r.json().get("results", [])
                if results and results[0].get("poster_path"):
                    print(f"    [movie] found poster for '{title}' (via: '{query}', yr: {yr or 'any'})")
                    return f"https://image.tmdb.org/t/p/w342{results[0]['poster_path']}"
            else:
                params = {
                    "api_key": TMDB_API_KEY,
                    "query": query,
                    "first_air_date_year": yr or "",
                }
                r = session.get("https://api.themoviedb.org/3/search/tv", params=params, timeout=10)
                r.raise_for_status()
                results = r.json().get("results", [])
                if results and results[0].get("poster_path"):
                    print(f"    [tv show] found poster for '{title}' (via: '{query}', yr: {yr or 'any'})")
                    return f"https://image.tmdb.org/t/p/w342{results[0]['poster_path']}"
        except Exception as e:
            print(f"  TMDB {search_type} lookup failed for '{query}': {e}")
        time.sleep(0.1)

    print(f"  [miss] no poster found for '{title}' after trying all fallbacks")
    return None


def main():
    print(f"Fetching Letterboxd data for: {LETTERBOXD_USER}")
    u = user.User(LETTERBOXD_USER)

    website_data = {"recent_likes": [], "random_five_stars": []}

    # ── Recent Likes ──
    liked_movies = list(u.get_liked_films().get("movies", {}).values())
    for movie in liked_movies[:16]:
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

    # ── Random 5-Star & 4.5-Star Picks ──
    # Combine both 5-star and 4.5-star rated films for more variety
    five_star_movies  = list(u.get_films_by_rating(5).get("movies", {}).values())
    four_half_movies  = list(u.get_films_by_rating(4.5).get("movies", {}).values())
    combined_pool     = five_star_movies + four_half_movies

    picks = random.sample(combined_pool, 16) if len(combined_pool) >= 16 else combined_pool
    for movie in picks:
        title  = movie.get("name", "")
        year   = movie.get("year")
        poster = get_tmdb_poster(title, year)
        print(f"  5/4.5star: {title} ({year}) → poster: {'ok' if poster else 'none'}")
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