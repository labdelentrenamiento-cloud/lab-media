"""v048 · ¿Las pesas te dejan bajito? (MITO VS. REALIDAD, serie HUESOS ·
paleta azul noche clásica (estilo Huesos) + cian + ámbar + verde)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext
from engine_ext import *

HU = CY            # hueso = cian
CR = AM            # cartílago de crecimiento = ámbar


def title(ctx, s, color=WH, y=345, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1160):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def long_bone(ctx, cx, top, h, a, plate=0.0, t=0.0, col=HU):
    """fémur esquemático con cartílagos de crecimiento (plate 0..1 = resaltado)"""
    if a <= 0: return
    w = 46
    ctx.move_to(cx - w / 2, top + 70); ctx.line_to(cx - w / 2, top + h - 70); ctx.line_to(cx + w / 2, top + h - 70); ctx.line_to(cx + w / 2, top + 70); ctx.close_path()
    ctx.set_source_rgba(*col, 0.08 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(4); ctx.stroke()
    for yy, s in ((top + 40, -1), (top + h - 40, 1)):
        for dx in (-34, 34):
            ctx.new_path(); ctx.arc(cx + dx, yy, 40, 0, 6.283); ctx.set_source_rgba(*col, 0.08 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.95 * a); ctx.stroke()
    pulse = 0.65 + 0.35 * math.sin(t * 6)
    for yy in (top + 82, top + h - 82):
        rrect(ctx, cx - 40, yy - 7, 80, 14, 7)
        ctx.set_source_rgba(*CR, (0.25 + 0.6 * plate * pulse) * a); ctx.fill_preserve(); ctx.set_source_rgba(*CR, (0.5 + 0.5 * plate) * a); ctx.set_line_width(3); ctx.stroke()


def kid(ctx, cx, base, hgt, a, col=CY):
    """silueta simple de niño/a con altura hgt"""
    s = hgt / 300
    ctx.save(); ctx.translate(cx, base); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, -270, 30, 0, 6.283); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5 / s); ctx.stroke()
    ctx.move_to(0, -235); ctx.line_to(0, -110); ctx.move_to(0, -110); ctx.line_to(-34, 0); ctx.move_to(0, -110); ctx.line_to(34, 0)
    ctx.move_to(-55, -200); ctx.line_to(0, -215); ctx.line_to(55, -200); ctx.stroke()
    ctx.restore()


def ruler(ctx, x, top, base, a):
    ctx.move_to(x, top); ctx.line_to(x, base); ctx.set_source_rgba(*WH, 0.6 * a); ctx.set_line_width(3); ctx.stroke()
    n = 12
    for j in range(n + 1):
        y = base - (base - top) * j / n
        ctx.move_to(x, y); ctx.line_to(x + (22 if j % 3 == 0 else 12), y); ctx.stroke()


def doc(ctx, x, y, a, col):
    rrect(ctx, x, y, 58, 74, 8); ctx.set_source_rgba(*col, 0.15 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(3); ctx.stroke()
    for ln in range(3):
        ctx.move_to(x + 12, y + 20 + ln * 17); ctx.line_to(x + 46 - ln * 8, y + 20 + ln * 17); ctx.set_source_rgba(*WH, 0.5 * a); ctx.set_line_width(2.5); ctx.stroke()


def shield(ctx, cx, cy, s, a, col=GR):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.move_to(0, -110); ctx.curve_to(60, -80, 90, -85, 100, -90); ctx.curve_to(100, 20, 70, 80, 0, 120)
    ctx.curve_to(-70, 80, -100, 20, -100, -90); ctx.curve_to(-90, -85, -60, -80, 0, -110); ctx.close_path()
    ctx.set_source_rgba(*col, 0.12 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(6); ctx.stroke()
    ctx.move_to(-40, 0); ctx.line_to(-8, 34); ctx.line_to(48, -36); ctx.set_line_width(10); ctx.stroke()
    ctx.restore()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        ruler(ctx, 250, 560, 1020, k)
        kid(ctx, 420, 1020, 300, k, CY)
        barbell_kb = ease((u - 0.6) / 0.5)
        if barbell_kb > 0:
            ctx.save(); ctx.translate(720, 860); ctx.scale(0.45, 0.45); barbell_icon(ctx, 0, 0, t, barbell_kb); ctx.restore()
        kq = easeb((u - lt(0) - 1.6) / 0.5)
        if kq > 0:
            ctx.save(); ctx.translate(720, 700); ctx.scale(kq, kq)
            text(ctx, "¿BAJITO?", 0, 0, F_BIG, 90, RD, 1, align="center"); ctx.restore()
    elif i == 1:
        long_bone(ctx, 540, 520, 520, k, plate=ease((u - 0.8) / 0.6), t=t)
        kc = ease((u - 1.2) / 0.5)
        callout(ctx, 585, 602, 760, 560, "CARTÍLAGO DE", CR, kc, sub="CRECIMIENTO")
        ka = ease((u - lt(1) - 2.2) / 0.5)
        if ka > 0:
            for yy in (500, 1060):
                ctx.move_to(540, yy - 40 if yy < 600 else yy + 40); ctx.line_to(540, yy)
                ctx.set_source_rgba(*RD, ka); ctx.set_line_width(8); ctx.stroke()
            text(ctx, "¿LO APLASTA?", 300, 820, F_BIG, 56, RD, ka, align="center")
    elif i == 2:
        n = int(clamp((u - 0.2) / 1.8) * 22)
        for j in range(n):
            c = j % 8; r = j // 8
            doc(ctx, 205 + c * 85, 560 + r * 105, k, CY)
        kb = easeb((u - lt(2) - 2.4) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 1000); ctx.scale(kb, kb)
            text(ctx, "22 ESTUDIOS EN NIÑOS", 0, 0, F_BIG, 80, AM, 1, align="center"); ctx.restore()
    elif i == 3:
        ruler(ctx, 200, 520, 1020, k)
        g = ease((u - 0.3) / 2.2)
        for j, (cx, col, lab) in enumerate([(430, CY, "SIN PESAS"), (730, GR, "CON PESAS")]):
            kj = ease((u - 0.2 - j * 0.3) / 0.5)
            kid(ctx, cx, 1000, 330 + 110 * g, kj, col)
            text(ctx, lab, cx, 1050, F_MONO, 26, col, kj, align="center", bold=True)
        if g > 0.9:
            ctx.move_to(330, 1000 - 440); ctx.line_to(830, 1000 - 440); ctx.set_source_rgba(*AM, 0.8); ctx.set_dash([12, 10]); ctx.set_line_width(3); ctx.stroke(); ctx.set_dash([])
    elif i == 4:
        for j, (lab, col, cx) in enumerate([("SÍ", AM, 330), ("NO", CY, 750)]):
            kj = easeb((u - 0.3 - j * 0.4) / 0.5)
            if kj <= 0: continue
            rrect(ctx, cx - 175, 560, 350, 320, 34); ctx.set_source_rgba(*col, 0.10 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(5); ctx.stroke()
            text(ctx, lab, cx, 790, F_BIG, 150, col, kj, align="center")
        cur = "▌" if int(t * 2.5) % 2 == 0 else " "
        text(ctx, "COMENTA: SÍ O NO" + cur, 540, 990, F_MONO, 34, AM, ease((u - 1.2) / 0.4), align="center", bold=True)
    elif i == 5:
        shield(ctx, 540, 760, 1.4, k, GR)
        kb = easeb((u - lt(5) - 2.0) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 1060); ctx.scale(kb, kb)
            text(ctx, "MUY POCAS LESIONES", 0, 0, F_BIG, 80, GR, 1, align="center"); ctx.restore()
    elif i == 6:
        skeleton(ctx, 540, 500, 0.6, t, hl={"legs": (GR, ease((u - 0.6) / 0.8)), "arms": (GR, ease((u - 0.9) / 0.8))}, scan=True)
    elif i == 7:
        steps = [("BUENA TÉCNICA", CY), ("SUPERVISIÓN", AM), ("CARGAS DE A POCO", GR)]
        for j, (lab, col) in enumerate(steps):
            kj = easeb((u - 0.3 - j * 0.6) / 0.5)
            if kj <= 0: continue
            y = 560 + j * 170
            rrect(ctx, 220, y, 640, 125, 30); ctx.set_source_rgba(*col, 0.12 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(4); ctx.stroke()
            text(ctx, str(j + 1), 290, y + 90, F_BIG, 72, col, kj, align="center")
            sz = fit_size(ctx, lab, F_BIG, 56, 470)
            text(ctx, lab, 585, y + 84, F_BIG, sz, WH, kj, align="center")
    elif i == 8:
        long_bone(ctx, 540, 560, 380, k, plate=0.6, t=t)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1060); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, AM, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "MITO VS. REALIDAD · HUESOS", W / 2, 196, CY, k, 28)
        title(ctx, "¿LAS PESAS TE DEJAN BAJITO?", WH, 368, 88, k)
    elif i == 1:
        pill(ctx, "LA IDEA POPULAR", W / 2, 196, RD, k, 30, filled=True)
        title(ctx, "“FRENA LA ESTATURA”", WH, 368, 96, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1120, F_MONO, 22, AM, k, align="center", bold=True)
    elif i == 2:
        pill(ctx, "REVISIÓN DE EVIDENCIA", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "LO ANALIZARON", WH, 368, 100, k)
        src(ctx, "Malina, Clin J Sport Med 2006 · niños prepúberes y en pubertad temprana · doi:10.1097/01.jsm.0000248843.31874.be", k, 1110)
    elif i == 3:
        pill(ctx, "RESULTADO", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "CRECIERON IGUAL", WH, 368, 100, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1110, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Malina, 2006 · sin efecto en estatura ni en peso", k, 1150)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿TE LO DIJERON A TI?", WH, 368, 96, k)
    elif i == 5:
        pill(ctx, "SEGURIDAD", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "PROGRAMAS SUPERVISADOS", WH, 368, 92, k)
        src(ctx, "Malina, 2006 · 10 estudios registraron lesiones: 3 en total", k, 1120)
    elif i == 6:
        pill(ctx, "ACADEMIA AMERICANA DE PEDIATRÍA", W / 2, 196, CY, k, 26, filled=True)
        title(ctx, "NO FRENAN EL CRECIMIENTO", WH, 368, 90, k)
        src(ctx, "AAP 2026 · Stricker et al., Pediatrics 2020 · doi:10.1542/peds.2020-1011", k, 1140)
    elif i == 7:
        pill(ctx, "LA CLAVE", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "TÉCNICA ANTES QUE PESO", WH, 368, 94, k)
        src(ctx, "Consenso internacional, Lloyd et al., BJSM 2014 · doi:10.1136/bjsports-2013-092952", k, 1120)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 48 · HUESOS")
