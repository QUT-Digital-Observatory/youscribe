"""
Copyright: Digital Observatory 2023 <digitalobservatory@qut.edu.au>
Author: Mat Bettinson <mat.bettinson@qut.edu.au>, Boyd Nguyen <thaihoang.nguyen@qut.edu.au>
"""

import logging
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from faster_whisper import WhisperModel
from faster_whisper.transcribe import Segment

from .transcript import WhisperTranscript

logger = logging.getLogger(__name__)

MODEL_SIZE = [
    "tiny",
    "tiny.en",
    "base",
    "base.en",
    "small",
    "small.en",
    "medium",
    "medium.en",
    "large-v1",
    "large-v2",
    "large-v3",
    "large",
]

DEVICE = ["cpu", "cuda", "auto"]

COMPUTE_STYLE = [
    "int8",
    "int8_float32",
    "int8_float16",
    "int8_bfloat16",
    "int16",
    "float16",
    "bfloat16",
    "float32",
]


class TranscriptionError(Exception):
    pass


class BaseTranscriber(ABC):
    @abstractmethod
    def transcribe(self, file, **kwargs) -> Any:
        pass


class WhisperTranscriber(BaseTranscriber):
    def __init__(
        self,
        model_size: str = "small",
        cpu_threads: int = 4,
        device: str = "cpu",
        device_index: int | list[int] = 0,
        compute_style: str = "int8",
        num_workers: int = 1,
    ):
        """Initialise the Whisper model

        Parameters
        ----------
        model_size : str, optional
            Size of the model to use (tiny, tiny.en, base, base.en,
            small, small.en, medium, medium.en, large-v1, large-v2,
            large-v3, or large), by default "small"
        cpu_threads : int, optional
            Number of threads to use when running on CPU, by default 4
        device : str, optional
            Device to use for computation ("cpu", "cuda", "auto"), by default "cpu"
        device_index : int | list[int], optional
            Device ID to use.
            The model can also be loaded on multiple GPUs by passing a list of IDs
            (e.g. [0, 1, 2, 3]).
            In that case, multiple transcriptions can run in parallel
            when transcribe() is called from multiple Python threads
            (see also num_workers), by default 0
        compute_style : str, optional
            Type to use for computation ("int8", "int8_float32", "int8_float16",
            "int8_bfloat16", "int16", "float16",
            "bfloat16", "float32"), by default "int8"
        num_workers : int, optional
            When transcribe() is called from multiple Python threads,
            having multiple workers enables true parallelism when
            running the model, by default 1

        Raises
        ------
        ValueError
            If model_size is not one of the acceptable values
        ValueError
            If device is not one of the acceptable values
        ValueError
            If compute_style is not one of the acceptable values
        """
        if model_size not in MODEL_SIZE:
            raise ValueError(f"model_name must be one of {MODEL_SIZE}")
        if device not in DEVICE:
            raise ValueError(f"device must be one of {DEVICE}")
        if compute_style not in COMPUTE_STYLE:
            raise ValueError(f"compute_style must be one of {COMPUTE_STYLE}")

        self._model = WhisperModel(
            model_size_or_path=model_size,
            device=device,
            device_index=device_index,
            cpu_threads=cpu_threads,
            compute_type=compute_style,
            num_workers=num_workers,
        )

    def transcribe(
        self, file: str | Path, prompt: str | None = None, vad_filter=True
    ) -> WhisperTranscript:
        """Transcribe an audio

        Parameters
        ----------
        file : str | Path
            Path to the audio file
        prompt : str | None, optional
            Optional text string or iterable of token ids to provide as a
            prompt for the first window, by default None
        vad_filter : bool, optional
            Enable the voice activity detection (VAD) to filter out parts of the audio
            without speech., by default True

        Raises
        ------
        TranscriptionError
            If nothing is returned, raise TranscriptionError.
        """
        segments, info = self._model.transcribe(
            file, initial_prompt=prompt, vad_filter=vad_filter  # type: ignore
        )

        if not segments and not info:
            raise TranscriptionError("Nothing was transcribed.")

        logger.info(
            f"Transcription completed. Language: {info.language}. Probability: {info.language_probability}. Duration: {info.duration}"
        )

        return WhisperTranscript(segments)
