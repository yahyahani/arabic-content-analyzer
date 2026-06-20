"""
Download audio van een YouTube video met yt-dlp.
"""
import yt_dlp
from pathlib import Path
from app.config import settings


def download_audio(youtube_url: str, job_id: str) -> tuple[str, str]:
    """
    Download de audio van een YouTube video als mp3.

    Returns:
        (audio_path, video_title)
    """
    output_template = str(settings.storage_dir / f"{job_id}.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        video_title = info.get("title", "Onbekende titel")

    audio_path = str(settings.storage_dir / f"{job_id}.mp3")

    if not Path(audio_path).exists():
        raise FileNotFoundError(
            f"Audio download mislukt, bestand niet gevonden op: {audio_path}"
        )

    return audio_path, video_title
