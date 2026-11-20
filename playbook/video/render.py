#!/usr/bin/env python3
"""Render renders/demo-v<N>.mp4 from manifest.json selections and narration-v1.json.

Each scene lasts max(footage, narration). Short footage is held on the scene's
end screenshot; narration is padded with silence. Captions come from the
narration receipt, offset to scene start, and are burned in and kept as SRT.
Never overwrites a render.
"""
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
version = sys.argv[1]
out = ROOT / "renders" / f"demo-v{version}.mp4"
if out.exists():
    raise SystemExit(f"{out} exists")
manifest = json.loads((ROOT / "manifest.json").read_text())
narration = {s["id"]: s for s in json.loads((ROOT / "narration-v1.json").read_text())["scenes"]}
BOLD = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"
REG = "/usr/share/fonts/liberation/LiberationSans-Regular.ttf"
VENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30"]


def run(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, args)], check=True)


def duration(path):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries",
         "stream=nb_read_frames", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True).stdout.strip()) / 30


def esc(text):
    return text.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\u2019")


tmp = pathlib.Path(tempfile.mkdtemp())
segments, srt, cursor = [], [], 0.0
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
            font = "/usr/share/fonts/liberation/LiberationMono-Regular.ttf" if "x" in line else BOLD if i == 0 else REG
            enable = f":enable='gte(t,{line['at']})'" if "at" in line else ""
            labels.append(
                f"drawtext=fontfile={font}:text='{esc(line['text'])}':expansion=none"
                f":fontcolor={line.get('color', 'white')}:fontsize={line['size']}:x={x}:y={line['y']}{enable}"
            )
        draw = ",".join(labels)
        run("-f", "lavfi", "-i", f"color=c=0x0b0b0f:s=1280x720:r=30:d={length}", "-i", audio,
            "-vf", draw, "-af", f"apad,atrim=0:{length}", *VENC, "-c:a", "aac", "-ar", "48000", "-ac", "2",
            "-t", length, seg)
    elif kind == "still":
        length = voice["durationSeconds"] + 0.3
        run("-loop", "1", "-i", ROOT / scene["selectedTake"], "-i", audio,
            "-vf", "scale=1280:720,fps=30", "-af", f"apad,atrim=0:{length}", *VENC,
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-t", length, seg)
    else:
        clip = ROOT / scene["selectedTake"]
        clip_len = duration(clip)
        length = max(clip_len, voice["durationSeconds"] + 0.3)
        hold = max(length - clip_len, 0.04)
        run("-i", clip, "-loop", "1", "-t", hold, "-i", ROOT / scene["endStill"], "-i", audio,
            "-filter_complex",
            "[0:v]scale=1280:720,fps=30,setsar=1[a];[1:v]scale=1280:720,fps=30,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v]",
            "-map", "[v]", "-map", "2:a", "-af", f"apad,atrim=0:{length}", *VENC,
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-t", length, seg)
    for cap in voice["captions"]:
        srt.append((cursor + cap["start"], cursor + cap["end"], cap["text"]))
    segments.append(seg)
    cursor += length

def stamp(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"

srt_path = ROOT / "captions" / f"demo-v{version}.srt"
srt_path.write_text("".join(f"{i}\n{stamp(a)} --> {stamp(b)}\n{t}\n\n" for i, (a, b, t) in enumerate(srt, 1)))
listing = tmp / "list.txt"
listing.write_text("".join(f"file '{s}'\n" for s in segments))
style = "FontName=Liberation Sans,FontSize=12,PrimaryColour=&H00FFFFFF,BackColour=&H99000000,BorderStyle=4,Outline=0,Shadow=0,MarginV=10"
run("-f", "concat", "-safe", "0", "-i", listing, "-vf", f"subtitles={srt_path}:force_style='{style}'",
    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", *VENC, "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
    "-movflags", "+faststart", out)
digest = subprocess.run(["sha256sum", str(out)], check=True, capture_output=True, text=True).stdout
(ROOT / "receipts" / f"{out.name}.sha256").write_text(digest)
print(digest.strip(), f"{cursor:.2f}s")
