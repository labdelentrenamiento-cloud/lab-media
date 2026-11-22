"""v041 · ¿Cardio antes o después de las pesas? (COMPARACIÓN, serie FUERZA ·
paleta grafito + lima + rojo + cian)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (0.72, 1.0, 0.36)   # lima = fuerza


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.075, 0.085, 0.085], [0.01, 0.012, 0.014])
from engine_ext import *
CY = ACC
TE = (0.30, 0.88, 1.0)    # cian = pesas
CA = (1.0, 0.38, 0.45)    # rojo = cardio


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


def hbar(ctx, x, y, w, h, frac, col, a, label, val=""):
    rrect(ctx, x, y, w, h, h / 2); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill()
    if frac > 0:
        rrect(ctx, x, y, max(h, w * frac), h, h / 2); ctx.set_source_rgba(*col, 0.35 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
    text(ctx, label, x, y - 16, F_MONO, 27, col, a, bold=True)
    if val: text(ctx, val, x + w, y - 16, F_MONO, 27, WH, a, align="right", bold=True)


def heart(ctx, cx, cy, r, col, a, t):
    if a <= 0: return
    p = 1 + 0.08 * max(0, math.sin(t * 7))
    ctx.save(); ctx.translate(cx, cy); ctx.scale(r / 100 * p, r / 100 * p)
    ctx.move_to(0, 70); ctx.curve_to(-120, -10, -80, -110, 0, -50); ctx.curve_to(80, -110, 120, -10, 0, 70); ctx.close_path()
    ctx.restore(); ctx.set_source_rgba(*col, 0.15 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()


def dumbbell(ctx, cx, cy, s, col, a, t=0, bob=False):
    if a <= 0: return
    dy = -abs(math.sin(t * 2.6)) * 18 if bob else 0
    ctx.save(); ctx.translate(cx, cy + dy); ctx.scale(s, s)
    ctx.move_to(-70, 0); ctx.line_to(70, 0); ctx.set_source_rgba(*WH, 0.9 * a); ctx.set_line_width(10); ctx.stroke()
    for sd in (-1, 1):
        for j, (h, w) in enumerate([(100, 30), (74, 22)]):
            x = sd * (78 + j * 30)
            rrect(ctx, x - w / 2, -h / 2, w, h, 8); ctx.set_source_rgba(*col, 0.18 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def ecg(ctx, x0, x1, y, t, col, a, amp=40):
    ctx.new_path()
    n = 200; per = 240.0; off = (t * 160) % per
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


def card(ctx, cx, cy, w, h, col, a, fill=0.10):
    rrect(ctx, cx - w / 2, cy - h / 2, w, h, 28); ctx.set_source_rgba(*col, fill * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()


def seq(ctx, y, first, a, t, lab_y=None):
    """fila de orden: [1 X] → [2 Y]"""
    if a <= 0: return
    items = [("PESAS", TE), ("CARDIO", CA)] if first == "pesas" else [("CARDIO", CA), ("PESAS", TE)]
    for j, (lab, col) in enumerate(items):
        cx = 330 + j * 420
        card(ctx, cx, y, 300, 110, col, a)
        text(ctx, "%d." % (j + 1), cx - 110, y + 14, F_BIG, 44, col, a, align="center")
        text(ctx, lab, cx + 25, y + 14, F_MONO, 36, WH, a, align="center", bold=True)
    ph = (t * 1.4) % 1
    ctx.move_to(505, y); ctx.line_to(575, y); ctx.set_source_rgba(*CY, a); ctx.set_line_width(5); ctx.stroke()
    ctx.move_to(560 + 10 * ph, y - 14); ctx.line_to(580 + 10 * ph, y); ctx.line_to(560 + 10 * ph, y + 14); ctx.stroke()


def check(ctx, cx, cy, r, col, a):
    if a <= 0: return
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*col, 0.15 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    ctx.move_to(cx - r * 0.45, cy + r * 0.02); ctx.line_to(cx - r * 0.1, cy + r * 0.38); ctx.line_to(cx + r * 0.5, cy - r * 0.35); ctx.set_line_width(7); ctx.stroke()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        xa, xb = 300, 780
        flip = int(t / 1.1) % 2
        for (cx, n) in ((xa, 1 + flip), (xb, 2 - flip)):
            ctx.new_path(); ctx.arc(cx, 470, 44, 0, 6.283); ctx.set_source_rgba(*CY, 0.9 * k); ctx.fill()
            text(ctx, "%d.º" % n, cx, 490, F_BIG, 48, (0.03, 0.04, 0.04), k, align="center")
        card(ctx, xa, 660, 320, 280, CA, k); heart(ctx, xa, 630, 70, CA, k, t); ecg(ctx, xa - 120, xa + 120, 740, t, CA, k, 22)
        card(ctx, xb, 660, 320, 280, TE, k); dumbbell(ctx, xb, 640, 1.0, TE, k, t, True)
        text(ctx, "CARDIO", xa, 860, F_MONO, 30, CA, k, align="center", bold=True)
        text(ctx, "PESAS", xb, 860, F_MONO, 30, TE, k, align="center", bold=True)
        kn = easeb((u - lt(0) - 2.0) / 0.5)
        if kn > 0:
            ctx.save(); ctx.translate(540, 1080); ctx.scale(kn, kn)
            text(ctx, "¿QUIÉN VA PRIMERO?", 0, 0, F_BIG, 84, CY, 1, align="center"); ctx.restore()
    elif i == 1:
        badge(ctx, 360, 640, "10", "ESTUDIOS", CY, ease((u - 0.1) / 0.4))
        badge(ctx, 720, 640, "5+", "SEMANAS", WH, ease((u - 1.2) / 0.4))
        seq(ctx, 920, "pesas", ease((u - lt(1) - 3.3) / 0.5), t)
        seq(ctx, 1060, "cardio", ease((u - lt(1) - 3.7) / 0.5), t)
    elif i == 2:
        kk = ease((u - 0.5) / 1.6)
        vbars(ctx, [("PESAS\nPRIMERO", 0.95, TE), ("CARDIO\nPRIMERO", 0.80, CA)], 300, 1000, 200, 80, 440, kk, k, 26)
        kp = easeb((u - lt(2) - 2.6) / 0.5)
        if kp > 0:
            ctx.save(); ctx.translate(400, 520); ctx.scale(kp, kp)
            text(ctx, "≈ +7 %", 0, 0, F_BIG, 76, CY, 1, align="center"); ctx.restore()
    elif i == 3:
        k1 = ease((u - 0.3) / 1.2)
        hbar(ctx, 170, 640, 680, 50, 0.72 * k1, TE, k1, "MÚSCULO · PESAS 1.º")
        hbar(ctx, 170, 760, 680, 50, 0.72 * k1, CA, k1, "MÚSCULO · CARDIO 1.º")
        k2 = ease((u - lt(3) - 2.6) / 1.2)
        hbar(ctx, 170, 920, 680, 50, 0.66 * k2, TE, k2, "AERÓBICO · PESAS 1.º")
        hbar(ctx, 170, 1040, 680, 50, 0.66 * k2, CA, k2, "AERÓBICO · CARDIO 1.º")
        if k1 > 0.95: text(ctx, "=", 905, 760, F_BIG, 90, CY, 1, align="center")
        if k2 > 0.95: text(ctx, "=", 905, 1040, F_BIG, 90, CY, 1, align="center")
    elif i == 4:
        for j, (lab, col) in enumerate([("CARDIO", CA), ("PESAS", TE)]):
            kj = easeb((u - 0.3 - j * 0.25) / 0.5)
            if kj <= 0: continue
            cx = 330 + j * 420
            card(ctx, cx, 760, 340, 230, col, kj, 0.14)
            text(ctx, lab, cx, 800, F_BIG, 96, col, kj, align="center")
        cur = "▌" if int(t * 2.5) % 2 == 0 else " "
        text(ctx, "COMENTA CUÁL VA PRIMERO " + cur, 540, 1010, F_MONO, 32, WH, ease((u - 0.6) / 0.4), align="center", bold=True)
    elif i == 5:
        badge(ctx, 540, 650, "+4 KG", "MÁXIMO DE PIERNAS\n(1 REPETICIÓN)", CY, ease((u - lt(5) - 2.6) / 0.4), w=420)
        dumbbell(ctx, 540, 1000, 1.3, TE, ease((u - 0.2) / 0.5), t, True)
    elif i == 6:
        for j, (lab, col) in enumerate([("CARDIO → PESAS", CA), ("PESAS → CARDIO", TE)]):
            kj = ease((u - 0.4 - j * 0.4) / 0.5)
            cx = 330 + j * 420
            card(ctx, cx, 720, 360, 300, col, kj)
            heart(ctx, cx, 680, 60, col, kj, t + j * 0.3)
            text(ctx, lab, cx, 830, F_MONO, 26, WH, kj, align="center", bold=True)
            check(ctx, cx, 950, 44, GR, easeb((u - lt(6) - 3.0 - j * 0.3) / 0.5))
        kb = easeb((u - lt(6) - 4.6) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 1100); ctx.scale(kb, kb)
            text(ctx, "NINGUNO GANÓ CLARAMENTE", 0, 0, F_BIG, 60, CY, 1, align="center"); ctx.restore()
    elif i == 7:
        k1 = ease((u - 0.3) / 0.5)
        card(ctx, 540, 640, 760, 190, TE, k1)
        text(ctx, "META: FUERZA", 540, 600, F_MONO, 30, TE, k1, align="center", bold=True)
        text(ctx, "PESAS PRIMERO", 540, 692, F_BIG, 64, WH, k1, align="center")
        k2 = ease((u - lt(7) - 2.6) / 0.5)
        card(ctx, 540, 900, 760, 190, GR, k2)
        text(ctx, "META: SALUD", 540, 860, F_MONO, 30, GR, k2, align="center", bold=True)
        text(ctx, "EL ORDEN QUE TE HAGA VOLVER", 540, 950, F_BIG, 52, WH, k2, align="center")
    elif i == 8:
        heart(ctx, 400, 640, 80, CA, k, t)
        dumbbell(ctx, 690, 640, 1.0, TE, k, t, True)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1010); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, CY, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "COMPARACIÓN · FUERZA", W / 2, 196, CY, k, 28)
        title(ctx, "¿CARDIO ANTES O DESPUÉS?", WH, 368, 96, k)
    elif i == 1:
        pill(ctx, "METAANÁLISIS · 2018", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "MISMO PLAN, OTRO ORDEN", WH, 368, 98, k)
        src(ctx, "Eddens et al., Sports Med 2018 · doi:10.1007/s40279-017-0784-1", k, 1180)
    elif i == 2:
        pill(ctx, "FUERZA DE PIERNAS", W / 2, 196, TE, k, 28, filled=True)
        title(ctx, "GANAN LAS PESAS PRIMERO", WH, 368, 96, k)
        text(ctx, "ESQUEMA ILUSTRATIVO · DIFERENCIA MEDIA 6,9 %", W / 2, 1130, F_MONO, 22, CY, k, align="center", bold=True)
        src(ctx, "Eddens et al., 2018 · fuerza dinámica del tren inferior", k, 1170)
    elif i == 3:
        pill(ctx, "SIN DIFERENCIA", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "MÚSCULO Y CARDIO: EMPATE", WH, 368, 96, k)
        src(ctx, "Eddens et al., 2018 · hipertrofia, VO2máx y grasa: sin efecto del orden", k, 1150)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 196, CY, k, 32, filled=True)
        title(ctx, "¿TÚ QUÉ HACES PRIMERO?", WH, 368, 96, k)
    elif i == 5:
        pill(ctx, "OTRO METAANÁLISIS", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "MISMA CONCLUSIÓN", WH, 368, 100, k)
        src(ctx, "Murlasits et al., J Sports Sci 2018 · +3,96 kg · doi:10.1080/02640414.2017.1364405", k, 1170)
    elif i == 6:
        pill(ctx, "EVIDENCIA 2026 · SALUD", W / 2, 196, GR, k, 28, filled=True)
        title(ctx, "DIABETES TIPO 2: LOS DOS SIRVEN", WH, 368, 88, k)
        src(ctx, "Li et al., Endocrine 2026 · 27 ensayos · doi:10.1007/s12020-026-04775-5", k, 1190)
    elif i == 7:
        pill(ctx, "REGLA SIMPLE", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "DEPENDE DE TU META", WH, 368, 100, k)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 41 · FUERZA")
