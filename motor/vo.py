"""Voz en off natural (sin cambio de tono) + tiempos por palabra."""
import json, re, subprocess, os, sys
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

TTS = "/home/claude/tts"
k = Kokoro(f"{TTS}/kokoro-v1.0.onnx", f"{TTS}/voices-v1.0.bin")
VOICE, SPEED = "ef_dora", 1.0
SR = 24000

script = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "script.json"))
os.makedirs("vo", exist_ok=True)


def syl(w):
    w = w.lower()
    n = len(re.findall(r"[aeiouáéíóúü]+", w))
    return max(1, n)


t = 0.15
out = []
for i, ln in enumerate(script["lines"]):
    a, sr = k.create(ln["say"], voice=VOICE, speed=SPEED, lang="es")
    raw = f"vo/{i}_raw.wav"; sf.write(raw, a, sr)
    proc = f"vo/{i}.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
                    "highpass=f=70,equalizer=f=250:t=q:w=1:g=-1.5,equalizer=f=3200:t=q:w=1.2:g=2.5,"
                    "acompressor=threshold=-20dB:ratio=3:attack=4:release=90:makeup=2",
                    "-ar", str(SR), "-ac", "1", proc], check=True)
    x, _ = sf.read(proc)
    env = np.abs(x); thr = 0.04 * env.max()
    idx = np.where(env > thr)[0]
    x = x[max(0, idx[0] - 240): idx[-1] + 2400]
    sf.write(proc, x, SR)
    dur = len(x) / SR
    # tiempos por palabra: reparto por sílabas sobre la parte con voz
    words = ln["show"].split()
    weights = [syl(w) + (0.6 if re.search(r"[.,!?…:]$", w) else 0) for w in words]
    tot = sum(weights); acc = 0.0; wt = []
    voiced = dur - 0.12
    for w, wg in zip(words, weights):
        s = t + 0.04 + voiced * acc / tot
        acc += wg
        wt.append({"w": w, "s": round(s, 3), "e": round(t + 0.04 + voiced * acc / tot, 3)})
    out.append({**ln, "file": proc, "start": round(t, 3), "dur": round(dur, 3), "words": wt})
    print(i, round(t, 2), round(dur, 2), ln["say"])
    t += dur + ln.get("gap", 0.32)
total = t + script.get("tail", 1.6)
json.dump({"lines": out, "total": round(total, 3)}, open("timeline.json", "w"), ensure_ascii=False, indent=1)
print("total", round(total, 2))
