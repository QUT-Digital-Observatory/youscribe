"""
Copyright: Digital Observatory 2023 <digitalobservatory@qut.edu.au>
Author: Mat Bettinson <mat.bettinson@qut.edu.au>
"""

import logging
import random
import string
from datetime import timedelta
from os import path, remove
from pathlib import Path
from time import time
from typing import Optional

from yt_dlp import YoutubeDL

from .scraper import VideoDetails, get_video_details
from .transcriber import BaseTranscriber, WhisperTranscriber
from .transcript import BaseTranscript

logger = logging.getLogger()


def transcribe(
    url: str,
    transcriber: BaseTranscriber = WhisperTranscriber(),
    prompt: str | bool | None = None,
    **kwargs,
) -> BaseTranscript:
    """Transcribe a YouTube video

    The function first downloads the audio of the video,
    then pass to the transcriber to do the transcription.

    Parameters
    ----------
    url : str
        Full URL of the YouTube video
    transcriber : BaseTranscriber, optional
        Any subclass of BaseTranscriber, by default WhisperTranscriber()
    prompt : str | bool | None, optional
        The prompt to be put to the transcription model,
        if None, use video title and description as prompt,
        if False, prompt will not be added,
        by default None

    Returns
    -------
    BaseTranscript
    """
    meta = _get_metadata(url)

    if prompt is None:
        logger.info("No prompt provided, using video title and description as prompt")
        if meta:
            prompt = meta.title + ": " + meta.shortDescription
    elif prompt == False:
        logger.info("prompt is set to False. No prompt is used")
        prompt = None

    if meta and meta.title:
        file_name = f"{meta.videoId}.webm"
    else:
        random_name = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        file_name = f"{random_name}.webm"

    _download_audio(url, file_name)

    start_time = time()
    transcript = transcriber.transcribe(file_name, prompt=prompt, **kwargs)

    logger.info(f"Transcription finished in {_get_duration(start_time, time())}")

    remove(file_name)

    return transcript


def _get_metadata(url: str) -> VideoDetails | None:
    start_time = time()
    video_details = get_video_details(url)

    if video_details is None:
        logger.warning("Failed to get video details")
        return None

    logger.info("Got metadata in" + str(timedelta(seconds=round(time() - start_time))))
    return video_details


def _download_audio(url: str, file: str | Path, opts: Optional[dict] = None):
    if not opts:
        ydl_opts = {"format": "worstaudio[ext=webm]", "outtmpl": "%(id)s.%(ext)s"}

    if not path.isfile(file):
        start_time = time()

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download(url)
        except Exception as e:
            raise e

        logger.info(f"{file} downloaded in {_get_duration(start_time, time())}")
    else:
        raise FileExistsError(f"{Path(file).resolve()} already exists.")


def _get_duration(start, end):
    return str(timedelta(seconds=round(end - start)))
