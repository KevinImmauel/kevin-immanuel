import json
import requests
import time

# --- CONFIG ---
RAWG_API_KEY = "a81d0b1453384496aaed24e7a522b924" # Get one at rawg.io/apidocs

# Your manually curated list (or load from an existing file)
MY_GAMES = [
    {"title": "Disco Elysium", "genre": "RPG", "status": "completed", "rating": 10, "notes": "Changed how I think about RPGs."},
    {"title": "Outer Wilds", "genre": "Exploration", "status": "completed", "rating": 10, "notes": "Most emotional ending."},
    {"title": "Elden Ring", "genre": "Action RPG", "status": "completed", "rating": 9, "notes": "Radahn festival survivor."},
    {"title": "Baldur's Gate 3", "genre": "RPG", "status": "playing", "rating": 9, "notes": "Act 3. Astarion is carrying."}
]

def get_game_poster(title):
    url = f"https://api.rawg.io/api/games"
    params = {"key": RAWG_API_KEY, "search": title, "page_size": 1}
    try:
        r = requests.get(url, params=params, timeout=5)
        data = r.json()
        if data['results']:
            # 'background_image' is the main high-res art
            return data['results'][0].get('background_image')
    except Exception as e:
        print(f"  Error finding {title}: {e}")
    return None

def main():
    print("Fetching Game Posters...")
    for game in MY_GAMES:
        if not game.get('poster'):
            print(f"  Searching for: {game['title']}")
            game['poster'] = get_game_poster(game['title'])
            time.sleep(0.2) # Polite delay

    with open("games.json", "w", encoding="utf-8") as f:
        json.dump({"games": MY_GAMES}, f, indent=2)
    print("Done. games.json updated.")

if __name__ == "__main__":
    main()