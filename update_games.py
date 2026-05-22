import json
import requests
import time
import os

# --- CONFIG ---
RAWG_API_KEY = os.environ.get("RAWG_API_KEY") # Get one at rawg.io/apidocs

# Your manually curated list (or load from an existing file)
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
    {"title": "Wuthering Waves", "genre": "Action RPG / Gacha", "status": "playing", "rating": 8, "notes": "Great combat mechanics."}
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