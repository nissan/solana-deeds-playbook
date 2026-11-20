#!/usr/bin/env python3
"""Create immutable local narration takes with the existing Kokoro environment; no downloads."""
import argparse
import hashlib
import importlib.metadata
import json
import pathlib
import textwrap

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

parser = argparse.ArgumentParser()
parser.add_argument('--manifest', type=pathlib.Path, required=True)
parser.add_argument('--model-dir', type=pathlib.Path, required=True)
parser.add_argument('--work-dir', type=pathlib.Path, required=True)
args = parser.parse_args()
manifest = json.loads(args.manifest.read_text())
audio_dir = args.work_dir / 'sources' / 'narration'
audio_dir.mkdir(parents=True, exist_ok=True)
receipt_path = args.work_dir / 'narration-v1.json'
if receipt_path.exists() or list(audio_dir.glob('*take-1.wav')):
    raise SystemExit('Existing takes preserved. Choose a new work directory for a retake.')

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

model = args.model_dir / 'kokoro-v1.0.onnx'
voices = args.model_dir / 'voices-v1.0.bin'
expected = {model: 'beb0d1848dee9a49da392cc3df26958d46cfa35d321edf434f52949153f0df3a', voices: 'bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d'}
for path, sha in expected.items():
    if digest(path) != sha:
        raise SystemExit(f'Unexpected local model/voice digest: {path.name}')
engine = Kokoro(str(model), str(voices))
receipt = {'engine': f'kokoro-onnx {importlib.metadata.version("kokoro-onnx")}', 'modelSha256': expected[model], 'voicesSha256': expected[voices], 'modelLicense': 'Apache-2.0', 'runtimeLicense': 'MIT', 'synthetic': True, 'cloned': False, 'voice': manifest['voice'], 'scriptSha256': digest(args.manifest), 'captionTiming': 'Measured sentence boundaries; intra-sentence chunks proportional to word count, requiring human timing review.', 'scenes': []}
for scene in manifest['scenes']:
    pieces, captions, cursor = [], [], 0.0
    for index, sentence in enumerate(scene['script'], 1):
        samples, rate = engine.create(sentence, voice=manifest['voice']['preset'], speed=manifest['voice']['speed'], lang=manifest['voice']['language'])
        sentence_path = audio_dir / f'{scene["id"]}-sentence-{index:02d}-take-1.wav'
        sf.write(str(sentence_path), samples, rate, subtype='PCM_16')
        duration = len(samples) / rate
        chunks = textwrap.wrap(sentence, width=76, break_long_words=False, break_on_hyphens=False)
        words = sum(len(chunk.split()) for chunk in chunks)
        offset = cursor
        for chunk in chunks:
            end = offset + duration * len(chunk.split()) / words
            captions.append({'start': round(offset, 3), 'end': round(end, 3), 'text': '\n'.join(textwrap.wrap(chunk, width=40, break_long_words=False, break_on_hyphens=False))})
            offset = end
        pieces.extend([samples, np.zeros(round(rate * 0.22), dtype=np.float32)])
        cursor += duration + 0.22
    pieces.append(np.zeros(round(rate * 0.65), dtype=np.float32))
    path = audio_dir / f'{scene["id"]}-narration-take-1.wav'
    sf.write(str(path), np.concatenate(pieces), rate, subtype='PCM_16')
    entry = {'id': scene['id'], 'audio': str(path.relative_to(args.work_dir)), 'sha256': digest(path), 'sampleRate': rate, 'durationSeconds': round(sf.info(str(path)).duration, 6), 'captions': captions}
    receipt['scenes'].append(entry)
    print(scene['id'], entry['durationSeconds'], entry['sha256'], flush=True)
receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
print('Narration receipt:', receipt_path)
