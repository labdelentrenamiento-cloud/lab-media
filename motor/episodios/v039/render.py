"""v039 · 3 cosas que la música le hace a tu entrenamiento (3 FACTORES, serie RENDIMIENTO ·
paleta ciruela + magenta + ámbar + cian)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (1.0, 0.40, 0.85)   # magenta = música


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.12, 0.03, 0.12], [0.02, 0.005, 0.03])
from engine_ext import *
CY = ACC
TE = (0.30, 0.90, 1.0)


def title(ctx, s, color=WH, y=345, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1170):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def badge(ctx, cx, cy, num, unit, col, a, w=300):
    if a <= 0: return
    rrect(ctx, cx - w / 2, cy - 150, w, 290, 26); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    big(ctx, num, cx, cy + 30, 120, col, a, maxw=w - 40)
    for li, part in enumerate(unit.split("\n")):
        text(ctx, part, cx, cy + 85 + li * 30, F_MONO, 23, WH, a, align="center", bold=True)


def eq(ctx, cx, cy, w, h, n, t, col, a, bpm=128):
    if a <= 0: return
    bw = w / n
    for j in range(n):
        v = 0.25 + 0.75 * abs(math.sin(t * bpm / 60 * math.pi + j * 0.9) * math.sin(t * 1.3 + j * 0.45))
        hh = h * v
        x = cx - w / 2 + j * bw + 4
        rrect(ctx, x, cy - hh / 2, bw - 8, hh, (bw - 8) / 2)
        ctx.set_source_rgba(*col, 0.35 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(2.5); ctx.stroke()


def headphones(ctx, cx, cy, s, col, a, t):
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 20, 190, math.pi * 1.05, math.pi * 1.95)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(22); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.set_line_cap(cairo.LINE_CAP_BUTT)
    for sd in (-1, 1):
        rrect(ctx, sd * 190 - 45, 10, 90, 170, 34); ctx.set_source_rgba(*col, 0.18 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(6); ctx.stroke()
        for r in range(3):
            ph = (t * 1.6 + r * 0.33) % 1
            ctx.new_path(); ctx.arc(sd * 190, 95, 110 + 60 * ph, -0.5 if sd > 0 else math.pi - 0.5, 0.5 if sd > 0 else math.pi + 0.5)
            ctx.set_source_rgba(*AM, 0.7 * (1 - ph) * a); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def face(ctx, cx, cy, r, smile, col, a):
    if a <= 0: return
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*col, 0.12 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(6); ctx.stroke()
    for sd in (-1, 1):
        ctx.new_path(); ctx.arc(cx + sd * r * 0.35, cy - r * 0.2, r * 0.09, 0, 6.283); ctx.set_source_rgba(*col, a); ctx.fill()
    ctx.move_to(cx - r * 0.45, cy + r * 0.3)
    ctx.curve_to(cx - r * 0.2, cy + r * (0.3 + 0.35 * smile), cx + r * 0.2, cy + r * (0.3 + 0.35 * smile), cx + r * 0.45, cy + r * 0.3)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(7); ctx.stroke()


def num(ctx, s, x, y, col, k):
    if k <= 0: return
    ctx.new_path(); ctx.arc(x, y, 62, 0, 6.283); ctx.set_source_rgba(*col, 0.9 * k); ctx.fill()
    text(ctx, s, x, y + 30, F_BIG, 86, (0.06, 0.02, 0.08), k, align="center")


def ecg(ctx, x0, x1, y, t, col, a, amp=50):
    ctx.new_path()
    n = 220; per = 260.0; off = (t * 160) % per
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        q = ((x - x0 + off) % per) / per
        v = 0
        if 0.40 < q < 0.44: v = -0.25
        elif 0.44 < q < 0.48: v = 1.0
        elif 0.48 < q < 0.52: v = -0.45
        elif 0.62 < q < 0.72: v = 0.18 * math.sin((q - 0.62) / 0.10 * math.pi)
        (ctx.move_to if i == 0 else ctx.line_to)(x, y - v * amp)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()


def hbar(ctx, x, y, w, h, frac, col, a, label, val=""):
    rrect(ctx, x, y, w, h, h / 2); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill()
    if frac > 0:
        rrect(ctx, x, y, max(h, w * frac), h, h / 2); ctx.set_source_rgba(*col, 0.35 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
    text(ctx, label, x, y - 16, F_MONO, 27, col, a, bold=True)
    if val: text(ctx, val, x + w, y - 16, F_MONO, 27, WH, a, align="right", bold=True)


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        headphones(ctx, 540, 640, 1.2, CY, k, t)
        eq(ctx, 540, 800, 300, 160, 7, t, AM, ease((u - 0.3) / 0.4))
        kn = easeb((u - lt(0) - 3.2) / 0.5)
        if kn > 0:
            ctx.save(); ctx.translate(540, 1080); ctx.scale(kn, kn)
            text(ctx, "139 ESTUDIOS", 0, 0, F_BIG, 90, AM, 1, align="center"); ctx.restore()
    elif i == 1:
        badge(ctx, 360, 760, "139", "ESTUDIOS", AM, ease((u - 0.1) / 0.4))
        badge(ctx, 720, 760, "3.599", "PERSONAS", CY, ease((u - 1.0) / 0.4))
        eq(ctx, 540, 1060, 600, 80, 16, t, CY, 0.7 * ease((u - 0.6) / 0.5))
    elif i == 2:
        num(ctx, "1", 540, 520, AM, easeb((u - 0.1) / 0.4))
        v = 0.78 - 0.26 * ease((u - 1.0) / 1.8)
        gauge(ctx, 540, 830, 200, v * k, k, col=GR)
        text(ctx, "ESFUERZO PERCIBIDO", 540, 1100, F_MONO, 28, WH, k, align="center", bold=True)
    elif i == 3:
        num(ctx, "2", 540, 520, AM, easeb((u - 0.1) / 0.4))
        kk = ease((u - 0.4) / 1.2)
        hbar(ctx, 170, 700, 740, 56, 0.70 * kk, MU, kk, "SIN MÚSICA")
        hbar(ctx, 170, 860, 740, 56, 0.80 * ease((kk - 0.2) / 0.8), GR, kk, "CON MÚSICA")
        kr = easeb((u - lt(3) - 3.4) / 0.5)
        if kr > 0:
            rrect(ctx, 340, 990, 400, 80, 40); ctx.set_source_rgba(*AM, 0.15 * kr); ctx.fill_preserve(); ctx.set_source_rgba(*AM, kr); ctx.set_line_width(4); ctx.stroke()
            text(ctx, "♪ MÚSICA RÁPIDA", 540, 1043, F_MONO, 30, AM, kr, align="center", bold=True)
    elif i == 4:
        num(ctx, "3", 540, 520, AM, easeb((u - 0.1) / 0.4))
        face(ctx, 540, 800, 170, ease((u - 0.6) / 1.2) * 2 - 0.6, GR, k)
        kb = easeb((u - lt(4) - 2.8) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 1080); ctx.scale(kb, kb)
            text(ctx, "EL EFECTO MÁS GRANDE", 0, 0, F_BIG, 64, AM, 1, align="center"); ctx.restore()
    elif i == 5:
        eq(ctx, 540, 650, 600, 200, 12, t, CY, k)
        kc = ease((u - 0.4) / 0.4)
        rrect(ctx, 190, 820, 700, 130, 30); ctx.set_source_rgba(*AM, 0.10 * kc); ctx.fill_preserve(); ctx.set_source_rgba(*AM, kc); ctx.set_line_width(4); ctx.stroke()
        cur = "▌" if int(t * 2.5) % 2 == 0 else " "
        text(ctx, "♪ TU CANCIÓN " + cur, 540, 905, F_MONO, 40, WH, kc, align="center", bold=True)
        text(ctx, "DÉJALA EN LOS COMENTARIOS", 540, 1030, F_MONO, 28, AM, ease((u - 1.2) / 0.4), align="center", bold=True)
    elif i == 6:
        ecg(ctx, 170, 910, 700, t, TE, 0.9 * k)
        text(ctx, "PULSO: SIN CAMBIO CLARO", 540, 800, F_MONO, 28, TE, k, align="center", bold=True)
        kg = ease((u - lt(6) - 2.4) / 0.6)
        if kg > 0:
            gauge(ctx, 540, 1010, 120, 0.45 * kg, kg, col=GR)
    elif i == 7:
        kk = ease((u - 0.4) / 1.4)
        hbar(ctx, 170, 720, 740, 56, 0.85 * kk, GR, kk, "LA QUE TÚ ELIGES")
        hbar(ctx, 170, 900, 740, 56, 0.55 * ease((kk - 0.2) / 0.8), MU, kk, "UNA IMPUESTA")
        text(ctx, "ÁNIMO ANTES DE ENTRENAR", 540, 1050, F_MONO, 26, WH, k, align="center", bold=True)
    elif i == 8:
        headphones(ctx, 540, 560, 0.9, CY, k, t)
        eq(ctx, 540, 690, 220, 110, 6, t, AM, k)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1010); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, AM, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "3 FACTORES · RENDIMIENTO", W / 2, 196, CY, k, 28)
        title(ctx, "¿TU MÚSICA TE HACE RENDIR MÁS?", WH, 368, 90, k)
    elif i == 1:
        pill(ctx, "METAANÁLISIS · 2020", W / 2, 196, AM, k, 28, filled=True)
        title(ctx, "LO QUE HACE LA MÚSICA", WH, 368, 98, k)
        src(ctx, "Terry et al., Psychological Bulletin 2020 · doi:10.1037/bul0000216", k, 1150)
    elif i == 2:
        pill(ctx, "FACTOR 1", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "SE SIENTE MÁS FÁCIL", WH, 368, 100, k)
        src(ctx, "Terry et al., 2020 · menor esfuerzo percibido", k, 1160)
    elif i == 3:
        pill(ctx, "FACTOR 2", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "RINDES UN POCO MÁS", WH, 368, 100, k)
        text(ctx, "ESQUEMA ILUSTRATIVO · EFECTO PEQUEÑO", W / 2, 1120, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Terry et al., 2020 · mayor efecto con tempo rápido", k, 1160)
    elif i == 4:
        pill(ctx, "FACTOR 3", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "MEJOR ÁNIMO AL ENTRENAR", WH, 368, 96, k)
        src(ctx, "Terry et al., 2020 · efecto sobre el ánimo: el mayor del estudio", k, 1160)
    elif i == 5:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿QUÉ CANCIÓN TE HACE RENDIR?", WH, 368, 92, k)
    elif i == 6:
        pill(ctx, "OJO · EVIDENCIA 2026", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "LO MÁS FIRME: MENOS ESFUERZO", WH, 368, 88, k)
        src(ctx, "Yang et al., Front Sports Act Living 2026 · doi:10.3389/fspor.2026.1860752", k, 1160)
    elif i == 7:
        pill(ctx, "TRUCO", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "ELIGE TU PROPIA MÚSICA", WH, 368, 98, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1110, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Delleli et al., Front Psychol 2023 · doi:10.3389/fpsyg.2023.1293783", k, 1150)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 39 · RENDIMIENTO")
