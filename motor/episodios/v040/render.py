"""v040 · ¿Hacer abdominales quema la grasa del abdomen? (MITO VS. REALIDAD, serie METABOLISMO ·
paleta cobre + coral + ámbar + cian)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (1.0, 0.52, 0.38)   # coral = metabolismo


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.13, 0.055, 0.03], [0.025, 0.01, 0.006])
from engine_ext import *
CY = ACC
TE = (0.30, 0.90, 1.0)    # cian = músculo
FAT = (1.0, 0.80, 0.32)   # ámbar = grasa


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


def hbar(ctx, x, y, w, h, frac, col, a, label, val=""):
    rrect(ctx, x, y, w, h, h / 2); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill()
    if frac > 0:
        rrect(ctx, x, y, max(h, w * frac), h, h / 2); ctx.set_source_rgba(*col, 0.35 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
    text(ctx, label, x, y - 16, F_MONO, 27, col, a, bold=True)
    if val: text(ctx, val, x + w, y - 16, F_MONO, 27, WH, a, align="right", bold=True)


def torso(ctx, cx, cy, s, a, t, fat=1.0, abs_glow=0.4, scan=True):
    """holograma de tronco: contorno, 'six pack' (cian) y capa de grasa (ámbar) de grosor `fat`"""
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    # contorno
    ctx.move_to(-230, -300); ctx.curve_to(-250, -180, -200, -60, -175, 40)
    ctx.curve_to(-165, 120, -190, 220, -200, 300); ctx.line_to(200, 300)
    ctx.curve_to(190, 220, 165, 120, 175, 40); ctx.curve_to(200, -60, 250, -180, 230, -300); ctx.close_path()
    ctx.set_source_rgba(*CY, 0.06 * a); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.9 * a); ctx.set_line_width(5); ctx.stroke()
    # pectorales
    for sd in (-1, 1):
        ctx.move_to(sd * 10, -250); ctx.curve_to(sd * 90, -265, sd * 190, -240, sd * 200, -170)
        ctx.curve_to(sd * 150, -120, sd * 60, -120, sd * 10, -140)
        ctx.set_source_rgba(*CY, 0.55 * a); ctx.set_line_width(3); ctx.stroke()
    # abdominales
    for r in range(3):
        for sd in (-1, 1):
            x = sd * 62 - 50; y = -100 + r * 95
            rrect(ctx, x, y, 100, 80, 22)
            ctx.set_source_rgba(*TE, (0.10 + 0.25 * abs_glow) * a); ctx.fill_preserve()
            ctx.set_source_rgba(*TE, (0.55 + 0.45 * abs_glow) * a); ctx.set_line_width(3.5); ctx.stroke()
    # capa de grasa sobre el abdomen
    if fat > 0.02:
        th = 70 * fat
        ctx.save(); ctx.translate(0, 70); ctx.scale(1.0, 0.95)
        ctx.new_path(); ctx.arc(0, 0, 150 + th, 0, 6.283); ctx.restore()
        wob = 0.5 + 0.5 * math.sin(t * 2.2)
        ctx.set_source_rgba(*FAT, (0.10 + 0.05 * wob) * a * min(1, fat * 1.5)); ctx.fill_preserve()
        ctx.set_dash([14, 10]); ctx.set_source_rgba(*FAT, 0.85 * a * min(1, fat * 1.5)); ctx.set_line_width(4); ctx.stroke(); ctx.set_dash([])
    if scan:
        sy = -300 + ((t * 0.45) % 1) * 600
        ctx.move_to(-240, sy); ctx.line_to(240, sy); ctx.set_source_rgba(*CY, 0.5 * a); ctx.set_line_width(3); ctx.stroke()
    ctx.restore()


def body(ctx, cx, top, s, a, hl_up=0.0, hl_leg=0.0):
    """figura de cuerpo completo: pierna derecha entrenada (cian), brazos y tronco con grasa que baja (verde)"""
    if a <= 0: return
    ctx.save(); ctx.translate(cx, top); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 50, 0, 6.283); ctx.set_source_rgba(*CY, 0.08 * a); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.85 * a); ctx.set_line_width(4); ctx.stroke()
    up = GR if hl_up > 0 else CY
    rrect(ctx, -85, 70, 170, 250, 40); ctx.set_source_rgba(*up, (0.06 + 0.22 * hl_up) * a); ctx.fill_preserve(); ctx.set_source_rgba(*up, 0.9 * a); ctx.stroke()
    for sd in (-1, 1):
        rrect(ctx, sd * 128 - 26, 80, 52, 240, 26); ctx.set_source_rgba(*up, (0.06 + 0.22 * hl_up) * a); ctx.fill_preserve(); ctx.set_source_rgba(*up, 0.9 * a); ctx.stroke()
    for sd in (-1, 1):
        col = TE if sd > 0 else MU
        g = (0.10 + 0.30 * hl_leg) if sd > 0 else 0.05
        rrect(ctx, sd * 45 - 34, 330, 68, 330, 30); ctx.set_source_rgba(*col, g * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(4 if sd < 0 else 6); ctx.stroke()
    ctx.restore()


def icon_heart(ctx, cx, cy, r, col, a, t):
    if a <= 0: return
    p = 1 + 0.08 * max(0, math.sin(t * 7))
    ctx.save(); ctx.translate(cx, cy); ctx.scale(r / 100 * p, r / 100 * p)
    ctx.move_to(0, 70); ctx.curve_to(-120, -10, -80, -110, 0, -50); ctx.curve_to(80, -110, 120, -10, 0, 70); ctx.close_path()
    ctx.restore(); ctx.set_source_rgba(*col, 0.15 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()


def icon_bolt(ctx, cx, cy, s, col, a):
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.move_to(15, -70); ctx.line_to(-35, 10); ctx.line_to(0, 10); ctx.line_to(-15, 70); ctx.line_to(35, -10); ctx.line_to(0, -10); ctx.close_path()
    ctx.restore(); ctx.set_source_rgba(*col, 0.18 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()


def icon_dumbbell(ctx, cx, cy, s, col, a):
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.move_to(-60, 0); ctx.line_to(60, 0); ctx.set_source_rgba(*WH, 0.9 * a); ctx.set_line_width(10); ctx.stroke()
    for sd in (-1, 1):
        rrect(ctx, sd * 70 - 16, -45, 32, 90, 8); ctx.set_source_rgba(*col, 0.18 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def cross(ctx, cx, cy, r, col, a):
    if a <= 0: return
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*col, a); ctx.set_line_width(6); ctx.stroke()
    d = r * 0.55
    ctx.move_to(cx - d, cy - d); ctx.line_to(cx + d, cy + d); ctx.move_to(cx + d, cy - d); ctx.line_to(cx - d, cy + d); ctx.stroke()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        torso(ctx, 540, 700, 0.92, k, t, fat=1.0, abs_glow=0.6 + 0.4 * math.sin(t * 3))
        kn = easeb((u - lt(0) - 1.6) / 0.5)
        if kn > 0:
            ctx.save(); ctx.translate(540, 1110); ctx.scale(kn, kn)
            text(ctx, "¿ABDOMINALES = MENOS GRASA?", 0, 0, F_BIG, 70, FAT, 1, align="center"); ctx.restore()
    elif i == 1:
        # calendario: 6 semanas x 7 días, 5 activos por semana
        x0, y0, cw, chh = 230, 560, 92, 62
        kk = ease((u - 0.3) / 3.6)
        n_on = int(30 * kk + 0.001); c = 0
        for wk in range(6):
            text(ctx, "S%d" % (wk + 1), x0 - 50, y0 + wk * (chh + 12) + 42, F_MONO, 22, MU, k, align="center", bold=True)
            for dd in range(7):
                x = x0 + dd * cw; y = y0 + wk * (chh + 12)
                on = dd < 5 and c < n_on
                if dd < 5: c += 1
                rrect(ctx, x, y, cw - 12, chh, 12)
                ctx.set_source_rgba(*(TE if on else MU), (0.30 if on else 0.05) * k); ctx.fill_preserve()
                ctx.set_source_rgba(*(TE if on else MU), (0.95 if on else 0.35) * k); ctx.set_line_width(2.5); ctx.stroke()
        kc = ease((u - lt(1) - 3.6) / 0.5)
        if kc > 0:
            rrect(ctx, 290, 1030, 500, 70, 35); ctx.set_source_rgba(*MU, 0.12 * kc); ctx.fill_preserve(); ctx.set_source_rgba(*MU, kc); ctx.set_line_width(3); ctx.stroke()
            text(ctx, "OTRO GRUPO: NADA", 540, 1077, F_MONO, 30, WH, kc, align="center", bold=True)
    elif i == 2:
        torso(ctx, 540, 700, 0.72, k, t, fat=1.0, abs_glow=0.3, scan=True)
        kk = ease((u - 1.0) / 1.0)
        hbar(ctx, 170, 1000, 740, 46, 0.62 * kk, FAT, kk, "GRASA DEL ABDOMEN", "= SIN CAMBIO" if kk > 0.9 else "")
        k2 = ease((u - lt(2) - 2.4) / 1.0)
        hbar(ctx, 170, 1110, 740, 46, 0.90 * k2, TE, k2, "RESISTENCIA ABDOMINAL", "↑ MEJORÓ" if k2 > 0.9 else "")
    elif i == 3:
        hu = ease((u - lt(3) - 2.0) / 1.0)
        body(ctx, 540, 520, 0.95, k, hl_up=hu, hl_leg=0.6 + 0.4 * math.sin(t * 4))
        ka = ease((u - 0.6) / 0.5)
        if ka > 0:
            ctx.move_to(700, 1010); ctx.line_to(600, 960); ctx.set_source_rgba(*TE, ka); ctx.set_line_width(3); ctx.stroke()
            text(ctx, "PIERNA", 790, 1010, F_MONO, 26, TE, ka, align="center", bold=True)
            text(ctx, "ENTRENADA", 790, 1042, F_MONO, 26, TE, ka, align="center", bold=True)
        if hu > 0:
            text(ctx, "↓ GRASA", 260, 730, F_MONO, 30, GR, hu, align="center", bold=True)
            text(ctx, "BRAZOS", 260, 765, F_MONO, 24, GR, hu, align="center", bold=True)
            text(ctx, "Y TRONCO", 260, 795, F_MONO, 24, GR, hu, align="center", bold=True)
        kl = ease((u - lt(3) - 3.6) / 0.6)
        if kl > 0:
            text(ctx, "= SIN CAMBIO", 790, 1090, F_MONO, 26, FAT, kl, align="center", bold=True)
    elif i == 4:
        kc = ease((u - 0.3) / 0.4)
        for j, (lab, col) in enumerate([("SÍ", GR), ("NO", RD)]):
            kj = easeb((u - 0.3 - j * 0.25) / 0.5)
            if kj <= 0: continue
            cx = 360 + j * 360
            rrect(ctx, cx - 140, 640, 280, 220, 40); ctx.set_source_rgba(*col, 0.14 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(5); ctx.stroke()
            text(ctx, lab, cx, 800, F_BIG, 140, col, kj, align="center")
        cur = "▌" if int(t * 2.5) % 2 == 0 else " "
        text(ctx, "COMENTA SÍ O NO " + cur, 540, 1010, F_MONO, 36, WH, kc, align="center", bold=True)
    elif i == 5:
        badge(ctx, 360, 700, "13", "ESTUDIOS", FAT, ease((u - 0.1) / 0.4))
        badge(ctx, 720, 700, "1.158", "PERSONAS", TE, ease((u - 0.8) / 0.4))
        kx = easeb((u - lt(5) - 2.6) / 0.5)
        if kx > 0:
            cross(ctx, 540, 1000, 70, RD, kx)
            text(ctx, "GRASA LOCALIZADA", 540, 1110, F_MONO, 28, RD, kx, align="center", bold=True)
    elif i == 6:
        for j, (fn, lab, col) in enumerate([("h", "CARDIO", RD), ("b", "INTERVALOS", FAT), ("d", "PESAS", TE)]):
            kj = easeb((u - lt(6) - 1.6 - j * 0.6) / 0.5)
            cx = 240 + j * 300
            if kj <= 0: continue
            if fn == "h": icon_heart(ctx, cx, 560, 85, col, kj, t)
            elif fn == "b": icon_bolt(ctx, cx, 560, 1.0, col, kj)
            else: icon_dumbbell(ctx, cx, 560, 1.0, col, kj)
            text(ctx, lab, cx, 680, F_MONO, 26, col, kj, align="center", bold=True)
        kf = ease((u - lt(6) - 3.6) / 1.6)
        torso(ctx, 540, 920, 0.55, k, t, fat=1.0 - 0.6 * kf, abs_glow=0.4 + 0.4 * kf, scan=False)
    elif i == 7:
        torso(ctx, 540, 760, 0.9, k, t, fat=0.8, abs_glow=0.7 + 0.3 * math.sin(t * 5), scan=False)
        kb = easeb((u - lt(7) - 2.4) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 1130); ctx.scale(kb, kb)
            text(ctx, "FORTALECEN, PERO NO QUEMAN GRASA", 0, 0, F_BIG, 58, FAT, 1, align="center"); ctx.restore()
    elif i == 8:
        torso(ctx, 540, 690, 0.62, k, t, fat=0.5, abs_glow=0.8, scan=True)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1050); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, FAT, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "MITO VS. REALIDAD · METABOLISMO", W / 2, 196, CY, k, 28)
        title(ctx, "¿ABDOMINALES PARA QUEMAR GRASA?", WH, 368, 88, k)
    elif i == 1:
        pill(ctx, "ENSAYO ALEATORIZADO", W / 2, 196, FAT, k, 28, filled=True)
        title(ctx, "5 DÍAS POR SEMANA · 6 SEMANAS", WH, 368, 88, k)
        src(ctx, "Vispute et al., J Strength Cond Res 2011 · doi:10.1519/JSC.0b013e3181fb4a46", k, 1160)
    elif i == 2:
        pill(ctx, "RESULTADO", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "LA GRASA NO SE MOVIÓ", WH, 368, 100, k)
        src(ctx, "Vispute et al., 2011 · grasa abdominal y pliegues: sin cambios", k, 1210)
    elif i == 3:
        pill(ctx, "ESTUDIO CHILENO", W / 2, 196, TE, k, 28, filled=True)
        title(ctx, "SOLO UNA PIERNA, 12 SEMANAS", WH, 368, 90, k)
        src(ctx, "Ramírez-Campillo et al., J Strength Cond Res 2013 · doi:10.1519/JSC.0b013e31827e8681", k, 1190)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 196, FAT, k, 32, filled=True)
        title(ctx, "¿HACES ABDOMINALES PARA MARCAR?", WH, 368, 86, k)
    elif i == 5:
        pill(ctx, "METAANÁLISIS · 2022", W / 2, 196, FAT, k, 28, filled=True)
        title(ctx, "NO EXISTE LA QUEMA LOCALIZADA", WH, 368, 88, k)
        src(ctx, "Human Movement 2022 · 13 estudios, 1.158 personas · doi:10.5114/hm.2022.110373", k, 1190)
    elif i == 6:
        pill(ctx, "LO QUE SÍ FUNCIONA", W / 2, 196, GR, k, 28, filled=True)
        title(ctx, "MOVER TODO EL CUERPO", WH, 368, 100, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1140, F_MONO, 22, FAT, k, align="center", bold=True)
        src(ctx, "Chen et al., Obes Rev 2024 · 84 ensayos · doi:10.1111/obr.13666", k, 1185)
    elif i == 7:
        pill(ctx, "CONSEJO", W / 2, 196, TE, k, 30, filled=True)
        title(ctx, "IGUAL HAZ ABDOMINALES", WH, 368, 98, k)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 40 · METABOLISMO")
