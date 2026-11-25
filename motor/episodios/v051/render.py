"""v051 · ¿El alcohol después de entrenar frena tu músculo? (ESTUDIO EXPLICADO con gancho en segunda persona, serie RECUPERACIÓN ·
paleta vino oscuro + rosa neón + ámbar + cian)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (1.0, 0.44, 0.64)   # rosa neón
C2 = (0.24, 0.94, 1.0)    # cian (proteína)


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.12, 0.03, 0.07], [0.02, 0.005, 0.012])
from engine_ext import *
CY = ACC
AL = AM      # alcohol = ámbar
PR = C2      # proteína = cian


def title(ctx, s, color=WH, y=380, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1150):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def glass(ctx, cx, base, s, a, fill=0.7, t=0.0, col=AL):
    """vaso con líquido ámbar y burbujas"""
    if a <= 0: return
    ctx.save(); ctx.translate(cx, base); ctx.scale(s, s)
    ctx.move_to(-60, -200); ctx.line_to(-48, 0); ctx.line_to(48, 0); ctx.line_to(60, -200)
    ctx.set_source_rgba(*WH, 0.85 * a); ctx.set_line_width(5); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()
    lv = -200 * fill
    ctx.move_to(-48 - 12 * fill, lv); ctx.line_to(-48, -4); ctx.line_to(48, -4); ctx.line_to(48 + 12 * fill, lv); ctx.close_path()
    ctx.set_source_rgba(*col, 0.35 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(3); ctx.stroke()
    for j in range(5):
        ph = (t * 0.7 + j * 0.21) % 1
        y = -10 + (lv + 10) * ph
        ctx.new_path(); ctx.arc(-28 + j * 14, y, 4, 0, 6.283); ctx.set_source_rgba(*WH, 0.7 * a * (1 - ph)); ctx.fill()
    ctx.restore()


def shaker(ctx, cx, base, s, a, col=PR):
    if a <= 0: return
    ctx.save(); ctx.translate(cx, base); ctx.scale(s, s)
    rrect(ctx, -55, -200, 110, 200, 18); ctx.set_source_rgba(*col, 0.14 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    rrect(ctx, -62, -240, 124, 44, 10); ctx.set_source_rgba(*col, 0.25 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.stroke()
    text(ctx, "PROT", 0, -90, F_MONO, 28, WH, a, align="center", bold=True)
    ctx.restore()


def dumbbell(ctx, cx, cy, s, a, col):
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.move_to(-60, 0); ctx.line_to(60, 0); ctx.set_source_rgba(*WH, 0.9 * a); ctx.set_line_width(10); ctx.stroke()
    for sx in (-1, 1):
        rrect(ctx, sx * 70 - 18, -48, 36, 96, 8); ctx.set_source_rgba(*col, 0.15 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def muscle(ctx, cx, cy, s, a, col, t, glow=0.5):
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.move_to(-120, 0); ctx.curve_to(-80, -110, 80, -110, 120, 0); ctx.curve_to(80, 70, -80, 70, -120, 0); ctx.close_path()
    ctx.set_source_rgba(*col, (0.12 + 0.2 * glow * (0.7 + 0.3 * math.sin(t * 5))) * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    for j in range(-2, 3):
        ctx.move_to(-100, j * 12 - 10); ctx.curve_to(-50, j * 18 - 30, 50, j * 18 - 30, 100, j * 12 - 10); ctx.set_source_rgba(*col, 0.45 * a); ctx.set_line_width(2.5); ctx.stroke()
    for sx in (-1, 1):
        ctx.move_to(sx * 120, 0); ctx.line_to(sx * 175, 0); ctx.set_source_rgba(*WH, 0.8 * a); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()


def check(ctx, x, y, a, col=GR):
    ctx.move_to(x - 20, y); ctx.line_to(x - 5, y + 16); ctx.line_to(x + 22, y - 18)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def down(ctx, x, y, a, col=RD):
    ctx.move_to(x, y - 22); ctx.line_to(x, y + 20); ctx.move_to(x - 16, y + 4); ctx.line_to(x, y + 22); ctx.line_to(x + 16, y + 4)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        dumbbell(ctx, 360, 860, 1.0, k, PR)
        kg = easeb((u - 0.7) / 0.5)
        glass(ctx, 720, 960, 1.1, kg, 0.75, t)
        kq = easeb((u - lt(0) - 1.8) / 0.5)
        if kq > 0:
            ctx.save(); ctx.translate(540, 620); ctx.scale(kq, kq)
            text(ctx, "¿CELEBRAS ASÍ?", 0, 0, F_BIG, 80, AL, 1, align="center"); ctx.restore()
    elif i == 1:
        dumbbell(ctx, 260, 800, 0.8, k, MU)
        text(ctx, "→", 410, 822, F_BIG, 80, WH, k, align="center")
        shaker(ctx, 580, 920, 1.0, easeb((u - 1.6) / 0.5))
        text(ctx, "+", 700, 830, F_BIG, 90, WH, easeb((u - 2.4) / 0.4), align="center")
        glass(ctx, 820, 920, 1.0, easeb((u - 2.6) / 0.5), 0.7, t)
    elif i == 2:
        kb = ease((u - 0.2) / 0.4)
        vbars(ctx, [("SOLO\nPROTEÍNA", 1.0, PR), ("PROTEÍNA\n+ ALCOHOL", 0.76, AL)], 270, 1010, 220, 100, 400, ease((u - 0.3) / 1.6), kb, 26)
        kk = easeb((u - lt(2) - 2.6) / 0.5)
        if kk > 0:
            ctx.save(); ctx.translate(710, 560); ctx.scale(kk, kk)
            text(ctx, "−24 %", 0, 0, F_BIG, 110, RD, 1, align="center"); ctx.restore()
    elif i == 3:
        n = int(clamp((u - 0.2) / 1.6) * 12)
        for j in range(n):
            c = j % 6; r = j // 6
            glass(ctx, 245 + c * 118, 720 + r * 210, 0.5, k, 0.7, t + j)
        kb = easeb((u - lt(3) - 1.8) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 1030); ctx.scale(kb, kb)
            text(ctx, "≈ 12 TRAGOS", 0, 0, F_BIG, 92, AL, 1, align="center"); ctx.restore()
    elif i == 4:
        for j, (lab, col, cx) in enumerate([("SÍ", AL, 330), ("NO", PR, 750)]):
            kj = easeb((u - 0.3 - j * 0.4) / 0.5)
            if kj <= 0: continue
            rrect(ctx, cx - 175, 560, 350, 320, 34); ctx.set_source_rgba(*col, 0.10 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(5); ctx.stroke()
            text(ctx, lab, cx, 790, F_BIG, 150, col, kj, align="center")
        cur = "▌" if int(t * 2.5) % 2 == 0 else " "
        text(ctx, "COMENTA: SÍ O NO" + cur, 540, 990, F_MONO, 34, AL, ease((u - 1.0) / 0.4), align="center", bold=True)
    elif i == 5:
        rows = [("RECUPERACIÓN DE LA FUERZA", 1.2), ("DOLOR MUSCULAR", 2.6)]
        for j, (lab, t0) in enumerate(rows):
            kj = easeb((u - t0) / 0.5)
            if kj <= 0: continue
            y = 600 + j * 200
            rrect(ctx, 190, y, 700, 140, 30); ctx.set_source_rgba(*GR, 0.10 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*GR, kj); ctx.set_line_width(4); ctx.stroke()
            check(ctx, 260, y + 70, kj)
            sz = fit_size(ctx, lab, F_BIG, 54, 540)
            text(ctx, lab, 320, y + 76, F_BIG, sz, WH, kj)
            text(ctx, "SIN CAMBIOS", 320 + 0, y + 125, F_MONO, 22, GR, kj, bold=True)
    elif i == 6:
        kl = easeb((u - 0.4) / 0.5); kr = easeb((u - lt(6) - 2.4) / 0.5)
        if kl > 0:
            rrect(ctx, 170, 540, 360, 480, 30); ctx.set_source_rgba(*GR, 0.08 * kl); ctx.fill_preserve(); ctx.set_source_rgba(*GR, kl); ctx.set_line_width(4); ctx.stroke()
            text(ctx, "IGUAL", 350, 610, F_BIG, 56, GR, kl, align="center")
            for j, lab in enumerate(["FUERZA", "POTENCIA", "DOLOR"]):
                check(ctx, 225, 700 + j * 100, kl); text(ctx, lab, 265, 714 + j * 100, F_MONO, 30, WH, kl, bold=True)
        if kr > 0:
            rrect(ctx, 560, 540, 360, 480, 30); ctx.set_source_rgba(*RD, 0.08 * kr); ctx.fill_preserve(); ctx.set_source_rgba(*RD, kr); ctx.set_line_width(4); ctx.stroke()
            text(ctx, "BAJARON", 740, 610, F_BIG, 56, RD, kr, align="center")
            for j, lab in enumerate(["SÍNTESIS DE", "PROTEÍNA", "TESTOSTERONA"]):
                if j == 0: down(ctx, 610, 750, kr)
                if j == 2: down(ctx, 610, 900, kr)
                text(ctx, lab, 645, 734 + (j * 50 if j < 2 else 166), F_MONO, 26, WH, kr, bold=True)
    elif i == 7:
        glass(ctx, 330, 960, 1.0, k, 0.12, t)
        text(ctx, "POCO O NADA", 330, 1040, F_MONO, 30, AL, k, align="center", bold=True)
        kb = easeb((u - 1.0) / 0.5)
        muscle(ctx, 740, 820, 0.95, kb, GR, t, 0.9)
        text(ctx, "MÚSCULO", 740, 1040, F_MONO, 30, GR, kb, align="center", bold=True)
    elif i == 8:
        muscle(ctx, 540, 720, 1.2, k, ACC, t, 0.8)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1020); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, AL, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "ESTUDIO EXPLICADO · RECUPERACIÓN", W / 2, 214, CY, k, 26)
        title(ctx, "¿ALCOHOL DESPUÉS DE ENTRENAR?", WH, 380, 86, k)
    elif i == 1:
        pill(ctx, "EL ESTUDIO", W / 2, 214, PR, k, 30, filled=True)
        title(ctx, "ENTRENARON Y LUEGO…", WH, 380, 96, k)
        src(ctx, "Parr et al., PLoS One 2014 · 8 hombres activos · doi:10.1371/journal.pone.0088384", k, 1110)
    elif i == 2:
        pill(ctx, "RESULTADO", W / 2, 214, RD, k, 30, filled=True)
        title(ctx, "MENOS CONSTRUCCIÓN DE MÚSCULO", WH, 380, 84, k)
        src(ctx, "Parr et al., 2014 · síntesis de proteína miofibrilar vs. solo proteína", k, 1140)
    elif i == 3:
        pill(ctx, "OJO CON LA DOSIS", W / 2, 214, AL, k, 30, filled=True)
        title(ctx, "FUE UNA DOSIS ENORME", WH, 380, 94, k)
        src(ctx, "Parr et al., 2014 · 1,5 g de alcohol por kg de peso (≈12 ± 2 tragos)", k, 1110)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 214, AL, k, 32, filled=True)
        title(ctx, "¿TOMAS DESPUÉS DE ENTRENAR?", WH, 380, 88, k)
    elif i == 5:
        pill(ctx, "OTROS ESTUDIOS · DOSIS MENORES", W / 2, 214, GR, k, 26, filled=True)
        title(ctx, "LA RECUPERACIÓN NO CAMBIÓ", WH, 380, 90, k)
        src(ctx, "Levitt et al., Eur J Appl Physiol 2017 (mujeres) · J Strength Cond Res 2020 (hombres)", k, 1060)
    elif i == 6:
        pill(ctx, "REVISIÓN SISTEMÁTICA", W / 2, 214, CY, k, 30, filled=True)
        title(ctx, "LO QUE CAMBIA Y LO QUE NO", WH, 380, 90, k)
        src(ctx, "Lakićević, J Funct Morphol Kinesiol 2019 · doi:10.3390/jfmk4030041", k, 1110)
    elif i == 7:
        pill(ctx, "CONCLUSIÓN", W / 2, 214, GR, k, 30, filled=True)
        title(ctx, "SI BUSCAS MÚSCULO", WH, 380, 96, k)
        src(ctx, "OMS 2023: ningún nivel de consumo de alcohol es seguro para la salud", k, 1110)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 380, 80, k)


run_episode(neon, txt, "EXPEDIENTE 51 · RECUPERACIÓN")
