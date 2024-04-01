import pytest
from yt_dlp.utils import DownloadError

from src.youscribe import transcribe


@pytest.fixture()
def urls() -> dict[str, str]:
    urls = {
        "valid": "https://www.youtube.com/watch?v=-c4CNB80SRc",
        "invalid": "https://pywb.readthedocs.io/en/latest/",
    }
    return urls


def test_transcribe(urls):
    test_transcription = transcribe(url=urls["valid"])
    assert test_transcription

    transcription_text = test_transcription.text()

    assert transcription_text
    assert len(transcription_text) > 50

    assert test_transcription.json()
    assert len(test_transcription.json()) > 5  # type: ignore
    assert test_transcription.srt()


def test_transcribe_invalid(urls):
    with pytest.raises(DownloadError):
        test_transcription = transcribe(url=urls["invalid"])
