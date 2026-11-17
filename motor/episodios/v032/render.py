"""v032 · Si quisieras conservar tu fuerza al envejecer, harías esto (serie LONGEVIDAD-FUERZA · paleta berenjena + menta + melocotón)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (0.42, 1.0, 0.78)   # menta
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.12, 0.05, 0.16], [0.018, 0.007, 0.026])
from engine_ext import *
CY = ACC
PE = (1.0, 0.62, 0.45)    # melocotón


def title(ctx, s, color=WH, y=345, size=86, a=1.0):
    """título centrado que no invade los 140 px de botones a la derecha"""
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def week(ctx, days, k, a, y=640, col=CY, label=None):
    labs = ["L", "M", "M", "J", "V", "S", "D"]
    sz = 112; x0 = (W - 7 * sz + 14) / 2 - 20
    if label:
        text(ctx, label, x0, y - 22, F_MONO, 26, col, a, bold=True)
    for d in range(7):
        x = x0 + d * sz
        on = d in days
        kk = ease((k - (days.index(d) * 0.3 if on else 0)) / 0.4) if on else 0
        rrect(ctx, x, y, sz - 14, 200, 18)
        c = col if on else MU
        ctx.set_source_rgba(*c, (0.05 + 0.2 * kk) * a); ctx.fill_preserve(); ctx.set_source_rgba(*c, (0.4 + 0.6 * kk) * a); ctx.set_line_width(3); ctx.stroke()
        text(ctx, labs[d], x + (sz - 14) / 2, y + 60, F_BIG, 44, WH, a, align="center")
        if on and kk > 0:
            dumb(ctx, x + (sz - 14) / 2, y + 140, 0.32, col, kk * a)


def dumb(ctx, cx, cy, s, col, a):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    rrect(ctx, -110, -12, 220, 24, 10); ctx.set_source_rgba(*col, a); ctx.fill()
    for sx in (-1, 1):
        rrect(ctx, sx * 80 - 18, -60, 36, 120, 8); ctx.fill()
    ctx.restore()


def badge(ctx, cx, cy, num, unit, col, a, w=400):
    rrect(ctx, cx - w / 2, cy - 160, w, 310, 28); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    big(ctx, num, cx, cy + 30, 120, col, a, maxw=w - 40)
    for li, part in enumerate(unit.split("\n")):
        text(ctx, part, cx, cy + 88 + li * 32, F_MONO, 25, WH, a, align="center", bold=True)


def src(ctx, s, k, y=1270):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        fm = lambda x: 0.85 - 0.12 * x
        ff = lambda x: 0.85 - 0.36 * x
        line_chart(ctx, 170, 560, 700, 440, [(fm, CY, ease((u - 0.2) / 2.2), False), (ff, PE, ease((u - 0.6) / 2.2), False)],
                   [(0, "70"), (0.5, "+1"), (1, "+3 AÑOS")], "", "", k)
        text(ctx, "MÚSCULO", 850, 560 + 440 * (1 - fm(1)) - 28, F_MONO, 26, CY, ease((u - 2.4) / 0.4), align="right", bold=True)
        text(ctx, "FUERZA", 850, 560 + 440 * (1 - ff(1)) + 55, F_MONO, 26, PE, ease((u - 2.8) / 0.4), align="right", bold=True)
        kb = easeb((u - 3.0) / 0.5)
        if kb > 0: big(ctx, "×3", 700, 1180, 110 * kb, PE, kb, maxw=300)
    elif i == 1:
        n = 0
        for r in range(14):
            for c in range(24):
                kk = ease((u - 0.1 - (r * 24 + c) * 0.004) / 0.3)
                if kk <= 0: continue
                ctx.new_path(); ctx.arc(205 + c * 28, 540 + r * 34, 8, 0, 6.283); ctx.set_source_rgba(*CY, 0.85 * kk); ctx.fill()
        clock(ctx, 540, 1100, 70, t, back=0.0, a=ease((u - 1.8) / 0.4), col=PE)
    elif i == 2:
        badge(ctx, 300, 780, "≈1 %", "MASA DE PIERNA\nPOR AÑO", CY, ease((u - 0.1) / 0.4), w=360)
        badge(ctx, 750, 780, "2,5–4 %", "FUERZA DE PIERNA\nPOR AÑO", PE, ease((u - lt(2) - 3.1) / 0.4), w=360)
        for j, (x, col, t0) in enumerate(((300, CY, 0.3), (750, PE, lt(2) + 3.4))):
            kk = ease((u - t0) / 0.5)
            if kk <= 0: continue
            ctx.move_to(x, 990); ctx.line_to(x, 990 + 120 * kk); ctx.set_source_rgba(*col, kk); ctx.set_line_width(8); ctx.stroke()
            ctx.move_to(x - 26, 990 + 120 * kk - 26); ctx.line_to(x, 990 + 120 * kk); ctx.line_to(x + 26, 990 + 120 * kk - 26); ctx.stroke()
    elif i == 3:
        for j in range(3):
            kk = easeb((u - 0.3 - j * 0.35) / 0.5)
            if kk <= 0: continue
            ctx.save(); ctx.translate(270 + j * 270, 800); ctx.scale(kk, kk)
            ctx.new_path(); ctx.arc(0, 0, 105, 0, 6.283); ctx.set_source_rgba(*(CY, PE, AM)[j], 0.14); ctx.fill_preserve(); ctx.set_source_rgba(*(CY, PE, AM)[j], 1); ctx.set_line_width(6); ctx.stroke()
            text(ctx, str(j + 1), 0, 50, F_BIG, 140, (CY, PE, AM)[j], 1, align="center"); ctx.restore()
    elif i == 4:
        week(ctx, [0, 3], ease((u - 0.4) / 0.8), k, y=640, col=CY, label="≥ 2 DÍAS DE FUERZA")
    elif i == 5:
        for j, (lab, col) in enumerate((("0", MU), ("1", PE), ("2", AM), ("3+", CY))):
            kk = easeb((u - 0.2 - j * 0.18) / 0.5)
            if kk <= 0: continue
            ctx.save(); ctx.translate(210 + j * 210, 800); ctx.scale(kk, kk)
            ctx.new_path(); ctx.arc(0, 0, 90, 0, 6.283); ctx.set_source_rgba(*col, 0.14); ctx.fill_preserve(); ctx.set_source_rgba(*col, 1); ctx.set_line_width(6); ctx.stroke()
            big(ctx, lab, 0, 42, 110, col, 1, maxw=150); ctx.restore()
    elif i == 6:
        f = lambda x: 0.12 + 0.70 * x ** 0.8
        line_chart(ctx, 170, 560, 740, 440, [(f, CY, ease((u - 0.4) / 2.8), True)], [(0, "POCAS"), (0.5, ""), (1, "MÁS")], "SERIES", "MÚSCULO GANADO", k)
    elif i == 7:
        f = lambda x: 0.82 - 0.38 * x
        line_chart(ctx, 170, 560, 740, 440, [(f, PE, ease((u - 0.4) / 2.6), True)], [(0, "50"), (0.5, "70"), (1, "90")], "EDAD", "MÚSCULO GANADO", k)
        kk = ease((u - lt(7) - 2.2) / 0.4)
        if kk > 0:
            rrect(ctx, 240, 1110, 600, 76, 20); ctx.set_source_rgba(*CY, 0.12 * kk); ctx.fill_preserve(); ctx.set_source_rgba(*CY, kk); ctx.set_line_width(3); ctx.stroke()
            text(ctx, "A TODA EDAD SE GANA", 540, 1160, F_MONO, 32, WH, kk, align="center", bold=True)
    elif i == 8:
        dumb(ctx, 540, 660, 1.2 + 0.05 * math.sin(t * 3), CY, k)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1000); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 150, CY, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "SI QUISIERAS… · LONGEVIDAD", W / 2, 196, CY, k, 28)
        title(ctx, "LA FUERZA SE VA PRIMERO", WH, 368, 96, k)
        text(ctx, "ESQUEMA", 300, 1170, F_MONO, 22, AM, k, align="center", bold=True)
    elif i == 1:
        pill(ctx, "ESTUDIO HEALTH ABC · 70–79 AÑOS", W / 2, 196, CY, k, 26, filled=True)
        title(ctx, "1.880 PERSONAS, 3 AÑOS", WH, 368, 100, k)
        src(ctx, "Goodpaster et al., J Gerontol A 2006 · doi:10.1093/gerona/61.10.1059", k, 1240)
    elif i == 2:
        pill(ctx, "PÉRDIDA ANUAL", W / 2, 196, PE, k, 30, filled=True)
        title(ctx, "LA FUERZA CAE MÁS RÁPIDO", WH, 368, 96, k)
        src(ctx, "Goodpaster et al., 2006 · fuerza de extensión de rodilla", k, 1240)
    elif i == 3:
        pill(ctx, "SI QUISIERAS FRENARLO", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "3 COSAS QUE HARÍAS", WH, 368, 104, k)
    elif i == 4:
        pill(ctx, "1 · GUÍA OMS 2020", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "FUERZA 2 DÍAS O MÁS", WH, 368, 102, k)
        src(ctx, "Bull et al., Br J Sports Med 2020 · doi:10.1136/bjsports-2020-102955", k, 1000)
    elif i == 5:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿CUÁNTOS DÍAS HACES?", WH, 368, 100, k)
        text(ctx, "ESCRIBE EL NÚMERO", W / 2, 1050, F_MONO, 34, AM, ease((u - 0.8) / 0.4), align="center", bold=True)
    elif i == 6:
        pill(ctx, "2 · VOLUMEN", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "MÁS SERIES, MÁS MÚSCULO", WH, 368, 96, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1150, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Peterson et al., MSSE 2011 · 49 estudios · doi:10.1249/MSS.0b013e3181eb6265", k, 1195)
    elif i == 7:
        pill(ctx, "3 · EMPIEZA HOY", W / 2, 196, PE, k, 30, filled=True)
        title(ctx, "NUNCA ES TARDE", WH, 368, 110, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1080, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Peterson et al., 2011", k, 1240)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 32 · LONGEVIDAD")
