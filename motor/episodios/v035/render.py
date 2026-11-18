"""v035 · ¿Media sentadilla o completa? (COMPARACIÓN + estudio explicado, serie MÚSCULO ·
paleta índigo + violeta + coral + cian)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.BG = engine_ext.BG = _bg([0.08, 0.06, 0.17], [0.015, 0.01, 0.04])
from engine_ext import *
CO = (1.0, 0.45, 0.40)


def title(ctx, s, color=WH, y=345, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1270):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def badge(ctx, cx, cy, num, unit, col, a, w=280):
    if a <= 0: return
    rrect(ctx, cx - w / 2, cy - 150, w, 290, 26); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    big(ctx, num, cx, cy + 30, 120, col, a, maxw=w - 40)
    for li, part in enumerate(unit.split("\n")):
        text(ctx, part, cx, cy + 85 + li * 30, F_MONO, 23, WH, a, align="center", bold=True)


def squat(ctx, ax, ay, s, flex, col, a, glute=None, quad=None, t=0.0):
    """sentadilla de perfil. ax, ay = tobillo. flex = flexión de rodilla en grados (0 de pie, 90 media, 140 completa)"""
    if a <= 0: return
    f = math.radians(flex)
    L1, L2, L3 = 170 * s, 180 * s, 210 * s
    sh = 0.42 * f / math.radians(140)              # inclinación de la tibia
    kx, ky = ax + math.sin(sh) * L1, ay - math.cos(sh) * L1
    th = f - sh                                    # muslo desde la vertical, hacia atrás
    hx, hy = kx - math.sin(th) * L2, ky - math.cos(th) * L2
    tl = 0.12 + 0.55 * f / math.radians(140)      # inclinación del tronco
    sx, sy = hx + math.sin(tl) * L3, hy - math.cos(tl) * L3
    # pie
    ctx.set_line_cap(1)
    ctx.move_to(ax - 20 * s, ay + 6 * s); ctx.line_to(ax + 60 * s, ay + 6 * s); ctx.set_source_rgba(*col, a); ctx.set_line_width(9 * s); ctx.stroke()
    ctx.move_to(ax, ay); ctx.line_to(kx, ky); ctx.set_line_width(16 * s); ctx.stroke()
    qc = quad if quad else col
    ctx.move_to(kx, ky); ctx.line_to(hx, hy); ctx.set_source_rgba(*qc, a); ctx.set_line_width(26 * s); ctx.stroke()
    ctx.move_to(hx, hy); ctx.line_to(sx, sy); ctx.set_source_rgba(*col, a); ctx.set_line_width(20 * s); ctx.stroke()
    ctx.new_path(); ctx.arc(sx + math.sin(tl) * 46 * s, sy - math.cos(tl) * 46 * s, 30 * s, 0, 6.283); ctx.set_line_width(7 * s); ctx.stroke()
    if glute:
        gcol, gk = glute
        p = 0.65 + 0.35 * math.sin(t * 6)
        ctx.save(); ctx.translate(hx - 22 * s, hy + 4 * s); ctx.rotate(-tl); ctx.scale(1.0, 1.25)
        ctx.new_path(); ctx.arc(0, 0, 40 * s * gk, 0, 6.283); ctx.restore()
        ctx.set_source_rgba(*gcol, 0.35 * a * p); ctx.fill_preserve(); ctx.set_source_rgba(*gcol, a); ctx.set_line_width(4); ctx.stroke()
    # barra
    ctx.move_to(sx - 70 * s, sy + 6 * s); ctx.line_to(sx + 70 * s, sy + 6 * s); ctx.set_source_rgba(*AM, a); ctx.set_line_width(8 * s); ctx.stroke()
    for px in (-70, 70):
        rrect(ctx, sx + px * s - 9 * s, sy - 50 * s, 18 * s, 112 * s, 5); ctx.set_source_rgba(*AM, 0.25 * a); ctx.fill_preserve(); ctx.set_source_rgba(*AM, a); ctx.set_line_width(3); ctx.stroke()
    ctx.set_line_cap(0)
    return (kx, ky), (hx, hy)


def pbars(ctx, items, k, a, maxv=7.5):
    x0, base, bw, gap, maxh = 250, 1080, 220, 140, 430
    for j, (lab, v, col, num, k0) in enumerate(items):
        kk = ease((k - k0) / 0.7)
        if kk <= 0: continue
        x = x0 + j * (bw + gap); hgt = maxh * v / maxv * kk
        rrect(ctx, x, base - hgt, bw, hgt, 14); ctx.set_source_rgba(*col, 0.22 * a); ctx.fill_preserve()
        ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(3); ctx.stroke()
        big(ctx, num, x + bw / 2, base - hgt - 22, 76, col, a * kk, maxw=bw + 40)
        text(ctx, lab, x + bw / 2, base + 42, F_MONO, 26, col, a * kk, align="center", bold=True)


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    cyc = 0.5 - 0.5 * math.cos(t * 2.0)
    if i == 0:
        squat(ctx, 290, 1090, 0.95, 20 + 70 * cyc, CY, k)
        squat(ctx, 720, 1090, 0.95, 20 + 120 * cyc, VI, ease((u - 0.3) / 0.4))
        text(ctx, "MEDIA", 330, 1150, F_MONO, 30, CY, k, align="center", bold=True)
        text(ctx, "COMPLETA", 760, 1150, F_MONO, 30, VI, ease((u - 0.3) / 0.4), align="center", bold=True)
    elif i == 1:
        badge(ctx, 250, 790, "17", "HOMBRES", CY, ease((u - 0.1) / 0.4))
        badge(ctx, 540, 790, "10", "SEMANAS", VI, ease((u - 1.4) / 0.4))
        badge(ctx, 830, 790, "RM", "RESONANCIA\nMAGNÉTICA", AM, ease((u - lt(1) - 0.2) / 0.4))
    elif i == 2:
        pbars(ctx, [("MEDIA", 4.6, CY, "4,6 %", 0.2), ("COMPLETA", 4.9, VI, "4,9 %", 0.5)], u, k)
        ke = easeb((u - lt(2) - 2.4) / 0.5)
        if ke > 0: big(ctx, "≈", 540, 820, 130 * ke, GR, ke, maxw=160)
    elif i == 3:
        pbars(ctx, [("MEDIA", 2.2, CY, "2,2 %", 0.2), ("COMPLETA", 6.7, VI, "6,7 %", 0.6)], u, k)
        kx = easeb((u - lt(3) - 2.0) / 0.5)
        if kx > 0:
            ctx.save(); ctx.translate(400, 600); ctx.scale(kx, kx)
            text(ctx, "×3", 0, 0, F_BIG, 120, CO, 1, align="center"); ctx.restore()
    elif i == 4:
        for j, (lab, col, x) in enumerate((("MEDIA", CY, 300), ("COMPLETA", VI, 780))):
            kk = easeb((u - 0.2 - j * 0.25) / 0.5)
            if kk <= 0: continue
            ctx.save(); ctx.translate(x, 800); ctx.scale(kk, kk)
            ctx.new_path(); ctx.arc(0, 0, 170, 0, 6.283); ctx.set_source_rgba(*col, 0.14); ctx.fill_preserve(); ctx.set_source_rgba(*col, 1); ctx.set_line_width(6); ctx.stroke()
            sz = fit_size(ctx, lab, F_BIG, 80, 290)
            text(ctx, lab, 0, 28, F_BIG, sz, col, 1, align="center"); ctx.restore()
    elif i == 5:
        badge(ctx, 270, 790, "16", "ESTUDIOS", VI, ease((u - 0.1) / 0.4))
        for j, (lab, col, t0) in enumerate((("FUERZA", GR, 2.6), ("MÚSCULO\nPIERNAS", CO, 3.8))):
            kk = easeb((u - lt(5) - t0) / 0.5)
            if kk <= 0: continue
            y = 690 + j * 210
            ctx.save(); ctx.translate(560, y); ctx.scale(kk, kk)
            ctx.move_to(0, 30); ctx.line_to(0, -40); ctx.move_to(-26, -14); ctx.line_to(0, -40); ctx.line_to(26, -14)
            ctx.set_source_rgba(*col, 1); ctx.set_line_width(8); ctx.stroke()
            for li, part in enumerate(lab.split("\n")):
                text(ctx, part, 50, 18 + li * 58 - (29 if "\n" in lab else 0), F_BIG, 52, col, 1)
            ctx.restore()
    elif i == 6:
        squat(ctx, 470, 1060, 1.5, 140 - 10 * cyc, VI, k, glute=(CO, ease((u - 0.6) / 0.6)), t=t)
        kl = ease((u - lt(6) - 2.2) / 0.5)
        if kl > 0:
            ctx.move_to(330, 960); ctx.line_to(230, 1080); ctx.set_source_rgba(*CO, kl); ctx.set_line_width(3); ctx.stroke()
            text(ctx, "ESTIRADO", 230, 1120, F_MONO, 30, CO, kl, align="center", bold=True)
    elif i == 7:
        gauge(ctx, 540, 860, 230, 0.56 + 0.04 * math.sin(t * 2), a=k, col=GR)
        text(ctx, "PARCIAL", 330, 1010, F_MONO, 28, CY, k, align="center", bold=True)
        text(ctx, "COMPLETO", 750, 1010, F_MONO, 28, VI, k, align="center", bold=True)
    elif i == 8:
        squat(ctx, 480, 890, 0.8, 30 + 110 * cyc, VI, k)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1075); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 100, VI, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "COMPARACIÓN · MÚSCULO", W / 2, 196, VI, k, 28)
        title(ctx, "¿MEDIA SENTADILLA O COMPLETA?", WH, 368, 92, k)
    elif i == 1:
        pill(ctx, "ESTUDIO · 2019", W / 2, 196, VI, k, 28, filled=True)
        title(ctx, "MIDIERON CADA MÚSCULO", WH, 368, 96, k)
        src(ctx, "Kubo et al., Eur J Appl Physiol 2019 · doi:10.1007/s00421-019-04181-y", k, 1080)
    elif i == 2:
        pill(ctx, "CUÁDRICEPS", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "CASI IGUAL", WH, 368, 116, k)
        src(ctx, "Kubo et al., 2019 · volumen muscular, 10 semanas", k, 1225)
    elif i == 3:
        pill(ctx, "GLÚTEO MAYOR", W / 2, 196, CO, k, 30, filled=True)
        title(ctx, "GANÓ LA COMPLETA", WH, 368, 108, k)
        src(ctx, "Kubo et al., 2019 · aductores: 6,2 % vs. 2,7 %", k, 1225)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿HASTA DÓNDE BAJAS TÚ?", WH, 368, 100, k)
    elif i == 5:
        pill(ctx, "METAANÁLISIS · 2021", W / 2, 196, VI, k, 28, filled=True)
        title(ctx, "RECORRIDO COMPLETO", WH, 368, 104, k)
        src(ctx, "Pallarés et al., Scand J Med Sci Sports 2021 · doi:10.1111/sms.14006", k, 1180)
    elif i == 6:
        pill(ctx, "LA CLAVE", W / 2, 196, CO, k, 30, filled=True)
        title(ctx, "EL MÚSCULO ESTIRADO", WH, 368, 104, k)
        src(ctx, "Wolf et al., Sports Med Health Sci 2025 · evidencia aún mixta", k, 1240)
    elif i == 7:
        pill(ctx, "SI UNA LESIÓN TE LIMITA", W / 2, 196, GR, k, 28, filled=True)
        title(ctx, "EL PARCIAL TAMBIÉN SIRVE", WH, 368, 96, k)
        text(ctx, "ESQUEMA · DIFERENCIA GENERAL PEQUEÑA", W / 2, 1120, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Wolf et al., Int J Strength Cond 2023 · metaanálisis", k, 1165)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 35 · MÚSCULO")
