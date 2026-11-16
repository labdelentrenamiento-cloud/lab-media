"""v028 · ¿El cardio te quita músculo? Mito vs. realidad (serie RENDIMIENTO-HÍBRIDO · paleta naranja neón + azul eléctrico)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (1.0, 0.58, 0.18)   # naranja neón
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.05, 0.07, 0.19], [0.006, 0.010, 0.035])
from engine_ext import *
CY = ACC
EB = (0.36, 0.62, 1.0)   # azul eléctrico = cardio
PW = (0.95, 0.95, 1.0)


def dumbbell(ctx, cx, cy, plate, col, a, tilt=0.0, s=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(tilt); ctx.scale(s, s)
    ctx.move_to(-150, 0); ctx.line_to(150, 0); ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(14); ctx.stroke()
    for sgn in (-1, 1):
        for j in range(plate):
            x = sgn * (70 + j * 26); h = 90 + 26 * plate - j * 10
            rrect(ctx, x - 11, -h / 2, 22, h, 6)
            ctx.set_source_rgba(*col, 0.2 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
    ctx.restore()


def runner(ctx, cx, cy, s, t, a, col=EB):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    bob = -abs(math.sin(t * 6)) * 10; sw = math.sin(t * 6)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(9); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.new_path(); ctx.arc(10, -170 + bob, 30, 0, 6.283); ctx.stroke()
    ctx.move_to(5, -135 + bob); ctx.line_to(-10, -20 + bob); ctx.stroke()
    ctx.move_to(-10, -20 + bob); ctx.line_to(-10 + 55 * sw, 50); ctx.line_to(-10 + 70 * sw, 120); ctx.stroke()
    ctx.move_to(-10, -20 + bob); ctx.line_to(-10 - 55 * sw, 50); ctx.line_to(-10 - 80 * sw, 110); ctx.stroke()
    ctx.move_to(2, -110 + bob); ctx.line_to(2 - 50 * sw, -60 + bob); ctx.line_to(2 - 30 * sw, -20 + bob); ctx.stroke()
    ctx.move_to(2, -110 + bob); ctx.line_to(2 + 50 * sw, -70 + bob); ctx.line_to(2 + 70 * sw, -40 + bob); ctx.stroke()
    ctx.restore()
    for j in range(3):
        y = cy - 60 * s + j * 40 * s
        x = cx - 120 * s - ((t * 300 + j * 50) % 120)
        ctx.move_to(x, y); ctx.line_to(x - 60, y); ctx.set_source_rgba(*col, 0.5 * a); ctx.set_line_width(4); ctx.stroke()


def group_bars(ctx, groups, base, maxh, k, a, bw=120, inner=24, gap=120, x0=None):
    """groups: [(etiqueta, [(v, col), (v, col)])]"""
    tw = len(groups) * (2 * bw + inner) + (len(groups) - 1) * gap
    x = (W - tw) / 2 if x0 is None else x0
    for gi, (lab, vals) in enumerate(groups):
        for j, (v, col) in enumerate(vals):
            kk = ease((k - gi * 0.2 - j * 0.1) / 0.6)
            if kk <= 0: continue
            xx = x + j * (bw + inner); h = maxh * v * kk
            rrect(ctx, xx, base - h, bw, h, 12); ctx.set_source_rgba(*col, 0.25 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
        text(ctx, lab, x + bw + inner / 2, base + 46, F_MONO, 26, WH, a * ease(k / 0.4), align="center", bold=True)
        x += 2 * bw + inner + gap


def legend(ctx, y, a):
    for j, (lab, col) in enumerate((("SOLO PESAS", CY), ("PESAS + CARDIO", EB))):
        x = 220 + j * 340
        rrect(ctx, x, y - 22, 34, 26, 6); ctx.set_source_rgba(*col, 0.8 * a); ctx.fill()
        text(ctx, lab, x + 48, y, F_MONO, 24, col, a, bold=True)


def src(ctx, s, k, y=1270):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        dumbbell(ctx, 300, 760, 3, CY, ease((u - 0.1) / 0.4), 0.08 * math.sin(t * 2), 0.85)
        runner(ctx, 790, 780, 1.1, t, ease((u - 0.6) / 0.4))
        k3 = ease((u - 1.6) / 0.4)
        big(ctx, "¿MENOS MÚSCULO?", 540, 1090, 84, RD, k3)
    elif i == 1:
        n = int(43 * ease((u - 0.1) / 1.6))
        big(ctx, str(n), 540, 760, 230, CY, k)
        text(ctx, "ESTUDIOS", W / 2, 840, F_MONO, 32, WH, k, align="center", bold=True)
        for j, (lab, col, x) in enumerate((("SOLO PESAS", CY, 300), ("PESAS + CARDIO", EB, 780))):
            aa = ease((u - 2.0 - j * 0.6) / 0.4)
            if aa <= 0: continue
            pill(ctx, lab, x, 960, col, aa, 30, filled=True)
    elif i == 2:
        group_bars(ctx, [("MÚSCULO", [(0.70, CY), (0.70, EB)]), ("FUERZA MÁX.", [(0.85, CY), (0.83, EB)])], 1060, 420, (u - 0.2) / 1.6, k)
        legend(ctx, 560, k)
    elif i == 3:
        for j, (lab, col, x) in enumerate((("ANTES", EB, 300), ("DESPUÉS", CY, 780))):
            kk = easeb((u - 0.2 - j * 0.25) / 0.5)
            if kk <= 0: continue
            ctx.save(); ctx.translate(x, 820); ctx.scale(kk, kk)
            rrect(ctx, -200, -110, 400, 220, 40); ctx.set_source_rgba(*col, 0.14); ctx.fill_preserve(); ctx.set_source_rgba(*col, 1); ctx.set_line_width(6); ctx.stroke()
            big(ctx, lab, 0, 35, 100, col, 1, maxw=360); ctx.restore()
    elif i == 4:
        group_bars(ctx, [("FUERZA EXPLOSIVA", [(0.80, CY), (0.58, EB)])], 1060, 420, (u - 0.2) / 1.6, k)
        legend(ctx, 560, k)
        kk = ease((u - 3.4) / 0.4)
        rrect(ctx, 650, 700, 330, 90, 20); ctx.set_source_rgba(*RD, 0.12 * kk); ctx.fill_preserve(); ctx.set_source_rgba(*RD, kk); ctx.set_line_width(3); ctx.stroke()
        text(ctx, "MISMA SESIÓN", 815, 758, F_MONO, 28, RD, kk, align="center", bold=True)
    elif i == 5:
        for j, (a_lab, a_col, b_lab, b_col, y) in enumerate(((("PESAS", CY, "CARDIO", EB, 660)), (("CARDIO", EB, "PESAS", CY, 900)))):
            kk = ease((u - 0.3 - j * 0.6) / 0.4)
            if kk <= 0: continue
            pill(ctx, a_lab, 330, y, a_col, kk, 40, filled=True)
            ctx.move_to(470, y + 28); ctx.line_to(600, y + 28); ctx.set_source_rgba(*WH, kk); ctx.set_line_width(5); ctx.stroke()
            ctx.move_to(580, y + 12); ctx.line_to(604, y + 28); ctx.line_to(580, y + 44); ctx.stroke()
            pill(ctx, b_lab, 750, y, b_col, kk, 40, filled=True)
        kk = ease((u - 3.6) / 0.4)
        text(ctx, "▲ TENDENCIA", 540, 820, F_MONO, 30, GR, kk, align="center", bold=True)
    elif i == 6:
        v = 0.25 + 0.5 * ease((u - 0.4) / 2.2)
        gauge(ctx, 540, 860, 230, v, k, col=EB)
        runner(ctx, 540, 1110, 0.45, t, k)
    elif i == 7:
        dumbbell(ctx, 220, 820, 2, CY, k, 0, 0.6)
        clock(ctx, 540, 820, 150, t, ease((u - 0.3) / 2.0), k)
        runner(ctx, 870, 850, 0.75, t, k)
        big(ctx, "≥ 3 H", 540, 1110, 100, WH, ease((u - 1.4) / 0.4), maxw=400)
    elif i == 8:
        dumbbell(ctx, 330, 640, 2, CY, k, 0.06 * math.sin(t * 2), 0.7)
        runner(ctx, 760, 660, 0.8, t, k)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1000); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 150, CY, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "MITO VS. REALIDAD · RENDIMIENTO", W / 2, 196, CY, k, 28)
        title(ctx, "¿EL CARDIO TE QUITA MÚSCULO?", WH, 368, 92, k)
    elif i == 1:
        pill(ctx, "METAANÁLISIS", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "PESAS VS. PESAS + CARDIO", WH, 368, 96, k)
        src(ctx, "Schumann et al., Sports Med 2022 · adultos sanos, ≥ 4 semanas · doi:10.1007/s40279-021-01587-7", k, 1110)
    elif i == 2:
        pill(ctx, "RESULTADO", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "PRÁCTICAMENTE IGUAL", WH, 368, 104, k)
        text(ctx, "ESQUEMA: SIN DIFERENCIA SIGNIFICATIVA", W / 2, 1180, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Schumann et al., Sports Med 2022 · 43 estudios", k, 1225)
    elif i == 3:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿CARDIO ANTES O DESPUÉS?", WH, 368, 96, k)
        text(ctx, "ESCRIBE  ANTES  O  DESPUÉS", W / 2, 1110, F_MONO, 34, AM, ease((u - 0.8) / 0.4), align="center", bold=True)
    elif i == 4:
        pill(ctx, "LO QUE SÍ SE FRENA", W / 2, 196, RD, k, 28, filled=True)
        title(ctx, "LA FUERZA EXPLOSIVA", WH, 368, 104, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1180, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Schumann et al., Sports Med 2022 · efecto mayor en la misma sesión", k, 1225)
    elif i == 5:
        pill(ctx, "REVISIÓN PARAGUAS 2026 · 17 METAANÁLISIS", W / 2, 196, CY, k, 26, filled=True)
        title(ctx, "¿IMPORTA EL ORDEN?", WH, 368, 104, k)
        text(ctx, "SIN DIFERENCIA SIGNIFICATIVA", W / 2, 1110, F_MONO, 26, WH, ease((u - 2.0) / 0.4), align="center", bold=True)
        src(ctx, "Held et al., Sports Med 2026 · 144 estudios · doi:10.1007/s40279-026-02401-y", k, 1170)
    elif i == 6:
        pill(ctx, "BONUS", W / 2, 196, EB, k, 30, filled=True)
        title(ctx, "MÁS CAPACIDAD AERÓBICA", WH, 368, 96, k)
        text(ctx, "VS. SOLO PESAS", W / 2, 1220, F_MONO, 26, EB, k, align="center", bold=True)
        src(ctx, "Held et al., Sports Med 2026 · doi:10.1007/s40279-026-02401-y", k, 1262)
    elif i == 7:
        pill(ctx, "SI BUSCAS EXPLOSIVIDAD", W / 2, 196, AM, k, 28, filled=True)
        title(ctx, "SEPÁRALOS O PESAS PRIMERO", WH, 368, 92, k)
        src(ctx, "Schumann et al., Sports Med 2022 · Held et al., Sports Med 2026", k, 1200)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 28 · RENDIMIENTO")
