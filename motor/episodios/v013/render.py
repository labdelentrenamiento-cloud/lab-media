"""v013 · ¿Pesas ligeras o pesadas? (serie FUERZA · paleta violeta)
Uso: copiar a la carpeta del episodio (con timeline.json) y correr
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

# ---- paleta de la serie FUERZA (acento violeta-lavanda, fondo índigo)
ACC = (0.70, 0.62, 1.0)
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.09, 0.06, 0.24], [0.012, 0.008, 0.05])
from engine_ext import *
CY = ACC
LT = (0.30, 0.95, 1.0)   # carga ligera = celeste
HV = AM                  # carga pesada = ámbar


def dumbbell(ctx, cx, cy, plate, col, a, tilt=0.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(tilt)
    ctx.move_to(-150, 0); ctx.line_to(150, 0); ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(14); ctx.stroke()
    for sgn in (-1, 1):
        for j in range(plate):
            x = sgn * (70 + j * 26)
            h = 90 + 26 * plate - j * 10
            rrect(ctx, x - 11, -h / 2, 22, h, 6)
            ctx.set_source_rgba(*col, 0.2 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
    ctx.restore()


def arm(ctx, cx, cy, s, g, col, a):
    """bíceps esquemático; g = crecimiento 0..1"""
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


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        a1 = ease((u - 0.1) / 0.4); a2 = ease((u - 0.9) / 0.4)
        dumbbell(ctx, 540, 640, 1, LT, a1, 0.08 * math.sin(t * 2))
        dumbbell(ctx, 540, 1000, 3, HV, a2, -0.08 * math.sin(t * 2))
        big(ctx, "VS", 540, 845, 90, WH, ease((u - 1.4) / 0.4))
    elif i == 1:
        n = int(21 * ease((u - 0.2) / 1.6))
        big(ctx, str(n), 540, 700, 220, CY, k)
        for j, (lab, col, x) in enumerate([("≤ 60 % 1RM", LT, 290), ("> 60 % 1RM", HV, 790)]):
            aa = ease((u - 2.4 - j * 1.2) / 0.4)
            if aa <= 0: continue
            dumbbell(ctx, x, 950, 1 + 2 * j, col, aa)
    elif i == 2:
        f = ease((u - 0.2) / 2.4)
        fiber_bundle(ctx, 200, 520, 680, 420, 7, f, t, a=k, col_on=RD, col_off=CY)
        gauge(ctx, 540, 1150, 120, f, a=k, col=RD)
    elif i == 3:
        g = ease((u - 0.3) / 2.0)
        arm(ctx, 300, 820, 1.05, g, LT, k)
        arm(ctx, 780, 820, 1.05, g, HV, k)
        big(ctx, "≈", 540, 860, 150, WH, ease((u - 1.6) / 0.4), maxw=200)
    elif i == 4:
        vbars(ctx, [("LIGERA", 0.62, LT), ("PESADA", 1.0, HV)], 290, 1080, 210, 90, 460, (u - 0.3) / 1.5, a=k, label_size=30)
        big(ctx, "1RM", 540, 560, 70, WH, ease((u - 1.6) / 0.4), maxw=300)
    elif i == 5:
        cols = 7; sz = 86; x0 = 540 - (cols - 1) * sz / 2
        for j in range(28):
            kk = ease(((u - 0.2) / 2.2 * 28 - j) / 3)
            if kk <= 0: continue
            r, c = divmod(j, cols)
            ctx.new_path(); ctx.arc(x0 + c * sz, 520 + r * sz, 28, 0, 6.283)
            ctx.set_source_rgba(*CY, 0.2 * kk * k); ctx.fill_preserve(); ctx.set_source_rgba(*CY, kk * k); ctx.set_line_width(3); ctx.stroke()
        n = int(747 * ease((u - 2.0) / 1.6))
        big(ctx, str(n), 540, 1150, 170, WH, ease((u - 1.8) / 0.4))
    elif i == 6:
        n = int(1 + 17 * ease((u - 0.2) / 3.2))
        dumbbell(ctx, 540, 760 - 60 * abs(math.sin(t * 4)), 1, LT, k)
        big(ctx, f"{n}", 540, 1110, 200, LT if n <= 15 else GR, k, maxw=400)
    elif i == 7:
        a1 = ease((u - 0.2) / 0.4); a2 = ease((u - 2.6) / 0.4)
        arm(ctx, 290, 720, 0.9, 1.0, GR, a1)
        dumbbell(ctx, 790, 720, 3, HV, a2)
        text(ctx, "MÚSCULO", 290, 950, F_BIG, 70, GR, a1, align="center")
        text(ctx, "FUERZA MÁX.", 790, 950, F_BIG, 70, HV, a2, align="center")
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
        pill(ctx, "EXPEDIENTE · FUERZA", W / 2, 196, CY, k, 28)
        title(ctx, "¿LIGERAS O PESADAS?", WH, 350, 96, k)
        text(ctx, "LIGERA", 540, 545, F_MONO, 30, LT, ease((u - 0.1) / 0.4), align="center", bold=True)
        text(ctx, "PESADA", 540, 1150, F_MONO, 30, HV, ease((u - 0.9) / 0.4), align="center", bold=True)
    elif i == 1:
        pill(ctx, "METAANÁLISIS · J STRENGTH COND RES 2017", W / 2, 196, CY, k, 26)
        title(ctx, "21 ESTUDIOS", WH, 345, 100, k)
        text(ctx, "ESTUDIOS", 540, 780, F_MONO, 34, CY, k, align="center", bold=True)
        for j, (lab, col, x) in enumerate([("≤ 60 % DEL MÁXIMO", LT, 290), ("> 60 % DEL MÁXIMO", HV, 790)]):
            aa = ease((u - 2.4 - j * 1.2) / 0.4)
            text(ctx, lab, x, 1110, F_MONO, 28, col, aa, align="center", bold=True)
        src(ctx, "Schoenfeld et al., 2017 · 1RM = peso máximo para 1 repetición", k)
    elif i == 2:
        pill(ctx, "CONDICIÓN DEL ESTUDIO", W / 2, 196, RD, k, 30)
        title(ctx, "HASTA EL FALLO", RD, 345, 100, k)
        text(ctx, "ESFUERZO", 540, 1300, F_MONO, 28, RD, k, align="center", bold=True)
    elif i == 3:
        pill(ctx, "RESULTADO 01 · HIPERTROFIA", W / 2, 196, GR, k, 28, filled=True)
        title(ctx, "MÚSCULO: SIMILAR", WH, 345, 96, k)
        text(ctx, "LIGERA", 300, 1030, F_MONO, 30, LT, k, align="center", bold=True)
        text(ctx, "PESADA", 780, 1030, F_MONO, 30, HV, k, align="center", bold=True)
        src(ctx, "esquema ilustrativo · Schoenfeld et al., J Strength Cond Res 2017", k)
    elif i == 4:
        pill(ctx, "RESULTADO 02 · FUERZA MÁXIMA", W / 2, 196, HV, k, 28, filled=True)
        title(ctx, "GANA LA PESADA", HV, 345, 100, k)
        src(ctx, "ganancia de 1RM mayor con cargas altas · esquema ilustrativo", k, 1220)
    elif i == 5:
        pill(ctx, "METAANÁLISIS EN RED · MSSE 2021", W / 2, 196, CY, k, 28)
        title(ctx, "MISMA CONCLUSIÓN", WH, 345, 96, k)
        text(ctx, "28 ESTUDIOS", 540, 880, F_MONO, 30, CY, k, align="center", bold=True)
        text(ctx, "ADULTOS", 540, 1215, F_MONO, 32, WH, ease((u - 1.8) / 0.4), align="center", bold=True)
        src(ctx, "Lopez et al., Med Sci Sports Exerc 2021", k)
    elif i == 6:
        pill(ctx, "CARGA BAJA = MÁS REPETICIONES", W / 2, 196, LT, k, 28)
        title(ctx, "MÁS DE 15 REPETICIONES", WH, 345, 92, k)
        text(ctx, "REPETICIONES", 540, 1180, F_MONO, 30, LT, k, align="center", bold=True)
        src(ctx, "carga baja: > 15 repeticiones máximas (Lopez et al., 2021)", k, 1250)
    elif i == 7:
        pill(ctx, "EN RESUMEN", W / 2, 196, GR, k, 30)
        title(ctx, "ELIGE SEGÚN TU META", WH, 345, 96, k)
        text(ctx, "carga que", 290, 1010, F_MONO, 30, WH, ease((u - 0.2) / 0.4), align="center")
        text(ctx, "manejes bien", 290, 1050, F_MONO, 30, WH, ease((u - 0.2) / 0.4), align="center")
        text(ctx, "cargas altas", 790, 1010, F_MONO, 30, WH, ease((u - 2.6) / 0.4), align="center")
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)
        a = ease((u - 0.8) / 0.4)
        if a > 0:
            pulse = 1 + 0.04 * math.sin(t * 7)
            ctx.save(); ctx.translate(540, 1000); ctx.scale(pulse, pulse)
            rrect(ctx, -170, -50, 340, 100, 50); ctx.set_source_rgba(*RD, a); ctx.fill()
            text(ctx, "SEGUIR", 0, 18, F_UI, 50, WH, a, align="center", bold=True); ctx.restore()


run_episode(neon, txt, "EXPEDIENTE 13 · CARGA")
