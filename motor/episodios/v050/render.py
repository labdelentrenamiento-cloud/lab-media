"""v050 · ¿Importa el orden de los ejercicios? (COMPARACIÓN A vs. B con gancho en segunda persona, serie FUERZA · RUTINA ·
paleta grafito + naranja + cian + verde)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (1.0, 0.60, 0.28)   # naranja
C2 = (0.24, 0.94, 1.0)    # cian


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.075, 0.08, 0.10], [0.012, 0.014, 0.02])
from engine_ext import *
CY = ACC
FAV = AM


def title(ctx, s, color=WH, y=380, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1150):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def star(ctx, cx, cy, r, a, col=FAV, fill=0.35):
    ctx.new_path()
    for j in range(10):
        ang = -math.pi / 2 + j * math.pi / 5
        rr = r if j % 2 == 0 else r * 0.45
        (ctx.move_to if j == 0 else ctx.line_to)(cx + math.cos(ang) * rr, cy + math.sin(ang) * rr)
    ctx.close_path(); ctx.set_source_rgba(*col, fill * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()


def ex_card(ctx, x, y, w, h, num, lab, col, a, fav=False, t=0.0):
    if a <= 0: return
    pulse = 0.7 + 0.3 * math.sin(t * 6) if fav else 1
    rrect(ctx, x, y, w, h, 24); ctx.set_source_rgba(*col, (0.10 + (0.12 * pulse if fav else 0)) * a); ctx.fill_preserve()
    ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    text(ctx, str(num), x + 52, y + h / 2 + 24, F_BIG, 66, col, a, align="center")
    sz = fit_size(ctx, lab, F_BIG, 50, w - 220)
    text(ctx, lab, x + 110, y + h / 2 + 18, F_BIG, sz, WH, a)
    if fav: star(ctx, x + w - 56, y + h / 2, 30, a)


ROUT = [("PRESS BANCA", C2), ("REMO", C2), ("ZANCADAS", C2), ("SENTADILLA", FAV)]


def routine(ctx, a, order, t, y0=530, gap=128):
    for slot, idx in enumerate(order):
        lab, col = ROUT[idx]
        ex_card(ctx, 230, y0 + slot * gap, 620, 104, slot + 1, lab, col, a, fav=(idx == 3), t=t)


def doc(ctx, x, y, a, col):
    rrect(ctx, x, y, 58, 74, 8); ctx.set_source_rgba(*col, 0.15 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(3); ctx.stroke()
    for ln in range(3):
        ctx.move_to(x + 12, y + 20 + ln * 17); ctx.line_to(x + 46 - ln * 8, y + 20 + ln * 17); ctx.set_source_rgba(*WH, 0.5 * a); ctx.set_line_width(2.5); ctx.stroke()


def dumbbell(ctx, cx, cy, s, a, col):
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.move_to(-60, 0); ctx.line_to(60, 0); ctx.set_source_rgba(*WH, 0.9 * a); ctx.set_line_width(10); ctx.stroke()
    for sx in (-1, 1):
        rrect(ctx, sx * 70 - 18, -48, 36, 96, 8); ctx.set_source_rgba(*col, 0.15 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def bicep(ctx, cx, cy, s, a, col, t):
    """músculo esquemático (vientre muscular) que 'crece'"""
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.move_to(-120, 0); ctx.curve_to(-80, -110, 80, -110, 120, 0); ctx.curve_to(80, 70, -80, 70, -120, 0); ctx.close_path()
    ctx.set_source_rgba(*col, (0.18 + 0.08 * math.sin(t * 5)) * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    for j in range(-2, 3):
        ctx.move_to(-100, j * 12 - 10); ctx.curve_to(-50, j * 18 - 30, 50, j * 18 - 30, 100, j * 12 - 10); ctx.set_source_rgba(*col, 0.45 * a); ctx.set_line_width(2.5); ctx.stroke()
    for sx in (-1, 1):
        ctx.move_to(sx * 120, 0); ctx.line_to(sx * 175, 0); ctx.set_source_rgba(*WH, 0.8 * a); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()


def squatter(ctx, cx, base, s, a, depth, col=FAV):
    """figura de palitos con barra en sentadilla; depth 0..1"""
    if a <= 0: return
    ctx.save(); ctx.translate(cx, base); ctx.scale(s, s)
    hip_y = -170 + 80 * depth; hip_x = -40 * depth
    knee = (40 * depth + 10, -85)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(9); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(-10, 0); ctx.line_to(*knee); ctx.line_to(hip_x, hip_y); ctx.stroke()
    sh = (hip_x + 30 * depth + 10, hip_y - 120 + 15 * depth)
    ctx.move_to(hip_x, hip_y); ctx.line_to(*sh); ctx.stroke()
    ctx.new_path(); ctx.arc(sh[0] + 8, sh[1] - 40, 26, 0, 6.283); ctx.stroke()
    ctx.move_to(sh[0] - 130, sh[1] + 6); ctx.line_to(sh[0] + 130, sh[1] + 6); ctx.set_source_rgba(*WH, 0.9 * a); ctx.set_line_width(8); ctx.stroke()
    for sx in (-1, 1):
        rrect(ctx, sh[0] + sx * 130 - 14, sh[1] - 50, 28, 112, 6); ctx.set_source_rgba(*C2, 0.2 * a); ctx.fill_preserve(); ctx.set_source_rgba(*C2, a); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        routine(ctx, k, [0, 1, 2, 3], t)
        kq = easeb((u - lt(0) - 2.6) / 0.5)
        if kq > 0:
            ctx.move_to(890, 530 + 3 * 128 + 52); ctx.line_to(950, 530 + 3 * 128 + 52)
            text(ctx, "¿AL FINAL?", 540, 1110, F_BIG, 70, RD, kq, align="center")
    elif i == 1:
        g = ease((u - lt(1) - 1.4) / 1.2)
        # la tarjeta favorita sube de la 4.ª a la 1.ª posición
        others = [0, 1, 2]
        for slot, idx in enumerate(others):
            lab, col = ROUT[idx]
            y = 530 + slot * 128 + 128 * g
            ex_card(ctx, 230, y, 620, 104, slot + 1 + (1 if g > 0.5 else 0), lab, col, k)
        y = 530 + 3 * 128 * (1 - g)
        x = 230 + 90 * math.sin(g * math.pi)
        ex_card(ctx, x, y, 620, 104, 4 if g < 0.5 else 1, "SENTADILLA", FAV, k, fav=True, t=t)
    elif i == 2:
        n = int(clamp((u - 0.2) / 1.6) * 11)
        for j in range(n):
            c = j % 6; r = j // 6
            doc(ctx, 230 + c * 105 + (52 if r else 0), 560 + r * 110, k, C2)
        kb = easeb((u - lt(2) - 2.0) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 960); ctx.scale(kb, kb)
            text(ctx, "11 ESTUDIOS", 0, 0, F_BIG, 110, FAV, 1, align="center"); ctx.restore()
    elif i == 3:
        kb = ease((u - 0.2) / 0.4)
        vbars(ctx, [("AL\nINICIO", 0.85, GR), ("AL\nFINAL", 0.50, MU)], 280, 1000, 220, 80, 420, ease((u - 0.3) / 1.6), kb, 28)
        if u > 2.0:
            kk = easeb((u - 2.0) / 0.4)
            text(ctx, "FUERZA", 390, 540, F_MONO, 30, GR, kk, align="center", bold=True)
            text(ctx, "FUERZA", 690, 540, F_MONO, 30, MU, kk, align="center", bold=True)
            star(ctx, 390, 480, 30, kk)
    elif i == 4:
        for j, (lab, col, cx) in enumerate([("GRANDES", C2, 330), ("PEQUEÑOS", FAV, 750)]):
            kj = easeb((u - 0.3 - j * 0.4) / 0.5)
            if kj <= 0: continue
            rrect(ctx, cx - 185, 560, 370, 330, 34); ctx.set_source_rgba(*col, 0.10 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(5); ctx.stroke()
            if j == 0:
                ctx.move_to(cx - 140, 680); ctx.line_to(cx + 140, 680); ctx.set_source_rgba(*WH, 0.9 * kj); ctx.set_line_width(8); ctx.stroke()
                for sx in (-1, 1):
                    for pj, hh in enumerate((120, 90)):
                        rrect(ctx, cx + sx * (100 - pj * 26) - 11, 680 - hh / 2, 22, hh, 6); ctx.set_source_rgba(*col, 0.18 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(4); ctx.stroke()
            else:
                dumbbell(ctx, cx, 680, 0.65, kj, col)
            sz = fit_size(ctx, lab, F_BIG, 70, 320)
            text(ctx, lab, cx, 850, F_BIG, sz, col, kj, align="center")
        cur = "▌" if int(t * 2.5) % 2 == 0 else " "
        text(ctx, "COMENTA: GRANDES O PEQUEÑOS" + cur, 540, 990, F_MONO, 32, FAV, ease((u - 1.2) / 0.4), align="center", bold=True)
    elif i == 5:
        g = ease((u - 0.5) / 2.0)
        bicep(ctx, 330, 760, 0.85 + 0.25 * g, k, C2, t)
        bicep(ctx, 750, 760, 0.85 + 0.25 * g, k, FAV, t + 1)
        text(ctx, "ORDEN A", 330, 940, F_MONO, 28, C2, k, align="center", bold=True)
        text(ctx, "ORDEN B", 750, 940, F_MONO, 28, FAV, k, align="center", bold=True)
        kb = easeb((u - lt(5) - 2.6) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 790); ctx.scale(kb, kb)
            text(ctx, "=", 0, 0, F_BIG, 120, GR, 1, align="center"); ctx.restore()
    elif i == 6:
        routine(ctx, k, [3, 0, 1, 2], t)
    elif i == 7:
        dep = 0.5 - 0.5 * math.cos(t * 2.4)
        squatter(ctx, 360, 1010, 1.25, k, dep)
        kb = easeb((u - 1.2) / 0.5)
        if kb > 0:
            pill(ctx, "1.º DE LA SESIÓN", 735, 860, GR, kb, 30, filled=True)
            text(ctx, "AL INICIO", 735, 820, F_BIG, 64, WH, kb, align="center")
    elif i == 8:
        ctx.save(); ctx.translate(540, 700); ctx.scale(1.2, 1.2); barbell_icon(ctx, 0, 0, t, k); ctx.restore()
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1020); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, FAV, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "COMPARACIÓN · FUERZA Y RUTINA", W / 2, 214, CY, k, 26)
        title(ctx, "¿TU EJERCICIO CLAVE VA AL FINAL?", WH, 380, 84, k)
    elif i == 1:
        pill(ctx, "LA PREGUNTA", W / 2, 214, C2, k, 30, filled=True)
        title(ctx, "¿IMPORTA EL ORDEN?", WH, 380, 100, k)
    elif i == 2:
        pill(ctx, "METAANÁLISIS", W / 2, 214, FAV, k, 30, filled=True)
        title(ctx, "SOLO CAMBIARON EL ORDEN", WH, 380, 90, k)
        src(ctx, "Nunes et al., Eur J Sport Sci 2021 · doi:10.1080/17461391.2020.1733672", k, 1120)
    elif i == 3:
        pill(ctx, "RESULTADO · FUERZA", W / 2, 214, GR, k, 30, filled=True)
        title(ctx, "GANA EL QUE VA PRIMERO", WH, 380, 92, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1110, F_MONO, 22, FAV, k, align="center", bold=True)
        src(ctx, "Nunes et al., 2021 · más fuerza en el ejercicio hecho al inicio", k, 1150)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 214, FAV, k, 32, filled=True)
        title(ctx, "¿CON QUÉ EMPIEZAS TÚ?", WH, 380, 96, k)
    elif i == 5:
        pill(ctx, "RESULTADO · TAMAÑO", W / 2, 214, C2, k, 30, filled=True)
        title(ctx, "EL MÚSCULO CRECIÓ PARECIDO", WH, 380, 88, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1060, F_MONO, 22, FAV, k, align="center", bold=True)
        src(ctx, "Nunes et al., 2021 · sin diferencia en hipertrofia entre órdenes", k, 1100)
    elif i == 6:
        pill(ctx, "REGLA PRÁCTICA", W / 2, 214, GR, k, 30, filled=True)
        title(ctx, "LO IMPORTANTE, PRIMERO", WH, 380, 94, k)
    elif i == 7:
        pill(ctx, "EJEMPLO", W / 2, 214, FAV, k, 30, filled=True)
        title(ctx, "¿QUIERES SUBIR TU SENTADILLA?", WH, 380, 86, k)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 380, 80, k)


run_episode(neon, txt, "EXPEDIENTE 50 · FUERZA")
