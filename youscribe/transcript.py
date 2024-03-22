import json
from abc import ABC, abstractmethod
from datetime import timedelta
from pathlib import Path
from typing import Iterable

from faster_whisper.transcribe import Segment


class BaseTranscript(ABC):
    @abstractmethod
    def text(self):
        pass

    @abstractmethod
    def json(self):
        pass

    @abstractmethod
    def srt(self):
        pass


class WhisperTranscript(BaseTranscript):
    def __init__(self, segments: Iterable[Segment]):
        self.segments = list(segments)

    def text(self) -> str:
        return " ".join([segment.text.strip() for segment in self.segments])

    def json(self) -> str:
        obj = []
        for segment in self.segments:
            obj.append(
                {
                    "id": segment.id,
                    "start": round(segment.start, 2),
                    "end": round(segment.end, 2),
                    "text": segment.text.strip(),
                }
            )
        return json.dumps(obj)

    def srt(self, file_path: str | Path | None = None) -> str:
        srt_str = ""

        for i, segment in enumerate(self.segments):
            # Convert start and end times to hh:mm:ss,sss format
            start_time = timedelta(seconds=segment.start)
            end_time = timedelta(seconds=segment.end)

            # Convert timedelta to appropriate string format
            str_start_time = str(start_time).zfill(8)
            if "." in str_start_time:
                str_start_time = str_start_time.replace(".", ",")
                if len(str_start_time.split(",")[1]) < 3:
                    str_start_time = str_start_time + "0" * (
                        3 - len(str_start_time.split(",")[1])
                    )
            else:
                str_start_time = str_start_time + ",000"

            str_end_time = str(end_time).zfill(8)
            if "." in str_end_time:
                str_end_time = str_end_time.replace(".", ",")
                if len(str_end_time.split(",")[1]) < 3:
                    str_end_time = str_end_time + "0" * (
                        3 - len(str_end_time.split(",")[1])
                    )
            else:
                str_end_time = str_end_time + ",000"

            # Add index, time range, and text to the string
            srt_str += f"{i+1}\n{str_start_time} --> {str_end_time}\n{segment.text.strip()}\n\n"

        if file_path:
            with open(file_path, "w") as f:
                f.write(srt_str)

        return srt_str

    # def segments(self) -> list[ShortSegment]:
    #     short_segments = []
    #     for segment in self.segments:
    #         short_segments.append(
    #             ShortSegment(
    #                 id=segment.id,
    #                 start=round(segment.start, 2),
    #                 end=round(segment.end, 2),
    #                 text=segment.text.strip(),
    #             )
    #         )
    #     return short_segments

    # def csv(self) -> str | None:
    #     try:
    #         output = io.StringIO()
    #         writer = csv.DictWriter(
    #             output, fieldnames=["id", "start", "end", "text"], quoting=csv.QUOTE_ALL
    #         )
    #         writer.writeheader()
    #         for segment in self.segmentlist:
    #             seg = {
    #                 "id": segment.id,
    #                 "start": round(segment.start, 2),
    #                 "end": round(segment.end, 2),
    #                 "text": segment.text.strip(),
    #             }
    #             # encode special characters in the 'text' field
    #             seg["text"] = seg["text"].encode("unicode_escape").decode("utf-8")
    #             writer.writerow(seg)
    #         return output.getvalue()
    #     except Exception as e:
    #         logger.error("An error occurred while creating the CSV string.")
    #         logger.error(str(e))
    #         return None
