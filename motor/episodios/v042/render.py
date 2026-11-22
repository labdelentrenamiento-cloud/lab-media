"""v042 · ¿Cuántas series por semana para que un músculo crezca? (ESTUDIO EXPLICADO, serie MÚSCULO ·
paleta azul noche clásica (estilo Huesos) + cian + verde + ámbar)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext
from engine_ext import *

TE = (0.30, 0.90, 1.0)


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


def hyp(x):   # curva ilustrativa: sube siempre, rendimientos decrecientes
    return 0.92 * (1 - math.exp(-2.2 * x)) / (1 - math.exp(-2.2)) * 0.95


def stren(x):  # la fuerza se aplana antes
    return 0.80 * (1 - math.exp(-5.5 * x)) / (1 - math.exp(-5.5))


def tally(ctx, cx, cy, n, col, a):
    """marcas de conteo de series (grupos de 5)"""
    if a <= 0: return
    w = 16; g = 30
    groups = (n + 4) // 5
    total_w = groups * (5 * w + g) - g
    x = cx - total_w / 2
    for gi in range(groups):
        m = min(5, n - gi * 5)
        for j in range(min(m, 4)):
            ctx.move_to(x + j * w + 6, cy - 50); ctx.line_to(x + j * w + 6, cy + 50)
        ctx.set_source_rgba(*col, a); ctx.set_line_width(6); ctx.stroke()
        if m == 5:
            ctx.move_to(x - 6, cy + 40); ctx.line_to(x + 4 * w + 10, cy - 40); ctx.set_source_rgba(*AM, a); ctx.set_line_width(6); ctx.stroke()
        x += 5 * w + g


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        act = 0.5 + 0.5 * math.sin(t * 1.6)
        fiber_bundle(ctx, 240, 520, 600, 300, 6, act, t, k, GR, CY)
        n = int(clamp((u - 0.4) / 4.0) * 15)
        tally(ctx, 540, 960, max(1, n), CY, k)
        kn = easeb((u - lt(0) - 4.4) / 0.5)
        if kn > 0:
            ctx.save(); ctx.translate(540, 1120); ctx.scale(kn, kn)
            text(ctx, "67 ESTUDIOS", 0, 0, F_BIG, 80, AM, 1, align="center"); ctx.restore()
    elif i == 1:
        badge(ctx, 360, 700, "67", "ESTUDIOS", AM, ease((u - 0.1) / 0.4))
        badge(ctx, 720, 700, "2.058", "PERSONAS", CY, ease((u - 1.4) / 0.4))
        kd = ease((u - lt(1) - 3.4) / 0.5)
        if kd > 0:
            rrect(ctx, 300, 960, 480, 90, 45); ctx.set_source_rgba(*GR, 0.12 * kd); ctx.fill_preserve(); ctx.set_source_rgba(*GR, kd); ctx.set_line_width(4); ctx.stroke()
            text(ctx, "¿LA DOSIS?", 540, 1020, F_BIG, 56, GR, kd, align="center")
    elif i == 2:
        up = ease((u - 0.3) / 2.6)
        line_chart(ctx, 190, 560, 700, 440, [(hyp, GR, up, True)], [(0, "0"), (0.5, "MÁS"), (1, "MUCHAS")], "SERIES POR SEMANA", "MÚSCULO", k)
    elif i == 3:
        line_chart(ctx, 190, 560, 700, 440, [(hyp, GR, 1.0, True)], [(0, "0"), (0.5, "MÁS"), (1, "MUCHAS")], "SERIES POR SEMANA", "MÚSCULO", k)
        # escalones: cuánto suma cada bloque extra de series
        for j in range(5):
            kj = ease((u - 0.5 - j * 0.45) / 0.4)
            if kj <= 0: continue
            x0 = j / 5; x1 = (j + 1) / 5
            px0 = 190 + x0 * 700; px1 = 190 + x1 * 700
            y0 = 560 + 440 - hyp(x0) * 440; y1 = 560 + 440 - hyp(x1) * 440
            ctx.move_to(px0, y0); ctx.line_to(px1, y0); ctx.line_to(px1, y1)
            ctx.set_source_rgba(*AM, kj); ctx.set_line_width(4); ctx.stroke()
            text(ctx, "+", px1 + 18, (y0 + y1) / 2 + 10, F_MONO, 26, AM, kj, bold=True)
    elif i == 4:
        line_chart(ctx, 190, 560, 700, 440, [(hyp, GR, 1.0, False), (stren, AM, ease((u - 0.6) / 2.0), False)],
                   [(0, "0"), (0.5, "MÁS"), (1, "MUCHAS")], "SERIES POR SEMANA", "", k)
        for (lx, lab, col, ka) in ((300, "MÚSCULO", GR, k), (620, "FUERZA", AM, ease((u - 0.6) / 0.5))):
            ctx.move_to(lx - 70, 515); ctx.line_to(lx - 20, 515); ctx.set_source_rgba(*col, ka); ctx.set_line_width(6); ctx.stroke()
            text(ctx, lab, lx, 524, F_MONO, 26, col, ka, bold=True)
    elif i == 5:
        kc = ease((u - 0.2) / 0.4)
        rrect(ctx, 260, 620, 560, 260, 36); ctx.set_source_rgba(*CY, 0.08 * kc); ctx.fill_preserve(); ctx.set_source_rgba(*CY, kc); ctx.set_line_width(5); ctx.stroke()
        n = int(4 + (t * 3) % 16)
        cur = "▌" if int(t * 2.5) % 2 == 0 else " "
        text(ctx, "%d%s" % (n, cur), 540, 800, F_BIG, 150, AM, kc, align="center")
        text(ctx, "SERIES DE PIERNAS / SEMANA", 540, 960, F_MONO, 28, WH, kc, align="center", bold=True)
        text(ctx, "COMENTA TU NÚMERO", 540, 1040, F_MONO, 32, AM, ease((u - 1.0) / 0.4), align="center", bold=True)
    elif i == 6:
        kb = ease((u - 0.2) / 0.5)
        rrect(ctx, 290, 520, 500, 110, 30); ctx.set_source_rgba(*WH, 0.06 * kb); ctx.fill_preserve(); ctx.set_source_rgba(*WH, 0.9 * kb); ctx.set_line_width(4); ctx.stroke()
        text(ctx, "1 SERIE DE PRESS DE BANCA", 540, 588, F_MONO, 28, WH, kb, align="center", bold=True)
        k1 = ease((u - lt(6) - 3.0) / 0.5)
        k2 = ease((u - lt(6) - 3.8) / 0.5)
        for (cx, kk) in ((340, k1), (740, k2)):
            if kk > 0:
                ctx.move_to(540, 640); ctx.line_to(cx, 720); ctx.set_source_rgba(*CY, 0.7 * kk); ctx.set_line_width(3); ctx.stroke()
        badge(ctx, 340, 870, "1", "PECHO\n(DIRECTA)", GR, k1, w=300)
        badge(ctx, 740, 870, "½", "TRÍCEPS\n(INDIRECTA)", AM, k2, w=300)
    elif i == 7:
        for j, (yr, col) in enumerate([("2017", CY), ("2026", GR)]):
            kj = easeb((u - lt(7) - 0.4 - j * 0.9) / 0.5)
            if kj <= 0: continue
            cx = 340 + j * 400
            rrect(ctx, cx - 150, 560, 300, 200, 28); ctx.set_source_rgba(*col, 0.10 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(4); ctx.stroke()
            text(ctx, yr, cx, 690, F_BIG, 100, col, kj, align="center")
        kk = ease((u - lt(7) - 2.6) / 1.4)
        vbars(ctx, [("POCAS", 0.35, CY), ("MEDIAS", 0.60, CY), ("MÁS", 0.85, GR)], 250, 1080, 160, 60, 240, kk, 1.0, 24)
    elif i == 8:
        act = 0.5 + 0.5 * math.sin(t * 2.0)
        fiber_bundle(ctx, 290, 520, 500, 250, 5, act, t, k, GR, CY)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1010); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, AM, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "ESTUDIO EXPLICADO · MÚSCULO", W / 2, 196, CY, k, 28)
        title(ctx, "¿CUÁNTAS SERIES PARA CRECER?", WH, 368, 90, k)
    elif i == 1:
        pill(ctx, "METAANÁLISIS · 2026", W / 2, 196, AM, k, 28, filled=True)
        title(ctx, "LA DOSIS DEL MÚSCULO", WH, 368, 100, k)
        src(ctx, "Pelland et al., Sports Med 2026 · doi:10.1007/s40279-025-02344-w", k, 1150)
    elif i == 2:
        pill(ctx, "HALLAZGO 1", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "MÁS SERIES, MÁS MÚSCULO", WH, 368, 96, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1130, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Pelland et al., 2026 · la curva sube en todo el rango estudiado", k, 1170)
    elif i == 3:
        pill(ctx, "HALLAZGO 2", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "CADA SERIE SUMA MENOS", WH, 368, 98, k)
        text(ctx, "ESQUEMA ILUSTRATIVO · RENDIMIENTOS DECRECIENTES", W / 2, 1130, F_MONO, 22, AM, k, align="center", bold=True)
    elif i == 4:
        pill(ctx, "HALLAZGO 3", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "LA FUERZA SE FRENA ANTES", WH, 368, 96, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1130, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Pelland et al., 2026 · fuerza: rendimientos decrecientes más marcados", k, 1170)
    elif i == 5:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿CUÁNTAS SERIES LE HACES A TUS PIERNAS?", WH, 368, 80, k)
    elif i == 6:
        pill(ctx, "DETALLE CLAVE", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "LAS INDIRECTAS CUENTAN A MEDIAS", WH, 368, 86, k)
        src(ctx, "Pelland et al., 2026 · método 'fraccional': serie indirecta = 0,5", k, 1170)
    elif i == 7:
        pill(ctx, "DOS METAANÁLISIS", W / 2, 196, GR, k, 28, filled=True)
        title(ctx, "MISMA CONCLUSIÓN", WH, 368, 100, k)
        src(ctx, "Schoenfeld et al., J Sports Sci 2017 · doi:10.1080/02640414.2016.1210197", k, 1210)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 42 · MÚSCULO")
