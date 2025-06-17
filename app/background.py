import os
import time
import json
import httpx
import logging
from utils import save_data, load_data

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

POLLING_INTERVAL = int(os.getenv("POLLING_INTERVAL", 3))
NOT_PLAYING_INTERVAL = int(os.getenv("NOT_PLAYING_INTERVAL", 10))
RATE_LIMIT_DELAY = int(os.getenv("RATE_LIMIT_DELAY", 1))
DATA_FILE = f"/data/{os.getenv('DATA_FILE', 'data.json')}"


TOKEN_URL = "https://accounts.spotify.com/api/token"
PLAYER_URL = "https://api.spotify.com/v1/me/player"

logger = logging.getLogger(__name__)

def refresh():
    """Refresh access token."""
    data = load_data(DATA_FILE)
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": data["refresh_token"],
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    res = httpx.post(
        TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload, headers=headers
    )
    res_data = res.json()
    data["access_token"] = res_data["access_token"]
    save_data(DATA_FILE, data)
    return


def skip_track(data):
    logger.info("skipping track!")
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    httpx.post(f"{PLAYER_URL}/next", headers=headers)


def run_background_task():
    logger.info(f"Starting background task.")

    while True:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE) as f:
                data = json.load(f)

            if data.get("refresh_token"):
                headers = {"Authorization": f"Bearer {data['access_token']}"}
                response = httpx.get(f"{PLAYER_URL}/currently-playing", headers=headers)
                match response.status_code:
                    case 200:
                        currentSong = response.json()
                        current_artists = [
                            artist.get("name")
                            for artist in currentSong.get("item").get("artists")
                        ]
                        logger.info(f"Playing: {currentSong.get('item').get('name')} By: {', '.join(current_artists)}")
                        artist_test = any(
                            artist in data["artists"] for artist in current_artists
                        )
                        if artist_test:
                            skip_track(data)
                        time.sleep(POLLING_INTERVAL)
                    case 204:
                        logger.info("Not playing content to display.")
                        time.sleep(NOT_PLAYING_INTERVAL)
                    case 401:
                        # do refresh actions here
                        logger.info("Refreshing token")
                        refresh()
                    case 429:
                        logging.warning("RATELIMIT")
                        time.sleep(RATE_LIMIT_DELAY)
                    case _:
                        logging.error(
                            f"{response.status_code} error, unable to proceed -- {response.content}"
                        )
            else:
                logger.info(f"No refresh token in {DATA_FILE}. Not processing.")
                time.sleep(10)
        else:
            logger.info(f"{DATA_FILE} not found. Visit browser to get connected and start.")
            time.sleep(10)