"""v046 · ¿Estirar antes de las pesas te quita fuerza? (MITO VS. REALIDAD, serie MITOS DEL GIMNASIO ·
paleta granate profundo + cian + ámbar + verde)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (0.30, 0.92, 1.0)   # cian


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.14, 0.035, 0.06], [0.025, 0.006, 0.012])
from engine_ext import *
CY = ACC
ST = AM                   # estiramiento = ámbar
FU = GR                   # fuerza = verde


def title(ctx, s, color=WH, y=345, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1160):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def stopwatch(ctx, cx, cy, r, frac, a, col=ST, label=None):
    if a <= 0: return
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*col, 0.07 * a); ctx.fill_preserve()
    ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(6); ctx.stroke()
    rrect(ctx, cx - 22, cy - r - 40, 44, 30, 6); ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(4); ctx.stroke()
    for k in range(12):
        ang = k / 12 * 6.283
        ctx.move_to(cx + math.cos(ang) * (r - 24), cy + math.sin(ang) * (r - 24)); ctx.line_to(cx + math.cos(ang) * (r - 8), cy + math.sin(ang) * (r - 8))
        ctx.set_source_rgba(*WH, 0.6 * a); ctx.set_line_width(3); ctx.stroke()
    if frac > 0:
        ctx.new_path(); ctx.move_to(cx, cy); ctx.arc(cx, cy, r - 14, -math.pi / 2, -math.pi / 2 + frac * 6.283); ctx.close_path()
        ctx.set_source_rgba(*col, 0.28 * a); ctx.fill()
    ang = -math.pi / 2 + frac * 6.283
    ctx.move_to(cx, cy); ctx.line_to(cx + math.cos(ang) * (r - 30), cy + math.sin(ang) * (r - 30))
    ctx.set_source_rgba(*WH, a); ctx.set_line_width(6); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, 10, 0, 6.283); ctx.set_source_rgba(*WH, a); ctx.fill()
    if label:
        text(ctx, label, cx, cy + r + 62, F_MONO, 40, col, a, align="center", bold=True)


def muscle(ctx, x, y, w, h, stretch, a, col=ST):
    """músculo fusiforme que se alarga (stretch 0..1)"""
    if a <= 0: return
    L = w * (1 + 0.28 * stretch); hh = h * (1 - 0.25 * stretch)
    cx = x + w / 2
    x0, x1 = cx - L / 2, cx + L / 2
    ctx.move_to(x0, y); ctx.curve_to(x0 + L * 0.3, y - hh, x1 - L * 0.3, y - hh, x1, y)
    ctx.curve_to(x1 - L * 0.3, y + hh, x0 + L * 0.3, y + hh, x0, y); ctx.close_path()
    ctx.set_source_rgba(*col, 0.12 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(5); ctx.stroke()
    for k in range(-2, 3):
        yy = y + k * hh * 0.28
        ctx.move_to(x0 + L * 0.12, yy * 0 + y + k * hh * 0.12); ctx.curve_to(x0 + L * 0.35, yy, x1 - L * 0.35, yy, x1 - L * 0.12, y + k * hh * 0.12)
        ctx.set_source_rgba(*col, 0.45 * a); ctx.set_line_width(2.5); ctx.stroke()
    for s, xx in ((-1, x0), (1, x1)):
        ctx.move_to(xx, y); ctx.line_to(xx + s * 70, y); ctx.set_source_rgba(*WH, 0.8 * a); ctx.set_line_width(7); ctx.stroke()
        if stretch > 0.05:
            ax = xx + s * 110
            ctx.move_to(ax - s * 20, y - 18); ctx.line_to(ax, y); ctx.line_to(ax - s * 20, y + 18)
            ctx.set_source_rgba(*ST, stretch * a); ctx.set_line_width(5); ctx.stroke()


def doc(ctx, x, y, a, col):
    rrect(ctx, x, y, 44, 56, 7); ctx.set_source_rgba(*col, 0.15 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(2.5); ctx.stroke()
    for ln in range(3):
        ctx.move_to(x + 9, y + 15 + ln * 13); ctx.line_to(x + 35 - ln * 6, y + 15 + ln * 13); ctx.set_source_rgba(*WH, 0.5 * a); ctx.set_line_width(2); ctx.stroke()


def jumper(ctx, cx, base, k, t, a):
    """arco de salto con figura simple"""
    if a <= 0: return
    ph = (t * 0.9) % 1
    hgt = 4 * ph * (1 - ph) * 200
    x = cx - 160 + 320 * ph
    ctx.new_path()
    for i in range(41):
        f = i / 40; xx = cx - 160 + 320 * f; yy = base - 4 * f * (1 - f) * 200
        (ctx.move_to if i == 0 else ctx.line_to)(xx, yy)
    ctx.set_source_rgba(*CY, 0.35 * a); ctx.set_line_width(3); ctx.set_dash([10, 10]); ctx.stroke(); ctx.set_dash([])
    y = base - hgt
    ctx.new_path(); ctx.arc(x, y - 92, 18, 0, 6.283); ctx.set_source_rgba(*WH, a); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(x, y - 72); ctx.line_to(x, y - 20); ctx.move_to(x, y - 20); ctx.line_to(x - 20, y + 10); ctx.move_to(x, y - 20); ctx.line_to(x + 20, y + 10)
    ctx.move_to(x - 28, y - 70); ctx.line_to(x, y - 58); ctx.line_to(x + 28, y - 70); ctx.stroke()
    ctx.move_to(cx - 220, base + 14); ctx.line_to(cx + 220, base + 14); ctx.set_source_rgba(*WH, 0.4 * a); ctx.set_line_width(3); ctx.stroke()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        muscle(ctx, 210, 760, 360, 110, 0.6 + 0.4 * math.sin(t * 2) ** 2, k)
        sec = min(60, int(u * 16))
        stopwatch(ctx, 790, 760, 130, sec / 60, ease((u - 0.3) / 0.4), ST, "00:%02d" % sec)
    elif i == 1:
        barbell_icon(ctx, 540, 720, t, k)
        kq = easeb((u - lt(1) - 1.5) / 0.5)
        if kq > 0:
            ctx.save(); ctx.translate(540, 1040); ctx.scale(kq, kq)
            text(ctx, "¿MENOS FUERZA?", 0, 0, F_BIG, 84, RD, 1, align="center"); ctx.restore()
    elif i == 2:
        n = int(clamp((u - 0.2) / 2.0) * 83)
        for j in range(n):
            c = j % 12; r = j // 12
            doc(ctx, 175 + c * 62, 520 + r * 70, k, CY)
        kb = easeb((u - lt(2) - 1.6) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 1080); ctx.scale(kb, kb)
            text(ctx, "83 ESTUDIOS", 0, 0, F_BIG, 92, AM, 1, align="center"); ctx.restore()
    elif i == 3:
        # esquema: pérdida de fuerza según duración del estiramiento
        x0, y0, w, h = 200, 560, 680, 380
        ctx.move_to(x0, y0); ctx.line_to(x0, y0 + h); ctx.line_to(x0 + w, y0 + h); ctx.set_source_rgba(*CY, 0.6 * k); ctx.set_line_width(3); ctx.stroke()
        up = ease((u - 0.4) / 3.0)
        n = 6
        for j in range(n):
            f = (j + 1) / n
            if f > up + 0.001: break
            v = 0.12 + 0.05 * j if j < 3 else 0.45 + 0.18 * (j - 3)
            col = AM if j < 3 else RD
            bx = x0 + 30 + j * 106; bh = h * v
            rrect(ctx, bx, y0 + h - bh, 80, bh, 10); ctx.set_source_rgba(*col, 0.25 * k); ctx.fill_preserve(); ctx.set_source_rgba(*col, k); ctx.set_line_width(3); ctx.stroke()
        mx = x0 + 30 + 3 * 106 - 13
        ctx.move_to(mx, y0 - 10); ctx.line_to(mx, y0 + h); ctx.set_source_rgba(*WH, 0.7 * k); ctx.set_dash([12, 10]); ctx.set_line_width(3); ctx.stroke(); ctx.set_dash([])
        text(ctx, "1 MIN", mx, y0 - 26, F_MONO, 28, WH, k, align="center", bold=True)
        text(ctx, "MENOS", x0 + w * 0.22, y0 + h + 44, F_MONO, 24, AM, k, align="center", bold=True)
        text(ctx, "MÁS TIEMPO", x0 + w * 0.78, y0 + h + 44, F_MONO, 24, RD, k, align="center", bold=True)
        text(ctx, "PÉRDIDA DE FUERZA", x0, y0 - 26, F_MONO, 22, MU, k)
    elif i == 4:
        for j, (lab, fr, col) in enumerate([("10 S", 10 / 60, GR), ("30 S", 0.5, AM), ("60 S", 1.0, RD)]):
            kj = easeb((u - 0.3 - j * 0.35) / 0.5)
            if kj <= 0: continue
            cx = 250 + j * 290
            rrect(ctx, cx - 125, 560, 250, 330, 30); ctx.set_source_rgba(*col, 0.10 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(4); ctx.stroke()
            stopwatch(ctx, cx, 710, 80, fr * ease((u - 0.5 - j * 0.35) / 0.8), kj, col)
            text(ctx, lab, cx, 860, F_BIG, 60, col, kj, align="center")
        cur = "▌" if int(t * 2.5) % 2 == 0 else " "
        text(ctx, "COMENTA: 10, 30 O 60" + cur, 540, 990, F_MONO, 34, AM, ease((u - 1.4) / 0.4), align="center", bold=True)
    elif i == 5:
        stopwatch(ctx, 540, 700, 150, 0.75 * ease((u - 0.2) / 1.2), k, GR, "< 60 S POR MÚSCULO")
        kb = easeb((u - lt(5) - 2.6) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 1080); ctx.scale(kb, kb)
            text(ctx, "≈ −1 % DE FUERZA", 0, 0, F_BIG, 88, AM, 1, align="center"); ctx.restore()
    elif i == 6:
        jumper(ctx, 540, 820, k, t, k)
        footprints(ctx, 200, 880, 930, t, 2.2, k, CY)
        kb = easeb((u - lt(6) - 1.6) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 1080); ctx.scale(kb, kb)
            text(ctx, "SIN EMPEORAR", 0, 0, F_BIG, 90, GR, 1, align="center"); ctx.restore()
    elif i == 7:
        steps = [("ESTIRA BREVE", ST), ("SERIES LIGERAS", CY), ("SERIES DE TRABAJO", GR)]
        for j, (lab, col) in enumerate(steps):
            kj = easeb((u - 0.3 - j * 0.6) / 0.5)
            if kj <= 0: continue
            y = 560 + j * 170
            rrect(ctx, 220, y, 640, 125, 30); ctx.set_source_rgba(*col, 0.12 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(4); ctx.stroke()
            text(ctx, str(j + 1), 290, y + 90, F_BIG, 72, col, kj, align="center")
            sz = fit_size(ctx, lab, F_BIG, 56, 470)
            text(ctx, lab, 585, y + 84, F_BIG, sz, WH, kj, align="center")
            if j < 2:
                ctx.move_to(540, y + 128); ctx.line_to(540, y + 166); ctx.set_source_rgba(*WH, 0.6 * kj); ctx.set_line_width(4); ctx.stroke()
    elif i == 8:
        muscle(ctx, 360, 720, 360, 100, 0.3 + 0.3 * math.sin(t * 2) ** 2, k, CY)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1000); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, AM, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "MITOS DEL GIMNASIO · FUERZA", W / 2, 196, CY, k, 28)
        title(ctx, "¿ESTIRAS 1 MINUTO ANTES?", WH, 368, 94, k)
    elif i == 1:
        pill(ctx, "LO QUE SE DICE", W / 2, 196, RD, k, 30, filled=True)
        title(ctx, "ESTIRAR TE QUITA FUERZA", WH, 368, 94, k)
    elif i == 2:
        pill(ctx, "METAANÁLISIS 2024", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "LO VOLVIERON A MEDIR", WH, 368, 96, k)
        src(ctx, "Warneke y Lohmann, J Sport Health Sci 2024 · doi:10.1016/j.jshs.2024.05.002", k)
    elif i == 3:
        pill(ctx, "RESULTADO", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "PÉRDIDA PEQUEÑA… QUE CRECE", WH, 368, 88, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1100, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Warneke y Lohmann, 2024 · efecto pequeño; mayor con ≥60 s por estiramiento", k)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿CUÁNTO LO MANTIENES?", WH, 368, 92, k)
    elif i == 5:
        pill(ctx, "ESTIRAMIENTO CORTO", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "CASI NADA", WH, 368, 104, k)
        src(ctx, "Behm et al., Appl Physiol Nutr Metab 2016 · <60 s: −1,1 % · doi:10.1139/apnm-2015-0235", k)
    elif i == 6:
        pill(ctx, "SALTOS Y CARRERAS", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "EL RENDIMIENTO NO BAJÓ", WH, 368, 94, k)
        src(ctx, "Warneke y Lohmann, 2024 · sin efecto negativo en rendimiento atlético", k)
    elif i == 7:
        pill(ctx, "EN LA PRÁCTICA", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "BREVE Y LUEGO SERIES LIGERAS", WH, 368, 84, k)
        src(ctx, "Behm et al., 2016 · con actividad dinámica después, sin efecto claro", k, 1120)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 46 · FUERZA")
