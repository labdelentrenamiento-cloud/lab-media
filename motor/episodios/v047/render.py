"""v047 · ¿Pensar en el músculo lo hace crecer más? (ESTUDIO EXPLICADO con resultado primero, serie CEREBRO Y MÚSCULO ·
paleta índigo medianoche + turquesa + violeta + ámbar)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (0.25, 1.0, 0.85)   # turquesa


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.035, 0.05, 0.17], [0.005, 0.008, 0.04])
from engine_ext import *
CY = ACC
MI = VI     # mente = violeta
MU_ = AM    # músculo = ámbar
PE = (0.55, 0.75, 1.0)   # peso = azul claro


def title(ctx, s, color=WH, y=345, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1160):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def arm(ctx, x, y, s, a, glow=0.0, curl=0.5, col=CY, t=0.0):
    """brazo flexionado (vista lateral): hombro en (x,y), bíceps resaltado con glow 0..1"""
    if a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ex, ey = 260, 0
    ang = -math.pi / 2 - (0.5 - curl) * 0.9
    hx, hy = ex + math.cos(ang) * 230, ey + math.sin(ang) * 230
    # húmero / antebrazo (contorno)
    ctx.move_to(0, -40); ctx.line_to(ex, -34); ctx.line_to(ex + 30, 0); ctx.line_to(ex, 38); ctx.line_to(0, 44); ctx.close_path()
    ctx.set_source_rgba(*col, 0.06 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(4); ctx.stroke()
    px, py = -math.sin(ang) * 30, math.cos(ang) * 30
    ctx.move_to(ex - px, ey - py); ctx.line_to(hx - px * 0.7, hy - py * 0.7); ctx.line_to(hx + px * 0.7, hy + py * 0.7); ctx.line_to(ex + px, ey + py)
    ctx.set_source_rgba(*col, 0.9 * a); ctx.stroke()
    ctx.new_path(); ctx.arc(hx, hy, 34, 0, 6.283); ctx.set_source_rgba(*col, 0.9 * a); ctx.stroke()
    # bíceps
    pulse = 0.75 + 0.25 * math.sin(t * 6)
    bulge = 42 + 22 * curl
    ctx.move_to(40, -40); ctx.curve_to(90, -40 - bulge * 1.6, 200, -40 - bulge * 1.6, 245, -36)
    ctx.curve_to(200, -30, 90, -30, 40, -40); ctx.close_path()
    ctx.set_source_rgba(*MU_, (0.12 + 0.35 * glow * pulse) * a); ctx.fill_preserve(); ctx.set_source_rgba(*MU_, (0.6 + 0.4 * glow) * a); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def dumbbell(ctx, cx, cy, s, a, col=PE):
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.move_to(-60, 0); ctx.line_to(60, 0); ctx.set_source_rgba(*WH, 0.9 * a); ctx.set_line_width(10); ctx.stroke()
    for sx in (-1, 1):
        rrect(ctx, sx * 70 - 18, -48, 36, 96, 8); ctx.set_source_rgba(*col, 0.15 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def person(ctx, x, y, s, a, col):
    ctx.new_path(); ctx.arc(x, y - 22 * s, 11 * s, 0, 6.283); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
    ctx.move_to(x - 18 * s, y + 22 * s); ctx.curve_to(x - 18 * s, y - 6 * s, x + 18 * s, y - 6 * s, x + 18 * s, y + 22 * s); ctx.stroke()


def link(ctx, p0, p1, t, a, col=MI):
    nerve(ctx, [p0, ((p0[0] + p1[0]) / 2, min(p0[1], p1[1]) - 60), p1], t, a, col, rate=1.4)


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        brain(ctx, 300, 600, 0.95, t, k, MI, fire=0.8)
        arm(ctx, 470, 880, 1.0, k, glow=ease((u - 0.6) / 0.8), curl=0.5 + 0.3 * math.sin(t * 2.4), t=t)
        link(ctx, (380, 640), (640, 820), t, ease((u - 0.3) / 0.5))
        kb = easeb((u - lt(0) - 2.4) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 1100); ctx.scale(kb, kb)
            text(ctx, "¿CASI EL DOBLE?", 0, 0, F_BIG, 84, AM, 1, align="center"); ctx.restore()
    elif i == 1:
        n = int(clamp((u - 0.2) / 1.5) * 30)
        for j in range(n):
            c = j % 10; r = j // 10
            person(ctx, 200 + c * 76, 600 + r * 95, 1.3, k, CY)
        kb = ease((u - 1.5) / 1.5)
        rrect(ctx, 200, 930, 680, 50, 25); ctx.set_source_rgba(*CY, 0.10 * k); ctx.fill()
        for w in range(8):
            if kb * 8 > w:
                rrect(ctx, 204 + w * 84.5, 934, 80, 42, 20); ctx.set_source_rgba(*GR, 0.6 * k); ctx.fill()
        text(ctx, "8 SEMANAS · 3 DÍAS/SEMANA", 540, 1040, F_MONO, 30, GR, ease((u - 1.6) / 0.4), align="center", bold=True)
    elif i == 2:
        kl = easeb((u - 0.2) / 0.5); kr = easeb((u - lt(2) - 2.0) / 0.5)
        if kl > 0:
            rrect(ctx, 130, 520, 390, 520, 30); ctx.set_source_rgba(*MI, 0.08 * kl); ctx.fill_preserve(); ctx.set_source_rgba(*MI, kl); ctx.set_line_width(4); ctx.stroke()
            brain(ctx, 325, 640, 0.55, t, kl, MI, fire=0.8)
            arm(ctx, 190, 880, 0.55, kl, glow=1.0, curl=0.5 + 0.3 * math.sin(t * 2.4), t=t)
            text(ctx, "EL MÚSCULO", 325, 1000, F_BIG, 50, MU_, kl, align="center")
        if kr > 0:
            rrect(ctx, 560, 520, 390, 520, 30); ctx.set_source_rgba(*PE, 0.08 * kr); ctx.fill_preserve(); ctx.set_source_rgba(*PE, kr); ctx.set_line_width(4); ctx.stroke()
            yy = 800 - 120 * abs(math.sin(t * 2.4))
            dumbbell(ctx, 755, yy, 1.0, kr)
            ctx.move_to(755, 640); ctx.line_to(735, 670); ctx.move_to(755, 640); ctx.line_to(775, 670); ctx.move_to(755, 640); ctx.line_to(755, 720)
            ctx.set_source_rgba(*PE, kr); ctx.set_line_width(5); ctx.stroke()
            text(ctx, "EL PESO", 755, 1000, F_BIG, 50, PE, kr, align="center")
    elif i == 3:
        vbars(ctx, [("PENSÓ EN\nEL MÚSCULO", 1.0, MU_), ("PENSÓ EN\nEL PESO", 6.9 / 12.4, PE)], 260, 980, 220, 120, 320, clamp((u - 0.2) / 1.6), k, 26)
        for j, (s, v, col) in enumerate([("+12,4 %", 1.0, MU_), ("+6,9 %", 6.9 / 12.4, PE)]):
            kj = ease((u - 1.2 - j * 0.3) / 0.4)
            text(ctx, s, 370 + j * 340, 980 - 320 * v - 26, F_BIG, 64, col, kj, align="center")
        text(ctx, "GROSOR DEL BÍCEPS", 540, 520, F_MONO, 26, MU, k, align="center", bold=True)
    elif i == 4:
        for j, (lab, col, cx) in enumerate([("MÚSCULO", MU_, 330), ("PESO", PE, 750)]):
            kj = easeb((u - 0.3 - j * 0.4) / 0.5)
            if kj <= 0: continue
            rrect(ctx, cx - 175, 560, 350, 320, 34); ctx.set_source_rgba(*col, 0.10 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(5); ctx.stroke()
            if j == 0:
                brain(ctx, cx, 690, 0.5, t, kj, MI, fire=0.6)
            else:
                dumbbell(ctx, cx, 700, 1.0, kj)
            text(ctx, lab, cx, 850, F_BIG, 60, col, kj, align="center")
        cur = "▌" if int(t * 2.5) % 2 == 0 else " "
        text(ctx, "COMENTA: MÚSCULO O PESO" + cur, 540, 990, F_MONO, 32, AM, ease((u - 1.2) / 0.4), align="center", bold=True)
    elif i == 5:
        for j, (cx, col) in enumerate([(380, MU_), (700, PE)]):
            kj = ease((u - 0.2 - j * 0.3) / 0.5)
            leg(ctx, cx, 520, 0.72, kj, col, fill=0.10)
        kb = easeb((u - lt(5) - 1.6) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 800); ctx.scale(kb, kb)
            text(ctx, "=", 0, 0, F_BIG, 150, WH, 1, align="center"); ctx.restore()
            ctx.save(); ctx.translate(540, 1060); ctx.scale(kb, kb)
            text(ctx, "SIN DIFERENCIA", 0, 0, F_BIG, 80, GR, 1, align="center"); ctx.restore()
    elif i == 6:
        for j, (lab, sub, col, fire, v) in enumerate([("MODERADA", "MÁS ACTIVACIÓN", GR, 1.0, 0.85), ("MUY PESADA", "SIN CAMBIO", RD, 0.0, 0.45)]):
            kj = easeb((u - 0.3 - j * (lt(6) + 2.6)) / 0.5)
            if kj <= 0: continue
            cx = 315 + j * 450
            rrect(ctx, cx - 195, 520, 390, 520, 30); ctx.set_source_rgba(*col, 0.08 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(4); ctx.stroke()
            text(ctx, "CARGA", cx, 580, F_MONO, 24, MU, kj, align="center", bold=True)
            text(ctx, lab, cx, 650, F_BIG, 56, WH, kj, align="center")
            gauge(ctx, cx, 820, 120, v * ease((u - 0.5 - j * (lt(6) + 2.6)) / 0.8), kj, col)
            text(ctx, sub, cx, 1000, F_BIG, 44, col, kj, align="center")
    elif i == 7:
        kb = easeb((u - 0.2) / 0.5)
        if kb > 0:
            rrect(ctx, 290, 520, 500, 150, 30); ctx.set_source_rgba(*AM, 0.12 * kb); ctx.fill_preserve(); ctx.set_source_rgba(*AM, kb); ctx.set_line_width(4); ctx.stroke()
            text(ctx, "ESTUDIO PEQUEÑO", 540, 590, F_BIG, 56, AM, kb, align="center")
            text(ctx, "30 PERSONAS · PRINCIPIANTES", 540, 640, F_MONO, 24, WH, kb, align="center", bold=True)
        arm(ctx, 390, 930, 0.8, ease((u - 1.0) / 0.5), glow=0.8, curl=0.5 + 0.35 * math.sin(t * 2.4), t=t)
    elif i == 8:
        brain(ctx, 540, 760, 1.0, t, k, MI, fire=0.9)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1040); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, AM, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "ESTUDIO EXPLICADO · CEREBRO Y MÚSCULO", W / 2, 196, CY, k, 26)
        title(ctx, "¿PENSAR EN TU BÍCEPS?", WH, 368, 96, k)
    elif i == 1:
        pill(ctx, "ENSAYO ALEATORIZADO", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "30 PRINCIPIANTES", WH, 368, 100, k)
        src(ctx, "Schoenfeld et al., Eur J Sport Sci 2018 · doi:10.1080/17461391.2018.1447020", k)
    elif i == 2:
        pill(ctx, "DOS GRUPOS · MISMA RUTINA", W / 2, 196, MI, k, 28, filled=True)
        title(ctx, "¿EN QUÉ PENSABAN?", WH, 368, 100, k)
    elif i == 3:
        pill(ctx, "RESULTADO · BÍCEPS", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "CASI EL DOBLE", WH, 368, 104, k)
        src(ctx, "Schoenfeld et al., 2018 · grosor del bíceps por ecografía: +12,4 % vs. +6,9 %", k, 1110)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿EN QUÉ PIENSAS TÚ?", WH, 368, 96, k)
    elif i == 5:
        pill(ctx, "PERO OJO · MUSLOS", W / 2, 196, RD, k, 30, filled=True)
        title(ctx, "EN LOS CUÁDRICEPS, IGUAL", WH, 368, 90, k)
        src(ctx, "Schoenfeld et al., 2018 · cambios similares en el cuádriceps", k, 1140)
    elif i == 6:
        pill(ctx, "OTRO ESTUDIO · ACTIVACIÓN", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "FUNCIONA CON CARGAS MODERADAS", WH, 368, 84, k)
        src(ctx, "Calatayud et al., Eur J Appl Physiol 2016 · efecto hasta 60 % del máximo, no a 80 %", k, 1120)
    elif i == 7:
        pill(ctx, "EN LA PRÁCTICA", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "PRUÉBALO SIN EXAGERAR", WH, 368, 94, k)
        src(ctx, "Evidencia limitada: 1 ensayo en principiantes · doi:10.1080/17461391.2018.1447020", k, 1140)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 47 · CEREBRO")
