# Transcribe YouTube videos using Whisper models

Adopts [faster_whisperer](https://github.com/SYSTRAN/faster-whisper), a cTransformer's based model for faster transcription.

## Usage

```python
from youtescribe import transcribe

transcript = transcribe(url="https://www.youtube.com/watch?v=9bZkp7q19f0")

transcript.text()
```

### Prompting

By default, the video title and description are used as prompts to the transcription model. But you can also specify your own prompt:

```python
transcript = transcribe(
    url="https://www.youtube.com/watch?v=9bZkp7q19f0",
    prompt="Enter prompt here"
)
```

You can also choose not to include prompt by setting `prompt=False`.

```python
transcript = transcribe(
    url="https://www.youtube.com/watch?v=9bZkp7q19f0",
    prompt=False
)
```

### Working with `WhisperTranscript` objects

The `transcribe()` function, if executed successfully, will return a `WhisperTranscript` object. You can view the transcript as plain text, SRT-formatted text, or a Python dictionary.

```python
transcript = transcribe(
    url="https://www.youtube.com/watch?v=9bZkp7q19f0",
    prompt=False
)

transcript.text()
transcript.srt()
transcript.json()
transcript.segment
```

### Customise Whisper model

In the transcribe function, you can pass your own custom Whisper model:

```python
from youtescribe import WhisperTranscriber
from youtescribe import models

custom_transcriber = WhisperTranscriber(model_size = models.TINY_EN, cpu_threads=6, device="auto")

transcript = transcribe(
    url="https://www.youtube.com/watch?v=9bZkp7q19f0",
    transcriber=custom_transcriber
)
transcript.text()
```


