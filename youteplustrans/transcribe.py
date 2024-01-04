"""
Copyright: Digital Observatory 2023 <digitalobservatory@qut.edu.au>
Author: Mat Bettinson <mat.bettinson@qut.edu.au>
"""
import logging
from datetime import timedelta
from os import path, remove
from time import time

from yt_dlp import YoutubeDL

from youteplustrans.scraper import get_VideoDetails
from youteplustrans.whisper import ShortSegment, WhisperTranscribe

logger = logging.getLogger(__name__)


class YouteTranscriber:
    def __init__(self, url: str, model: str = "small", cpu_threads: int = 4):
        self.url = url
        self.model = model
        self.threads = cpu_threads

    def _get_elapsed(self, start: float, end: float) -> str:
        return str(timedelta(seconds=round(end - start)))

    def transcribe(self) -> list[ShortSegment] | None:
        """Execute the transcription job, saving output as appropriate"""
        starttime = time()
        videodetails = get_VideoDetails(self.url)
        if videodetails is None:
            logger.error("Failed to get video details")
            return None
        logger.info("Got metadata in", self._get_elapsed(starttime, time()))

        prompt = (
            videodetails.title + ": " + videodetails.shortDescription
        )  # Will feed to Whisper API
        ydl_opts = {"format": "worstaudio[ext=webm]", "outtmpl": "%(id)s.%(ext)s"}
        sourcefilename = videodetails.videoId + ".webm"

        if not path.isfile(sourcefilename):
            starttime = time()
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            logger.info("Downloaded in", self._get_elapsed(starttime, time()))
        # <id>.webm in the current directory now

        starttime = time()
        logger.info("Transcribing...")
        transcriber = WhisperTranscribe(
            sourcefilename, prompt, self.model, cpu_threads=self.threads
        )
        logger.info("Whisper transcribed in", self._get_elapsed(starttime, time()))

        remove(sourcefilename)
        return transcriber.segments
