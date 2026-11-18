"""v033 · ¿Qué les pasa a tus rodillas si corres durante años? (formato "qué pasa si…", serie ARTICULACIONES ·
paleta azul petróleo + verde + coral)
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


engine.BG = engine_ext.BG = _bg([0.03, 0.12, 0.14], [0.006, 0.025, 0.035])
from engine_ext import *
CO = (1.0, 0.45, 0.40)    # coral


def title(ctx, s, color=WH, y=345, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1270):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def badge(ctx, cx, cy, num, unit, col, a, w=300):
    if a <= 0: return
    rrect(ctx, cx - w / 2, cy - 150, w, 290, 26); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    big(ctx, num, cx, cy + 30, 130, col, a, maxw=w - 40)
    for li, part in enumerate(unit.split("\n")):
        text(ctx, part, cx, cy + 85 + li * 32, F_MONO, 24, WH, a, align="center", bold=True)


def knee(ctx, cx, cy, s, cart_col, a, wear=0.0, t=0.0, bend=0.0):
    """rodilla esquemática: fémur arriba, tibia abajo, cartílago en medio (wear = zonas alteradas)"""
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    # fémur
    ctx.save(); ctx.rotate(-bend)
    ctx.move_to(-55, -330); ctx.line_to(-60, -90)
    ctx.curve_to(-120, -60, -125, 30, -60, 40); ctx.curve_to(-20, 50, 20, 50, 60, 40)
    ctx.curve_to(125, 30, 120, -60, 60, -90); ctx.line_to(55, -330)
    ctx.set_source_rgba(*CY, 0.08 * a); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.95 * a); ctx.set_line_width(5); ctx.stroke()
    # cartílago femoral
    ctx.new_path(); ctx.move_to(-110, 0); ctx.curve_to(-100, 45, -30, 52, 0, 50); ctx.curve_to(30, 52, 100, 45, 110, 0)
    ctx.set_source_rgba(*cart_col, a); ctx.set_line_width(12); ctx.stroke()
    ctx.restore()
    # tibia
    ctx.move_to(-115, 75); ctx.line_to(115, 75); ctx.curve_to(120, 120, 80, 140, 55, 150); ctx.line_to(48, 380)
    ctx.line_to(-48, 380); ctx.line_to(-55, 150); ctx.curve_to(-80, 140, -120, 120, -115, 75)
    ctx.set_source_rgba(*CY, 0.08 * a); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.95 * a); ctx.set_line_width(5); ctx.stroke()
    ctx.move_to(-110, 68); ctx.line_to(110, 68); ctx.set_source_rgba(*cart_col, a); ctx.set_line_width(12); ctx.stroke()
    if wear > 0:
        for j, x in enumerate((-70, -20, 45)):
            p = 0.6 + 0.4 * math.sin(t * 5 + j)
            ctx.new_path(); ctx.arc(x, 66, 13 * wear, 0, 6.283); ctx.set_source_rgba(*RD, 0.9 * a * p); ctx.fill()
    ctx.restore()


def bar3(ctx, items, k, a):
    """barras con cifra arriba"""
    x0, base, bw, gap, maxh = 190, 1080, 190, 60, 470
    for j, (lab, v, col, num, k0) in enumerate(items):
        kk = ease((k - k0) / 0.6)
        if kk <= 0: continue
        x = x0 + j * (bw + gap); hgt = maxh * v / 14.0 * kk
        rrect(ctx, x, base - hgt, bw, hgt, 14); ctx.set_source_rgba(*col, 0.22 * a); ctx.fill_preserve()
        ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(3); ctx.stroke()
        big(ctx, num, x + bw / 2, base - hgt - 22, 76, col, a * kk, maxw=bw + 40)
        for li, part in enumerate(lab.split("\n")):
            text(ctx, part, x + bw / 2, base + 42 + li * 30, F_MONO, 24, col, a * kk, align="center", bold=True)


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        skeleton(ctx, 540, 415, 0.70, t, hl={"legs": (CO, 1.0)})
        kq = easeb((u - 1.2) / 0.5)
        if kq > 0:
            for sx in (-1, 1):
                ctx.new_path(); ctx.arc(540 + sx * 43, 415 + 0.70 * 804, 46 * kq, 0, 6.283)
                ctx.set_source_rgba(*CO, 0.9 * kq); ctx.set_line_width(5); ctx.stroke()
        footprints(ctx, 150, 930, 1190, t, 1.6, a=0.7 * k, col=GR)
    elif i == 1:
        badge(ctx, 330, 790, "17", "ESTUDIOS", CY, ease((u - 0.1) / 0.4), w=300)
        badge(ctx, 750, 790, "114.829", "PERSONAS", GR, ease((u - 1.4) / 0.4), w=360)
    elif i == 2:
        bar3(ctx, [("NO\nCORRÍAN", 10.2, AM, "10 %", 0.3)], u, k)
    elif i == 3:
        bar3(ctx, [("NO\nCORRÍAN", 10.2, AM, "10 %", -1), ("RECREA-\nTIVOS", 3.5, GR, "3,5 %", 0.1), ("ÉLITE", 13.3, CO, "13 %", lt(3) + 2.0)], u, 1)
    elif i == 4:
        for j, (lab, col, x) in enumerate((("SÍ", GR, 330), ("NO", CO, 750))):
            kk = easeb((u - 0.2 - j * 0.25) / 0.5)
            if kk <= 0: continue
            ctx.save(); ctx.translate(x, 800); ctx.scale(kk, kk)
            ctx.new_path(); ctx.arc(0, 0, 150, 0, 6.283); ctx.set_source_rgba(*col, 0.14); ctx.fill_preserve(); ctx.set_source_rgba(*col, 1); ctx.set_line_width(6); ctx.stroke()
            text(ctx, lab, 0, 55, F_BIG, 150, col, 1, align="center"); ctx.restore()
    elif i == 5:
        for j, (lab, col, x) in enumerate((("CORRER", GR, 290), ("ARTROSIS", CO, 790))):
            kk = ease((u - 0.1 - j * 0.3) / 0.4)
            ctx.new_path(); ctx.arc(x, 760, 130, 0, 6.283); ctx.set_source_rgba(*col, 0.12 * kk); ctx.fill_preserve(); ctx.set_source_rgba(*col, kk); ctx.set_line_width(5); ctx.stroke()
            text(ctx, lab, x, 772, F_MONO, 30, col, kk, align="center", bold=True)
        kd = ease((u - 0.9) / 0.6)
        ctx.set_dash([18, 14]); ctx.move_to(430, 760); ctx.line_to(430 + 220 * kd, 760); ctx.set_source_rgba(*WH, 0.8 * kd); ctx.set_line_width(4); ctx.stroke(); ctx.set_dash([])
        kx = easeb((u - 1.6) / 0.5)
        if kx > 0: big(ctx, "≠", 540, 790, 120 * kx, AM, kx, maxw=160)
        kl = ease((u - lt(5) - 3.2) / 0.5)
        if kl > 0:
            ctx.new_path(); ctx.arc(540, 1000, 60, 0, 6.283); ctx.set_source_rgba(*AM, 0.15 * kl); ctx.fill_preserve(); ctx.set_source_rgba(*AM, kl); ctx.set_line_width(4); ctx.stroke()
            text(ctx, "+", 540, 1022, F_BIG, 70, AM, kl, align="center")
    elif i == 6:
        knee(ctx, 310, 760, 0.85, GR, k, bend=0.12 * math.sin(t * 3))
        knee(ctx, 770, 760, 0.85, CY, ease((u - 0.3) / 0.4))
        ke = easeb((u - lt(6) - 3.0) / 0.5)
        if ke > 0: big(ctx, "=", 540, 800, 150 * ke, GR, ke, maxw=200)
    elif i == 7:
        knee(ctx, 250, 790, 0.62, GR, k)
        knee(ctx, 540, 790, 0.62, CY, ease((u - 0.2) / 0.4))
        knee(ctx, 830, 790, 0.62, CO, ease((u - 0.5) / 0.4), wear=ease((u - 1.2) / 0.6), t=t)
        for lab, col, x, t0 in (("CORREN", GR, 250, 0), ("NO CORREN", CY, 540, 0.2), ("OBESIDAD", CO, 830, 0.5)):
            text(ctx, lab, x, 1080, F_MONO, 26, col, ease((u - t0) / 0.4), align="center", bold=True)
    elif i == 8:
        footprints(ctx, 150, 930, 620, t, 1.6, a=0.8 * k, col=GR)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 900); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 150, GR, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "QUÉ PASA SI… · ARTICULACIONES", W / 2, 196, GR, k, 28)
        title(ctx, "¿CORRER DESGASTA TUS RODILLAS?", WH, 368, 92, k)
    elif i == 1:
        pill(ctx, "METAANÁLISIS · 2017", W / 2, 196, GR, k, 28, filled=True)
        title(ctx, "MÁS DE 100.000 PERSONAS", WH, 368, 96, k)
        src(ctx, "Alentorn-Geli et al., J Orthop Sports Phys Ther 2017 · doi:10.2519/jospt.2017.7137", k, 1080)
    elif i in (2, 3):
        pill(ctx, "ARTROSIS DE CADERA O RODILLA", W / 2, 196, AM, k if i == 2 else 1, 28, filled=True)
        title(ctx, "¿QUIÉN TIENE MÁS?" if i == 2 else "LOS RECREATIVOS, MENOS", WH, 368, 100, k)
        src(ctx, "Prevalencia · Alentorn-Geli et al., 2017", k if i == 2 else 1, 1225)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿TÚ CORRES?", WH, 368, 120, k)
        text(ctx, "ESCRIBE SÍ O NO", W / 2, 1110, F_MONO, 34, AM, ease((u - 0.8) / 0.4), align="center", bold=True)
    elif i == 5:
        pill(ctx, "OJO", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "ASOCIACIÓN NO ES CAUSA", WH, 368, 96, k)
        text(ctx, "LESIONES PREVIAS", W / 2, 1125, F_MONO, 28, AM, ease((u - lt(5) - 3.4) / 0.5), align="center", bold=True)
    elif i == 6:
        pill(ctx, "RESONANCIA · 2026", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "MISMO CARTÍLAGO", WH, 368, 110, k)
        text(ctx, "CORREDORES", 310, 1180, F_MONO, 26, GR, k, align="center", bold=True)
        text(ctx, "NO CORREN", 770, 1180, F_MONO, 26, CY, k, align="center", bold=True)
        src(ctx, "Slovák et al., Med Sci Sports Exerc 2026 · 183 adultos · doi:10.1249/MSS.0000000000004118", k, 1235)
    elif i == 7:
        pill(ctx, "LO QUE SÍ SE ASOCIÓ", W / 2, 196, CO, k, 30, filled=True)
        title(ctx, "MÁS DAÑO: OBESIDAD", WH, 368, 104, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1150, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Slovák et al., 2026 · IMC ≥ 30", k, 1195)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 33 · ARTICULACIONES")
