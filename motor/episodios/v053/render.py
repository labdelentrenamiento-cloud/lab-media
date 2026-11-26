"""v053 · Superseries: menos tiempo, mismo músculo (COMPARACIÓN A vs. B, serie RUTINA EFICIENTE ·
paleta verde azulado profundo + verde lima + coral)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (0.66, 1.0, 0.36)   # verde lima


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.02, 0.10, 0.10], [0.004, 0.02, 0.025])
from engine_ext import *
CY = ACC
SS = ACC                     # superserie = lima
TR = (0.24, 0.94, 1.0)       # tradicional = cian
CO = (1.0, 0.50, 0.42)       # coral (letra chica)


def title(ctx, s, color=WH, y=380, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1110):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def stopwatch(ctx, cx, cy, r, a, t, frac, col=SS):
    if a <= 0: return
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve()
    ctx.set_source_rgba(*col, a); ctx.set_line_width(6); ctx.stroke()
    rrect(ctx, cx - 22, cy - r - 34, 44, 26, 6); ctx.set_source_rgba(*col, a); ctx.fill()
    ctx.new_path(); ctx.arc(cx, cy, r - 18, -math.pi / 2, -math.pi / 2 + 6.283 * frac)
    ctx.set_source_rgba(*col, 0.5 * a); ctx.set_line_width(14); ctx.stroke()
    ang = -math.pi / 2 + 6.283 * frac
    ctx.move_to(cx, cy); ctx.line_to(cx + math.cos(ang) * (r - 30), cy + math.sin(ang) * (r - 30))
    ctx.set_source_rgba(*WH, a); ctx.set_line_width(6); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def dumbbell(ctx, cx, cy, s, a, col):
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.move_to(-60, 0); ctx.line_to(60, 0); ctx.set_source_rgba(*WH, 0.9 * a); ctx.set_line_width(10); ctx.stroke()
    for sx in (-1, 1):
        rrect(ctx, sx * 70 - 18, -48, 36, 96, 8); ctx.set_source_rgba(*col, 0.15 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def block(ctx, x, y, w, h, col, a, lab=None):
    if a <= 0 or w <= 1: return
    rrect(ctx, x, y, w, h, 10); ctx.set_source_rgba(*col, 0.25 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
    if lab and w > 40:
        text(ctx, lab, x + w / 2, y + h / 2 + 10, F_MONO, 26, WH, a, align="center", bold=True)


def timeline_row(ctx, y, seq, k, a, label, col):
    """seq: lista de (tipo, ancho) tipo A/B=ejercicio, R=descanso"""
    text(ctx, label, 270, y - 18, F_MONO, 26, col, a, bold=True)
    x = 270; tot = sum(w for _, w in seq); lim = 270 + tot * k
    for typ, w in seq:
        ww = max(0, min(w, lim - x))
        if typ == "R":
            if ww > 0:
                ctx.move_to(x + 4, y + 30); ctx.line_to(x + ww - 4, y + 30)
                ctx.set_source_rgba(*MU, 0.7 * a); ctx.set_line_width(3); ctx.set_dash([8, 8]); ctx.stroke(); ctx.set_dash([])
        else:
            block(ctx, x + 2, y, ww - 4, 60, TR if typ == "A" else SS if col == SS else TR, a, typ if ww > 30 else None)
        x += w
    return x


def muscle(ctx, cx, cy, s, a, col, t, glow=0.5):
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.move_to(-120, 0); ctx.curve_to(-80, -110, 80, -110, 120, 0); ctx.curve_to(80, 70, -80, 70, -120, 0); ctx.close_path()
    ctx.set_source_rgba(*col, (0.12 + 0.2 * glow * (0.7 + 0.3 * math.sin(t * 5))) * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    for j in range(-2, 3):
        ctx.move_to(-100, j * 12 - 10); ctx.curve_to(-50, j * 18 - 30, 50, j * 18 - 30, 100, j * 12 - 10); ctx.set_source_rgba(*col, 0.45 * a); ctx.set_line_width(2.5); ctx.stroke()
    ctx.restore()


def eq(ctx, x, y, a, col=GR):
    ctx.move_to(x - 22, y - 9); ctx.line_to(x + 22, y - 9); ctx.move_to(x - 22, y + 9); ctx.line_to(x + 22, y + 9)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(7); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        stopwatch(ctx, 540, 760, 170, k, t, (t * 0.35) % 1)
        kq = easeb((u - lt(0) - 1.6) / 0.5)
        if kq > 0:
            ctx.save(); ctx.translate(540, 1030); ctx.scale(kq, kq)
            text(ctx, "MENOS TIEMPO", 0, 0, F_BIG, 90, SS, 1, align="center"); ctx.restore()
    elif i == 1:
        dumbbell(ctx, 330, 760, 1.1, k, TR)
        text(ctx, "EJERCICIO A", 330, 880, F_MONO, 28, TR, k, align="center", bold=True)
        kb = easeb((u - 1.2) / 0.5)
        if kb > 0:
            ctx.move_to(450, 760); ctx.line_to(620, 760); ctx.move_to(595, 735); ctx.line_to(622, 760); ctx.line_to(595, 785)
            ctx.set_source_rgba(*WH, kb); ctx.set_line_width(7); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
            text(ctx, "SIN PAUSA", 535, 725, F_MONO, 22, MU, kb, align="center", bold=True)
        kc = easeb((u - 1.8) / 0.5)
        dumbbell(ctx, 750, 760, 1.1, kc, SS)
        text(ctx, "EJERCICIO B", 750, 880, F_MONO, 28, SS, kc, align="center", bold=True)
    elif i == 2:
        kk = ease((u - 0.3) / 2.6)
        trad = [("A", 80), ("R", 70), ("A", 80), ("R", 70), ("B", 80), ("R", 70), ("B", 80)]
        sup = [("A", 80), ("B", 80), ("R", 70), ("A", 80), ("B", 80)]
        timeline_row(ctx, 640, trad, kk, k, "SERIES DE SIEMPRE", TR)
        timeline_row(ctx, 860, sup, kk, easeb((u - 0.6) / 0.5), "SUPERSERIE", SS)
        kn = easeb((u - lt(2) - 1.2) / 0.5)
        if kn > 0:
            ctx.save(); ctx.translate(540, 540); ctx.scale(kn, kn)
            text(ctx, "19 ESTUDIOS", 0, 0, F_BIG, 84, WH, 1, align="center"); ctx.restore()
    elif i == 3:
        kb = ease((u - 0.2) / 1.6)
        vbars(ctx, [("SERIES DE\nSIEMPRE", 1.0, TR), ("SUPER-\nSERIE", 0.68, SS)], 170, 1000, 190, 70, 400, kb, k, 26)
        text(ctx, "DURACIÓN (esquema)", 395, 560, F_MONO, 26, MU, k, align="center", bold=True)
        kr = easeb((u - lt(3) - 2.6) / 0.5)
        if kr > 0:
            for j, lab in enumerate(["REPETICIONES", "PESO TOTAL"]):
                y = 700 + j * 120
                eq(ctx, 700, y - 12, kr)
                text(ctx, lab, 740, y, F_MONO, 26, WH, kr, bold=True)
            text(ctx, "IGUAL", 790, 940, F_BIG, 60, GR, kr, align="center")
    elif i == 4:
        ka = easeb((u - 0.3) / 0.5); kb = easeb((u - 1.0) / 0.5)
        muscle(ctx, 330, 760, 0.95, ka, TR, t, 0.7)
        text(ctx, "SERIES DE SIEMPRE", 330, 900, F_MONO, 24, TR, ka, align="center", bold=True)
        eq(ctx, 540, 760, kb)
        muscle(ctx, 750, 760, 0.95, kb, SS, t, 0.7)
        text(ctx, "SUPERSERIE", 750, 900, F_MONO, 24, SS, kb, align="center", bold=True)
        kc = easeb((u - lt(4) - 1.6) / 0.5)
        text(ctx, "FUERZA Y MÚSCULO: IGUAL", 540, 1030, F_BIG, 64, GR, kc, align="center")
    elif i == 5:
        for j, (lab, col, cx) in enumerate([("SÍ", SS, 330), ("NO", TR, 750)]):
            kj = easeb((u - 0.3 - j * 0.4) / 0.5)
            if kj <= 0: continue
            rrect(ctx, cx - 175, 560, 350, 320, 34); ctx.set_source_rgba(*col, 0.10 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(5); ctx.stroke()
            text(ctx, lab, cx, 790, F_BIG, 150, col, kj, align="center")
        cur = "▌" if int(t * 2.5) % 2 == 0 else " "
        text(ctx, "COMENTA: SÍ O NO" + cur, 540, 990, F_MONO, 34, AM, ease((u - 1.0) / 0.4), align="center", bold=True)
    elif i == 6:
        rows = [("SE SIENTEN MÁS DURAS", 0.3), ("PUEDEN PEDIR MÁS RECUPERACIÓN", lt(6) + 1.6)]
        for j, (lab, t0) in enumerate(rows):
            kj = easeb((u - t0) / 0.5)
            if kj <= 0: continue
            y = 620 + j * 200
            rrect(ctx, 170, y, 740, 140, 30); ctx.set_source_rgba(*CO, 0.10 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*CO, kj); ctx.set_line_width(4); ctx.stroke()
            text(ctx, "!", 235, y + 95, F_BIG, 80, CO, kj, align="center")
            sz = fit_size(ctx, lab, F_BIG, 50, 600)
            text(ctx, lab, 290, y + 88, F_BIG, sz, WH, kj)
    elif i == 7:
        kl = easeb((u - 0.3) / 0.5); kr = easeb((u - lt(7) - 3.0) / 0.5)
        if kl > 0:
            rrect(ctx, 150, 540, 380, 470, 30); ctx.set_source_rgba(*GR, 0.08 * kl); ctx.fill_preserve(); ctx.set_source_rgba(*GR, kl); ctx.set_line_width(4); ctx.stroke()
            text(ctx, "MEJOR", 340, 610, F_BIG, 56, GR, kl, align="center")
            text(ctx, "PECHO", 340, 720, F_BIG, 58, WH, kl, align="center")
            text(ctx, "+", 340, 790, F_BIG, 50, GR, kl, align="center")
            text(ctx, "ESPALDA", 340, 860, F_BIG, 58, WH, kl, align="center")
            text(ctx, "MÚSCULOS OPUESTOS", 340, 950, F_MONO, 22, GR, kl, align="center", bold=True)
        if kr > 0:
            rrect(ctx, 550, 540, 380, 470, 30); ctx.set_source_rgba(*CO, 0.08 * kr); ctx.fill_preserve(); ctx.set_source_rgba(*CO, kr); ctx.set_line_width(4); ctx.stroke()
            text(ctx, "OJO", 740, 610, F_BIG, 56, CO, kr, align="center")
            text(ctx, "MISMO", 740, 720, F_BIG, 58, WH, kr, align="center")
            text(ctx, "MÚSCULO", 740, 790, F_BIG, 58, WH, kr, align="center")
            text(ctx, "MENOS PESO", 740, 880, F_MONO, 26, CO, kr, align="center", bold=True)
            text(ctx, "TOTAL", 740, 920, F_MONO, 26, CO, kr, align="center", bold=True)
    elif i == 8:
        stopwatch(ctx, 540, 720, 150, k, t, (t * 0.35) % 1)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1010); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, AM, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "COMPARACIÓN · RUTINA EFICIENTE", W / 2, 214, CY, k, 26)
        title(ctx, "¿POCO TIEMPO PARA ENTRENAR?", WH, 380, 88, k)
    elif i == 1:
        pill(ctx, "QUÉ ES", W / 2, 214, SS, k, 30, filled=True)
        title(ctx, "LA SUPERSERIE", WH, 380, 100, k)
    elif i == 2:
        pill(ctx, "METAANÁLISIS", W / 2, 214, CY, k, 30, filled=True)
        title(ctx, "SUPERSERIE VS. SERIES DE SIEMPRE", WH, 380, 80, k)
        src(ctx, "Zhang et al., Sports Medicine 2025 · 19 estudios, 313 personas", k, 1110)
    elif i == 3:
        pill(ctx, "EN CADA SESIÓN", W / 2, 214, SS, k, 30, filled=True)
        title(ctx, "MÁS CORTA, MISMO TRABAJO", WH, 380, 90, k)
        src(ctx, "Zhang et al., 2025 · doi:10.1007/s40279-025-02176-8", k, 1125)
    elif i == 4:
        pill(ctx, "CON LAS SEMANAS", W / 2, 214, GR, k, 30, filled=True)
        title(ctx, "EL RESULTADO", WH, 380, 100, k)
        src(ctx, "Zhang et al., 2025 · fuerza máxima, resistencia e hipertrofia sin diferencias", k, 1110)
    elif i == 5:
        pill(ctx, "COMENTA", W / 2, 214, AM, k, 32, filled=True)
        title(ctx, "¿HACES SUPERSERIES?", WH, 380, 94, k)
    elif i == 6:
        pill(ctx, "LA LETRA CHICA", W / 2, 214, CO, k, 30, filled=True)
        title(ctx, "NO ES GRATIS", WH, 380, 100, k)
        src(ctx, "Zhang et al., 2025 · más esfuerzo percibido, lactato y gasto de energía", k, 1110)
    elif i == 7:
        pill(ctx, "CÓMO ARMARLAS", W / 2, 214, GR, k, 30, filled=True)
        title(ctx, "ELIGE BIEN LA PAREJA", WH, 380, 96, k)
        src(ctx, "Zhang et al., 2025 · análisis por tipo de superserie", k, 1110)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 380, 80, k)


run_episode(neon, txt, "EXPEDIENTE 53 · RUTINA EFICIENTE")
