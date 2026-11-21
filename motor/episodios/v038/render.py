"""v038 · ¿Las mujeres ganan menos músculo con pesas? (MITO VS. REALIDAD, serie MÚSCULO ·
paleta verde bosque + rosa + turquesa + ámbar)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (0.35, 0.95, 0.70)   # verde menta = músculo


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.02, 0.11, 0.08], [0.003, 0.025, 0.02])
from engine_ext import *
CY = ACC
RO = (1.0, 0.47, 0.76)    # rosa = ellas
TE = (0.33, 0.80, 1.0)    # celeste = ellos


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


def person(ctx, cx, top, s, col, a, lift=0.0):
    """figura simple con barra sobre los hombros (sentadilla trasera); lift 0..1 baja/sube"""
    if a <= 0: return
    dy = 40 * lift
    ctx.save(); ctx.translate(cx, top + dy); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 44, 0, 6.283); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    rrect(ctx, -70, 60, 140, 200, 40); ctx.set_source_rgba(*col, 0.08 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.stroke()
    # barra
    ctx.move_to(-170, 70); ctx.line_to(170, 70); ctx.set_source_rgba(*AM, a); ctx.set_line_width(10); ctx.stroke()
    for xx in (-170, 170):
        rrect(ctx, xx - 14, 20, 28, 100, 8); ctx.set_source_rgba(*AM, 0.25 * a); ctx.fill_preserve(); ctx.set_source_rgba(*AM, a); ctx.set_line_width(4); ctx.stroke()
    # piernas
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_source_rgba(*col, a); ctx.set_line_width(18)
    kx = 40 + 30 * lift
    for sd in (-1, 1):
        ctx.move_to(sd * 40, 255); ctx.line_to(sd * kx, 360 - dy / s * 0.5); ctx.line_to(sd * 45, 470 - dy / s); ctx.stroke()
    ctx.set_line_cap(cairo.LINE_CAP_BUTT)
    ctx.restore()


def xsec(ctx, cx, cy, r0, grow, col, a, t):
    """corte transversal de músculo: r0 = tamaño inicial, grow = fracción de crecimiento"""
    if a <= 0: return
    r1 = r0 * (1 + grow)
    ctx.new_path(); ctx.arc(cx, cy, r1, 0, 6.283); ctx.set_source_rgba(*col, 0.22 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, r0, 0, 6.283); ctx.set_source_rgba(*WH, 0.5 * a); ctx.set_line_width(3); ctx.set_dash([10, 8]); ctx.stroke(); ctx.set_dash([])
    for j in range(7):
        ang = j / 7 * 6.283 + t * 0.2
        ctx.new_path(); ctx.arc(cx + math.cos(ang) * r0 * 0.55, cy + math.sin(ang) * r0 * 0.55, r0 * 0.18, 0, 6.283)
        ctx.set_source_rgba(*col, 0.5 * a); ctx.set_line_width(2); ctx.stroke()


def stamp(ctx, s, cx, cy, col, k):
    if k <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.16); ctx.scale(1.6 - 0.6 * k, 1.6 - 0.6 * k)
    font(ctx, F_BIG, 110); tw = ctx.text_extents(s).x_advance
    rrect(ctx, -tw / 2 - 40, -95, tw + 80, 130, 18); ctx.set_source_rgba(*col, 0.15 * k); ctx.fill_preserve(); ctx.set_source_rgba(*col, k); ctx.set_line_width(7); ctx.stroke()
    text(ctx, s, 0, 18, F_BIG, 110, col, k, align="center"); ctx.restore()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    lift = 0.5 - 0.5 * math.cos(t * 2.6)
    if i == 0:
        person(ctx, 280, 620, 0.8, RO, k, lift)
        person(ctx, 800, 620, 0.8, TE, ease((u - 0.3) / 0.4), 1 - lift)
        kq = easeb((u - 1.6) / 0.5)
        if kq > 0: big(ctx, "?", 540, 820, 150 * kq, AM, kq, maxw=200)
        text(ctx, "ELLAS", 280, 1080, F_MONO, 30, RO, k, align="center", bold=True)
        text(ctx, "ELLOS", 800, 1080, F_MONO, 30, TE, k, align="center", bold=True)
    elif i == 1:
        badge(ctx, 360, 760, "29", "ESTUDIOS", AM, ease((u - 0.1) / 0.4))
        badge(ctx, 720, 760, "=", "MISMO\nPROGRAMA", CY, ease((u - lt(1) - 3.8) / 0.4))
    elif i == 2:
        kk = ease((u - 0.2) / 1.4)
        vbars(ctx, [("ELLAS", 0.80, RO), ("ELLOS", 0.80, TE)], 290, 1060, 200, 100, 420, kk, label_size=30)
        text(ctx, "≈", 540, 820, F_BIG, 110, WH, ease((u - 1.4) / 0.4), align="center")
        stamp(ctx, "MITO", 540, 560, RD, easeb((u - lt(2) - 3.4) / 0.4))
    elif i == 3:
        g = 0.12 * ease((u - 0.4) / 1.6)
        xsec(ctx, 330, 780, 120, g, RO, k, t)
        xsec(ctx, 750, 780, 160, g, TE, ease((u - 0.2) / 0.4), t)
        text(ctx, "ELLAS", 330, 1010, F_MONO, 28, RO, k, align="center", bold=True)
        text(ctx, "ELLOS", 750, 1010, F_MONO, 28, TE, k, align="center", bold=True)
    elif i == 4:
        for j, (lab, col, x) in enumerate((("SÍ", GR, 330), ("TODAVÍA NO", AM, 750))):
            kj = easeb((u - 0.3 - j * 0.3) / 0.45)
            if kj <= 0: continue
            rrect(ctx, x - 180, 620, 360, 260, 30); ctx.set_source_rgba(*col, 0.12 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(4); ctx.stroke()
            big(ctx, lab, x, 790, 96, col, kj, maxw=320)
        text(ctx, "COMENTA", 540, 980, F_MONO, 30, WH, k, align="center", bold=True)
    elif i == 5:
        kk = ease((u - 0.3) / 1.4)
        for j, (lab, v, col) in enumerate((("ELLAS", 0.92, RO), ("ELLOS", 0.66, TE))):
            kj = ease((kk - j * 0.2) / 0.5)
            if kj <= 0: continue
            y = 660 + j * 190
            text(ctx, lab, 170, y - 18, F_MONO, 30, col, kj, bold=True)
            rrect(ctx, 170, y, 740, 60, 30); ctx.set_source_rgba(*col, 0.10 * kj); ctx.fill()
            rrect(ctx, 170, y, max(60, 740 * v * kj), 60, 30); ctx.set_source_rgba(*col, 0.35 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(3); ctx.stroke()
        text(ctx, "MEJORA RELATIVA DE FUERZA · TREN SUPERIOR", 540, 1060, F_MONO, 23, MU, k, align="center", bold=True)
    elif i == 6:
        days = ["L", "M", "M", "J", "V", "S", "D"]; on = (1, 4)
        for j, dd in enumerate(days):
            kj = easeb((u - 0.2 - j * 0.08) / 0.4)
            if kj <= 0: continue
            x = 210 + j * 110
            ctx.new_path(); ctx.arc(x, 800, 44, 0, 6.283)
            lit = j in on and u > lt(6) + 3.2
            if lit: ctx.set_source_rgba(*AM, 0.85 * kj); ctx.fill_preserve()
            ctx.set_source_rgba(*AM, kj); ctx.set_line_width(3); ctx.stroke()
            text(ctx, dd, x, 812, F_MONO, 32, (0.02, 0.05, 0.05) if lit else WH, kj, align="center", bold=True)
        kb = easeb((u - lt(6) - 3.4) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 1000); ctx.scale(kb, kb)
            text(ctx, "MÍNIMO 2 DÍAS", 0, 0, F_BIG, 80, GR, 1, align="center"); ctx.restore()
    elif i == 7:
        kk = ease((u - 0.3) / 0.8)
        x0, x1 = 160, 920
        ctx.move_to(x0, 820); ctx.line_to(x1, 820); ctx.set_source_rgba(*MU, 0.8 * kk); ctx.set_line_width(4); ctx.stroke()
        def X(age): return x0 + (x1 - x0) * age / 90
        for age in (0, 18, 45, 65, 90):
            ctx.move_to(X(age), 800); ctx.line_to(X(age), 840); ctx.stroke()
            text(ctx, str(age), X(age), 890, F_MONO, 26, WH, kk, align="center", bold=True)
        kh = ease((u - 0.8) / 0.6)
        rrect(ctx, X(18), 770, (X(45) - X(18)) * kh, 100, 20); ctx.set_source_rgba(*GR, 0.25 * kh); ctx.fill_preserve(); ctx.set_source_rgba(*GR, kh); ctx.set_line_width(4); ctx.stroke()
        text(ctx, "ESTUDIADO", (X(18) + X(45)) / 2, 740, F_MONO, 26, GR, kh, align="center", bold=True)
        kq = easeb((u - lt(7) - 3.6) / 0.5)
        if kq > 0:
            ctx.save(); ctx.translate((X(45) + X(90)) / 2, 720); ctx.scale(kq, kq)
            text(ctx, "?", 0, 0, F_BIG, 110, AM, 1, align="center"); ctx.restore()
        text(ctx, "AÑOS", 540, 960, F_MONO, 24, MU, kk, align="center", bold=True)
    elif i == 8:
        person(ctx, 300, 500, 0.65, RO, k, lift)
        person(ctx, 780, 500, 0.65, TE, k, 1 - lift)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1010); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, AM, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "MITO O REALIDAD · MÚSCULO", W / 2, 196, CY, k, 28)
        title(ctx, "¿ELLAS GANAN MENOS MÚSCULO?", WH, 368, 92, k)
    elif i == 1:
        pill(ctx, "METAANÁLISIS · 2025", W / 2, 196, AM, k, 28, filled=True)
        title(ctx, "HOMBRES VS. MUJERES", WH, 368, 100, k)
        src(ctx, "Refalo et al., PeerJ 2025 · doi:10.7717/peerj.19042", k, 1120)
    elif i == 2:
        pill(ctx, "EN PROPORCIÓN", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "CRECIERON IGUAL", WH, 368, 110, k)
        src(ctx, "Refalo et al., 2025 · aumento relativo: sin diferencia clara (≈0,7 %)", k, 1170)
    elif i == 3:
        pill(ctx, "EN CENTÍMETROS", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "ELLOS, ALGO MÁS", WH, 368, 110, k)
        text(ctx, "ESQUEMA ILUSTRATIVO · MISMO % SOBRE DISTINTA BASE", W / 2, 1080, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Refalo et al., 2025 · ganancia absoluta levemente mayor en hombres", k, 1130)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿TÚ ENTRENAS FUERZA?", WH, 368, 104, k)
    elif i == 5:
        pill(ctx, "FUERZA · TREN SUPERIOR", W / 2, 196, RO, k, 28, filled=True)
        title(ctx, "ELLAS MEJORARON MÁS", WH, 368, 100, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1110, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Roberts, Nuckols y Krieger, J Strength Cond Res 2020 · doi:10.1519/JSC.0000000000003521", k, 1150)
    elif i == 6:
        pill(ctx, "RECOMENDACIÓN OMS", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "FUERZA PARA TODOS", WH, 368, 104, k)
        src(ctx, "OMS 2020 · Bull et al., Br J Sports Med · doi:10.1136/bjsports-2020-102955", k, 1120)
    elif i == 7:
        pill(ctx, "OJO", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "ADULTOS DE 18 A 45 AÑOS", WH, 368, 96, k)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 38 · MÚSCULO")
