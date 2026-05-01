# LinuxMusic — DJ Edition

```
██▓     ██▓ ███▄    █  ██╗   ██╗██╗  ██╗███╗   ███╗██╗   ██╗███████╗██╗ ██████╗
▓██▒    ▓██▒ ██ ▀█   █  ██║   ██║╚██╗██╔╝████╗ ████║██║   ██║██╔════╝██║██╔════╝
▒██░    ▒██▒▓██  ▀█ ██▒ ██║   ██║ ╚███╔╝ ██╔████╔██║██║   ██║███████╗██║██║
▒██░    ░██░▓██▒  ▐▌██▒ ██║   ██║ ██╔██╗ ██║╚██╔╝██║██║   ██║╚════██║██║██║
░██████▒░██░▒██░   ▓██░ ╚██████╔╝██╔╝ ██╗██║ ╚═╝ ██║╚██████╔╝███████║██║╚██████╗
░ ▒░▓  ░░▓  ░ ▒░   ▒ ▒   ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝
```

> **No browser. No Electron. No ads. No RAM waste. Just music.**
> Terminal-native YouTube Music streamer for Linux power users.

---

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux-orange?style=flat-square&logo=linux)](https://kernel.org)
[![Engine](https://img.shields.io/badge/Engine-mpv%20IPC-purple?style=flat-square)](https://mpv.io)

---

## What This Is

LinuxMusic is a **headless YouTube Music client** that lives entirely in your terminal.
It uses `mpv` as a background audio slave, controlled over a UNIX IPC socket.
No GUI. No browser process. No 300MB Electron runtime eating your RAM.

The backend authenticates directly with YouTube Music via `ytmusicapi`,
pulls stream URLs via `yt-dlp`, and feeds them to `mpv` — bypassing every
ad injection point in the normal YouTube player stack.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         LinuxMusic Stack                            │
├──────────────────┬──────────────────────────────────────────────────┤
│  TUI (terminal)  │  ANSI 256-color  |  raw tty input  |  20fps      │
├──────────────────┼──────────────────────────────────────────────────┤
│  PlaybackEngine  │  Queue mgmt  |  autoplay  |  monitor thread      │
├──────────────────┼──────────────────────────────────────────────────┤
│  StreamResolver  │  Thread pool (4 workers)  |  background prefetch │
├──────────────────┼──────────────────────────────────────────────────┤
│  yt_backend      │  ytmusicapi (library)  |  yt-dlp (stream URL)    │
├──────────────────┼──────────────────────────────────────────────────┤
│  MPVController   │  UNIX socket IPC  |  JSON commands  |  no video  │
└──────────────────┴──────────────────────────────────────────────────┘
```

**Data flow:**

```
ytmusicapi          yt-dlp              mpv (slave)
    │                  │                    │
    ▼                  ▼                    ▼
Library/Search  →  CDN Stream URL  →  UNIX IPC Socket  →  ALSA  →  Speakers
```

---

## Features

| Feature | Detail |
|---|---|
| **Zero ads** | Stream URLs extracted directly from YouTube CDN — no player, no ad layer |
| **Zero telemetry** | No analytics, no crash reporting, no phoning home |
| **Low RAM** | `mpv --no-video` uses ~40–80 MB vs 300 MB+ for a browser tab |
| **Autoplay** | Continuous playback via `get_watch_playlist` recommendations |
| **Background prefetch** | `StreamResolver` resolves next track's URL while current track plays |
| **Personal library** | Full access to your YouTube Music playlists via `ytmusicapi` auth |
| **Search** | Search any song by name or paste a YouTube URL directly |
| **IPC control** | Full playback control (play/pause/skip/volume) via mpv JSON socket |
| **Non-blocking UI** | `select()` + raw `tty` — UI never freezes during URL resolution |
| **Signal-safe** | `SIGINT`/`SIGTERM` handlers clean up socket and mpv process |

---

## Prerequisites

| Dependency | Version | Install |
|---|---|---|
| `python3` | 3.10+ | `sudo apt install python3` |
| `mpv` | any recent | `sudo apt install mpv` |
| `yt-dlp` | 2024.1+ | `pip install yt-dlp` |
| `ytmusicapi` | 1.5+ | `pip install ytmusicapi` |
| `git` | any | `sudo apt install git` |

> **Linux users:** all of the above are in the default repos.

---

## Installation

```bash
# 1. Clone
git clone https://github.com/x0rkr/LinuxMusic.git
cd LinuxMusic

# 2. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Verify mpv is present
which mpv || sudo apt install mpv
```

### requirements.txt

```
yt-dlp>=2024.1.1
ytmusicapi>=1.5.0
```

---

## Authentication

LinuxMusic authenticates with YouTube Music using raw browser headers.
This gives it the same access level as your logged-in browser — your playlists,
liked songs, recommendations — without storing your password anywhere.

### Setup (one-time)

```bash
python3 -c "from ytmusicapi import YTMusic; YTMusic.setup(filepath='browser.json')"
```

You will see a prompt like this:

```
> Please paste the request headers from your browser below (press Enter twice when done):
```

**How to get your headers:**

1. Open [music.youtube.com](https://music.youtube.com) in any browser
2. Log in to your account
3. Open **DevTools** → **Network** tab (`F12`)
4. Click any request to `music.youtube.com`
5. Right-click → **Copy → Copy as cURL**
6. Paste the header block into the terminal prompt
7. Press `Enter` twice

This generates `browser.json` in your project directory. 

```bash
echo "browser.json" >> .gitignore
```

> **No auth / guest mode:** If `browser.json` is missing, LinuxMusic falls back to
> unauthenticated mode. Search still works. Personal library access is disabled.

---

## Usage

```bash
# Activate venv if you used one
source venv/bin/activate

# Launch
python3 linuxmusic.py
```

### Main Menu

```
╔════════════════════════════════════════════════════════════╗
║   🎧 DJ CONTROL PANEL 🎧                                   ║
╠════════════════════════════════════════════════════════════╣
║   [1]  🎵  LOAD PLAYLIST                                   ║
║   [2]  🔍  SEARCH & PLAY                                   ║
║   [3]  🎧  TOGGLE AUTOPLAY                                 ║
║   [4]  🚪  EXIT                                            ║
╚════════════════════════════════════════════════════════════╝
```

### Search example

```
▸ Select: 2
▸ Enter song name: Despacito
[*] Searching...
[✓] Found: Despacito-Official Music Video
    Starting playback...
```

You can also paste a direct YouTube URL:

```
▸ Enter song name: https://music.youtube.com/watch?v=xyz
```

### Playback controls

| Key | Action |
|---|---|
| `Space` | Play / Pause |
| `N` | Skip to next track |
| `+` / `=` | Volume up (+5%) |
| `-` | Volume down (-5%) |
| `A` | Toggle autoplay on/off |
| `Q` | Return to menu |

---

## How Autoplay Works

When autoplay is enabled, `QueueManager` runs a background fetcher thread that:

1. Calls `ytmusicapi.get_watch_playlist(videoId=current_track)` to get YouTube Music's
   own recommendation graph for the current song
2. Filters out recently played tracks (rolling window of 30 IDs)
3. Falls back to genre-based search (`"electronic dance music"`, `"house music"`, etc.)
   if recommendations are unavailable
4. Pre-resolves stream URLs via `StreamResolver` (4-worker thread pool) so the
   next track is ready before the current one ends

Result: **continuous gapless-ish playback with zero manual input.**

---

## How the Ad Bypass Works

YouTube serves audio and video as separate streams from its CDN.
The standard YouTube player loads ads by intercepting requests at the JS player layer.

LinuxMusic bypasses this entirely:

```
Normal path:  Browser → YouTube JS player → Ad server → CDN stream
LinuxMusic:   yt-dlp (Python API) → CDN stream URL → mpv → speakers
```

`yt-dlp` extracts the direct CDN URL using YouTube's own internal API.
`mpv` fetches the audio stream directly — there is no YouTube player involved,
so there is no hook for ads to attach to.

---

## IPC Architecture

`mpv` is launched with:

```bash
mpv --no-video --really-quiet \
    --input-ipc-server=/tmp/dj_mpv_<PID>.sock \
    --idle=yes \
    --volume=100
```

`MPVController` communicates via UNIX domain socket using mpv's JSON IPC protocol:

```python
# Load a stream URL
{"command": ["loadfile", "<cdn_url>", "replace"]}

# Get playback position
{"command": ["get_property", "time-pos"]}

# Toggle pause
{"command": ["cycle", "pause"]}
```

The socket is cleaned up on exit via `SIGINT`/`SIGTERM` handlers.

---

## File Structure

```
LinuxMusic/
├── linuxmusic.py      # Main app: TUI, MPVController, PlaybackEngine, QueueManager
├── yt_backend.py      # YTHandler: ytmusicapi + yt-dlp stream resolution
├── requirements.txt   # Python deps
├── browser.json       # Your auth headers (git-ignored, generated once)
└── README.md
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `mpv not found` | `sudo apt install mpv` |
| `No results found` | Update yt-dlp: `pip install -U yt-dlp` |
| `No playlists found` | Run the auth setup step — guest mode has no library access |
| `mpv IPC failed` | Socket collision — kill stale mpv: `pkill -f dj_mpv` |
| Audio but no sound | Check ALSA: `aplay -l` — verify your output device |
| `browser.json` invalid | Re-run `YTMusic.setup(filepath='browser.json')` with fresh headers |

### Debug log

All `yt-dlp` and `ytmusicapi` errors are printed inline before the TUI starts.
If the TUI is already running and something breaks, press `Q` to return to menu
— the error will print there.

---

## Security Note

`browser.json` contains authenticated session headers for your Google account.

- **Do not commit it.** It is in `.gitignore`.
- **Do not share it.** Treat it like a password.
- Headers expire naturally when your YouTube Music session expires.
  Re-run setup if library access stops working.

---

## Dev

```
x0rkr
github.com/x0rkr
```

Built for Linux. Works on Any OS.
No corporate involvement. No ads. No data collection.

---

*"The best music player is the one that gets out of the way."*
