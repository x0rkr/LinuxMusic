#!/usr/bin/env python3
"""
yt_backend.py - YouTube Music backend for LinuxMusic v4.0
Handles authentication, playlist fetching, and stream URL extraction.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yt_dlp
from ytmusicapi import YTMusic

logger = logging.getLogger(__name__)


class YTHandler:
    """Handles YouTube Music authentication and stream extraction."""

    def __init__(self, browser_file: str = "browser.json"):
        """
        Initialize YouTube Music handler with authentication.

        Args:
            browser_file: Path to browser.json with authentication headers
        """
        self.browser_file = Path(browser_file)
        self.ytmusic = None
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate with YouTube Music using browser.json."""
        if not self.browser_file.exists():
            raise FileNotFoundError(
                f"browser.json not found at {self.browser_file.absolute()}. "
                "Required for YouTube Music API access."
            )

        try:
            self.ytmusic = YTMusic(str(self.browser_file))
            logger.info("YouTube Music authentication successful")
        except Exception as e:
            raise RuntimeError(
                f"Failed to authenticate with YouTube Music: {e}"
            ) from e

    def get_playlists(self) -> List[Dict[str, str]]:
        """
        Fetch all user playlists.

        Returns:
            List of dicts with 'title' and 'playlistId' keys
        """
        if not self.ytmusic:
            raise RuntimeError("YTMusic not initialized. Call _authenticate() first.")

        try:
            playlists = self.ytmusic.get_library_playlists(limit=None)
            return [
                {
                    "title": playlist.get("title", "Untitled Playlist"),
                    "playlistId": playlist.get("playlistId", ""),
                }
                for playlist in playlists
                if playlist.get("playlistId")
            ]
        except Exception as e:
            logger.error(f"Failed to fetch playlists: {e}")
            return []

    def get_playlist_tracks(self, playlist_id: str) -> List[Dict[str, str]]:
        """
        Get tracks from a specific playlist.

        Args:
            playlist_id: YouTube Music playlist ID

        Returns:
            List of dicts with 'videoId', 'title', 'artist' keys
        """
        if not self.ytmusic:
            raise RuntimeError("YTMusic not initialized.")

        try:
            playlist_data = self.ytmusic.get_playlist(playlist_id, limit=None)
            tracks = []
            for track in playlist_data.get("tracks", []):
                video_id = track.get("videoId")
                if video_id:
                    tracks.append(
                        {
                            "videoId": video_id,
                            "title": track.get("title", "Unknown"),
                            "artist": ", ".join(
                                artist.get("name", "")
                                for artist in track.get("artists", [])
                            )
                            or "Unknown Artist",
                        }
                    )
            return tracks
        except Exception as e:
            logger.error(f"Failed to fetch playlist tracks: {e}")
            return []

    @staticmethod
    def get_stream_url(video_id: str) -> Tuple[Optional[str], Optional[str], Optional[int]]:
        """
        Extract direct audio stream URL for a video ID using yt-dlp.
        Bypasses YouTube web player for ad-free playback.

        Args:
            video_id: YouTube video ID

        Returns:
            Tuple of (stream_url, title, duration_sec) or (None, None, None) on failure
        """
        url = f"https://www.youtube.com/watch?v={video_id}"

        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "socket_timeout": 20,
            "nocheckcertificate": True,
            "extract_flat": False,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            if not info:
                logger.error(f"No info returned for video ID: {video_id}")
                return None, None, None

            title = info.get("title", "Unknown Title")
            duration = int(info.get("duration") or 0)

            # Extract best audio stream URL
            stream_url = info.get("url", "")
            if not stream_url:
                formats = info.get("formats") or []
                # Prefer audio-only streams, pick highest bitrate
                audio_streams = [
                    f for f in formats
                    if f.get("vcodec") == "none" and f.get("url")
                ]
                if audio_streams:
                    best = max(
                        audio_streams,
                        key=lambda f: float(f.get("abr") or f.get("tbr") or 0)
                    )
                    stream_url = best["url"]
                elif formats:
                    stream_url = formats[-1].get("url", "")

            if not stream_url:
                logger.error(f"No playable URL found for video ID: {video_id}")
                return None, None, None

            return stream_url, title, duration

        except yt_dlp.utils.DownloadError as e:
            if "signature" in str(e).lower():
                logger.error(f"Signature extraction failed for {video_id}: {e}")
            elif "geo" in str(e).lower() or "blocked" in str(e).lower():
                logger.error(f"Geographic restriction for {video_id}: {e}")
            else:
                logger.error(f"Download error for {video_id}: {e}")
            return None, None, None

        except Exception as e:
            logger.error(f"Unexpected error extracting stream for {video_id}: {e}")
            return None, None, None

    def search_and_get_stream(self, query: str) -> Tuple[Optional[str], Optional[str], Optional[int]]:
        """
        Search YouTube Music and get stream URL for first result.

        Args:
            query: Search query string

        Returns:
            Tuple of (stream_url, title, duration_sec) or (None, None, None) on failure
        """
        # Use yt-dlp's built-in search for direct resolution
        search_query = f"ytsearch1:{query}"

        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "socket_timeout": 20,
            "nocheckcertificate": True,
            "extract_flat": False,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=False)

            if not info or "entries" not in info:
                logger.error(f"No search results for: {query}")
                return None, None, None

            entry = info["entries"][0]
            video_id = entry.get("id", "")

            if video_id:
                return self.get_stream_url(video_id)
            else:
                logger.error(f"No video ID in search result for: {query}")
                return None, None, None

        except Exception as e:
            logger.error(f"Search failed for '{query}': {e}")
            return None, None, None


# Convenience function for backward compatibility with existing code
def resolve_stream_url(query: str) -> Tuple[str, str, int]:
    """
    Resolve a search query or URL to a stream URL.
    Maintains compatibility with existing linuxmusic.py code.

    Args:
        query: Search term or YouTube URL

    Returns:
        Tuple of (stream_url, title, duration_sec)

    Raises:
        ValueError: If resolution fails
    """
    handler = YTHandler("browser.json")

    is_url = query.startswith("http://") or query.startswith("https://")
    if is_url:
        # Extract video ID from URL
        if "watch?v=" in query:
            video_id = query.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in query:
            video_id = query.split("youtu.be/")[1].split("?")[0]
        else:
            raise ValueError(f"Cannot extract video ID from URL: {query}")

        url, title, duration = handler.get_stream_url(video_id)
    else:
        url, title, duration = handler.search_and_get_stream(query)

    if not url:
        raise ValueError(f"Failed to resolve stream for: {query}")

    return url, title, duration
