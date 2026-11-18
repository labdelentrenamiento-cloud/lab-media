"""v034 · ¿30 minutos de una vez o 10 después de cada comida? (COMPARACIÓN, serie METABOLISMO ·
paleta vino oscuro + ámbar + verde + violeta)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math, random
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


engine.BG = engine_ext.BG = _bg([0.13, 0.05, 0.09], [0.03, 0.01, 0.025])
from engine_ext import *


def title(ctx, s, color=WH, y=345, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1270):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def badge(ctx, cx, cy, num, unit, col, a, w=280):
    if a <= 0: return
    rrect(ctx, cx - w / 2, cy - 150, w, 290, 26); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    big(ctx, num, cx, cy + 30, 120, col, a, maxw=w - 40)
    for li, part in enumerate(unit.split("\n")):
        text(ctx, part, cx, cy + 85 + li * 30, F_MONO, 23, WH, a, align="center", bold=True)


def plate(ctx, cx, cy, r, col, a, moon=False):
    if a <= 0: return
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, r * 0.66, 0, 6.283); ctx.set_source_rgba(*col, 0.6 * a); ctx.set_line_width(2.5); ctx.stroke()
    for sx in (-1, 1):   # cubiertos
        x = cx + sx * (r + 26)
        ctx.move_to(x, cy - r * 0.8); ctx.line_to(x, cy + r * 0.8); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    if moon:
        ctx.new_path(); ctx.arc(cx, cy - r - 46, 22, 0, 6.283); ctx.set_source_rgba(*VI, a); ctx.fill()
        ctx.new_path(); ctx.arc(cx + 11, cy - r - 52, 20, 0, 6.283); ctx.set_operator(0); ctx.fill(); ctx.set_operator(2)


def walker(ctx, cx, cy, s, t, col, a):
    """figura caminando (palitos)"""
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ph = math.sin(t * 6)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(7); ctx.set_line_cap(1)
    ctx.new_path(); ctx.arc(0, -150, 26, 0, 6.283); ctx.stroke()
    ctx.move_to(0, -120); ctx.line_to(4, -20); ctx.stroke()
    ctx.move_to(2, -100); ctx.line_to(-34 * ph, -50); ctx.move_to(2, -100); ctx.line_to(34 * ph, -50); ctx.stroke()
    ctx.move_to(4, -20); ctx.line_to(40 * ph, 60); ctx.move_to(4, -20); ctx.line_to(-40 * ph, 60); ctx.stroke()
    ctx.set_line_cap(0); ctx.restore()


def glucose_chart(ctx, k, a, show_green):
    x0, y0, w, h = 170, 560, 740, 440
    hi = lambda x: 0.12 + 0.78 * math.exp(-((x - 0.32) / 0.2) ** 2)
    lo = lambda x: 0.12 + 0.62 * math.exp(-((x - 0.28) / 0.19) ** 2)
    series = [(hi, AM, k, False)]
    if show_green: series.append((lo, GR, ease((k - 0.2) / 0.8), True))
    line_chart(ctx, x0, y0, w, h, series, [(0, "COMIDA"), (0.5, "+1,5 h"), (1, "+3 h")], "", "AZÚCAR EN SANGRE", a)


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        # día: 3 comidas; arriba 1 bloque de 30, abajo 10 tras cada comida
        xs = (250, 540, 830)
        for j, x in enumerate(xs):
            plate(ctx, x, 640, 62, AM, ease((u - 0.1 * j) / 0.4), moon=(j == 2))
        kb = ease((u - 0.8) / 0.5)
        rrect(ctx, 170, 790, 740 * kb, 70, 20); ctx.set_source_rgba(*VI, 0.2 * kb); ctx.fill_preserve(); ctx.set_source_rgba(*VI, kb); ctx.set_line_width(4); ctx.stroke()
        text(ctx, "30 MIN DE UNA VEZ", 540, 836, F_MONO, 30, WH, kb, align="center", bold=True)
        for j, x in enumerate(xs):
            kk = easeb((u - lt(0) - 2.6 - j * 0.25) / 0.5)
            if kk <= 0: continue
            rrect(ctx, x - 100, 900, 200, 70, 20); ctx.set_source_rgba(*GR, 0.2 * kk); ctx.fill_preserve(); ctx.set_source_rgba(*GR, kk); ctx.set_line_width(4); ctx.stroke()
            text(ctx, "10 MIN", x, 946, F_MONO, 30, WH, kk, align="center", bold=True)
        kv = easeb((u - lt(0) - 1.6) / 0.5)
        if kv > 0: big(ctx, "VS", 540, 1080, 90 * kv, WH, kv, maxw=200)
    elif i == 1:
        badge(ctx, 250, 790, "41", "ADULTOS\nDIABETES TIPO 2", AM, ease((u - 0.1) / 0.4))
        badge(ctx, 540, 790, "2", "PLANES\nMISMOS MINUTOS", VI, ease((u - 1.6) / 0.4))
        badge(ctx, 830, 790, "2+2", "SEMANAS\nCADA UNO", GR, ease((u - 3.4) / 0.4))
    elif i == 2:
        glucose_chart(ctx, ease((u - 0.2) / 1.6), k, True)
        kn = easeb((u - lt(2) - 3.6) / 0.5)
        if kn > 0:
            ctx.save(); ctx.translate(700, 700); ctx.scale(kn, kn)
            text(ctx, "−12 %", 0, 0, F_BIG, 110, GR, 1, align="center"); ctx.restore()
    elif i == 3:
        plate(ctx, 540, 720, 120, AM, k, moon=True)
        kn = easeb((u - lt(3) - 3.8) / 0.5)
        if kn > 0:
            ctx.save(); ctx.translate(540, 1060); ctx.scale(kn, kn)
            text(ctx, "−22 %", 0, 0, F_BIG, 150, GR, 1, align="center"); ctx.restore()
    elif i == 4:
        for j, (lab, x) in enumerate((("DESAYUNO", 250), ("ALMUERZO", 540), ("CENA", 830))):
            kk = easeb((u - 0.2 - j * 0.2) / 0.5)
            plate(ctx, x, 760, 80 * max(kk, 0.01), AM, kk, moon=(j == 2))
            text(ctx, lab, x, 900, F_MONO, 26, AM, kk, align="center", bold=True)
        kq = easeb((u - 1.0) / 0.5)
        if kq > 0: big(ctx, "?", 540, 1080, 120 * kq, WH, kq, maxw=200)
    elif i == 5:
        leg(ctx, 540, 520, 0.95, a=k, col=GR, fill=0.1)
        rnd = random.Random(7)
        for n in range(26):
            ph = (t * 0.45 + rnd.random()) % 1.0
            x0 = 200 + rnd.random() * 680
            x = x0 + (540 - x0) * ph * 0.85; y = 480 + ph * 400
            al = k * clamp(ph * 4) * clamp((1 - ph) * 4)
            ctx.new_path(); ctx.arc(x, y, 9, 0, 6.283); ctx.set_source_rgba(*AM, al); ctx.fill()
        text(ctx, "GLUCOSA", 860, 560, F_MONO, 26, AM, k, align="center", bold=True)
        text(ctx, "MÚSCULO", 250, 900, F_MONO, 26, GR, ease((u - 0.6) / 0.4), align="center", bold=True)
    elif i == 6:
        kk = ease((u - 0.3) / 1.4)
        vbars(ctx, [("SENTADO", 0.95, RD), ("DE PIE", 0.78, AM), ("CAMINAR\nSUAVE", 0.52, GR)], 175, 1060, 190, 60, 440, kk, k, label_size=24)
        text(ctx, "GLUCOSA E INSULINA TRAS COMER", 540, 560, F_MONO, 24, WH, k, align="center", bold=True)
    elif i == 7:
        walker(ctx, 540, 820, 1.5, t, GR, k)
        footprints(ctx, 150, 930, 1020, t, 1.0, a=0.7 * k, col=GR)
    elif i == 8:
        walker(ctx, 540, 760, 1.15, t, GR, k)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1030); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 130, AM, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "COMPARACIÓN · METABOLISMO", W / 2, 196, AM, k, 28)
        title(ctx, "¿CUÁNDO TE CONVIENE CAMINAR?", WH, 368, 92, k)
    elif i == 1:
        pill(ctx, "ENSAYO CRUZADO · 2016", W / 2, 196, AM, k, 28, filled=True)
        title(ctx, "LOS MISMOS, CON LOS 2 PLANES", WH, 368, 92, k)
        src(ctx, "Reynolds et al., Diabetologia 2016 · doi:10.1007/s00125-016-4085-2", k, 1080)
    elif i == 2:
        pill(ctx, "10 MIN TRAS COMER", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "MENOS AZÚCAR TRAS COMER", WH, 368, 96, k)
        text(ctx, "ESQUEMA DE LA CURVA · CIFRA REAL: −12 %", W / 2, 1150, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Reynolds et al., 2016 · glucosa 3 h tras cada comida", k, 1195)
    elif i == 3:
        pill(ctx, "LA CENA", W / 2, 196, VI, k, 30, filled=True)
        title(ctx, "LA MAYOR DIFERENCIA", WH, 368, 104, k)
        src(ctx, "Reynolds et al., 2016 · la comida con más carbohidratos", k, 1180)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿TU COMIDA MÁS PESADA?", WH, 368, 100, k)
    elif i == 5:
        pill(ctx, "POR QUÉ FUNCIONA", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "TUS PIERNAS USAN GLUCOSA", WH, 368, 96, k)
    elif i == 6:
        pill(ctx, "METAANÁLISIS · 7 ENSAYOS", W / 2, 196, GR, k, 28, filled=True)
        title(ctx, "CAMINAR GANA A ESTAR DE PIE", WH, 368, 92, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1180, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Buffey et al., Sports Med 2022 · doi:10.1007/s40279-022-01649-4", k, 1225)
    elif i == 7:
        pill(ctx, "EN LA PRÁCTICA", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "UN PASEO TRANQUILO", WH, 368, 104, k)
        text(ctx, "DESPUÉS DE COMER", W / 2, 1150, F_MONO, 34, AM, ease((u - 0.8) / 0.4), align="center", bold=True)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 34 · METABOLISMO")
