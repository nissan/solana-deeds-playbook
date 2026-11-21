#!/usr/bin/env python3
"""Render a cut from manifest.json selections and narration-v1.json.

    python3 render.py N          renders/demo-vN.mp4, captions burned in: the draft for review
    python3 render.py N clean    renders/demo-vN-clean.mp4, the same picture with no captions:
                                 the source for the voice booth (see VOICE.md)

Each scene lasts max(footage, narration). Short footage is held on the scene's
end screenshot; narration is padded with silence. Captions come from the
narration receipt, offset to the scene's real start, and are kept as SRT.
receipts/<render>-segments.json records each scene's exact length in frames.
Never overwrites a render.
"""
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
version = sys.argv[1]
clean = len(sys.argv) > 2 and sys.argv[2] == "clean"
out = ROOT / "renders" / f"demo-v{version}{'-clean' if clean else ''}.mp4"
if out.exists():
    raise SystemExit(f"{out} exists")
for folder in ("renders", "captions", "receipts"):
    (ROOT / folder).mkdir(exist_ok=True)
manifest = json.loads((ROOT / "manifest.json").read_text())
narration = {s["id"]: s for s in json.loads((ROOT / "narration-v1.json").read_text())["scenes"]}
BOLD = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"
REG = "/usr/share/fonts/liberation/LiberationSans-Regular.ttf"
MONO = "/usr/share/fonts/liberation/LiberationMono-Regular.ttf"
# Every scene is marked as limited range. Unmarked, a card that follows an animation (which
# is marked full range) is read as full range by the joiner, and its blacks come out grey.
VENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-color_range", "tv", "-r", "30"]
AENC = ["-c:a", "aac", "-ar", "48000", "-ac", "2"]


def run(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, args)], check=True)


def frames_of(path):
    """Decodes the file: the frame count in the container is not reliable."""
    info = subprocess.run(
        ["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
         "stream=nb_read_frames", "-of", "json", str(path)],
        check=True, capture_output=True, text=True)
    return int(json.loads(info.stdout)["streams"][0]["nb_read_frames"])


def esc(text):
    return text.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\u2019")


def two_lines(text):
    """Captions are at most two lines tall; a taller one is refilled as two lines of similar width."""
    if len(text.splitlines()) <= 2:
        return text
    words = text.split()
    return "\n".join(min(((" ".join(words[:i]), " ".join(words[i:])) for i in range(1, len(words))),
                         key=lambda pair: max(map(len, pair))))


tmp = pathlib.Path(tempfile.mkdtemp())
segments, seg_frames, srt, cursor = [], [], [], 0
for scene in manifest["scenes"]:
    sid = scene["id"]
    voice = narration[sid]
    audio = ROOT / voice["audio"]
    seg = tmp / f"{sid}.mp4"
    kind = scene["mediaType"]
    if kind == "card":
        length = voice["durationSeconds"] + 0.5
        labels = []
        if any("at" in line for line in scene["lines"]):
            labels.append("drawbox=x=52:y=162:w=1176:h=390:color=0x151f2b:t=fill")
        for i, line in enumerate(scene["lines"]):
            x = line.get("x", "(w-text_w)/2")
            font = MONO if "x" in line else BOLD if i == 0 else REG
            enable = f":enable='gte(t,{line['at']})'" if "at" in line else ""
            labels.append(
                f"drawtext=fontfile={font}:text='{esc(line['text'])}':expansion=none"
                f":fontcolor={line.get('color', 'white')}:fontsize={line['size']}:x={x}:y={line['y']}{enable}"
            )
        draw = ",".join(labels)
        run("-f", "lavfi", "-i", f"color=c=0x0b0b0f:s=1280x720:r=30:d={length}", "-i", audio,
            "-vf", draw, "-af", f"apad,atrim=0:{length}", *VENC, *AENC, "-t", length, seg)
    elif kind == "still":
        length = voice["durationSeconds"] + 0.3
        run("-loop", "1", "-i", ROOT / scene["selectedTake"], "-i", audio,
            "-vf", "scale=1280:720,fps=30", "-af", f"apad,atrim=0:{length}", *VENC, *AENC, "-t", length, seg)
    else:
        # A screen recording ("source") or a pre-rendered animation ("clip"), held on its end still.
        clip = ROOT / scene["selectedTake"]
        clip_len = frames_of(clip) / 30
        length = max(clip_len, voice["durationSeconds"] + 0.3)
        hold = max(length - clip_len, 0.04)
        run("-i", clip, "-loop", "1", "-t", hold, "-i", ROOT / scene["endStill"], "-i", audio,
            "-filter_complex",
            "[0:v]scale=1280:720,fps=30,setsar=1[a];[1:v]scale=1280:720,fps=30,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v]",
            "-map", "[v]", "-map", "2:a", "-af", f"apad,atrim=0:{length}", *VENC, *AENC, "-t", length, seg)
    for cap in voice["captions"]:
        srt.append((cursor / 30 + cap["start"], cursor / 30 + cap["end"], two_lines(cap["text"])))
    segments.append(seg)
    # Measured, not computed: the encoder rounds each scene to whole frames, and both the
    # caption times and the voice booth's scene boundaries must follow the real cuts.
    frames = frames_of(seg)
    seg_frames.append({"id": sid, "frames": frames})
    cursor += frames


def stamp(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


burn = []
if not clean:
    srt_path = ROOT / "captions" / f"demo-v{version}.srt"
    srt_path.write_text("".join(f"{i}\n{stamp(a)} --> {stamp(b)}\n{t}\n\n" for i, (a, b, t) in enumerate(srt, 1)))
    style = "FontName=Liberation Sans,FontSize=12,PrimaryColour=&H00FFFFFF,BackColour=&H99000000,BorderStyle=4,Outline=0,Shadow=0,MarginV=10"
    burn = ["-vf", f"subtitles={srt_path}:force_style='{style}'"]
listing = tmp / "list.txt"
# Each file's audio runs a few milliseconds past its video. Naming the video length keeps
# the joiner from drifting the cuts by that much at every scene.
listing.write_text("".join(
    f"file '{s}'\nduration {f['frames'] / 30:.6f}\n" for s, f in zip(segments, seg_frames)))
# Frames pass straight through: asking for a frame rate here would repeat the opening frame
# and move every cut one frame late.
run("-f", "concat", "-safe", "0", "-i", listing, *burn, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-color_range", "tv",
    "-fps_mode", "passthrough", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", out)
made = frames_of(out)
if made != cursor:
    out.unlink()
    raise SystemExit(f"the final video has {made} frames but the scenes add up to {cursor}")
(ROOT / "receipts" / f"{out.stem}-segments.json").write_text(
    json.dumps({"fps": 30, "scenes": seg_frames}, indent=1) + "\n")
digest = subprocess.run(["sha256sum", str(out)], check=True, capture_output=True, text=True).stdout
(ROOT / "receipts" / f"{out.name}.sha256").write_text(digest)
print(digest.strip(), f"{cursor / 30:.2f}s")
