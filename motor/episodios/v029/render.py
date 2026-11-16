"""v029 · ¿Qué pasa si entrenas cada músculo solo 1 vez por semana? (serie MÚSCULO-FUERZA · paleta vino + lima + rosa)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (0.80, 1.0, 0.32)   # lima
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.15, 0.035, 0.09], [0.022, 0.005, 0.014])
from engine_ext import *
CY = ACC
PK = (1.0, 0.52, 0.72)   # rosa


def week(ctx, days, k, a, y=640, col=CY, sets=None, label=None):
    """semana L–D; days = índices encendidos; sets = series por día encendido (bloques)."""
    labs = ["L", "M", "M", "J", "V", "S", "D"]
    sz = 122; x0 = (W - 7 * sz + 14) / 2
    if label:
        text(ctx, label, x0, y - 22, F_MONO, 26, col, a, bold=True)
    for d in range(7):
        x = x0 + d * sz
        on = d in days
        kk = ease((k - (days.index(d) * 0.25 if on else 0)) / 0.4) if on else 0
        rrect(ctx, x, y, sz - 14, 230, 18)
        c = col if on else MU
        ctx.set_source_rgba(*c, (0.05 + 0.18 * kk) * a); ctx.fill_preserve(); ctx.set_source_rgba(*c, (0.4 + 0.6 * kk) * a); ctx.set_line_width(3); ctx.stroke()
        text(ctx, labs[d], x + (sz - 14) / 2, y + 56, F_BIG, 44, WH, a, align="center")
        if on and sets:
            n = sets
            for s_ in range(n):
                bh = min(22, 130 / n - 4)
                yy = y + 214 - (s_ + 1) * (bh + 4)
                rrect(ctx, x + 18, yy, sz - 50, bh, 5)
                ctx.set_source_rgba(*c, 0.85 * a * kk); ctx.fill()


def arm(ctx, cx, cy, s, g, col, a):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    b = 1 + 0.18 * g
    ctx.move_to(-120, 120); ctx.curve_to(-125, 40, -90, -20, -40, -40)
    ctx.curve_to(-10, -110 * b, 70, -120 * b, 95, -40)
    ctx.curve_to(110, 0, 115, 60, 120, 120)
    ctx.curve_to(60, 140, -60, 140, -120, 120); ctx.close_path()
    ctx.set_source_rgba(*col, (0.08 + 0.12 * g) * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    for k in range(4):
        ctx.move_to(-60 + k * 40, 70); ctx.curve_to(-50 + k * 40, -10 * b, -30 + k * 40, -40 * b, -10 + k * 40, -60 * b)
        ctx.set_source_rgba(*col, 0.45 * a); ctx.set_line_width(2.5); ctx.stroke()
    ctx.restore()


def badge(ctx, cx, cy, num, unit, col, a):
    rrect(ctx, cx - 210, cy - 170, 420, 330, 30); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    big(ctx, num, cx, cy + 40, 170, col, a, maxw=380)
    for li, part in enumerate(unit.split("\n")):
        text(ctx, part, cx, cy + 100 + li * 34, F_MONO, 26, WH, a, align="center", bold=True)


def src(ctx, s, k, y=1270):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        week(ctx, [0], ease((u - 0.1) / 0.5), k, y=560, col=PK, label="1 VEZ")
        week(ctx, [0, 2, 4], ease((u - 1.2) / 0.5), ease((u - 1.0) / 0.4), y=900, col=CY, label="3 VECES")
    elif i == 1:
        week(ctx, [0], ease((u - 0.2) / 0.5), k, y=560, col=PK, sets=9, label="9 SERIES EN 1 DÍA")
        week(ctx, [0, 2, 4], ease((u - 1.4) / 0.6), ease((u - 1.2) / 0.4), y=900, col=CY, sets=3, label="3 + 3 + 3 SERIES")
    elif i == 2:
        vbars(ctx, [("1 DÍA", 0.74, PK), ("2 DÍAS", 0.76, AM), ("3 DÍAS", 0.77, CY)], 165, 1080, 190, 80, 420, ease((u - 0.2) / 1.6), k, label_size=28)
        big(ctx, "≈", 540, 620, 110, WH, ease((u - 2.6) / 0.4), maxw=200)
    elif i == 3:
        f = lambda x: 0.1 + 0.75 * (1 - math.exp(-x * 2.6))
        line_chart(ctx, 170, 560, 740, 440, [(f, CY, ease((u - 0.3) / 2.6), True)], [(0, "0"), (0.33, "10"), (0.66, "20"), (1, "30")], "SERIES POR SEMANA", "MÚSCULO", k)
    elif i == 4:
        for j, (lab, col, x) in enumerate((("1", PK, 260), ("2", AM, 540), ("3", CY, 820))):
            kk = easeb((u - 0.2 - j * 0.2) / 0.5)
            if kk <= 0: continue
            ctx.save(); ctx.translate(x, 820); ctx.scale(kk, kk)
            ctx.new_path(); ctx.arc(0, 0, 115, 0, 6.283); ctx.set_source_rgba(*col, 0.14); ctx.fill_preserve(); ctx.set_source_rgba(*col, 1); ctx.set_line_width(6); ctx.stroke()
            text(ctx, lab, 0, 55, F_BIG, 150, col, 1, align="center"); ctx.restore()
    elif i == 5:
        f = lambda x: 0.15 + 0.7 * (1 - math.exp(-x * 2.2))
        line_chart(ctx, 170, 560, 740, 440, [(f, AM, ease((u - 0.3) / 2.6), True)], [(0, "1"), (0.33, "2"), (0.66, "3"), (1, "4+")], "SESIONES POR SEMANA", "FUERZA", k)
    elif i == 6:
        badge(ctx, 300, 800, "≥ 2", "SESIONES\nPOR SEMANA", AM, ease((u - 0.2) / 0.5))
        badge(ctx, 780, 800, "~10", "SERIES POR\nMÚSCULO/SEMANA", CY, ease((u - 2.4) / 0.5))
    elif i == 7:
        if u < d * 0.48:
            week(ctx, [2], ease((u - 0.1) / 0.4), k, y=640, col=PK, sets=6, label="1 DÍA: SIRVE")
        else:
            kk = ease((u - d * 0.48) / 0.4)
            week(ctx, [0, 3], kk, k, y=640, col=CY, sets=3, label="MÁS DÍAS: REPARTE")
    elif i == 8:
        arm(ctx, 540, 640, 1.1, 0.6 + 0.4 * ease(u / 1.0), CY, k)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1000); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 150, CY, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "QUÉ PASA SI… · MÚSCULO", W / 2, 196, CY, k, 28)
        title(ctx, "¿1 VEZ POR SEMANA ALCANZA?", WH, 368, 94, k)
    elif i == 1:
        pill(ctx, "METAANÁLISIS · 25 ESTUDIOS", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "MISMAS SERIES, OTRO REPARTO", WH, 368, 90, k)
        src(ctx, "Schoenfeld, Grgic y Krieger, J Sports Sci 2019 · doi:10.1080/02640414.2018.1555906", k, 1235)
    elif i == 2:
        pill(ctx, "RESULTADO", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "MÚSCULO: PARECIDO", WH, 368, 106, k)
        text(ctx, "ESQUEMA · CON EL MISMO VOLUMEN", W / 2, 1180, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Schoenfeld et al., J Sports Sci 2019", k, 1225)
    elif i == 3:
        pill(ctx, "LA CLAVE", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "EL VOLUMEN SEMANAL", WH, 368, 104, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1150, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Pelland et al., Sports Med 2025 · 67 estudios · doi:10.1007/s40279-025-02344-w", k, 1200)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿CUÁNTOS DÍAS DE PIERNA?", WH, 368, 96, k)
        text(ctx, "ESCRIBE EL NÚMERO", W / 2, 1090, F_MONO, 34, AM, ease((u - 0.8) / 0.4), align="center", bold=True)
    elif i == 5:
        pill(ctx, "FUERZA", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "MÁS DÍAS, MÁS FUERZA", WH, 368, 104, k)
        text(ctx, "ESQUEMA · CADA DÍA EXTRA SUMA MENOS", W / 2, 1150, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Pelland et al., Sports Med 2025 · doi:10.1007/s40279-025-02344-w", k, 1200)
    elif i == 6:
        pill(ctx, "GUÍA ACSM 2026", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "LO QUE RECOMIENDA", WH, 368, 106, k)
        src(ctx, "ACSM Position Stand, Currier et al., Med Sci Sports Exerc 2026 · doi:10.1249/MSS.0000000000003897", k, 1080)
    elif i == 7:
        pill(ctx, "EN LA PRÁCTICA", W / 2, 196, PK, k, 30, filled=True)
        title(ctx, "UN DÍA SIRVE, DOS AYUDAN", WH, 368, 96, k)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 29 · MÚSCULO")
