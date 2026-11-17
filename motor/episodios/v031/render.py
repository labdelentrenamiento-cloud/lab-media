"""v031 · ¿Pesas libres o máquinas? Comparación (serie MÚSCULO-FUERZA · paleta grafito cálido + cian + naranja)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (0.30, 0.92, 1.0)   # cian
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.12, 0.10, 0.085], [0.018, 0.015, 0.012])
from engine_ext import *
CY = ACC
OR = (1.0, 0.58, 0.22)    # naranja


def title(ctx, s, color=WH, y=345, size=86, a=1.0):
    """título centrado que no invade los 140 px de botones a la derecha"""
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def dumbbell(ctx, cx, cy, s, col, a, ang=0.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(ang); ctx.scale(s, s)
    rrect(ctx, -110, -12, 220, 24, 10); ctx.set_source_rgba(*col, 0.3 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    for sx in (-1, 1):
        for j, (w_, h_) in enumerate(((34, 140), (26, 110))):
            x = sx * (70 + j * 36) - (w_ if sx < 0 else 0) * 0 - w_ / 2
            rrect(ctx, x, -h_ / 2, w_, h_, 8); ctx.set_source_rgba(*col, 0.18 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def machine(ctx, cx, cy, s, col, a, lift=0.0):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(5)
    ctx.move_to(-120, 200); ctx.line_to(-120, -200); ctx.line_to(120, -200); ctx.line_to(120, 200); ctx.stroke()
    ctx.move_to(-150, 200); ctx.line_to(150, 200); ctx.stroke()
    ctx.new_path(); ctx.arc(0, -170, 18, 0, 6.283); ctx.stroke()
    top = 40 - 110 * lift
    ctx.move_to(0, -152); ctx.line_to(0, top); ctx.set_line_width(3); ctx.stroke()
    for j in range(6):
        y = top + j * 26
        rrect(ctx, -70, y, 140, 20, 5); ctx.set_source_rgba(*col, (0.35 if j < 4 else 0.12) * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
    ctx.move_to(-60, 196); ctx.line_to(-60, 190); ctx.restore()


def arm(ctx, cx, cy, s, g, col, a):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    b = 1 + 0.22 * g
    ctx.move_to(-120, 120); ctx.curve_to(-125, 40, -90, -20, -40, -40)
    ctx.curve_to(-10, -110 * b, 70, -120 * b, 95, -40)
    ctx.curve_to(110, 0, 115, 60, 120, 120)
    ctx.curve_to(60, 140, -60, 140, -120, 120); ctx.close_path()
    ctx.set_source_rgba(*col, (0.08 + 0.12 * g) * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    for k in range(4):
        ctx.move_to(-60 + k * 40, 70); ctx.curve_to(-50 + k * 40, -10 * b, -30 + k * 40, -40 * b, -10 + k * 40, -60 * b)
        ctx.set_source_rgba(*col, 0.45 * a); ctx.set_line_width(2.5); ctx.stroke()
    ctx.restore()


def badge(ctx, cx, cy, num, unit, col, a, w=300):
    rrect(ctx, cx - w / 2, cy - 150, w, 290, 26); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    big(ctx, num, cx, cy + 30, 130, col, a, maxw=w - 40)
    for li, part in enumerate(unit.split("\n")):
        text(ctx, part, cx, cy + 85 + li * 32, F_MONO, 24, WH, a, align="center", bold=True)


def src(ctx, s, k, y=1270):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        dumbbell(ctx, 300, 780, 1.05, OR, k, ang=-0.25 + 0.1 * math.sin(t * 2))
        machine(ctx, 770, 780, 1.0, CY, ease((u - 0.3) / 0.4), lift=0.5 + 0.5 * math.sin(t * 2.2))
        kv = easeb((u - 0.8) / 0.5)
        if kv > 0: big(ctx, "VS", 540, 820, 130 * kv, WH, kv, maxw=200)
    elif i == 1:
        badge(ctx, 250, 760, "13", "ESTUDIOS", CY, ease((u - 0.1) / 0.4), w=240)
        badge(ctx, 535, 760, "1.016", "PERSONAS", OR, ease((u - 1.4) / 0.4), w=290)
        badge(ctx, 815, 760, "≥6", "SEMANAS", AM, ease((u - 3.0) / 0.4), w=240)
    elif i == 2:
        g = ease((u - 0.6) / 2.0)
        arm(ctx, 300, 760, 0.95, g, OR, k)
        arm(ctx, 780, 760, 0.95, g, CY, ease((u - 0.2) / 0.4))
        text(ctx, "PESO LIBRE", 300, 990, F_MONO, 30, OR, k, align="center", bold=True)
        text(ctx, "MÁQUINAS", 780, 990, F_MONO, 30, CY, k, align="center", bold=True)
        ke = easeb((u - 2.0) / 0.5)
        if ke > 0: big(ctx, "=", 540, 790, 150 * ke, GR, ke, maxw=200)
    elif i == 3:
        kk = ease((u - 0.2) / 1.4)
        # prueba con peso libre
        text(ctx, "PRUEBA CON PESO LIBRE", 300, 560, F_MONO, 24, WH, k, align="center", bold=True)
        vbars(ctx, [("ENTRENÓ\nLIBRE", 0.85, OR), ("ENTRENÓ\nMÁQUINA", 0.62, CY)], 150, 1000, 130, 40, 380, kk, k, label_size=22)
        text(ctx, "PRUEBA EN MÁQUINA", 780, 560, F_MONO, 24, WH, ease((u - 1.0) / 0.4), align="center", bold=True)
        vbars(ctx, [("ENTRENÓ\nLIBRE", 0.64, OR), ("ENTRENÓ\nMÁQUINA", 0.84, CY)], 630, 1000, 130, 40, 380, ease((u - 1.2) / 1.4), ease((u - 1.0) / 0.4), label_size=22)
    elif i == 4:
        for j, (lab, col, x) in enumerate((("M", CY, 330), ("L", OR, 750))):
            kk = easeb((u - 0.2 - j * 0.25) / 0.5)
            if kk <= 0: continue
            ctx.save(); ctx.translate(x, 800); ctx.scale(kk, kk)
            ctx.new_path(); ctx.arc(0, 0, 150, 0, 6.283); ctx.set_source_rgba(*col, 0.14); ctx.fill_preserve(); ctx.set_source_rgba(*col, 1); ctx.set_line_width(6); ctx.stroke()
            text(ctx, lab, 0, 55, F_BIG, 150, col, 1, align="center"); ctx.restore()
        text(ctx, "MÁQUINAS", 330, 1010, F_MONO, 28, CY, ease((u - 0.6) / 0.4), align="center", bold=True)
        text(ctx, "PESO LIBRE", 750, 1010, F_MONO, 28, OR, ease((u - 0.8) / 0.4), align="center", bold=True)
    elif i == 5:
        for j, (col, x) in enumerate(((OR, 360), (CY, 720))):
            jmp = abs(math.sin((t - j * 0.3) * 2.6)) * 160 * ease((u - 0.2) / 0.4)
            leg(ctx, x, 600 - jmp, 0.75, a=k, col=col)
        ctx.move_to(180, 1080); ctx.line_to(900, 1080); ctx.set_source_rgba(*MU, 0.7 * k); ctx.set_line_width(3); ctx.stroke()
        ke = easeb((u - 1.4) / 0.5)
        if ke > 0: big(ctx, "=", 540, 760, 130 * ke, GR, ke, maxw=200)
    elif i == 6:
        cx, cy = 540, 780
        sq = 0.5 + 0.5 * math.sin(t * 2.2)
        y = cy - 60 + 120 * sq
        ctx.move_to(260, y); ctx.line_to(820, y); ctx.set_source_rgba(*OR, k); ctx.set_line_width(10); ctx.stroke()
        for sx in (-1, 1):
            for j in range(2):
                x = 540 + sx * (230 + j * 30)
                rrect(ctx, x - 12, y - 80 + j * 15, 24, 160 - j * 30, 6); ctx.set_source_rgba(*OR, 0.2 * k); ctx.fill_preserve(); ctx.set_source_rgba(*OR, k); ctx.set_line_width(4); ctx.stroke()
        ctx.new_path(); ctx.arc(540, y - 40, 34, 0, 6.283); ctx.set_source_rgba(*CY, k); ctx.set_line_width(5); ctx.stroke()
        ctx.move_to(540, y); ctx.line_to(540, y + 150 - 60 * sq); ctx.stroke()
        ctx.move_to(540, y + 150 - 60 * sq); ctx.line_to(470, 1000 - 30 * sq); ctx.line_to(500, 1100)
        ctx.move_to(540, y + 150 - 60 * sq); ctx.line_to(610, 1000 - 30 * sq); ctx.line_to(580, 1100); ctx.stroke()
    elif i == 7:
        items = [("TE GUSTE", OR, 0.2), ("ESFUERZO", CY, 1.6), ("CONSTANCIA", AM, 3.0)]
        for j, (s, col, t0) in enumerate(items):
            kk = easeb((u - lt(7) - t0) / 0.5)
            if kk <= 0: continue
            ctx.save(); ctx.translate(540, 620 + j * 170); ctx.scale(kk, kk)
            rrect(ctx, -320, -65, 640, 130, 30); ctx.set_source_rgba(*col, 0.12); ctx.fill_preserve(); ctx.set_source_rgba(*col, 1); ctx.set_line_width(5); ctx.stroke()
            text(ctx, s, 0, 30, F_BIG, 84, col, 1, align="center"); ctx.restore()
    elif i == 8:
        dumbbell(ctx, 330, 640, 0.9, OR, k, ang=-0.25)
        machine(ctx, 760, 640, 0.75, CY, k, lift=0.5 + 0.5 * math.sin(t * 2.2))
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1000); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 150, CY, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "COMPARACIÓN · MÚSCULO", W / 2, 196, CY, k, 28)
        title(ctx, "¿PESO LIBRE O MÁQUINAS?", WH, 368, 96, k)
    elif i == 1:
        pill(ctx, "METAANÁLISIS · 2023", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "LA CIENCIA LOS COMPARÓ", WH, 368, 100, k)
        src(ctx, "Haugen et al., BMC Sports Sci Med Rehabil 2023 · doi:10.1186/s13102-023-00713-4", k, 1080)
    elif i == 2:
        pill(ctx, "MÚSCULO", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "EMPATE", WH, 368, 120, k)
        text(ctx, "ESQUEMA · 5 ESTUDIOS MIDIERON EL MÚSCULO", W / 2, 1080, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Haugen et al., 2023", k, 1125)
    elif i == 3:
        pill(ctx, "FUERZA", W / 2, 196, OR, k, 30, filled=True)
        title(ctx, "GANAS EN LO QUE PRACTICAS", WH, 368, 92, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1130, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Haugen et al., 2023 · en máquinas fue una tendencia", k, 1175)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿MÁQUINAS O PESO LIBRE?", WH, 368, 96, k)
        text(ctx, "ESCRIBE M O L", W / 2, 1110, F_MONO, 34, AM, ease((u - 0.8) / 0.4), align="center", bold=True)
    elif i == 5:
        pill(ctx, "SALTO VERTICAL", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "TAMBIÉN EMPATE", WH, 368, 110, k)
        src(ctx, "Haugen et al., 2023 · 5 estudios de salto", k, 1180)
    elif i == 6:
        pill(ctx, "SI TU META ES UN EJERCICIO", W / 2, 196, OR, k, 28, filled=True)
        title(ctx, "PRACTICA ESE EJERCICIO", WH, 368, 96, k)
    elif i == 7:
        pill(ctx, "PARA CRECER", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "ELIGE LO QUE SOSTENGAS", WH, 368, 96, k)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 31 · MÚSCULO")
