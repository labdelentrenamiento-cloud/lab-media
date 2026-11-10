"""Tech music bed + SFX + voice mix with ducking. Usage: python3 audio.py timeline.json out.wav"""
import json, sys, numpy as np, soundfile as sf
TL = json.load(open(sys.argv[1])); OUT = sys.argv[2]
SR = 44100; TOTAL = TL["total"]; N = int(TOTAL * SR) + SR
rng = np.random.default_rng(7)
music = np.zeros(N); sfx = np.zeros(N); voice = np.zeros(N)
def add(buf, sig, t0, g=1.0):
    i = int(t0 * SR); j = min(N, i + len(sig))
    if i < N and j > i: buf[i:j] += g * sig[:j - i]
def tt(d): return np.arange(int(d * SR)) / SR
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def lp(x, a):  # one-pole lowpass
    y = np.empty_like(x); acc = 0.0
    for k in range(len(x)): acc += a * (x[k] - acc); y[k] = acc
    return y
BPM = 96; B = 60 / BPM
PROG = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
bar = 4 * B
nb = int(TOTAL / bar) + 2
# pads (detuned saws, filtered) per bar
for b in range(nb):
    ch = PROG[(b // 2) % 4]; t0 = b * bar
    t = tt(bar + 0.6)
    s = np.zeros(len(t))
    for m in ch:
        for det in (-0.08, 0.08):
            f = mtof(m + det)
            s += 2 * ((t * f) % 1) - 1
    s = lp(s / 6, 0.05)
    env = np.minimum(1, t / 0.5) * np.minimum(1, np.maximum(0, (bar + 0.6 - t)) / 0.6)
    add(music, s * env, t0, 0.22)
    # sub bass pulse 8ths
    root = ch[0] - 24
    for e in range(8):
        tb = t0 + e * B / 2
        u = tt(B / 2)
        sb = np.sin(2 * np.pi * mtof(root) * u) * np.exp(-u * 6)
        add(music, sb, tb, 0.42 if e % 2 == 0 else 0.25)
    # hats 16ths + soft kick on beats
    for e in range(16):
        u = tt(0.05); nz = rng.uniform(-1, 1, len(u)); nz = nz - lp(nz, 0.3)
        add(music, nz * np.exp(-u * 90), t0 + e * B / 4, 0.05 if e % 2 else 0.08)
    for e in range(4):
        u = tt(0.25); f = 45 + 70 * np.exp(-u * 35)
        add(music, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-u * 14), t0 + e * B, 0.35)
    # arp sparkle
    for e in range(8):
        m = ch[e % 3] + 24
        u = tt(0.25)
        add(music, np.sin(2 * np.pi * mtof(m) * u) * np.exp(-u * 12), t0 + e * B / 2, 0.035)
# scene SFX: whoosh + blip
starts = [0.0] + [l["start"] - 0.12 for l in TL["lines"][1:]]
for s in starts[1:]:
    u = tt(0.45); nz = rng.uniform(-1, 1, len(u))
    sweep = lp(nz, 0.02) * 0 + nz
    a = np.linspace(0.02, 0.4, len(u))
    y = np.empty_like(nz); acc = 0
    for k in range(len(nz)): acc += a[k] * (nz[k] - acc); y[k] = acc
    env = np.sin(np.pi * u / 0.45) ** 2
    add(sfx, y * env, s - 0.3, 0.35)
    u = tt(0.12)
    add(sfx, np.sin(2 * np.pi * (1200 + 900 * u / 0.12) * u) * np.exp(-u * 30), s + 0.32, 0.12)
# voice
for l in TL["lines"]:
    x, sr = sf.read(l["file"])
    xi = np.interp(np.arange(int(len(x) * SR / sr)) * sr / SR, np.arange(len(x)), x)
    add(voice, xi, l["start"], 1.0)
v = np.abs(voice); w = int(0.2 * SR); env = np.convolve(v, np.ones(w) / w, mode="same")
env = np.clip(env / (env.max() * 0.25), 0, 1)
mix = music * (1 - 0.55 * env) * 0.55 + sfx * 0.8 + voice * 1.0
fade = int(1.0 * SR); mix[-fade:] *= np.linspace(1, 0, fade)
mix = mix[:int(TOTAL * SR)]
mix /= np.max(np.abs(mix)) / 0.9
sf.write(OUT, np.stack([mix, mix], 1), SR, subtype="PCM_16")
print("ok", TOTAL)
