import json
import os
import sys
import time
import requests
from dotenv import load_dotenv

# Force UTF-8 output so arrow/unicode chars don't crash on Windows cp1252 terminals
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Load .env for local dev (GitHub Actions injects secrets as real env vars)
load_dotenv()

# --- CONFIG ---
IGDB_CLIENT_ID = os.environ.get("IGDB_CLIENT_ID")
IGDB_TOKEN     = os.environ.get("IGDB_TOKEN")

IGDB_HEADERS = {
    "Client-ID":     IGDB_CLIENT_ID or "",
    "Authorization": f"Bearer {IGDB_TOKEN or ''}",
}

# Your manually curated game list
MY_GAMES = [
    {"title": "Tomb Raider", "genre": "Action-Adventure", "status": "completed", "rating": 8, "notes": "Survivor timeline part 1."},
    {"title": "Rise of the Tomb Raider", "genre": "Action-Adventure", "status": "completed", "rating": 8, "notes": "Survivor timeline part 2."},
    {"title": "Shadow of the Tomb Raider", "genre": "Action-Adventure", "status": "completed", "rating": 8, "notes": "Survivor timeline part 3."},
    {"title": "Far Cry 3", "genre": "FPS / Open World", "status": "completed", "rating": 9, "notes": "Did I ever tell you the definition of insanity?"},
    {"title": "Call of Duty 4: Modern Warfare", "genre": "FPS", "status": "completed", "rating": 9, "notes": "Original 2007 release."},
    {"title": "Call of Duty: Modern Warfare 2", "genre": "FPS", "status": "completed", "rating": 9, "notes": "Original 2009 release."},
    {"title": "Call of Duty: Modern Warfare 3", "genre": "FPS", "status": "completed", "rating": 8, "notes": "Original 2011 release."},
    {"title": "Call of Duty: Black Ops", "genre": "FPS", "status": "completed", "rating": 9, "notes": "The numbers, Mason."},
    {"title": "Call of Duty: Black Ops II", "genre": "FPS", "status": "completed", "rating": 9, "notes": "Peak multiplayer era."},
    {"title": "Call of Duty: Black Ops III", "genre": "FPS", "status": "completed", "rating": 8, "notes": "Great zombies mode."},
    {"title": "Marvel's Spider-Man", "genre": "Action-Adventure", "status": "completed", "rating": 9, "notes": "Best web-swinging mechanics."},
    {"title": "Marvel's Spider-Man: Miles Morales", "genre": "Action-Adventure", "status": "completed", "rating": 8, "notes": "Great standalone expansion."},
    {"title": "Batman: Arkham Knight", "genre": "Action-Adventure", "status": "completed", "rating": 9, "notes": "Batmobile is fun but overused."},
    {"title": "Alan Wake", "genre": "Survival Horror", "status": "completed", "rating": 8, "notes": "It's not a lake, it's an ocean."},
    {"title": "Control", "genre": "Action-Adventure", "status": "completed", "rating": 9, "notes": "Ashtray maze was incredible."},
    {"title": "God of War", "genre": "Action-Adventure", "status": "completed", "rating": 10, "notes": "Boy."},
    {"title": "God of War Ragnarök", "genre": "Action-Adventure", "status": "completed", "rating": 10, "notes": "Incredible conclusion to the Norse saga."},
    {"title": "Dark Souls", "genre": "Action RPG", "status": "playing", "rating": 0, "notes": "Currently dying repeatedly."},
    {"title": "Forza Horizon 4", "genre": "Racing", "status": "completed", "rating": 9, "notes": "Beautiful UK map and seasons."},
    {"title": "EA Sports FC 25", "genre": "Sports", "status": "playing", "rating": 7, "notes": "Standard football grind."},
    {"title": "Honkai: Star Rail", "genre": "RPG / Gacha", "status": "playing", "rating": 8, "notes": "Turn-based space train."},
    {"title": "Valorant", "genre": "Tactical Shooter", "status": "playing", "rating": 8, "notes": "Clicking heads."},
    {"title": "Counter-Strike 2", "genre": "Tactical Shooter", "status": "playing", "rating": 8, "notes": "Rush B."},
    {"title": "Wuthering Waves", "genre": "Action RPG / Gacha", "status": "playing", "rating": 8, "notes": "Great combat mechanics."},
    # --- New entries ---
    {"title": "Minecraft", "genre": "Sandbox", "status": "playing", "rating": 9, "notes": "Still surviving, still building."},
    {"title": "R.E.P.O.", "genre": "Co-op Horror", "status": "playing", "rating": 8, "notes": "Physics-based chaos with friends."},
    {"title": "Grand Theft Auto V", "genre": "Open World", "status": "playing", "rating": 9, "notes": "Los Santos never gets old."},
    {"title": "Demonologist", "genre": "Co-op Horror", "status": "completed", "rating": 7, "notes": "Ghost hunting done right."},
    {"title": "Detroit: Become Human", "genre": "Narrative / Adventure", "status": "completed", "rating": 9, "notes": "Become human. Feel things."},
    {"title": "Need for Speed: Most Wanted", "genre": "Racing", "status": "completed", "rating": 9, "notes": "Blacklist #1. Razor. Enough said."},
    {"title": "Peak", "genre": "Co-op Adventure", "status": "playing", "rating": 0, "notes": "Climbing a mountain with friends. What could go wrong."},
    {"title": "Grand Theft Auto: Vice City", "genre": "Open World", "status": "completed", "rating": 9, "notes": "Tommy Vercetti. Neon lights. 80s vibes."},
    {"title": "Grand Theft Auto: San Andreas", "genre": "Open World", "status": "completed", "rating": 10, "notes": "CJ. Grove Street. All day."},
    {"title": "Grand Theft Auto IV", "genre": "Open World", "status": "completed", "rating": 9, "notes": "The most cinematic GTA ever made."},
]

# Hardcoded IGDB ID overrides — use when the search returns the wrong version.
# Key must exactly match the 'title' field in MY_GAMES.
GAME_ID_OVERRIDES = {
    "Tomb Raider":                      1164,   # 2013 Crystal Dynamics reboot
    "Call of Duty 4: Modern Warfare":   623,    # 2007 original (not the remaster)
    "God of War":                       19560,  # 2018 PS4 soft reboot (not 2005 original)
    "Grand Theft Auto V":               1020,   # 2013 original release
    "Grand Theft Auto: Vice City":      733,    # 2002 original
    "Grand Theft Auto: San Andreas":    732,    # 2004 original
    "Grand Theft Auto IV":              731,    # 2008 original
    "R.E.P.O.":                          332780, # 2025 co-op horror
    "Need for Speed: Most Wanted":       242992, # 2005 classic
    "Peak":                              349524, # 2025 co-op climbing game
}


def igdb_game_id(title):
    """
    3-tier IGDB game search:
      1. Exact name match (where name = "...")
      2. Fuzzy full-text search (search "...") — pick the result with highest
         name similarity to our query, reject if score < 0.55
      3. Retry fuzzy search with sanitized title (strip subtitles after ':')
    """
    import difflib

    # Normalize: replace curly apostrophes with straight ones for IGDB queries
    safe_title = title.replace("\u2019", "'").replace('"', '\\"')

    def similarity(a, b):
        return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def best_fuzzy(results, query):
        """Return the closest-matching result and its similarity score."""
        if not results:
            return None, 0
        scored = [(g, similarity(query, g.get("name", ""))) for g in results]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[0]

    # ── Tier 1: Exact name match ──────────────────────────────────────────────
    try:
        r = requests.post(
            "https://api.igdb.com/v4/games",
            headers=IGDB_HEADERS,
            data=f'where name = "{safe_title}"; fields id, name; limit 1;',
            timeout=10,
        )
        results = [g for g in r.json() if not g.get("status")]
        if results:
            g = results[0]
            print(f"    [exact] '{title}' -> '{g['name']}' (id={g['id']})")
            return g["id"]
    except Exception as e:
        print(f"    [warn] exact search error for '{title}': {e}")

    # ── Tier 2: Fuzzy search with similarity gate ─────────────────────────────
    try:
        r = requests.post(
            "https://api.igdb.com/v4/games",
            headers=IGDB_HEADERS,
            data=f'search "{safe_title}"; fields id, name; limit 10;',
            timeout=10,
        )
        results = [g for g in r.json() if not g.get("status")]
        best, score = best_fuzzy(results, title)
        if best and score >= 0.55:
            print(f"    [fuzzy {score:.2f}] '{title}' -> '{best['name']}' (id={best['id']})")
            return best["id"]
        elif best:
            print(f"    [low-conf {score:.2f}] best was '{best['name']}' — trying short title...")
    except Exception as e:
        print(f"    [warn] fuzzy search error for '{title}': {e}")

    # ── Tier 3: Retry with base title (drop subtitle after ':') ───────────────
    base = safe_title.split(":")[0].strip()
    if base != safe_title:
        try:
            r = requests.post(
                "https://api.igdb.com/v4/games",
                headers=IGDB_HEADERS,
                data=f'search "{base}"; fields id, name; limit 10;',
                timeout=10,
            )
            results = [g for g in r.json() if not g.get("status")]
            best, score = best_fuzzy(results, title)
            if best and score >= 0.45:
                print(f"    [short-title {score:.2f}] '{title}' -> '{best['name']}' (id={best['id']})")
                return best["id"]
        except Exception as e:
            print(f"    [warn] short-title search error for '{title}': {e}")

    print(f"    [miss] no confident match found for '{title}'")
    return None



def igdb_cover_url(game_id):
    """Phase 3+4: Fetch cover image_id and return a t_cover_big URL."""
    try:
        r = requests.post(
            "https://api.igdb.com/v4/covers",
            headers=IGDB_HEADERS,
            data=f"fields image_id; where game = {game_id};",
            timeout=10,
        )
        results = r.json()
        if results and results[0].get("image_id"):
            image_id = results[0]["image_id"]
            # t_cover_big = 264×374 px portrait — perfect for the grid
            url = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{image_id}.jpg"
            print(f"    [cover] {url}")
            return url
        else:
            print(f"    [no cover] for game id {game_id}")
    except Exception as e:
        print(f"    [error] cover fetch failed for game id {game_id}: {e}")
    return None


def get_game_poster(title):
    # Use pinned ID if available — skips search entirely, guarantees correct version
    if title in GAME_ID_OVERRIDES:
        game_id = GAME_ID_OVERRIDES[title]
        print(f"    [pinned] id={game_id}")
    else:
        game_id = igdb_game_id(title)
    if not game_id:
        return None
    time.sleep(0.1)  # small gap between search and cover requests
    return igdb_cover_url(game_id)


def main():
    if not IGDB_CLIENT_ID or not IGDB_TOKEN:
        print("ERROR: IGDB_CLIENT_ID or IGDB_TOKEN not set — check your .env file.")
        return

    print(f"IGDB client: {IGDB_CLIENT_ID[:6]}...  token: {IGDB_TOKEN[:6]}...")
    print("Fetching portrait cover art from IGDB...\n")

    for game in MY_GAMES:
        print(f"  [{game['title']}]")
        game["poster"] = get_game_poster(game["title"])
        time.sleep(0.25)  # polite rate limit

    with open("games.json", "w", encoding="utf-8") as f:
        json.dump({"games": MY_GAMES}, f, indent=2)

    hits   = sum(1 for g in MY_GAMES if g.get("poster"))
    misses = len(MY_GAMES) - hits
    print(f"\nDone. {hits} covers fetched, {misses} missed. games.json updated.")


if __name__ == "__main__":
    main()