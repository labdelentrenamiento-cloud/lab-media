"""v043 · ¿Cardio en ayunas quema más grasa? (MITO VS. REALIDAD, serie METABOLISMO ·
paleta amanecer: ciruela + naranja + ámbar + cian)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (1.0, 0.56, 0.30)   # naranja amanecer


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.15, 0.05, 0.13], [0.025, 0.008, 0.03])
from engine_ext import *
CY = ACC
FAT = AM                  # grasa = ámbar
CHO = (0.35, 0.85, 1.0)   # carbohidratos = cian


def title(ctx, s, color=WH, y=345, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1170):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def badge(ctx, cx, cy, num, unit, col, a, w=300):
    if a <= 0: return
    rrect(ctx, cx - w / 2, cy - 150, w, 290, 26); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    big(ctx, num, cx, cy + 30, 120, col, a, maxw=w - 40)
    for li, part in enumerate(unit.split("\n")):
        text(ctx, part, cx, cy + 85 + li * 30, F_MONO, 23, WH, a, align="center", bold=True)


def sun(ctx, cx, hy, r, rise, t, a, hw=330):
    """sol saliendo sobre el horizonte hy"""
    if a <= 0: return
    cy = hy + r * (1 - rise)
    ctx.save(); ctx.rectangle(0, 0, W, hy); ctx.clip()
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*CY, 0.18 * a); ctx.fill_preserve(); ctx.set_source_rgba(*CY, a); ctx.set_line_width(5); ctx.stroke()
    for j in range(12):
        ang = math.pi + j / 11 * math.pi
        l = 30 + 10 * math.sin(t * 3 + j)
        ctx.move_to(cx + math.cos(ang) * (r + 18), cy + math.sin(ang) * (r + 18))
        ctx.line_to(cx + math.cos(ang) * (r + 18 + l), cy + math.sin(ang) * (r + 18 + l))
        ctx.set_source_rgba(*AM, 0.8 * a * rise); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()
    ctx.move_to(cx - hw, hy); ctx.line_to(cx + hw, hy); ctx.set_source_rgba(*CY, 0.8 * a); ctx.set_line_width(4); ctx.stroke()


def plate(ctx, cx, cy, r, a, full=0.0, col=None):
    col = col or WH
    if a <= 0: return
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*col, 0.06 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(4); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, r * 0.68, 0, 6.283); ctx.set_source_rgba(*col, 0.45 * a); ctx.set_line_width(2.5); ctx.stroke()
    if full > 0:
        for j, (dx, dy, rr, c) in enumerate([(-0.25, -0.1, 0.22, AM), (0.2, -0.18, 0.18, GR), (0.05, 0.22, 0.2, CHO)]):
            kk = ease((full - j * 0.2) / 0.5)
            if kk <= 0: continue
            ctx.new_path(); ctx.arc(cx + dx * r, cy + dy * r, rr * r * kk, 0, 6.283); ctx.set_source_rgba(*c, 0.35 * a); ctx.fill_preserve(); ctx.set_source_rgba(*c, a); ctx.set_line_width(3); ctx.stroke()
    # tenedor
    fx = cx - r - 40
    ctx.move_to(fx, cy - r * 0.7); ctx.line_to(fx, cy + r * 0.8); ctx.set_source_rgba(*col, 0.8 * a); ctx.set_line_width(5); ctx.stroke()
    for dx in (-12, 0, 12):
        ctx.move_to(fx + dx, cy - r * 0.7); ctx.line_to(fx + dx, cy - r * 0.35); ctx.stroke()


def flame(ctx, cx, cy, s, t, col, a):
    if a <= 0: return
    fl = 1 + 0.06 * math.sin(t * 11) + 0.04 * math.sin(t * 17)
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s * fl)
    ctx.new_path(); ctx.move_to(0, -110)
    ctx.curve_to(50, -50, 75, 0, 60, 45); ctx.curve_to(45, 90, -45, 90, -60, 45)
    ctx.curve_to(-75, 0, -30, -30, 0, -110); ctx.close_path()
    ctx.set_source_rgba(*col, 0.22 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5 / s); ctx.stroke()
    ctx.new_path(); ctx.move_to(0, -30); ctx.curve_to(25, 0, 35, 30, 20, 55); ctx.curve_to(10, 70, -10, 70, -20, 55); ctx.curve_to(-35, 30, -15, 0, 0, -30)
    ctx.set_source_rgba(*AM, 0.6 * a); ctx.fill()
    ctx.restore()


def hbar(ctx, x, y, w, h, frac, col, a, label, val=""):
    rrect(ctx, x, y, w, h, h / 2); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill()
    if frac > 0:
        rrect(ctx, x, y, max(h, w * frac), h, h / 2); ctx.set_source_rgba(*col, 0.35 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
    text(ctx, label, x, y - 14, F_MONO, 26, col, a, bold=True)
    if val: text(ctx, val, x + w, y - 14, F_MONO, 26, WH, a, align="right", bold=True)


def fuel_mix(ctx, x, y, w, fat, a, label):
    """barra de mezcla de combustible: grasa (ámbar) | carbohidratos (cian)"""
    if a <= 0: return
    h = 70
    text(ctx, label, x, y - 18, F_MONO, 27, WH, a, bold=True)
    rrect(ctx, x, y, w, h, 18); ctx.set_source_rgba(*CHO, 0.25 * a); ctx.fill_preserve(); ctx.set_source_rgba(*CHO, a); ctx.set_line_width(3); ctx.stroke()
    rrect(ctx, x, y, max(36, w * fat), h, 18); ctx.set_source_rgba(*FAT, 0.45 * a); ctx.fill_preserve(); ctx.set_source_rgba(*FAT, a); ctx.set_line_width(3); ctx.stroke()


def calendar(ctx, x0, y0, cell, lit, a, mark_day=-1):
    for wk in range(4):
        for dd in range(7):
            n = wk * 7 + dd
            on = n < lit
            xx = x0 + dd * (cell + 10); yy = y0 + wk * (cell + 10)
            rrect(ctx, xx, yy, cell, cell, 10)
            ctx.set_source_rgba(*(GR if on else CY), (0.30 if on else 0.05) * a); ctx.fill_preserve()
            ctx.set_source_rgba(*(GR if on else CY), (0.95 if on else 0.35) * a); ctx.set_line_width(2.5); ctx.stroke()
            if n == mark_day:
                rrect(ctx, xx - 6, yy - 6, cell + 12, cell + 12, 14); ctx.set_source_rgba(*AM, a); ctx.set_line_width(5); ctx.stroke()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        sun(ctx, 540, 860, 150, ease((u - 0.2) / 2.2), t, k)
        plate(ctx, 560, 1020, 85, ease((u - 1.0) / 0.5))
        kq = easeb((u - lt(0) - 3.0) / 0.5)
        if kq > 0:
            ctx.save(); ctx.translate(540, 600); ctx.scale(kq, kq)
            text(ctx, "¿MÁS GRASA?", 0, 0, F_BIG, 92, AM, 1, align="center"); ctx.restore()
    elif i == 1:
        flame(ctx, 540, 600, 1.0, t, CY, k)
        fuel_mix(ctx, 200, 820, 680, lerp(0.38, 0.62, ease((u - 0.8) / 1.6)), ease((u - 0.3) / 0.4), "EN AYUNAS")
        fuel_mix(ctx, 200, 980, 680, 0.38, ease((u - 0.5) / 0.4), "CON COMIDA")
        kl = ease((u - 1.6) / 0.5)
        text(ctx, "■ GRASA", 330, 1110, F_MONO, 26, FAT, kl, align="center", bold=True)
        text(ctx, "■ CARBOHIDRATOS", 700, 1110, F_MONO, 26, CHO, kl, align="center", bold=True)
    elif i == 2:
        flame(ctx, 540, 590, 0.8, t, CY, k)
        kb = easeb((u - lt(2) - 1.6) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 830); ctx.scale(kb, kb)
            text(ctx, "≈ +3 g", 0, 40, F_BIG, 190, AM, 1, align="center"); ctx.restore()
        text(ctx, "DE GRASA QUEMADA POR SESIÓN", 540, 960, F_MONO, 28, WH, ease((u - lt(2) - 2.2) / 0.4), align="center", bold=True)
        text(ctx, "(MIENTRAS ENTRENAS EN AYUNAS)", 540, 1010, F_MONO, 24, MU, ease((u - lt(2) - 2.6) / 0.4), align="center")
    elif i == 3:
        lit = int(clamp((u - 0.6) / 3.0) * 28)
        calendar(ctx, 225, 520, 80, lit, k, mark_day=0)
        kk = ease((u - 0.4) / 0.4)
        text(ctx, "1 SESIÓN", 225, 495, F_MONO, 26, AM, kk, bold=True)
        text(ctx, "SEMANAS", 855, 960, F_MONO, 30, GR, ease((u - 2.0) / 0.5), align="right", bold=True)
    elif i == 4:
        kk = ease((u - 0.3) / 2.0)
        vbars(ctx, [("AYUNAS", 0.72, AM), ("CON\nCOMIDA", 0.72, CHO)], 290, 970, 190, 120, 380, kk, 1.0, 26)
        ke = easeb((u - lt(4) - 3.4) / 0.5)
        if ke > 0:
            ctx.save(); ctx.translate(540, 820); ctx.scale(ke, ke)
            text(ctx, "=", 0, 10, F_BIG, 150, GR, 1, align="center"); ctx.restore()
        text(ctx, "GRASA PERDIDA", 540, 560, F_MONO, 26, MU, k, align="center", bold=True)
    elif i == 5:
        for j, (lab, col, cx) in enumerate([("AYUNAS", AM, 330), ("COMIDA", CHO, 750)]):
            kj = easeb((u - 0.3 - j * 0.4) / 0.5)
            if kj <= 0: continue
            rrect(ctx, cx - 175, 600, 350, 250, 34); ctx.set_source_rgba(*col, 0.10 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(5); ctx.stroke()
            if j == 0:
                sun(ctx, cx, 760, 52, 1.0, t, kj, hw=110)
            else:
                plate(ctx, cx + 20, 720, 48, kj, full=1.0)
            text(ctx, lab, cx, 820, F_BIG, 54, col, kj, align="center")
        cur = "▌" if int(t * 2.5) % 2 == 0 else " "
        text(ctx, "COMENTA: AYUNAS O COMIDA" + cur, 540, 960, F_MONO, 32, AM, ease((u - 1.2) / 0.4), align="center", bold=True)
    elif i == 6:
        rows = [("DÉFICIT DE CALORÍAS", GR, 0.3), ("+ EJERCICIO", GR, 1.0), ("AYUNO", MU, 1.8)]
        for j, (s, col, dl) in enumerate(rows):
            kj = ease((u - dl) / 0.4)
            if kj <= 0: continue
            yy = 600 + j * 130
            text(ctx, s, 540, yy, F_BIG, 70, col, kj, align="center")
            if j == 2:
                kx = ease((u - lt(6) - 3.8) / 0.4)
                if kx > 0:
                    ctx.move_to(360, yy - 26); ctx.line_to(360 + 360 * kx, yy - 26); ctx.set_source_rgba(*RD, kx); ctx.set_line_width(8); ctx.stroke()
        kr = ease((u - 1.2) / 0.5)
        if kr > 0:
            ctx.move_to(260, 880); ctx.line_to(820, 880); ctx.set_source_rgba(*WH, 0.5 * kr); ctx.set_line_width(2); ctx.stroke()
            text(ctx, "= MENOS GRASA", 540, 980, F_BIG, 76, AM, ease((u - 1.4) / 0.4), align="center")
    elif i == 7:
        gauge(ctx, 540, 760, 220, lerp(0.25, 0.8, ease((u - lt(7) - 3.2) / 1.2)), k, GR)
        text(ctx, "TU RENDIMIENTO", 540, 900, F_MONO, 30, WH, k, align="center", bold=True)
        plate(ctx, 560, 1010, 50, ease((u - lt(7) - 3.0) / 0.5), full=ease((u - lt(7) - 3.2) / 1.0))
    elif i == 8:
        sun(ctx, 540, 760, 140, 1.0, t, k)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1000); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, AM, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "MITO VS. REALIDAD · METABOLISMO", W / 2, 196, CY, k, 28)
        title(ctx, "¿CARDIO EN AYUNAS?", WH, 368, 100, k)
    elif i == 1:
        pill(ctx, "LO QUE SÍ ES CIERTO", W / 2, 196, GR, k, 28, filled=True)
        title(ctx, "MÁS GRASA COMO COMBUSTIBLE", WH, 368, 88, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1160, F_MONO, 22, AM, k, align="center", bold=True)
    elif i == 2:
        pill(ctx, "METAANÁLISIS · 27 ESTUDIOS", W / 2, 196, AM, k, 28, filled=True)
        title(ctx, "¿CUÁNTO MÁS?", WH, 368, 100, k)
        src(ctx, "Vieira et al., Br J Nutr 2016 · doi:10.1017/S0007114516003160", k, 1150)
    elif i == 3:
        pill(ctx, "PERO…", W / 2, 196, RD, k, 30, filled=True)
        title(ctx, "UNA SESIÓN NO ES UN RESULTADO", WH, 368, 86, k)
    elif i == 4:
        pill(ctx, "DURANTE SEMANAS · MISMA DIETA", W / 2, 196, GR, k, 28, filled=True)
        title(ctx, "LA MISMA GRASA PERDIDA", WH, 368, 96, k)
        src(ctx, "Schoenfeld et al., JISSN 2014 · doi:10.1186/s12970-014-0054-7", k, 1130)
        src(ctx, "Hackett y Hagstrom, J Funct Morphol Kinesiol 2017 · doi:10.3390/jfmk2040043", k, 1165)
    elif i == 5:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿ENTRENAS EN AYUNAS O COMES ANTES?", WH, 368, 80, k)
    elif i == 6:
        pill(ctx, "LA CLAVE", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "NO FUE EL AYUNO", WH, 368, 100, k)
        src(ctx, "En los estudios: dieta con déficit + ejercicio en ambos grupos", k, 1150)
    elif i == 7:
        pill(ctx, "EN LA PRÁCTICA", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "ELIGE LO QUE TE HAGA RENDIR", WH, 368, 88, k)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 43 · METABOLISMO")
