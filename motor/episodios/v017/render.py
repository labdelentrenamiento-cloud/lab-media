"""v017 · ¿Tu metabolismo se frena a los 30? (serie METABOLISMO · paleta naranja brasa + turquesa)
Uso: copiar a la carpeta del episodio (con timeline.json) y correr
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

# ---- paleta de la serie METABOLISMO (acento naranja brasa, fondo café profundo)
ACC = (1.0, 0.62, 0.24)
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.17, 0.08, 0.03], [0.025, 0.012, 0.006])
from engine_ext import *
CY = ACC
TL = (0.36, 0.95, 0.85)   # turquesa para datos


def flame(ctx, cx, cy, s, t, a, col=None):
    col = col or CY
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    for j, (sc, al) in enumerate(((1.0, 0.10), (0.62, 0.22))):
        w = 1 + 0.04 * math.sin(t * 6 + j)
        ctx.save(); ctx.scale(sc * w, sc)
        ctx.move_to(0, -200)
        ctx.curve_to(60, -120, 130, -60, 120, 40)
        ctx.curve_to(110, 130, 50, 170, 0, 170)
        ctx.curve_to(-50, 170, -110, 130, -120, 40)
        ctx.curve_to(-125, -30, -70, -60, -40, -130)
        ctx.curve_to(-20, -80, -10, -60, 0, -200)
        ctx.close_path(); ctx.restore()
        ctx.set_source_rgba(*(col if j == 0 else AM), al * a); ctx.fill_preserve()
        ctx.set_source_rgba(*(col if j == 0 else AM), a); ctx.set_line_width(6 if j == 0 else 4); ctx.stroke()
    for k in range(7):
        ph = (t * 0.8 + k / 7) % 1
        x = math.sin(k * 3.1) * 70; y = -180 - ph * 140
        ctx.new_path(); ctx.arc(x, y, 6 * (1 - ph) + 2, 0, 6.283); ctx.set_source_rgba(*AM, a * (1 - ph)); ctx.fill()
    ctx.restore()


# ---- curva de vida (esquema basado en Pontzer 2021): gasto ajustado / adulto
def life(age):
    if age <= 1: return 1.0 + 0.5 * math.sin(age * math.pi / 2)
    if age <= 20: return 1.0 + 0.5 * (1 - (age - 1) / 19) ** 1.4
    if age <= 60: return 1.0
    return 1.0 * (1 - 0.007) ** (age - 60)


def ax(age):   # 0–20 años ocupa el 30 % del ancho
    return 0.3 * age / 20 if age <= 20 else 0.3 + 0.7 * (age - 20) / 75


def lifecurve(ctx, x0, y0, w, h, upto, a, zone=None, zk=0.0, mark1=0.0):
    lo, hi = 0.6, 1.6
    Y = lambda v: y0 + h - (v - lo) / (hi - lo) * h
    ctx.set_line_width(2)
    for i in range(5):
        yy = y0 + h - i * h / 4
        ctx.move_to(x0, yy); ctx.line_to(x0 + w, yy); ctx.set_source_rgba(*CY, 0.12 * a); ctx.stroke()
    ctx.move_to(x0, y0); ctx.line_to(x0, y0 + h); ctx.line_to(x0 + w, y0 + h); ctx.set_source_rgba(*CY, 0.6 * a); ctx.set_line_width(3); ctx.stroke()
    for ag in (1, 20, 60, 90):
        text(ctx, str(ag), x0 + ax(ag) * w, y0 + h + 40, F_MONO, 24, MU, a, align="center")
    text(ctx, "EDAD (AÑOS)", x0 + w, y0 + h + 82, F_MONO, 22, MU, a, align="right")
    text(ctx, "GASTO AJUSTADO POR TAMAÑO", x0, y0 - 18, F_MONO, 22, MU, a)
    ctx.move_to(x0, Y(1.0)); ctx.line_to(x0 + w, Y(1.0)); ctx.set_dash([10, 10]); ctx.set_source_rgba(*WH, 0.3 * a); ctx.stroke(); ctx.set_dash([])
    text(ctx, "ADULTO = 100 %", x0 + w, Y(1.0) - 14, F_MONO, 20, MU, a, align="right")
    if zone and zk > 0:
        a0, a1, col = zone
        xs, xe = x0 + ax(a0) * w, x0 + ax(a1) * w
        rrect(ctx, xs, y0, (xe - xs) * zk, h, 10); ctx.set_source_rgba(*col, 0.14 * a); ctx.fill()
    ages = [i * 0.05 for i in range(21)] + [1 + i * 0.5 for i in range(1, 189)]
    pts = [(x0 + ax(g) * w, Y(life(g))) for g in ages if ax(g) <= upto]
    if len(pts) >= 2:
        ctx.new_path(); ctx.move_to(*pts[0])
        for p in pts[1:]: ctx.line_to(*p)
        ctx.set_source_rgba(*TL, a); ctx.set_line_width(7); ctx.stroke()
        ctx.new_path(); ctx.arc(*pts[-1], 10, 0, 6.283); ctx.set_source_rgba(*WH, a); ctx.fill()
    if mark1 > 0:
        mx, my = x0 + ax(1) * w, Y(1.5)
        ctx.new_path(); ctx.arc(mx, my, 20 + 4 * math.sin(mark1 * 9), 0, 6.283); ctx.set_source_rgba(*AM, mark1 * a); ctx.set_line_width(5); ctx.stroke()


def people(ctx, cx, cy, k, a, t):
    # nube de puntos = personas medidas
    import random as _r
    rg = _r.Random(7)
    for j in range(120):
        ang = rg.random() * 6.283; r = 60 + rg.random() * 300
        x = cx + math.cos(ang) * r * 1.2; y = cy + math.sin(ang) * r * 0.55
        kk = ease((k - j / 160) / 0.3)
        if kk <= 0: continue
        fl = 0.7 + 0.3 * math.sin(t * 4 + j)
        ctx.new_path(); ctx.arc(x, y, 7, 0, 6.283); ctx.set_source_rgba(*(TL if j % 3 else CY), kk * a * fl); ctx.fill()


def scatter(ctx, x0, y0, w, h, k, a, t):
    import random as _r
    rg = _r.Random(11)
    my = y0 + h / 2
    ctx.move_to(x0, my); ctx.line_to(x0 + w, my); ctx.set_source_rgba(*TL, a); ctx.set_line_width(6); ctx.stroke()
    text(ctx, "PROMEDIO", x0, y0 - 10, F_MONO, 24, TL, a, bold=True)
    for j in range(70):
        x = x0 + rg.random() * w; dy = rg.gauss(0, h * 0.18)
        kk = ease((k - j / 90) / 0.3)
        if kk <= 0: continue
        ctx.new_path(); ctx.arc(x, my + dy, 8, 0, 6.283); ctx.set_source_rgba(*CY, 0.85 * kk * a); ctx.fill()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        flame(ctx, 540, 720, 0.95, t, k)
        a2 = easeb((u - 0.9) / 0.5) * k
        if a2 > 0:
            rrect(ctx, 340, 960, 400, 150, 30); ctx.set_source_rgba(0.05, 0.02, 0.01, 0.85 * a2); ctx.fill_preserve()
            ctx.set_source_rgba(*AM, a2); ctx.set_line_width(4); ctx.stroke()
            big(ctx, "30 AÑOS", 540, 1075, 100, AM, a2)
    elif i == 1:
        people(ctx, 540, 760, ease((u - 0.2) / 2.5), k, t)
    elif i == 2:
        lifecurve(ctx, 150, 600, 800, 460, 0.016 + 0.29 * ease((u - 3.4) / 2.2), k, mark1=ease((u - 1.6) / 0.4))
        big(ctx, "+50 % QUE UN ADULTO", 540, 1262, 76, AM, ease((u - 2.4) / 0.4))
    elif i == 3:
        lifecurve(ctx, 150, 600, 800, 460, 0.32 + 0.38 * ease((u - 0.2) / 1.8), k, zone=(20, 60, GR), zk=ease((u - 1.2) / 1.0))
    elif i == 4:
        lifecurve(ctx, 150, 600, 800, 460, 0.7 + 0.3 * ease((u - 0.2) / 2.0), k, zone=(60, 95, RD), zk=ease((u - 1.6) / 1.0))
        big(ctx, "−0,7 % / AÑO", 540, 1230, 90, RD, ease((u - 2.2) / 0.4))
    elif i == 5:
        fiber_bundle(ctx, 190, 640, 700, 380, 8, ease((u - 0.6) / 2.4), t, k, col_on=TL, col_off=CY)
    elif i == 6:
        scatter(ctx, 150, 620, 780, 440, ease((u - 0.2) / 1.6), k, t)
    elif i == 7:
        barbell_icon(ctx, 540, 760, t, a=k)
        gauge(ctx, 540, 1060, 120, 0.15 + 0.6 * ease((u - 1.2) / 2.0), a=ease((u - 0.8) / 0.4), col=TL)
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
        pill(ctx, "MITO VS. REALIDAD · METABOLISMO", W / 2, 196, CY, k, 28)
        title(ctx, "¿SE FRENA A LOS 30?", WH, 350, 100, k)
    elif i == 1:
        pill(ctx, "ESTUDIO · SCIENCE 2021", W / 2, 196, TL, k, 30, filled=True)
        title(ctx, "6.600+ PERSONAS · 29 PAÍSES", WH, 345, 84, k)
        a = ease((u - 2.6) / 0.4)
        text(ctx, "DE 8 DÍAS A 95 AÑOS DE EDAD", W / 2, 1130, F_MONO, 30, WH, a, align="center", bold=True)
        src(ctx, "agua doblemente marcada · Pontzer et al., Science 2021", k, 1220)
    elif i == 2:
        pill(ctx, "RÉCORD DEL CUERPO", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "EL PICO: AL AÑO DE VIDA", WH, 345, 92, k)
        src(ctx, "esquema ilustrativo · Pontzer et al., Science 2021", k, 1318)
    elif i == 3:
        pill(ctx, "DE 20 A 60 AÑOS", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "ESTABLE", GR, 345, 110, k)
        text(ctx, "ESTABLE", 150 + ax(40) * 800, 860, F_MONO, 28, GR, ease((u - 2.0) / 0.4), align="center", bold=True)
        src(ctx, "esquema ilustrativo · ajustado por masa libre de grasa", k, 1220)
    elif i == 4:
        pill(ctx, "DESPUÉS DE LOS 60", W / 2, 196, RD, k, 30)
        title(ctx, "RECIÉN AHÍ EMPIEZA A BAJAR", WH, 345, 86, k)
        src(ctx, "esquema ilustrativo · Pontzer et al., Science 2021", k, 1300)
    elif i == 5:
        pill(ctx, "LO QUE MÁS PESA", W / 2, 196, TL, k, 30, filled=True)
        title(ctx, "TAMAÑO Y MÚSCULO", WH, 345, 100, k)
        a = ease((u - 2.0) / 0.4)
        text(ctx, "MASA LIBRE DE GRASA", W / 2, 1110, F_MONO, 32, TL, a, align="center", bold=True)
        src(ctx, "el gasto total crece con la masa libre de grasa · Pontzer 2021", k, 1200)
    elif i == 6:
        pill(ctx, "OJO", W / 2, 196, RD, k, 30)
        title(ctx, "SON PROMEDIOS", WH, 345, 100, k)
        src(ctx, "cada punto = una persona (esquema)", k, 1160)
    elif i == 7:
        pill(ctx, "QUÉ HACER", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "CONSERVA TU MÚSCULO", GR, 345, 96, k)
        text(ctx, "ENTRENAMIENTO DE FUERZA", W / 2, 930, F_MONO, 30, WH, ease((u - 1.0) / 0.4), align="center", bold=True)
        src(ctx, "OMS 2020: fuerza ≥ 2 días/semana · Bull et al., Br J Sports Med 2020", k, 1250)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)


run_episode(neon, txt, "EXPEDIENTE 17 · METABOLISMO")
