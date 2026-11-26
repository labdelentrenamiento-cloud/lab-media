"""v052 · ¿Duermes poco y estás a dieta? (QUÉ PASA SI…, serie SUEÑO ·
paleta índigo noche + lavanda + ámbar)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (0.70, 0.62, 1.0)   # lavanda


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.40) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.06, 0.04, 0.16], [0.01, 0.008, 0.04])
from engine_ext import *
CY = ACC
FAT = AM          # grasa = ámbar
LEAN = (0.24, 0.94, 1.0)   # masa libre de grasa = cian


def title(ctx, s, color=WH, y=380, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1110):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def moon(ctx, cx, cy, r, a, t, col=ACC):
    if a <= 0: return
    ctx.save()
    ix, iy, ir = cx + r * 0.45, cy - r * 0.25, r * 0.85
    ctx.push_group()
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283)
    ctx.set_source_rgba(*col, 0.25 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    ctx.new_path(); ctx.arc(ix, iy, ir + 2.5, 0, 6.283); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.save(); ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.clip()
    ctx.new_path(); ctx.arc(ix, iy, ir, 0, 6.283); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()
    ctx.pop_group_to_source(); ctx.paint()
    for j in range(5):
        ph = (t * 0.4 + j * 0.2) % 1
        sx = cx - r * 1.6 + j * r * 0.8; sy = cy - r * 1.3 + math.sin(j * 2.1) * r * 0.5
        ctx.new_path(); ctx.arc(sx, sy, 4 + 3 * math.sin(t * 3 + j), 0, 6.283)
        ctx.set_source_rgba(*WH, a * (0.4 + 0.5 * abs(math.sin(t * 2 + j)))); ctx.fill()
    ctx.restore()


def bed(ctx, cx, cy, s, a, col=ACC):
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.set_line_width(6); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(-170, -110); ctx.line_to(-170, 60); ctx.move_to(-170, 10); ctx.line_to(170, 10); ctx.line_to(170, 60)
    ctx.set_source_rgba(*col, a); ctx.stroke()
    rrect(ctx, -150, -45, 90, 50, 18); ctx.set_source_rgba(*col, 0.25 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.stroke()
    rrect(ctx, -50, -55, 215, 62, 22); ctx.set_source_rgba(*col, 0.15 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.stroke()
    ctx.restore()


def zzz(ctx, x, y, t, a, col=WH):
    for j in range(3):
        ph = (t * 0.6 + j / 3) % 1
        text(ctx, "Z", x + j * 30 + ph * 30, y - ph * 120, F_BIG, 36 + j * 10, col, a * (1 - ph), align="center")


def plate(ctx, cx, cy, s, a, col=GR):
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 95, 0, 6.283); ctx.set_source_rgba(*col, 0.12 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    ctx.new_path(); ctx.arc(0, 0, 62, 0, 6.283); ctx.set_source_rgba(*col, 0.6 * a); ctx.set_line_width(3); ctx.stroke()
    text(ctx, "DIETA", 0, 10, F_MONO, 26, WH, a, align="center", bold=True)
    ctx.restore()


def hours(ctx, cx, cy, label, col, a, frac, t):
    if a <= 0: return
    r = 120
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*col, 0.25 * a); ctx.set_line_width(14); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, r, -math.pi / 2, -math.pi / 2 + 6.283 * frac); ctx.set_source_rgba(*col, a); ctx.set_line_width(14); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    text(ctx, label, cx, cy + 22, F_BIG, 70, WH, a, align="center")
    text(ctx, "HORAS", cx, cy + 62, F_MONO, 22, col, a, align="center", bold=True)


def body_comp(ctx, cx, top, h, fat_kg, lean_kg, a, k, lab):
    """columna de peso perdido: grasa (ámbar) + masa libre de grasa (cian)"""
    if a <= 0: return
    sc = h / 3.2
    hf = fat_kg * sc * k; hl = lean_kg * sc * k
    base = top + h
    rrect(ctx, cx - 90, base - hl, 180, max(hl, 1), 10); ctx.set_source_rgba(*LEAN, 0.30 * a); ctx.fill_preserve(); ctx.set_source_rgba(*LEAN, a); ctx.set_line_width(4); ctx.stroke()
    rrect(ctx, cx - 90, base - hl - hf - 8, 180, max(hf, 1), 10); ctx.set_source_rgba(*FAT, 0.30 * a); ctx.fill_preserve(); ctx.set_source_rgba(*FAT, a); ctx.stroke()
    text(ctx, lab, cx, base + 50, F_BIG, 46, WH, a, align="center")


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        plate(ctx, 330, 800, 1.1, k)
        kb = easeb((u - 0.8) / 0.5)
        moon(ctx, 760, 760, 95, kb, t)
        zzz(ctx, 840, 700, t, kb)
        kq = easeb((u - lt(0) - 1.7) / 0.5)
        if kq > 0:
            ctx.save(); ctx.translate(540, 1030); ctx.scale(kq, kq)
            text(ctx, "¿DUERMES POCO?", 0, 0, F_BIG, 80, AM, 1, align="center"); ctx.restore()
    elif i == 1:
        ka = easeb((u - 0.3) / 0.5); kb = easeb((u - lt(1) - 2.6) / 0.5)
        hours(ctx, 320, 760, "8,5", GR, ka, ease((u - 0.3) / 1.2) * 8.5 / 12, t)
        hours(ctx, 760, 760, "5,5", RD, kb, ease((u - lt(1) - 2.6) / 1.2) * 5.5 / 12, t)
        text(ctx, "VS", 540, 785, F_BIG, 60, WH, min(ka, kb), align="center")
        text(ctx, "MISMA DIETA · 14 DÍAS", 540, 1000, F_MONO, 30, ACC, ease((u - 3.2) / 0.5), align="center", bold=True)
    elif i == 2:
        kk = ease((u - 0.3) / 1.4)
        body_comp(ctx, 330, 560, 380, 1.4, 1.5, k, kk, "8,5 H")
        body_comp(ctx, 750, 560, 380, 0.6, 2.4, k, kk, "5,5 H")
        kd = easeb((u - lt(2) - 3.0) / 0.5)
        if kd > 0:
            ctx.save(); ctx.translate(750, 520); ctx.scale(kd, kd)
            text(ctx, "−55 % GRASA", 0, 0, F_BIG, 64, FAT, 1, align="center"); ctx.restore()
        rrect(ctx, 260, 1050, 26, 26, 6); ctx.set_source_rgba(*FAT, k); ctx.fill()
        text(ctx, "GRASA", 300, 1072, F_MONO, 24, WH, k, bold=True)
        rrect(ctx, 520, 1050, 26, 26, 6); ctx.set_source_rgba(*LEAN, k); ctx.fill()
        text(ctx, "MASA LIBRE DE GRASA", 560, 1072, F_MONO, 24, WH, k, bold=True)
    elif i == 3:
        body_comp(ctx, 330, 560, 380, 1.4, 1.5, 0.45, 1, "8,5 H")
        body_comp(ctx, 750, 560, 380, 0.6, 2.4, 1, 1, "5,5 H")
        pulse = 0.6 + 0.4 * math.sin(t * 6)
        hl = 2.4 * 380 / 3.2
        rrect(ctx, 650, 940 - hl - 10, 200, hl + 20, 16); ctx.set_source_rgba(*LEAN, pulse * k); ctx.set_line_width(5); ctx.stroke()
        kd = easeb((u - lt(3) - 1.8) / 0.5)
        if kd > 0:
            ctx.save(); ctx.translate(540, 520); ctx.scale(kd, kd)
            text(ctx, "+60 % MASA LIBRE DE GRASA", 0, 0, F_BIG, 58, LEAN, 1, align="center"); ctx.restore()
    elif i == 4:
        for j, (lab, col) in enumerate([("5", RD), ("6", AM), ("7", GR), ("8", GR), ("9+", ACC)]):
            kj = easeb((u - 0.3 - j * 0.18) / 0.45)
            if kj <= 0: continue
            cx = 220 + j * 160
            rrect(ctx, cx - 65, 600, 130, 220, 26); ctx.set_source_rgba(*col, 0.10 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(4); ctx.stroke()
            text(ctx, lab, cx, 750, F_BIG, 96, col, kj, align="center")
        cur = "▌" if int(t * 2.5) % 2 == 0 else " "
        text(ctx, "COMENTA TUS HORAS" + cur, 540, 940, F_MONO, 36, AM, ease((u - 1.0) / 0.4), align="center", bold=True)
    elif i == 5:
        days = ["L", "M", "M", "J", "V", "S", "D"]
        for j, dd in enumerate(days):
            kj = easeb((u - 0.3 - j * 0.15) / 0.4)
            if kj <= 0: continue
            short = j < 5
            col = RD if short else GR
            cx = 190 + j * 117
            hh = 230 if short else 290
            rrect(ctx, cx - 42, 900 - hh, 84, hh, 14); ctx.set_source_rgba(*col, 0.18 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(4); ctx.stroke()
            text(ctx, dd, cx, 950, F_BIG, 44, WH, kj, align="center")
        kb = easeb((u - lt(5) - 2.0) / 0.5)
        text(ctx, "−1 HORA DE SUEÑO", 540, 1040, F_BIG, 60, RD, kb, align="center")
        moon(ctx, 540, 520, 50, k, t)
    elif i == 6:
        for j, (lab, y) in enumerate([("ESTUDIO 1 · 10 PERSONAS", 620), ("ESTUDIO 2 · 36 PERSONAS", 800)]):
            kj = easeb((u - 0.3 - j * 0.6) / 0.5)
            if kj <= 0: continue
            rrect(ctx, 200, y, 680, 130, 30); ctx.set_source_rgba(*ACC, 0.10 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*ACC, kj); ctx.set_line_width(4); ctx.stroke()
            text(ctx, lab, 540, y + 80, F_MONO, 32, WH, kj, align="center", bold=True)
        ka = easeb((u - 2.0) / 0.5)
        if ka > 0:
            ctx.move_to(540, 950); ctx.line_to(540, 1030); ctx.move_to(510, 1000); ctx.line_to(540, 1032); ctx.line_to(570, 1000)
            ctx.set_source_rgba(*AM, ka); ctx.set_line_width(7); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    elif i == 7:
        plate(ctx, 330, 780, 1.1, k)
        text(ctx, "+", 540, 810, F_BIG, 100, WH, k, align="center")
        kb = easeb((u - 0.8) / 0.5)
        bed(ctx, 760, 800, 0.85, kb)
        zzz(ctx, 840, 700, t, kb)
        kq = easeb((u - lt(7) - 2.0) / 0.5)
        text(ctx, "SUEÑO = PARTE DE LA DIETA", 540, 1020, F_BIG, 62, GR, kq, align="center")
    elif i == 8:
        moon(ctx, 540, 700, 140, k, t)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1010); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, AM, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "QUÉ PASA SI… · SUEÑO", W / 2, 214, CY, k, 28)
        title(ctx, "A DIETA Y DURMIENDO POCO", WH, 380, 88, k)
    elif i == 1:
        pill(ctx, "EL ESTUDIO", W / 2, 214, CY, k, 30, filled=True)
        title(ctx, "DOS FORMAS DE DORMIR", WH, 380, 96, k)
        src(ctx, "Nedeltcheva et al., Ann Intern Med 2010 · ensayo cruzado, 10 adultos con sobrepeso", k, 1110)
    elif i == 2:
        pill(ctx, "RESULTADO 1", W / 2, 214, AM, k, 30, filled=True)
        title(ctx, "MENOS GRASA PERDIDA", WH, 380, 96, k)
        src(ctx, "Nedeltcheva et al., 2010 · grasa perdida: 1,4 kg (8,5 h) vs. 0,6 kg (5,5 h)", k, 1140)
    elif i == 3:
        pill(ctx, "RESULTADO 2", W / 2, 214, LEAN, k, 30, filled=True)
        title(ctx, "MÁS MASA LIBRE DE GRASA PERDIDA", WH, 380, 80, k)
        src(ctx, "Nedeltcheva et al., 2010 · 1,5 kg vs. 2,4 kg · doi:10.7326/0003-4819-153-7-201010050-00006", k, 1110)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 214, AM, k, 32, filled=True)
        title(ctx, "¿CUÁNTAS HORAS DUERMES?", WH, 380, 90, k)
    elif i == 5:
        pill(ctx, "OTRO ENSAYO · 8 SEMANAS", W / 2, 214, CY, k, 28, filled=True)
        title(ctx, "SOLO 1 HORA MENOS", WH, 380, 96, k)
        src(ctx, "Wang et al., Sleep 2018 · menos proporción de grasa perdida · doi:10.1093/sleep/zsy027", k, 1110)
    elif i == 6:
        pill(ctx, "OJO", W / 2, 214, AM, k, 32, filled=True)
        title(ctx, "ESTUDIOS PEQUEÑOS, MISMA SEÑAL", WH, 380, 84, k)
    elif i == 7:
        pill(ctx, "CONCLUSIÓN", W / 2, 214, GR, k, 30, filled=True)
        title(ctx, "PIERDE GRASA, NO MÚSCULO", WH, 380, 92, k)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 380, 80, k)


run_episode(neon, txt, "EXPEDIENTE 52 · SUEÑO")
