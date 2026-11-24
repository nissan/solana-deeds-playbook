"""Put each caption on the words the owner said, in the voice booth's package file.

    python3 place_captions.py --package <media>/deed-NN/package.json \
      --record <media>/deed-NN/renders/deed-NN-voice-vKK.json \
      --words words.json --said said.json --out package-captions-on-words.json

    ... --in-place     write the package file itself, keeping a copy from before beside it

Inputs:
  --package  the booth's package.json: each scene's captions, timed against the reference voice
  --record   the record of the cut the owner last assembled; its .srt is read from beside it
  --words    word times for that same cut, from transcribe.py
  --said     {"scene id": "the wording the owner confirmed for that scene"}, for every scene

The booth spreads a caption's reference time over the owner's speech in a scene. So each
word time is converted back through that scene's speech span before it is written, and the
booth's next assembly lands the caption on the word. The span is read from the last cut's
.srt, which is why the record, its .srt, the words and the package must all describe the same
assembly: transcribe the cut named by --record, and run this before any --replace import.

The caption text becomes what the owner said, cut into sentences, and again at a comma or
colon when a sentence is too long for two lines of 42 characters.

It only reads the takes' record; it never touches a take. It stops, writing nothing, when the
files do not describe the same scenes, when a caption has no heard word to sit on, or when
under half of a scene's confirmed words were heard in it (the wording and the cut do not
belong together; the share is printed for every scene, and was 0.74 or more in a real cut).

After the booth assembles again, check the new .srt: cues in order, none overlapping, at
most two lines. Captions are checked here inside each scene only; the edges between scenes
exist only in the assembled file.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import shutil
import textwrap
from pathlib import Path

LINE = 42  # characters in one caption line
CUE = 2 * LINE  # a caption is at most two lines
EDGE = 0.4  # seconds either side of a scene in which a word is still offered to it
HEARD = 0.5  # a scene with a smaller share of its confirmed words heard is refused


def stamp(text: str) -> float:
    hours, minutes, rest = text.strip().split(":")
    seconds, millis = rest.split(",")
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(millis) / 1000


def cue_times(srt: str) -> list[tuple[float, float]]:
    cues = []
    for block in srt.strip().split("\n\n"):
        begin, end = block.split("\n")[1].split("-->")
        cues.append((stamp(begin), stamp(end)))
    return cues


def tokens_of(text: str) -> list[str]:
    return re.sub(r"[^a-z0-9' ]", "", text.lower().replace("-", " ")).split()


def chunks(text: str) -> list[str]:
    """Sentences, cut again at a comma or colon when one is too long for two lines."""
    out = []
    for sentence in re.findall(r"[^.?!]+[.?!]+", text):
        sentence = sentence.strip()
        while len(sentence) > CUE:
            cut = max((m.end() for m in re.finditer(r"[,:;] ", sentence[:CUE])), default=None)
            if cut is None or cut < 30:
                cut = sentence.rfind(" ", 0, CUE) + 1
            out.append(sentence[:cut].strip())
            sentence = sentence[cut:].strip()
        out.append(sentence)
    return out


def place(package: dict, record: dict, cues: list[tuple[float, float]], words: list[dict], said: dict) -> list[tuple]:
    """Rewrite every scene's captions in `package`; return one report row per scene."""
    if [s["id"] for s in package["scenes"]] != [s["id"] for s in record["scenes"]]:
        raise SystemExit("the package and the record do not list the same scenes in the same order")
    missing = [s["id"] for s in package["scenes"] if not said.get(s["id"], "").strip()]
    if missing:
        raise SystemExit("no confirmed wording for: " + ", ".join(missing))
    if sum(len(s["captions"]) for s in package["scenes"]) != len(cues):
        raise SystemExit("the .srt does not have one cue per caption in the package: not the same assembly")
    fps = record["fps"]
    at, used, report, placed = 0.0, 0, [], []
    for scene, rec in zip(package["scenes"], record["scenes"]):
        sid = scene["id"]
        count = len(scene["captions"])
        first, final = cues[used][0], cues[used + count - 1][1]
        used += count
        # Where the owner's speech starts in the scene, and how far the booth stretched the
        # reference times to cover it. The first caption starts at 0 in the reference.
        span0 = first - at - scene["captions"][0]["start"]
        factor = (final - at - span0) / scene["captions"][-1]["end"]
        scene_len = rec["frames"] / fps
        # Word times are loose at a scene's edges, so words a little either side are offered
        # to the match, and their times are kept inside the scene.
        heard, times = [], []
        for word in words:
            if at - EDGE <= word["s"] < at + scene_len + EDGE:
                for token in tokens_of(word["w"]):
                    heard.append(token)
                    times.append((min(max(word["s"] - at, 0.0), scene_len - 0.5),
                                  min(max(word["e"] - at, 0.1), scene_len - 0.1)))
        parts = chunks(said[sid])
        if not parts:
            raise SystemExit(f"{sid}: the confirmed wording has no sentence in it")
        tokens, owner = [], []
        for index, part in enumerate(parts):
            for token in tokens_of(part):
                tokens.append(token)
                owner.append(index)
        match = {}
        for a, b, size in difflib.SequenceMatcher(None, tokens, heard, autojunk=False).get_matching_blocks():
            for k in range(size):
                match[a + k] = b + k
        share = len(match) / len(tokens)
        if share < HEARD:
            raise SystemExit(f"{sid}: only {share:.2f} of the confirmed words were heard in this scene; "
                             "is this the wording for this cut?")
        starts = []
        for index, part in enumerate(parts):
            mine = [j for j, o in enumerate(owner) if o == index]
            found = next((j for j in mine if j in match), None)
            if found is None:
                raise SystemExit(f"{sid}: no heard word for caption {part!r}")
            # step back over unmatched words at the head of the caption
            starts.append(times[max(0, match[found] - (found - mine[0]))][0])
        last_word = times[max(match.values())][1]

        def to_reference(seconds: float) -> float:
            return round(max(0.0, (seconds - span0) / factor), 3)

        captions = []
        for index, part in enumerate(parts):
            begin = max(starts[index] - 0.05, 0)
            end = (starts[index + 1] - 0.1) if index + 1 < len(parts) else min(last_word + 0.3, scene_len - 0.05)
            lines = textwrap.wrap(part, LINE)
            captions.append({"start": to_reference(begin), "end": to_reference(max(end, begin + 0.4)),
                             "text": "\n".join(lines) if len(lines) <= 2 else part})
        for cue in captions:
            if not cue["start"] < cue["end"]:
                raise SystemExit(f"{sid}: caption {cue['text']!r} would have no length")
        for a, b in zip(captions, captions[1:]):
            if a["end"] > b["start"] + 1e-6:
                raise SystemExit(f"{sid}: captions would overlap: {a['text']!r} and {b['text']!r}")
        placed.append(captions)
        report.append((sid, len(parts), round(span0, 2), round(factor, 3), round(share, 2)))
        at += scene_len
    # Nothing is changed until every scene has been placed.
    for scene, captions in zip(package["scenes"], placed):
        scene["captions"] = captions
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--words", type=Path, required=True)
    parser.add_argument("--said", type=Path, required=True)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--out", type=Path, help="write the new package here; must not exist")
    target.add_argument("--in-place", action="store_true",
                        help="write --package, after copying it to package.before-captions-on-words.json")
    args = parser.parse_args(argv)

    load = lambda path: json.loads(path.read_text(encoding="utf-8"))
    package = load(args.package)
    report = place(package, load(args.record), cue_times(args.record.with_suffix(".srt").read_text(encoding="utf-8")),
                   load(args.words), load(args.said))
    if args.in_place:
        before = args.package.with_name("package.before-captions-on-words.json")
        if not before.exists():  # the first copy is the one from before any placement; keep it
            shutil.copyfile(args.package, before)
        out = args.package
    else:
        if args.out.exists():
            raise SystemExit(f"{args.out} exists; nothing written")
        out = args.out
    out.write_text(json.dumps(package, indent=1), encoding="utf-8")
    print("scene, captions, speech starts at (s), stretch, share of confirmed words heard")
    for row in report:
        print(*row)
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
