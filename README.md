# Skipify 🎵

Skipify is a Flask-based web application that automatically skips songs by specific artists on Spotify. It runs a background task that monitors your currently playing music and automatically skips to the next track when it detects songs by artists you've configured to skip.

## Features

- 🔄 **Automatic Song Skipping**: Monitors your Spotify playback and skips songs by specified artists
- 🌐 **Web Interface**: Simple web UI to manage your skip list and authorize Spotify
- 🔐 **OAuth Authentication**: Secure Spotify authorization using OAuth 2.0
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose
- ⚡ **Background Processing**: Runs continuously in the background to monitor playback

## Prerequisites

- Docker and Docker Compose installed
- A Spotify Premium account
- Spotify Developer account (free)

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Spotify API Credentials (Required)
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
REDIRECT_URI=http://localhost:7080/callback

# Spotify Scopes (Required)
SCOPES=user-read-playback-state,user-modify-playback-state

# Application Settings (Optional)
PORT=8000
DATA_FILE=data.json

# Background Task Settings (Optional)
POLLING_INTERVAL=3
NOT_PLAYING_INTERVAL=10
RATE_LIMIT_DELAY=1
```

### Environment Variable Details

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `CLIENT_ID` | ✅ | Your Spotify app client ID | - |
| `CLIENT_SECRET` | ✅ | Your Spotify app client secret | - |
| `REDIRECT_URI` | ✅ | OAuth redirect URI (must match Spotify app settings) | - |
| `SCOPES` | ✅ | Spotify API scopes needed for the app | - |
| `PORT` | ❌ | Port for the web interface | 8000 |
| `DATA_FILE` | ❌ | Filename for storing app data | data.json |
| `POLLING_INTERVAL` | ❌ | Seconds between playback checks when playing | 3 |
| `NOT_PLAYING_INTERVAL` | ❌ | Seconds between checks when not playing | 10 |
| `RATE_LIMIT_DELAY` | ❌ | Seconds to wait when rate limited | 1 |

## Spotify Developer App Setup

### 1. Create a Spotify Developer Account

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Accept the terms and conditions

### 2. Create a New App

1. Click **"Create an App"**
2. Fill in the required information:
   - **App name**: `Skipify` (or any name you prefer)
   - **App description**: `Auto-skip songs by specific artists`
   - **Website**: `http://localhost:7080` (for development)
   - **Redirect URIs**: `http://localhost:7080/callback`
   - **API/SDKs**: Select "Web API"
3. Click **"Save"**

### 3. Get Your Credentials

1. After creating the app, you'll be taken to the app dashboard
2. Note down your **Client ID** (visible on the dashboard)
3. Click **"Show Client Secret"** and note down your **Client Secret**
4. Add these to your `.env` file

### 4. Configure Redirect URIs

1. In your app dashboard, click **"Edit Settings"**
2. Under **"Redirect URIs"**, add:
   - `http://localhost:7080/callback` (for local development)
   - `https://your-domain.com/callback` (requires the use of HTTPS unless using above url)
3. Click **"Save"**

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd skipify-docker
```

### 2. Create Environment File

```bash
cp sample.env .env  # if example exists, or create manually
```

Edit `.env` with your Spotify credentials (see Environment Variables section above).

### 3. Run with Docker

```bash
docker-compose up -d
```

### 4. Access the Application

1. Open your browser and go to `http://127.0.0.1 :7080`
2. Click **"Connect with Spotify"** to authorize the app
3. After authorization, you'll be redirected back to the app
4. Add artists you want to skip using the web interface

### 5. Start Skipping

Once you've added artists to your skip list, the background task will automatically:
- Monitor your Spotify playback
- Skip songs by the specified artists
- Continue running even when you close the browser

## How It Works

1. **Authorization**: The app uses Spotify's OAuth 2.0 flow to get access to your account
2. **Background Monitoring**: A background task continuously polls Spotify's API to check what's currently playing
3. **Artist Detection**: When a song is playing, it checks if any of the artists match your skip list
4. **Auto-Skip**: If a match is found, it automatically skips to the next track
5. **Token Refresh**: Automatically refreshes access tokens when they expire

## Data Storage

The app stores its data in a JSON file (`data.json` by default) containing:
- List of artists to skip
- Spotify access and refresh tokens

This file is persisted in the `./data` directory and mounted as a Docker volume.

## Troubleshooting

### Common Issues

1. **"No refresh token" error**: Make sure you've completed the Spotify authorization flow
2. **"401 Unauthorized" error**: The app will automatically refresh tokens, but you may need to re-authorize
3. **Songs not being skipped**: Ensure the artist names in your skip list exactly match how they appear in Spotify

### Logs

View application logs:
```bash
docker-compose logs -f skipify
```

### Restart the Application

```bash
docker-compose restart
```

## Development

### Local Development (without Docker)

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`

3. Run the application:
   ```bash
   python app/app.py
   ```

### Project Structure

```
skipify-docker/
├── app/
│   ├── app.py          # Main Flask application
│   ├── background.py   # Background task for monitoring
│   ├── utils.py        # Utility functions
│   ├── skeleton.json   # Data structure template
│   └── templates/
│       └── index.html  # Web interface
├── data/               # Persistent data storage
├── docker-compose.yml  # Docker configuration
├── Dockerfile         # Container definition
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Contributing

Feel free to submit issues and enhancement requests! Contributions welcome, but please make them simple enough for me to follow along!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
