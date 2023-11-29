# Transcriber for Youte+

This is a spin of youtalk, the CLI tool for transcribing YouTube videos. This version is designed to work with the Youte+ web app. It has these changes:

1. Adopts faster_whisperer, a cTransformer's based model for faster transcription.
2. Uses CPU only, and medium sized 8-bit quant models.
3. Doesn't have the file caching, downloading, and file output features.

## Usage

```python
from youteplustrans.transcriber import YouteTranscriber

# Set model to medium, and 3 CPU threads
transcriber = YouteTranscriber(
    "https://www.youtube.com/watch?v=9bZkp7q19f0",
    "medium",
    3)
# Get a list of ShortSegment NamedTuples
segments = transcriber.transcribe()
for segment of segments:
    print(f"id: {segment.id}, start: {segment.start}, end: {segment.end}, text: {segment.text}")
```
## data format

```python
class ShortSegment(NamedTuple):
    id: int
    start: float
    end: float
    text: str
```

## Performance/deployment

4 core beefy CPU transcribes at about 3.5X realtime. The on-disk model is around 1.5GB for medium.

I expect performance will be around 2X realtime setting 3 threads on a Google server.

## Faster Whisperer

If you need to know anything else, it's going to be here:
https://github.com/SYSTRAN/faster-whisper
