#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                              ║
║     ██▓     ██▓ ███▄    █   █    ██  ██▓  ███▄ ▄███▓ █    ██  ██████  ██▓ ██████     ██▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█╗
║    ▓██▒    ▓██▒ ██ ▀█   █   ██  ▓██▒▓██▒ ▓██▒▀█▀ ██▒ ██  ▓██▒▒██    ▒ ▓██▒▒██    ▒    ██║ v1.0 DJ EDITION ██║
║    ▒██░    ▒██▒▓██  ▀█ ██▒ ▓██  ▒██░▒██▒ ▓██    ▓██░▓██  ▒██░░ ▓██▄   ▒██▒░ ▓██▄      ██║     CLUB MIX     ██║
║    ▒██░    ░██░▓██▒  ▐▌██▒ ▓▓█  ░██░░██░ ▒██    ▒██ ▓▓█  ░██░  ▒   ██▒░██░  ▒   ██▒   ██║   INFINITE BEAT  ██║
║    ░██████▒░██░▒██░   ▓██░ ▒▒█████▓ ░██░ ▒██▒   ░██▒▒▒█████▓ ▒██████▒▒░██░▒██████▒▒   ██║    NO ADS  ♪     ██║
║    ░ ▒░▓  ░░▓  ░ ▒░   ▒ ▒  ░▒▓▒ ▒ ▒ ░▓  ░ ▒░   ░  ░░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░░▓  ▒ ▒▓▒ ▒ ░   ██║  TERMINAL STUDIO  ██║
║    ░ ░ ▒  ░ ▒ ░░ ░░   ░ ▒░ ░░▒░ ░ ░  ▒ ░░  ░      ░░░▒░ ░ ░ ░ ░▒  ░ ░ ▒ ░░ ░▒  ░ ░   ██║   POWERED BY MPV   ██║
║      ░ ░    ▒ ░   ░   ░ ░   ░░░ ░ ░  ▒ ░░      ░    ░░░ ░ ░ ░  ░  ░   ▒ ░░  ░  ░     ██║   YT MUSIC API    ██║
║        ░  ░ ░           ░     ░      ░        ░      ░         ░     ░        ░     ██╚═══════════════════██║
║                                                                                                  ░          ██║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import json
import time
import threading
import queue
import signal
import subprocess
import socket
import random
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass, field
from collections import deque
import select
import tty
import termios

from yt_backend import YTHandler

# ═══════════════════════════════════════════════════════════════════════════════
# CLUB COLOR SYSTEM - NEON NIGHTCLUB THEME
# ═══════════════════════════════════════════════════════════════════════════════

class C:
    CLUB_RED     = '\033[38;5;196m'
    CLUB_BLUE    = '\033[38;5;51m'
    CLUB_GREEN   = '\033[38;5;46m'
    CLUB_YELLOW  = '\033[38;5;226m'
    CLUB_PURPLE  = '\033[38;5;129m'
    CLUB_PINK    = '\033[38;5;198m'
    CLUB_ORANGE  = '\033[38;5;208m'
    CLUB_CYAN    = '\033[38;5;87m'
    CLUB_GOLD    = '\033[38;5;220m'
    CLUB_SILVER  = '\033[38;5;250m'
    CLUB_HOTPINK = '\033[38;5;201m'
    
    BOLD        = '\033[1m'
    DIM         = '\033[2m'
    ITALIC      = '\033[3m'
    UNDERLINE   = '\033[4m'
    BLINK       = '\033[5m'
    
    END         = '\033[0m'

# ═══════════════════════════════════════════════════════════════════════════════
# BANNER / LOGO
# ═══════════════════════════════════════════════════════════════════════════════

BANNER = f"""
{C.CLUB_PURPLE}╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
{C.CLUB_PURPLE}║{C.END}                                                                                                              {C.CLUB_PURPLE}║
{C.CLUB_PURPLE}║{C.END}     {C.CLUB_PINK}██▓     ██▓ ███▄    █   █    ██  ██▓  ███▄ ▄███▓ █    ██  ██████  ██▓ ██████{C.END}     {C.CLUB_PURPLE}║
{C.CLUB_PURPLE}║{C.END}    {C.CLUB_CYAN}▓██▒    ▓██▒ ██ ▀█   █   ██  ▓██▒▓██▒ ▓██▒▀█▀ ██▒ ██  ▓██▒▒██    ▒ ▓██▒▒██    ▒{C.END}    {C.CLUB_PURPLE}║
{C.CLUB_PURPLE}║{C.END}    {C.CLUB_CYAN}▒██░    ▒██▒▓██  ▀█ ██▒ ▓██  ▒██░▒██▒ ▓██    ▓██░▓██  ▒██░░ ▓██▄   ▒██▒░ ▓██▄{C.END}      {C.CLUB_PURPLE}║
{C.CLUB_PURPLE}║{C.END}    {C.CLUB_CYAN}▒██░    ░██░▓██▒  ▐▌██▒ ▓▓█  ░██░░██░ ▒██    ▒██ ▓▓█  ░██░  ▒   ██▒░██░  ▒   ██▒{C.END}   {C.CLUB_PURPLE}║
{C.CLUB_PURPLE}║{C.END}    {C.CLUB_PINK}░██████▒░██░▒██░   ▓██░ ▒▒█████▓ ░██░ ▒██▒   ░██▒▒▒█████▓ ▒██████▒▒░██░▒██████▒▒{C.END}   {C.CLUB_PURPLE}║
{C.CLUB_PURPLE}║{C.END}    {C.CLUB_PINK}░ ▒░▓  ░░▓  ░ ▒░   ▒ ▒  ░▒▓▒ ▒ ▒ ░▓  ░ ▒░   ░  ░░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░░▓  ▒ ▒▓▒ ▒ ░{C.END}   {C.CLUB_PURPLE}║
{C.CLUB_PURPLE}║{C.END}    {C.CLUB_PINK}░ ░ ▒  ░ ▒ ░░ ░░   ░ ▒░ ░░▒░ ░ ░  ▒ ░░  ░      ░░░▒░ ░ ░ ░ ░▒  ░ ░ ▒ ░░ ░▒  ░ ░{C.END}   {C.CLUB_PURPLE}║
{C.CLUB_PURPLE}║{C.END}    {C.CLUB_PURPLE}  ░ ░    ▒ ░   ░   ░ ░   ░░░ ░ ░  ▒ ░░      ░    ░░░ ░ ░ ░  ░  ░   ▒ ░░  ░  ░{C.END}     {C.CLUB_PURPLE}║
{C.CLUB_PURPLE}║{C.END}    {C.CLUB_PURPLE}    ░  ░ ░           ░     ░      ░        ░      ░         ░     ░        ░{C.END}     {C.CLUB_PURPLE}║
{C.CLUB_PURPLE}║{C.END}                                                                                                              {C.CLUB_PURPLE}║
{C.CLUB_PURPLE}║{C.END}                           Dev: x0rkr | Handle: github.com/x0rkr                                         {C.CLUB_PURPLE}║
{C.CLUB_PURPLE}╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{C.END}
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CREDITS
# ═══════════════════════════════════════════════════════════════════════════════

CREDITS = f"""
{C.DIM}{'═' * 80}{C.END}
{C.CLUB_GOLD}  🎧  DEVELOPER    : {C.CLUB_CYAN}x0rkr{C.END}
{C.CLUB_GOLD}  🔗  GITHUB       : {C.CLUB_CYAN}github.com/x0rkr{C.END}
{C.CLUB_GOLD}  🎵  VERSION      : {C.CLUB_CYAN}DJ EDITION v1.0{C.END}
{C.CLUB_GOLD}  💿  ENGINE       : {C.CLUB_CYAN}YouTube Music API + MPV{C.END}
{C.CLUB_GOLD}  🔊  AUDIO        : {C.CLUB_CYAN}No Ads. Pure Audio.{C.END}
{C.DIM}{'═' * 80}{C.END}
"""

# ═══════════════════════════════════════════════════════════════════════════════
# VISUAL EFFECTS
# ═══════════════════════════════════════════════════════════════════════════════

class Visualizer:
    @staticmethod
    def equalizer(amplitude: float, width: int = 40) -> str:
        bars = int(amplitude * width)
        if bars > width:
            bars = width
        
        if amplitude > 0.7:
            color = C.CLUB_RED
        elif amplitude > 0.4:
            color = C.CLUB_YELLOW
        else:
            color = C.CLUB_GREEN
        
        bar_chars = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
        result = []
        for i in range(width):
            if i < bars:
                idx = min(int((i / width) * 8), 7)
                result.append(f"{color}{bar_chars[idx]}{C.END}")
            else:
                result.append(f"{C.DIM}░{C.END}")
        return ''.join(result)

# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Track:
    video_id: str
    title: str
    artist: str
    stream_url: Optional[str] = None
    duration: int = 0
    resolved: bool = False
    failed: bool = False
    source: str = "playlist"

@dataclass
class PlayerState:
    playlist_queue: List[Track] = field(default_factory=list)
    autoplay_queue: List[Track] = field(default_factory=list)
    history: deque = field(default_factory=lambda: deque(maxlen=50))
    recent_ids: deque = field(default_factory=lambda: deque(maxlen=30))
    current_track: Optional[Track] = None
    playlist_name: str = "DANCE FLOOR"
    autoplay_enabled: bool = True
    playing: bool = False
    volume: int = 100
    mode: str = "menu"
    shutdown: bool = False

# ═══════════════════════════════════════════════════════════════════════════════
# MPV IPC CONTROLLER
# ═══════════════════════════════════════════════════════════════════════════════

class MPVController:
    def __init__(self, socket_path: str):
        self.socket_path = socket_path
        self.sock: Optional[socket.socket] = None
        self._lock = threading.Lock()
    
    def connect(self, timeout: float = 15.0) -> bool:
        start = time.time()
        while time.time() - start < timeout:
            try:
                if os.path.exists(self.socket_path):
                    self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    self.sock.settimeout(2.0)
                    self.sock.connect(self.socket_path)
                    return True
            except:
                time.sleep(0.2)
        return False
    
    def _send_raw(self, cmd: dict) -> Optional[dict]:
        if not self.sock:
            return None
        with self._lock:
            try:
                msg = (json.dumps(cmd) + '\n').encode()
                self.sock.sendall(msg)
                response = b''
                try:
                    self.sock.settimeout(0.3)
                    chunk = self.sock.recv(4096)
                    if chunk:
                        response = chunk
                except socket.timeout:
                    pass
                if response:
                    return json.loads(response.decode().strip())
            except:
                pass
        return None
    
    def command(self, *args):
        cmd = {"command": list(args)}
        resp = self._send_raw(cmd)
        if resp and 'data' in resp:
            return resp['data']
        return None
    
    def play(self): self.command("set_property", "pause", False)
    def pause(self): self.command("set_property", "pause", True)
    def toggle_pause(self): self.command("cycle", "pause")
    def stop(self): self.command("stop")
    def loadfile(self, url: str): return self.command("loadfile", url, "replace")
    
    def get_pause(self) -> bool:
        r = self.command("get_property", "pause")
        return r if isinstance(r, bool) else False
    
    def get_time_pos(self) -> float:
        r = self.command("get_property", "time-pos")
        return float(r) if r else 0.0
    
    def get_duration(self) -> float:
        r = self.command("get_property", "duration")
        return float(r) if r else 0.0
    
    def get_volume(self) -> int:
        r = self.command("get_property", "volume")
        return int(r) if r else 100
    
    def set_volume(self, vol: int):
        self.command("set_property", "volume", max(0, min(100, vol)))
    
    def disconnect(self):
        if self.sock:
            try: self.sock.close()
            except: pass
            self.sock = None

# ═══════════════════════════════════════════════════════════════════════════════
# STREAM RESOLVER
# ═══════════════════════════════════════════════════════════════════════════════

class StreamResolver:
    def __init__(self, handler: YTHandler, pool_size: int = 4):
        self.handler = handler
        self.task_queue = queue.Queue()
        self.results: Dict[str, Track] = {}
        self._lock = threading.Lock()
        self.running = True
        for _ in range(pool_size):
            t = threading.Thread(target=self._worker, daemon=True)
            t.start()
    
    def resolve_async(self, track: Track):
        if track and track.video_id:
            self.task_queue.put(track)
    
    def resolve_sync(self, video_id: str, timeout: float = 15.0) -> Optional[Track]:
        start = time.time()
        while time.time() - start < timeout:
            with self._lock:
                if video_id in self.results and self.results[video_id].resolved:
                    return self.results[video_id]
            time.sleep(0.2)
        return None
    
    def _worker(self):
        while self.running:
            try:
                track = self.task_queue.get(timeout=1)
                if not track or not track.video_id:
                    self.task_queue.task_done()
                    continue
                with self._lock:
                    if track.video_id in self.results:
                        self.task_queue.task_done()
                        continue
                try:
                    url, title, duration = self.handler.get_stream_url(track.video_id)
                    with self._lock:
                        if url and title:
                            track.stream_url = url
                            track.title = title
                            track.duration = duration or 0
                            track.resolved = True
                        else:
                            track.failed = True
                        self.results[track.video_id] = track
                except:
                    with self._lock:
                        track.failed = True
                        self.results[track.video_id] = track
                self.task_queue.task_done()
            except queue.Empty:
                continue
            except:
                continue
    
    def stop(self):
        self.running = False

# ═══════════════════════════════════════════════════════════════════════════════
# QUEUE MANAGER WITH AUTOPLAY
# ═══════════════════════════════════════════════════════════════════════════════

class QueueManager:
    def __init__(self, handler: YTHandler, resolver: StreamResolver, state: PlayerState):
        self.handler = handler
        self.resolver = resolver
        self.state = state
        self._genres = [
            "electronic dance music", "house music", "techno", "trance", 
            "dubstep", "drum and bass", "club hits", "party mix",
            "edm festival", "bass boosted"
        ]
        self._autoplay_fetcher = None
    
    def add_playlist_tracks(self, tracks: List[Track]):
        for track in tracks:
            if track and track.video_id:
                self.state.playlist_queue.append(track)
                self.resolver.resolve_async(track)
    
    def get_next_track(self) -> Optional[Track]:
        # First play playlist tracks
        if self.state.playlist_queue:
            track = self.state.playlist_queue.pop(0)
            if track and not track.failed:
                return track
        
        # Then autoplay if enabled
        if self.state.autoplay_enabled and self.state.autoplay_queue:
            track = self.state.autoplay_queue.pop(0)
            if track and not track.failed:
                return track
        
        return None
    
    def has_tracks(self) -> bool:
        return bool(self.state.playlist_queue) or (self.state.autoplay_enabled and bool(self.state.autoplay_queue))
    
    def start_autoplay_fetcher(self, seed_video_id: str = ""):
        def fetcher():
            while not self.state.shutdown:
                try:
                    # Only fetch if autoplay is enabled and queue is low
                    if self.state.autoplay_enabled and len(self.state.autoplay_queue) < 5:
                        tracks = []
                        
                        # Try getting recommendations from current seed
                        if seed_video_id:
                            try:
                                watch_data = self.handler.ytmusic.get_watch_playlist(videoId=seed_video_id, limit=15)
                                if watch_data and 'tracks' in watch_data:
                                    for item in watch_data['tracks']:
                                        vid = item.get('videoId', '')
                                        if not vid or vid in self.state.recent_ids:
                                            continue
                                        title = item.get('title', 'Unknown')
                                        artists = item.get('artists', [])
                                        artist = artists[0].get('name', 'DJ Mix') if artists else 'DJ Mix'
                                        track = Track(video_id=vid, title=title, artist=artist, source="autoplay")
                                        tracks.append(track)
                                        self.state.recent_ids.append(vid)
                                        if len(tracks) >= 5:
                                            break
                            except:
                                pass
                        
                        # Fallback: random search
                        if len(tracks) < 2:
                            genre = random.choice(self._genres)
                            try:
                                search_data = self.handler.ytmusic.search(genre, filter="songs", limit=10)
                                if search_data:
                                    for item in search_data:
                                        vid = item.get('videoId', '')
                                        if not vid or vid in self.state.recent_ids:
                                            continue
                                        title = item.get('title', 'Unknown')
                                        artists = item.get('artists', [])
                                        artist = artists[0].get('name', 'Club Mix') if artists else 'Club Mix'
                                        track = Track(video_id=vid, title=title, artist=artist, source="autoplay")
                                        tracks.append(track)
                                        self.state.recent_ids.append(vid)
                                        if len(tracks) >= 5:
                                            break
                            except:
                                pass
                        
                        # Add to queue and resolve
                        for track in tracks:
                            self.resolver.resolve_async(track)
                            self.state.autoplay_queue.append(track)
                        
                        # Update seed for next fetch
                        if tracks:
                            seed_video_id = tracks[-1].video_id
                    
                    time.sleep(3)
                except:
                    time.sleep(4)
        
        self._autoplay_fetcher = threading.Thread(target=fetcher, daemon=True)
        self._autoplay_fetcher.start()

# ═══════════════════════════════════════════════════════════════════════════════
# PLAYBACK ENGINE (FIXED AUTOPLAY)
# ═══════════════════════════════════════════════════════════════════════════════

class PlaybackEngine:
    def __init__(self, mpv: MPVController, queue_manager: QueueManager, resolver: StreamResolver, state: PlayerState):
        self.mpv = mpv
        self.queue_manager = queue_manager
        self.resolver = resolver
        self.state = state
        self._monitor_thread: Optional[threading.Thread] = None
        self._playing = False
        self._position = 0.0
        self._duration = 0.0
        self._visual_amplitude = 0.0
    
    def start_playback(self, seed_tracks: List[Track] = None, playlist_name: str = "DANCE FLOOR"):
        if seed_tracks:
            self.queue_manager.add_playlist_tracks(seed_tracks)
        
        self.state.playlist_name = playlist_name
        self.state.mode = "playing"
        self._playing = True
        
        # Start autoplay fetcher
        self.queue_manager.start_autoplay_fetcher()
        
        # Start playing
        if self.queue_manager.has_tracks():
            self._play_next()
        
        if not self._monitor_thread or not self._monitor_thread.is_alive():
            self._start_monitor()
    
    def _play_next(self) -> bool:
        track = self.queue_manager.get_next_track()
        
        if not track:
            self._playing = False
            self.state.current_track = None
            return False
        
        # Wait for resolution if needed
        if not track.resolved and not track.failed:
            resolved = self.resolver.resolve_sync(track.video_id, timeout=12.0)
            if resolved and resolved.resolved:
                track = resolved
            else:
                track.failed = True
        
        if track.failed or not track.stream_url:
            return self._play_next()
        
        try:
            self.mpv.loadfile(track.stream_url)
            time.sleep(0.3)
            self.mpv.play()
            
            self._position = 0.0
            self._duration = float(track.duration) if track.duration > 0 else 0.0
            
            # Try to get actual duration if not available
            if self._duration <= 0:
                for _ in range(10):
                    time.sleep(0.2)
                    d = self.mpv.get_duration()
                    if d and d > 0:
                        self._duration = d
                        break
                if self._duration <= 0:
                    self._duration = 180.0
            
            self.state.current_track = track
            self.state.history.append(track)
            
            if track.video_id and track.video_id not in self.state.recent_ids:
                self.state.recent_ids.append(track.video_id)
            
            return True
        except:
            track.failed = True
            return self._play_next()
    
    def _start_monitor(self):
        def _monitor():
            beat_counter = 0
            last_position = 0.0
            stall_count = 0
            
            while not self.state.shutdown:
                try:
                    if self.state.mode == "playing" and self._playing and self.state.current_track:
                        pause = self.mpv.get_pause()
                        
                        if not pause:
                            pos = self.mpv.get_time_pos()
                            if pos and pos > 0:
                                self._position = pos
                            
                            dur = self.mpv.get_duration()
                            if dur and dur > 0:
                                self._duration = dur
                            
                            # Update visualizer
                            beat_counter = (beat_counter + 1) % 15
                            if beat_counter == 0:
                                self._visual_amplitude = random.uniform(0.3, 0.9)
                            else:
                                self._visual_amplitude = max(0.1, self._visual_amplitude * 0.93)
                            
                            # Check if song ended
                            remaining = self._duration - self._position
                            
                            # Auto-play next song when current ends (within 2 seconds of end)
                            if remaining <= 2.0 and remaining > -0.5:
                                if stall_count == 0:
                                    stall_count = 1
                                    # Schedule next track
                                    def play_next():
                                        time.sleep(0.5)
                                        if not self._play_next():
                                            self._playing = False
                                    threading.Thread(target=play_next, daemon=True).start()
                            else:
                                stall_count = 0
                    
                    time.sleep(0.1)
                except:
                    time.sleep(0.5)
        
        self._monitor_thread = threading.Thread(target=_monitor, daemon=True)
        self._monitor_thread.start()
    
    def get_playback_info(self) -> tuple:
        return (self._position, self._duration, self._visual_amplitude)
    
    def toggle_pause(self):
        try:
            self.mpv.toggle_pause()
        except:
            pass
    
    def skip_next(self):
        try:
            self.mpv.stop()
            time.sleep(0.2)
            if not self._play_next():
                self._playing = False
        except:
            pass
    
    def adjust_volume(self, delta: int):
        try:
            current = self.mpv.get_volume()
            new_vol = max(0, min(100, current + delta))
            self.mpv.set_volume(new_vol)
            self.state.volume = new_vol
        except:
            pass
    
    def toggle_autoplay(self):
        self.state.autoplay_enabled = not self.state.autoplay_enabled
        if not self.state.autoplay_enabled:
            self.state.autoplay_queue.clear()
    
    def stop(self):
        self._playing = False
        self.state.shutdown = True
        try: self.mpv.stop()
        except: pass

# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL UI
# ═══════════════════════════════════════════════════════════════════════════════

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def format_time(seconds: float) -> str:
    if seconds < 0: seconds = 0
    s = int(seconds)
    m, sec = s // 60, s % 60
    return f"{m:02d}:{sec:02d}"

def club_progress_bar(value: float, maximum: float, width: int = 52) -> str:
    if maximum <= 0:
        ratio = 0
    else:
        ratio = min(value / maximum, 1.0)
    
    filled = int(ratio * width)
    empty = width - filled
    
    gradient = [C.CLUB_RED, C.CLUB_ORANGE, C.CLUB_YELLOW, C.CLUB_GREEN, 
                C.CLUB_CYAN, C.CLUB_BLUE, C.CLUB_PURPLE, C.CLUB_PINK]
    
    bar = ""
    for i in range(filled):
        color_idx = int((i / width) * len(gradient))
        bar += f"{gradient[min(color_idx, len(gradient)-1)]}█{C.END}"
    bar += f"{C.DIM}{'░' * empty}{C.END}"
    return bar

def draw_club_hud(engine: PlaybackEngine):
    state = engine.state
    
    if state.mode != "playing":
        return
    
    track = state.current_track
    
    if not track:
        print(f"\n{C.DIM}╔{'═' * 80}╗{C.END}")
        print(f"║{C.CLUB_YELLOW}  🔄 LOADING NEXT TRACK...{C.END}{' ' * 56}║")
        print(f"{C.DIM}╚{'═' * 80}╝{C.END}")
        return
    
    position, duration, amplitude = engine.get_playback_info()
    
    if duration <= 0:
        duration = track.duration or 0
    
    paused = engine.mpv.get_pause() if engine.mpv else False
    volume = state.volume
    
    if not engine._playing:
        status = f"{C.CLUB_RED}⏹ STOPPED{C.END}"
    elif paused:
        status = f"{C.CLUB_YELLOW}⏸ PAUSED{C.END} {C.BLINK}◉{C.END}"
    else:
        status = f"{C.CLUB_GREEN}▶ PLAYING{C.END} {C.CLUB_GREEN}◉{C.END}"
    
    source_tag = f"{C.CLUB_HOTPINK}[AUTOPLAY]{C.END} 🎧" if track.source == "autoplay" else f"{C.CLUB_CYAN}[PLAYLIST]{C.END} 📀"
    ap_status = f"{C.CLUB_GREEN}🔴 LIVE{C.END}" if state.autoplay_enabled else f"{C.CLUB_RED}⚫ OFF{C.END}"
    
    vol_bars = int(volume / 20)
    vol_meter = f"{C.CLUB_GREEN}{'█' * vol_bars}{C.DIM}{'░' * (5 - vol_bars)}{C.END}"
    
    eq = Visualizer.equalizer(amplitude, 40)
    time_display = f"{C.CLUB_GOLD}{format_time(position)}{C.END} {C.DIM}/{C.END} {C.CLUB_SILVER}{format_time(duration)}{C.END}"
    progress = club_progress_bar(position, duration, 52)
    
    song_title = track.title[:58]
    song_artist = track.artist[:58]
    
    print(f"\n{C.CLUB_PURPLE}╔{'═' * 80}╗{C.END}")
    print(f"{C.CLUB_PURPLE}║{C.END}  {status}  {source_tag}  {C.CLUB_PURPLE}│{C.END}  {C.CLUB_CYAN}AUTOPLAY:{C.END} {ap_status}  {C.CLUB_PURPLE}│{C.END}  {C.CLUB_YELLOW}VOL:{C.END} {vol_meter} {volume}%  {C.CLUB_PURPLE}║{C.END}")
    print(f"{C.CLUB_PURPLE}╠{'═' * 80}╣{C.END}")
    print(f"{C.CLUB_PURPLE}║{C.END}  {C.BOLD}{C.CLUB_PINK}🎵 NOW SPINNING{C.END}  {C.CLUB_PURPLE}║{C.END}")
    print(f"{C.CLUB_PURPLE}║{C.END}  {C.CLUB_GOLD}{song_title}{C.END}{' ' * (78 - len(song_title))}{C.CLUB_PURPLE}║{C.END}")
    print(f"{C.CLUB_PURPLE}║{C.END}  {C.ITALIC}{C.CLUB_SILVER}{song_artist}{C.END}{' ' * (78 - len(song_artist))}{C.CLUB_PURPLE}║{C.END}")
    print(f"{C.CLUB_PURPLE}║{C.END}{' ' * 80}{C.CLUB_PURPLE}║{C.END}")
    print(f"{C.CLUB_PURPLE}║{C.END}  {progress}{C.CLUB_PURPLE}║{C.END}")
    print(f"{C.CLUB_PURPLE}║{C.END}  {time_display}{' ' * 65}{C.CLUB_PURPLE}║{C.END}")
    print(f"{C.CLUB_PURPLE}║{C.END}{' ' * 80}{C.CLUB_PURPLE}║{C.END}")
    print(f"{C.CLUB_PURPLE}║{C.END}  {C.CLUB_CYAN}🎚 EQ:{C.END} {eq}{C.CLUB_PURPLE}║{C.END}")
    print(f"{C.CLUB_PURPLE}║{C.END}{' ' * 80}{C.CLUB_PURPLE}║{C.END}")
    
    playlist_count = len(state.playlist_queue)
    autoplay_count = len(state.autoplay_queue)
    
    print(f"{C.CLUB_PURPLE}║{C.END}  {C.DIM}📋 QUEUE:{C.END} {C.CLUB_GREEN}{playlist_count}{C.END} tracks  {C.DIM}🎧 AUTOPLAY:{C.END} {C.CLUB_CYAN}{autoplay_count}{C.END} tracks{' ' * 35}{C.CLUB_PURPLE}║{C.END}")
    
    if state.playlist_queue:
        next_track = state.playlist_queue[0].title[:50]
        print(f"{C.CLUB_PURPLE}║{C.END}  {C.DIM}⏩ NEXT:{C.END} {next_track}{' ' * (70 - len(next_track))}{C.CLUB_PURPLE}║{C.END}")
    elif state.autoplay_queue and state.autoplay_enabled:
        next_track = state.autoplay_queue[0].title[:50]
        print(f"{C.CLUB_PURPLE}║{C.END}  {C.DIM}⏩ NEXT AUTOPLAY:{C.END} {C.CLUB_ORANGE}{next_track}{C.END}{' ' * (58 - len(next_track))}{C.CLUB_PURPLE}║{C.END}")
    
    print(f"{C.CLUB_PURPLE}║{C.END}{' ' * 80}{C.CLUB_PURPLE}║{C.END}")
    controls = f"{C.CLUB_GREEN}[SPACE]{C.END} PLAY/PAUSE  {C.CLUB_GREEN}[N]{C.END} SKIP  {C.CLUB_GREEN}[+/-]{C.END} VOL  {C.CLUB_GREEN}[A]{C.END} AUTOPLAY  {C.CLUB_GREEN}[Q]{C.END} MENU"
    print(f"{C.CLUB_PURPLE}║{C.END}  {controls}{' ' * (80 - len(controls) - 2)}{C.CLUB_PURPLE}║{C.END}")
    print(f"{C.CLUB_PURPLE}╚{'═' * 80}╝{C.END}")

def draw_club_menu(state: PlayerState):
    ap_status = "🔴 LIVE" if state.autoplay_enabled else "⚫ OFF"
    ap_color = C.CLUB_GREEN if state.autoplay_enabled else C.CLUB_RED
    
    print(f"\n{C.CLUB_CYAN}╔{'═' * 60}╗{C.END}")
    print(f"{C.CLUB_CYAN}║{C.END}   {C.BOLD}{C.CLUB_YELLOW}🎧 DJ CONTROL PANEL 🎧{C.END}{' ' * 32}{C.CLUB_CYAN}║{C.END}")
    print(f"{C.CLUB_CYAN}╠{'═' * 60}╣{C.END}")
    print(f"{C.CLUB_CYAN}║{C.END}                                                         {C.CLUB_CYAN}║{C.END}")
    print(f"{C.CLUB_CYAN}║{C.END}     {C.CLUB_GREEN}[1]{C.END}  🎵  LOAD PLAYLIST                         {C.CLUB_CYAN}║{C.END}")
    print(f"{C.CLUB_CYAN}║{C.END}     {C.CLUB_GREEN}[2]{C.END}  🔍  SEARCH & PLAY                        {C.CLUB_CYAN}║{C.END}")
    print(f"{C.CLUB_CYAN}║{C.END}     {C.CLUB_GREEN}[3]{C.END}  🎧  TOGGLE AUTOPLAY                      {C.CLUB_CYAN}║{C.END}")
    print(f"{C.CLUB_CYAN}║{C.END}     {C.CLUB_GREEN}[4]{C.END}  🚪  EXIT                                 {C.CLUB_CYAN}║{C.END}")
    print(f"{C.CLUB_CYAN}║{C.END}                                                         {C.CLUB_CYAN}║{C.END}")
    print(f"{C.CLUB_CYAN}╠{'═' * 60}╣{C.END}")
    print(f"{C.CLUB_CYAN}║{C.END}     {C.DIM}AUTOPLAY STATUS:{C.END} {ap_color}{ap_status}{C.END}{' ' * 33}{C.CLUB_CYAN}║{C.END}")
    print(f"{C.CLUB_CYAN}╚{'═' * 60}╝{C.END}")
    print(f"\n{C.CLUB_PURPLE}▸ SELECT:{C.END} ", end='', flush=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PLAYBACK LOOP
# ═══════════════════════════════════════════════════════════════════════════════

def playback_loop(engine: PlaybackEngine):
    engine.state.mode = "playing"
    
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    
    try:
        tty.setcbreak(fd)
        
        while engine.state.mode == "playing" and not engine.state.shutdown:
            clear_screen()
            print(BANNER)
            draw_club_hud(engine)
            
            ready, _, _ = select.select([sys.stdin], [], [], 0.1)
            if ready:
                try:
                    ch = sys.stdin.read(1).lower()
                except:
                    ch = ''
                
                if ch == ' ':
                    engine.toggle_pause()
                elif ch == 'n':
                    engine.skip_next()
                elif ch in ('+', '='):
                    engine.adjust_volume(5)
                elif ch == '-':
                    engine.adjust_volume(-5)
                elif ch == 'a':
                    engine.toggle_autoplay()
                elif ch == 'q':
                    engine.state.mode = "menu"
                    break
            
            time.sleep(0.1)
    
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    
    engine.state.mode = "menu"

# ═══════════════════════════════════════════════════════════════════════════════
# UI HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

def browse_playlists(handler: YTHandler, queue_manager: QueueManager, engine: PlaybackEngine):
    clear_screen()
    print(BANNER)
    print(f"\n{C.CLUB_YELLOW}╔{'═' * 50}╗{C.END}")
    print(f"{C.CLUB_YELLOW}║{C.END}  {C.BOLD}{C.CLUB_PINK}🎵 YOUR PLAYLISTS 🎵{C.END}{' ' * 27}{C.CLUB_YELLOW}║{C.END}")
    print(f"{C.CLUB_YELLOW}╚{'═' * 50}╝{C.END}")
    
    try:
        playlists = handler.get_playlists()
        if not playlists:
            print(f"\n{C.CLUB_RED}[!] No playlists found.{C.END}")
            input(f"\n{C.DIM}Press Enter...{C.END}")
            return
        
        print()
        for i, pl in enumerate(playlists, 1):
            print(f"  {C.CLUB_CYAN}[{i}]{C.END} {C.CLUB_GOLD}{pl.get('title', 'Untitled')[:50]}{C.END}")
        
        print(f"\n{C.DIM}[0] Back{C.END}")
        print(f"\n{C.CLUB_PURPLE}▸ Select playlist:{C.END} ", end='', flush=True)
        
        choice = input().strip()
        if choice == '0' or not choice:
            return
        
        idx = int(choice) - 1
        if 0 <= idx < len(playlists):
            selected = playlists[idx]
            load_playlist(handler, queue_manager, engine, selected.get('playlistId', ''), selected.get('title', 'Playlist'))
    except ValueError:
        print(f"\n{C.CLUB_RED}[!] Invalid choice{C.END}")
        time.sleep(1)
    except Exception as e:
        print(f"\n{C.CLUB_RED}[!] Error: {str(e)[:60]}{C.END}")
        time.sleep(1)

def load_playlist(handler: YTHandler, queue_manager: QueueManager, engine: PlaybackEngine, playlist_id: str, title: str):
    if not playlist_id:
        return
    
    clear_screen()
    print(BANNER)
    print(f"\n{C.CLUB_CYAN}╔{'═' * 50}╗{C.END}")
    print(f"{C.CLUB_CYAN}║{C.END}  {C.CLUB_YELLOW}📀 LOADING PLAYLIST...{C.END}{' ' * 24}{C.CLUB_CYAN}║{C.END}")
    print(f"{C.CLUB_CYAN}╚{'═' * 50}╝{C.END}")
    print(f"\n{C.CLUB_PURPLE}🎵 {C.CLUB_GOLD}{title}{C.END}")
    
    try:
        raw = handler.get_playlist_tracks(playlist_id)
        if not raw:
            print(f"\n{C.CLUB_RED}[!] Empty playlist.{C.END}")
            time.sleep(2)
            return
        
        tracks = []
        for t in raw:
            vid = t.get('videoId', '')
            if not vid: continue
            track = Track(video_id=vid, title=t.get('title', 'Unknown'), artist=t.get('artist', 'Unknown'), source="playlist")
            tracks.append(track)
        
        if not tracks:
            print(f"\n{C.CLUB_RED}[!] No valid tracks.{C.END}")
            time.sleep(2)
            return
        
        print(f"\n{C.CLUB_GREEN}✓ Loaded {len(tracks)} tracks{C.END}")
        print(f"{C.DIM}Starting DJ session...{C.END}")
        time.sleep(1)
        
        engine.start_playback(tracks, title.upper())
        playback_loop(engine)
    except Exception as e:
        print(f"\n{C.CLUB_RED}[!] Error: {str(e)[:60]}{C.END}")
        time.sleep(2)

def search_stream(handler: YTHandler, queue_manager: QueueManager, engine: PlaybackEngine):
    clear_screen()
    print(BANNER)
    print(f"\n{C.CLUB_GREEN}╔{'═' * 50}╗{C.END}")
    print(f"{C.CLUB_GREEN}║{C.END}  {C.BOLD}{C.CLUB_PINK}🔍 SEARCH & PLAY 🔍{C.END}{' ' * 24}{C.CLUB_GREEN}║{C.END}")
    print(f"{C.CLUB_GREEN}╚{'═' * 50}╝{C.END}")
    print(f"\n{C.CLUB_PURPLE}▸ Enter song name:{C.END} ", end='', flush=True)
    query = input(f"{C.CLUB_CYAN}").strip()
    
    if not query:
        return
    
    print(f"\n{C.CLUB_YELLOW}[*] Searching...{C.END}")
    
    try:
        url, title, duration = handler.search_and_get_stream(query)
        if not url:
            print(f"{C.CLUB_RED}[!] No results found.{C.END}")
            time.sleep(2)
            return
        
        print(f"{C.CLUB_GREEN}[✓] Found: {title[:50]}{C.END}")
        time.sleep(0.5)
        
        track = Track(video_id=f"search_{int(time.time())}", title=title or "Unknown", artist="Request", stream_url=url, resolved=True, duration=duration or 0, source="playlist")
        engine.start_playback([track], "NOW PLAYING")
        playback_loop(engine)
    except Exception as e:
        print(f"{C.CLUB_RED}[!] Error: {str(e)[:60]}{C.END}")
        time.sleep(2)

def shutdown(engine: Optional[PlaybackEngine] = None):
    clear_screen()
    print(BANNER)
    print(CREDITS)
    print(f"\n{C.CLUB_PURPLE}╔{'═' * 50}╗{C.END}")
    print(f"{C.CLUB_PURPLE}║{C.END}     {C.CLUB_YELLOW}👋 THANKS FOR SPINNING! 👋{C.END}{' ' * 12}{C.CLUB_PURPLE}║{C.END}")
    print(f"{C.CLUB_PURPLE}║{C.END}     {C.DIM}DJ System Shutting Down...{C.END}{' ' * 15}{C.CLUB_PURPLE}║{C.END}")
    print(f"{C.CLUB_PURPLE}╚{'═' * 50}╝{C.END}")
    if engine: engine.stop()
    sys.exit(0)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    if subprocess.run(["which", "mpv"], capture_output=True).returncode != 0:
        clear_screen()
        print(BANNER)
        print(f"\n{C.CLUB_RED}[!] mpv required: sudo apt install mpv{C.END}")
        sys.exit(1)
    
    try:
        handler = YTHandler("browser.json")
    except Exception as e:
        clear_screen()
        print(BANNER)
        print(f"\n{C.CLUB_RED}[!] Backend error: {e}{C.END}")
        sys.exit(1)
    
    socket_path = f"/tmp/dj_mpv_{os.getpid()}.sock"
    
    try:
        proc = subprocess.Popen(
            ["mpv", "--no-video", "--really-quiet", f"--input-ipc-server={socket_path}", "--idle=yes", "--volume=100"],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except:
        print(f"{C.CLUB_RED}[!] Cannot start mpv{C.END}")
        sys.exit(1)
    
    mpv = MPVController(socket_path)
    if not mpv.connect():
        print(f"{C.CLUB_RED}[!] mpv IPC failed{C.END}")
        proc.terminate()
        sys.exit(1)
    
    resolver = StreamResolver(handler)
    state = PlayerState()
    state.autoplay_enabled = True
    queue_manager = QueueManager(handler, resolver, state)
    engine = PlaybackEngine(mpv, queue_manager, resolver, state)
    
    def cleanup(sig=None, frame=None):
        try:
            engine.stop()
            mpv.disconnect()
            proc.terminate()
            proc.wait(timeout=2)
        except:
            try: proc.kill()
            except: pass
        if os.path.exists(socket_path):
            try: os.unlink(socket_path)
            except: pass
        sys.exit(0)
    
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    
    while True:
        try:
            clear_screen()
            print(BANNER)
            print(CREDITS)
            print(f"\n  {C.CLUB_GREEN}💿 SYSTEM READY{C.END}  {C.CLUB_CYAN}🎧 AUTOPLAY: {'ON' if state.autoplay_enabled else 'OFF'}{C.END}  {C.CLUB_YELLOW}🔊 VOL: {state.volume}%{C.END}")
            draw_club_menu(state)
            
            choice = input().strip().lower()
            
            if choice == '1':
                browse_playlists(handler, queue_manager, engine)
            elif choice == '2':
                search_stream(handler, queue_manager, engine)
            elif choice == '3':
                state.autoplay_enabled = not state.autoplay_enabled
                clear_screen()
                print(BANNER)
                print(CREDITS)
                print(f"\n{C.CLUB_GREEN}✓ Autoplay: {'ON' if state.autoplay_enabled else 'OFF'}{C.END}")
                time.sleep(1)
            elif choice in ('4', 'q', 'quit', 'exit'):
                cleanup()
        except KeyboardInterrupt:
            cleanup()
        except Exception as e:
            print(f"\n{C.CLUB_RED}[!] {str(e)[:80]}{C.END}")
            time.sleep(2)

if __name__ == "__main__":
    main()