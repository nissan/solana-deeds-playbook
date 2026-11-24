"""Transcribe an assembled cut on this machine, with a time for every word.

    uv run --no-project --with faster-whisper==1.2.1 --with av==18.1.1 \
      python transcribe.py CUT.mp4 words.json [--model small.en]

Pin both: faster-whisper 1.2.1 fails to open the file with PyAV 19.

Writes a list of {"w": word, "s": start, "e": end}, in seconds from the start of the cut.
Nothing leaves the machine and the takes are not touched: it reads the one file it is given.
The first run downloads the model.

The transcriber mishears. Numerals and odd spellings are its own; a phrase it reports as
added, dropped or reworded is put to the owner before it becomes a caption (VOICE.md step 6).
Word times are loose at the edges of a scene; place_captions.py allows for that.
"""
import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("cut", type=Path, help="the assembled video or its audio")
    parser.add_argument("out", type=Path, help="where to write the words")
    parser.add_argument("--model", default="small.en")
    args = parser.parse_args()
    if args.out.exists():
        raise SystemExit(f"{args.out} exists; this script never overwrites a transcript")

    from faster_whisper import WhisperModel

    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(str(args.cut), word_timestamps=True, vad_filter=False, beam_size=5)
    words = [
        {"w": word.word.strip(), "s": round(word.start, 2), "e": round(word.end, 2)}
        for segment in segments
        for word in segment.words
    ]
    args.out.write_text(json.dumps(words), encoding="utf-8")
    print(len(words), "words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
