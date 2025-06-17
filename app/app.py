import os
from flask import Flask, render_template, request, redirect
import json
from threading import Thread
from urllib.parse import urlencode
from background import run_background_task
from utils import load_data, save_data
import httpx
import logging
import time

from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPES = os.getenv('SCOPES')
PORT = os.getenv('PORT', 8000)
DATA_FILE = f"/data/{os.getenv('DATA_FILE', 'data.json')}"

TOKEN_URL = 'https://accounts.spotify.com/api/token'

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,  # Or DEBUG if you want more detailed output
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
)

logger = logging.getLogger(__name__)

def get_spotify_auth_url():
    logger.info("Spotify Auth URL provided")
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': SCOPES,
        'redirect_uri': REDIRECT_URI,
    }
    return f"https://accounts.spotify.com/authorize?{urlencode(params)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    data = load_data(DATA_FILE)
    if request.method == 'POST':
        # key = request.form['key']
        # value = request.form['value']
        artist = request.form['artist']
        data['artists'].append(artist)
        save_data(DATA_FILE, data)
        return redirect('/')
    spotify_auth_url = get_spotify_auth_url()
    return render_template('index.html', data=data['artists'], spotify_auth_url=spotify_auth_url)

@app.route('/callback', methods=['GET'])
def callback():
    args = request.args
    code = args.get('code')
    # code here to convert code to refresh token
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }
    res = httpx.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload)
    tokens = res.json()
    data = load_data(DATA_FILE)
    data['access_token'] = tokens['access_token']
    data['refresh_token'] = tokens['refresh_token']
    save_data(DATA_FILE, data)
    logger.info("Spotify authorization completed")
    return redirect('/')



def safe_background_wrapper():
    while True:
        try:
            logging.info("Starting background task...")
            run_background_task()
        except Exception as e:
            logging.exception(f"Background task crashed. Restarting in 5 seconds. Reason: {e}")
            time.sleep(5)  

if __name__ == '__main__':
    # Run background task in a separate thread
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        thread = Thread(target=safe_background_wrapper, daemon=True)
        thread.start()
    app.run(host='0.0.0.0', port=PORT, debug=True)
    #TODO: disable reloader when in docker
    # app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=False)