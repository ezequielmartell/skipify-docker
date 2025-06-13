import os
from flask import Flask, render_template, request, redirect
import json
from threading import Thread
from urllib.parse import urlencode
from background import run_background_task
import httpx

from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPES = os.getenv('SCOPES')
PORT = os.getenv('PORT', 8000)

TOKEN_URL = 'https://accounts.spotify.com/api/token'

DATA_FILE = 'app/data.json'
SKELETON_FILE = 'app/skeleton.json'
app = Flask(__name__)

def load_data():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        with open(DATA_FILE, 'w') as data_file:
            with open(SKELETON_FILE, 'r') as skeleton_file:
                data = json.load(skeleton_file)
                json.dump(data, data_file, indent=4)
        return load_data()

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_spotify_auth_url():
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': SCOPES,
        'redirect_uri': REDIRECT_URI,
    }
    return f"https://accounts.spotify.com/authorize?{urlencode(params)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    data = load_data()
    if request.method == 'POST':
        # key = request.form['key']
        # value = request.form['value']
        artist = request.form['artist']
        data['artist'].append(artist)
        save_data(data)
        return redirect('/')
    spotify_auth_url = get_spotify_auth_url()
    return render_template('index.html', data=data['artist'], spotify_auth_url=spotify_auth_url)

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
    data = load_data()
    data['access_token'] = tokens['access_token']
    data['refresh_token'] = tokens['refresh_token']
    save_data(data)
    print("authorization completed")
    return redirect('/')

if __name__ == '__main__':
    # Run background task in a separate thread
    thread = Thread(target=run_background_task, args=(DATA_FILE,), daemon=True)
    thread.start()
    
    app.run(host='0.0.0.0', port=PORT, debug=True)
