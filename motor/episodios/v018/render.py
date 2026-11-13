"""v018 · ¿Estirar te protege de lesiones? (serie LESIONES · paleta lima + violeta)
Uso: copiar a la carpeta del episodio (con timeline.json) y correr
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

# ---- paleta de la serie LESIONES (acento lima, fondo verde pizarra)
ACC = (0.74, 1.0, 0.32)
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.05, 0.13, 0.08], [0.008, 0.02, 0.014])
from engine_ext import *
CY = ACC
SK = (0.40, 0.85, 1.0)   # celeste: propiocepción
ST = VI                  # violeta: estiramiento


def shield(ctx, cx, cy, s, a, col, fill=0.1, check=0.0):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.move_to(0, -150); ctx.curve_to(60, -110, 110, -110, 130, -115); ctx.curve_to(135, 20, 90, 110, 0, 160)
    ctx.curve_to(-90, 110, -135, 20, -130, -115); ctx.curve_to(-110, -110, -60, -110, 0, -150); ctx.close_path()
    ctx.set_source_rgba(*col, fill * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(7); ctx.stroke()
    if check > 0:
        ctx.move_to(-55, 5); ctx.line_to(-15, 50 * check); ctx.line_to(-15 + 85 * check, -60 * check)
        ctx.set_source_rgba(*WH, check * a); ctx.set_line_width(16); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.restore()


def stretch_leg(ctx, cx, cy, t, a):
    # pierna estirada con flechas de tensión
    sw = 0.5 + 0.5 * math.sin(t * 2.2)
    shield(ctx, cx, cy - 30, 1.0, a, ST, 0.08)
    big(ctx, "?", cx, cy + 50, 200, WH, a)
    for j in range(3):
        y = cy - 120 + j * 90
        L = 60 + 40 * sw
        for sg in (-1, 1):
            x = cx + sg * 250
            ctx.move_to(x, y); ctx.line_to(x + sg * L, y)
            ctx.move_to(x + sg * L - sg * 18, y - 14); ctx.line_to(x + sg * L, y); ctx.line_to(x + sg * L - sg * 18, y + 14)
            ctx.set_source_rgba(*ST, 0.8 * a); ctx.set_line_width(5); ctx.stroke()


BARS = [("SIN PROGRAMA", 1.0, MU), ("ESTIRAR", 0.963, ST), ("EQUILIBRIO", 0.550, SK), ("FUERZA", 0.315, AM)]


def hbars(ctx, n_show, k_last, a, x0=150, y0=600, w=760, bh=86, gap=44, hl=None):
    for j in range(n_show):
        lab, v, col = BARS[j]
        kk = k_last if j == n_show - 1 else 1.0
        y = y0 + j * (bh + gap)
        text(ctx, lab, x0, y - 12, F_MONO, 26, col, a, bold=True)
        rrect(ctx, x0, y, w, bh, 16); ctx.set_source_rgba(*col, 0.05 * a); ctx.fill()
        ww = max(1, w * v * ease(kk))
        rrect(ctx, x0, y, ww, bh, 16)
        on = hl is None or hl == j
        ctx.set_source_rgba(*col, (0.30 if on else 0.12) * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, (0.95 if on else 0.5) * a); ctx.set_line_width(3); ctx.stroke()
        if kk > 0.6:
            text(ctx, "%d %%" % round(v * 100), x0 + ww - 18, y + bh / 2 + 15, F_MONO, 34, WH, a * ease((kk - 0.6) / 0.4), align="right", bold=True)


def dose(ctx, x0, y0, w, h, upto, a):
    line_chart(ctx, x0, y0, w, h, [(lambda f: 0.85 - 0.6 * f, AM, upto, True)],
               [(0.0, "BAJO"), (0.5, "MEDIO"), (1.0, "ALTO")], "VOLUMEN DE FUERZA", "RIESGO DE LESIÓN", a)


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        stretch_leg(ctx, 540, 820, t, k)
    elif i == 1:
        n1 = int(25 * ease((u - 0.3) / 1.5)); n2 = int(26610 * ease((u - 1.3) / 1.8))
        big(ctx, str(n1), 540, 760, 220, CY, k)
        big(ctx, "{:,}".format(n2).replace(",", "."), 540, 1090, 150, SK, ease((u - 1.2) / 0.4))
    elif i == 2:
        hbars(ctx, 2, (u - 0.6) / 1.4, k)
    elif i == 3:
        hbars(ctx, 3, (u - 0.6) / 1.4, k, hl=2)
    elif i == 4:
        hbars(ctx, 4, (u - 0.6) / 1.4, k, hl=3)
    elif i == 5:
        dose(ctx, 150, 600, 780, 440, ease((u - 0.3) / 2.6), k)
    elif i == 6:
        gauge(ctx, 300, 820, 150, 0.2 + 0.6 * ease((u - 0.6) / 1.8), a=k, col=ST)
        shield(ctx, 790, 800, 0.85, k, MU, 0.05)
        big(ctx, "=", 790, 840, 120, WH, ease((u - 2.6) / 0.4))
    elif i == 7:
        shield(ctx, 540, 720, 1.05, k, AM, 0.12, check=ease((u - 1.0) / 0.6))
        barbell_icon(ctx, 540, 1060, t, a=ease((u - 0.4) / 0.4))
    elif i == 8:
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 820); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 190, CY, 1, align="center"); ctx.restore()


def src(ctx, s, k, y=1290):
    text(ctx, s, W / 2, y, F_MONO, 21, MU, k, align="center")


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "MITO VS. REALIDAD · LESIONES", W / 2, 196, CY, k, 28)
        title(ctx, "¿ESTIRAR TE PROTEGE?", WH, 350, 100, k)
    elif i == 1:
        pill(ctx, "METAANÁLISIS · BR J SPORTS MED", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "ENSAYOS CONTROLADOS", WH, 345, 92, k)
        text(ctx, "ENSAYOS", W / 2, 860, F_MONO, 30, CY, k, align="center", bold=True)
        text(ctx, "PARTICIPANTES", W / 2, 1150, F_MONO, 30, SK, ease((u - 1.2) / 0.4), align="center", bold=True)
        src(ctx, "deportistas y personas activas · Lauersen et al., 2014", k, 1240)
    elif i in (2, 3, 4):
        labs = {2: ("ESTIRAR", "SIN EFECTO PROTECTOR", ST), 3: ("EQUILIBRIO", "CASI LA MITAD", SK), 4: ("FUERZA", "MENOS DE 1/3", AM)}
        p, ttl, col = labs[i]
        pill(ctx, "RIESGO DE LESIÓN · " + p, W / 2, 196, col, k, 28, filled=(i == 4))
        title(ctx, ttl, col if i != 2 else WH, 345, 98, k)
        src(ctx, "riesgo relativo vs. sin programa · Lauersen et al., Br J Sports Med 2014", k, 1240)
    elif i == 5:
        pill(ctx, "REVISIÓN 2018", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "MÁS FUERZA, MENOS LESIONES", WH, 345, 86, k)
        src(ctx, "esquema ilustrativo · Lauersen et al., Br J Sports Med 2018", k, 1250)
    elif i == 6:
        pill(ctx, "OJO", W / 2, 196, RD, k, 30)
        title(ctx, "ESTIRAR SÍ SIRVE PARA…", WH, 345, 92, k)
        text(ctx, "FLEXIBILIDAD", 300, 1040, F_MONO, 30, ST, k, align="center", bold=True)
        text(ctx, "LESIONES", 790, 1040, F_MONO, 30, MU, k, align="center", bold=True)
        src(ctx, "Rudisill et al., Am J Sports Med 2022 · Lauersen 2014", k, 1200)
    elif i == 7:
        pill(ctx, "QUÉ HACER", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "NO DEJES FUERA LA FUERZA", AM, 345, 90, k)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)


run_episode(neon, txt, "EXPEDIENTE 18 · LESIONES")
