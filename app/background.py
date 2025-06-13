import os
import time
import json
import httpx


from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

POLLING_INTERVAL=int(os.getenv('POLLING_INTERVAL', 3))

TOKEN_URL = 'https://accounts.spotify.com/api/token'
PLAYER_URL = 'https://api.spotify.com/v1/me/player'



def run_background_task(data_file):

    if os.path.exists(data_file):
        while True:
            with open(data_file) as f:
                data = json.load(f)
            
            if data.get('refresh_token'):    
                # Example action on the data
                print("[Background] Task Completed")

            time.sleep(POLLING_INTERVAL)  # adjust interval as needed
