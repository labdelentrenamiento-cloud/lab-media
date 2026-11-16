"""v027 · ¿Hay que llegar al fallo para ganar músculo? Fallo vs. repeticiones en reserva (serie MÚSCULO · paleta esmeralda + coral)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (0.25, 0.95, 0.66)   # esmeralda
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.03, 0.12, 0.10], [0.004, 0.022, 0.018])
from engine_ext import *
CY = ACC
CO = (1.0, 0.46, 0.38)   # coral = fallo
SK = (0.55, 0.85, 1.0)   # celeste = reserva


def dumbbell(ctx, cx, cy, plate, col, a, tilt=0.0, s=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(tilt); ctx.scale(s, s)
    ctx.move_to(-150, 0); ctx.line_to(150, 0); ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(14); ctx.stroke()
    for sgn in (-1, 1):
        for j in range(plate):
            x = sgn * (70 + j * 26); h = 90 + 26 * plate - j * 10
            rrect(ctx, x - 11, -h / 2, 22, h, 6)
            ctx.set_source_rgba(*col, 0.2 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
    ctx.restore()


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


def rep_bar(ctx, y, done, total, a, reserve=0, x0=150, w=780):
    """barra de repeticiones: celdas llenas = hechas; las últimas `reserve` quedan en reserva."""
    cw = w / total
    for j in range(total):
        x = x0 + j * cw
        rrect(ctx, x + 4, y, cw - 8, 70, 10)
        last = j >= total - reserve
        if j < done:
            col = CO if (j == total - 1 and reserve == 0) else CY
            ctx.set_source_rgba(*col, 0.55 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a)
        else:
            col = SK if last else MU
            ctx.set_source_rgba(*col, 0.06 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, (0.9 if last else 0.4) * a)
        ctx.set_line_width(3); ctx.stroke()


def docs(ctx, n, k, a, x0=170, y0=560, cols=8, col=CY, cw=78, ch=96, gx=14, gy=16):
    m = int(n * k)
    for j in range(m):
        r, c = divmod(j, cols)
        x = x0 + c * (cw + gx); y = y0 + r * (ch + gy)
        rrect(ctx, x, y, cw, ch, 8); ctx.set_source_rgba(*col, 0.12 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.85 * a); ctx.set_line_width(2.5); ctx.stroke()
        for li in range(3):
            ctx.move_to(x + 14, y + 26 + li * 22); ctx.line_to(x + cw - 14 - (18 if li == 2 else 0), y + 26 + li * 22)
            ctx.set_source_rgba(*col, 0.5 * a); ctx.set_line_width(2); ctx.stroke()


def src(ctx, s, k, y=1270):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        n = int(10 * clamp((u - 0.2) / 2.6))
        dumbbell(ctx, 540, 700 - 50 * abs(math.sin(t * 3.2)) * (n < 10), 3, CY if n < 10 else CO, k)
        rep_bar(ctx, 900, n, 10, k)
        if n >= 10:
            big(ctx, "FALLO", 540, 1120, 110, CO, ease((u - 2.9) / 0.3))
    elif i == 1:
        n = min(10, int(1 + 10 * clamp((u - 0.1) / 2.4)))
        big(ctx, str(n), 540, 820, 240, CO if n == 10 else CY, k)
        rep_bar(ctx, 930, n, 10, k)
        text(ctx, "0 REPETICIONES EN RESERVA", W / 2, 1100, F_MONO, 30, CO, ease((u - 2.6) / 0.4), align="center", bold=True)
    elif i == 2:
        docs(ctx, 15, ease((u - 0.1) / 1.4), k, x0=150, y0=520, cols=8)
        vbars(ctx, [("AL FALLO", 0.62, CO), ("SIN FALLO", 0.60, SK)], 250, 1120, 220, 140, 260, ease((u - 2.4) / 1.4), k, label_size=26)
        big(ctx, "≈", 540, 1010, 120, WH, ease((u - 3.8) / 0.4), maxw=200)
    elif i == 3:
        n = int(137 * ease((u - 0.2) / 1.8))
        big(ctx, str(n), 540, 760, 230, CY, k)
        text(ctx, "REVISIONES SISTEMÁTICAS", W / 2, 840, F_MONO, 30, WH, k, align="center", bold=True)
        ka = ease((u - 2.6) / 0.5)
        rrect(ctx, 190, 930, 700, 130, 24); ctx.set_source_rgba(*CY, 0.12 * ka); ctx.fill_preserve(); ctx.set_source_rgba(*CY, ka); ctx.set_line_width(4); ctx.stroke()
        text(ctx, "FALLO = NO NECESARIO", W / 2, 1015, F_BIG, 64, CY, ka, align="center")
    elif i == 4:
        for j, (lab, col, x) in enumerate((("SÍ", CO, 330), ("NO", SK, 750))):
            kk = easeb((u - 0.2 - j * 0.25) / 0.5)
            if kk <= 0: continue
            ctx.save(); ctx.translate(x, 820); ctx.scale(kk, kk)
            ctx.new_path(); ctx.arc(0, 0, 150, 0, 6.283); ctx.set_source_rgba(*col, 0.14); ctx.fill_preserve(); ctx.set_source_rgba(*col, 1); ctx.set_line_width(6); ctx.stroke()
            text(ctx, lab, 0, 50, F_BIG, 150, col, 1, align="center"); ctx.restore()
    elif i in (5, 6):
        hyp = lambda x: 0.85 - 0.6 * x
        stg = lambda x: 0.62 - 0.04 * x
        ser = [(hyp, CY, ease((u - 0.3) / 2.4) if i == 5 else 1.0, True)]
        if i == 6:
            ser.append((stg, AM, ease((u - 0.3) / 2.2), False))
        line_chart(ctx, 170, 560, 740, 440, ser, [(0, "0"), (0.25, "2"), (0.5, "4"), (0.75, "6"), (1, "8")], "REPETICIONES EN RESERVA", "GANANCIA", k)
        if i == 6:
            text(ctx, "FUERZA", 900, 560 + 440 - 0.6 * 440 - 30, F_MONO, 28, AM, ease((u - 2.2) / 0.4), align="right", bold=True)
            text(ctx, "MÚSCULO", 250, 560 + 440 - 0.85 * 440 - 24, F_MONO, 28, CY, 0.6 * k, bold=True)
        else:
            text(ctx, "MÚSCULO", 250, 560 + 440 - 0.85 * 440 - 24, F_MONO, 28, CY, ease((u - 1.0) / 0.4), bold=True)
    elif i == 7:
        g = ease((u - 0.8) / 2.6)
        arm(ctx, 300, 800, 1.0, g, CO, k)
        arm(ctx, 780, 800, 1.0, g, SK, k)
        text(ctx, "AL FALLO", 300, 1010, F_MONO, 28, CO, k, align="center", bold=True)
        text(ctx, "1–3 EN RESERVA", 780, 1010, F_MONO, 28, SK, k, align="center", bold=True)
        big(ctx, "=", 540, 840, 140, WH, ease((u - 3.6) / 0.4), maxw=200)
    elif i == 8:
        dumbbell(ctx, 540, 640, 3, CY, k, 0.06 * math.sin(t * 2))
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1000); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 150, CY, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "FALLO VS. RESERVA · MÚSCULO", W / 2, 196, CY, k, 28)
        title(ctx, "¿HAY QUE LLEGAR AL FALLO?", WH, 368, 100, k)
    elif i == 1:
        pill(ctx, "DEFINICIÓN", W / 2, 196, CO, k, 30, filled=True)
        title(ctx, "NI UNA REPETICIÓN MÁS", WH, 368, 100, k)
    elif i == 2:
        pill(ctx, "METAANÁLISIS · 15 ESTUDIOS", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "SIN DIFERENCIA CLARA", WH, 368, 104, k)
        text(ctx, "FUERZA Y MÚSCULO · ESQUEMA", W / 2, 1210, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Grgic et al., J Sport Health Sci 2022 · doi:10.1016/j.jshs.2021.01.007", k, 1250)
    elif i == 3:
        pill(ctx, "GUÍA ACSM 2026", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "LA GUÍA COINCIDE", WH, 368, 110, k)
        src(ctx, "ACSM Position Stand, Currier et al., Med Sci Sports Exerc 2026 · doi:10.1249/MSS.0000000000003897", k, 1170)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿VAS AL FALLO EN CADA SERIE?", WH, 368, 88, k)
        text(ctx, "ESCRIBE  SÍ  O  NO", W / 2, 1110, F_MONO, 34, AM, ease((u - 0.8) / 0.4), align="center", bold=True)
    elif i == 5:
        pill(ctx, "PERO OJO", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "MÁS CERCA = MÁS MÚSCULO", WH, 368, 96, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1150, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Robinson et al., Sports Med 2024 · metarregresiones · doi:10.1007/s40279-024-02069-2", k, 1200)
    elif i == 6:
        pill(ctx, "FUERZA", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "FUERZA: CASI IGUAL", WH, 368, 104, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1150, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Robinson et al., Sports Med 2024 · doi:10.1007/s40279-024-02069-2", k, 1200)
    elif i == 7:
        pill(ctx, "ESTUDIO 2026 · UN BRAZO VS. EL OTRO", W / 2, 196, SK, k, 28, filled=True)
        title(ctx, "CRECIERON IGUAL", WH, 368, 110, k)
        src(ctx, "Vasconcelos, Refalo et al., Muscles 2026 · 19 adultos entrenados, 8 semanas · doi:10.3390/muscles5030061", k, 1110)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 27 · MÚSCULO")
