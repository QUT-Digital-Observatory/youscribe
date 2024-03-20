"""
Copyright: Digital Observatory 2023 <digitalobservatory@qut.edu.au>
Author: Mat Bettinson <mat.bettinson@qut.edu.au>
"""

import logging
from datetime import timedelta
from os import path, remove
from time import time

from yt_dlp import YoutubeDL

from .scraper import get_video_details
from .whisper import ShortSegment, WhisperTranscribe

logger = logging.getLogger(__name__)


class Youscribe:
    def __init__(self, url: str, model: str = "small", cpu_threads: int = 4):
        """Initiliase Youscribe class and specify the model for Whisper transcription

        Parameters
        ----------
        url : str
            _description_
        model : str, optional
            _description_, by default "small"
        cpu_threads : int, optional
            _description_, by default 4
        """
        self.url = url
        self.model = model
        self.threads = cpu_threads

    def _get_elapsed(self, start: float, end: float) -> str:
        return str(timedelta(seconds=round(end - start)))

    def transcribe(self) -> list[ShortSegment] | None:
        """Execute the transcription job, saving output as appropriate"""
        start_time = time()
        video_details = get_video_details(self.url)
        if video_details is None:
            logger.error("Failed to get video details")
            return None
        logger.info("Got metadata in" + self._get_elapsed(start_time, time()))

        prompt = (
            video_details.title + ": " + video_details.shortDescription
        )  # Will feed to Whisper API
        ydl_opts = {"format": "worstaudio[ext=webm]", "outtmpl": "%(id)s.%(ext)s"}
        source_file = video_details.videoId + ".webm"

        if not path.isfile(source_file):
            start_time = time()
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            logger.info("Downloaded in" + self._get_elapsed(start_time, time()))
        # <id>.webm in the current directory now

        start_time = time()
        logger.info("Transcribing...")
        transcriber = WhisperTranscribe(
            source_file, prompt, self.model, cpu_threads=self.threads
        )
        logger.info("Whisper transcribed in" + self._get_elapsed(start_time, time()))

        remove(source_file)
        return transcriber.segments
