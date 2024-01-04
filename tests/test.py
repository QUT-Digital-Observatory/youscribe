from youteplustrans.transcribe import YouteTranscriber


def transcribe(
    url: str, format_: str = "json", model: str = "medium", cpu_threads: int = 4
) -> list[dict]:
    transcriber = YouteTranscriber(url=url, model=model, cpu_threads=cpu_threads)
    segments = transcriber.transcribe()

    output = []

    if not segments:
        raise Exception(f"Nothing was transcribed for {url}.")

    for segment in segments:
        output.append(
            {
                "id": segment.id,
                "start": segment.start,
                "end": segment.end,
                "text": segment.text,
            }
        )

    return output


test = transcribe("https://www.youtube.com/watch?v=wjFKgMUMpYI")
print(test)
