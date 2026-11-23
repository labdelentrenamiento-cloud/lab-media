"""v045 · ¿Existe la "ventana anabólica" de 30 minutos? (MITO VS. REALIDAD, serie MÚSCULO/NUTRICIÓN ·
paleta azul noche (estilo Huesos) + violeta + ámbar + cian)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (0.66, 0.58, 1.0)   # violeta


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.07, 0.07, 0.22], [0.01, 0.01, 0.05])
from engine_ext import *
CY = ACC
PR = AM                    # proteína = ámbar
TI = (0.30, 0.90, 1.0)     # tiempo = cian


def title(ctx, s, color=WH, y=345, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1170):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def shaker(ctx, cx, cy, s, a, level=0.7, t=0.0, shake=0.0):
    if a <= 0: return
    ctx.save(); ctx.translate(cx + shake * 10 * math.sin(t * 30), cy); ctx.scale(s, s)
    ctx.move_to(-70, -120); ctx.line_to(70, -120); ctx.line_to(58, 140); ctx.line_to(-58, 140); ctx.close_path()
    ctx.set_source_rgba(*PR, 0.06 * a); ctx.fill_preserve(); ctx.set_source_rgba(*PR, a); ctx.set_line_width(5); ctx.stroke()
    if level > 0:
        top = 140 - 260 * level
        ctx.save(); ctx.move_to(-70, -120); ctx.line_to(70, -120); ctx.line_to(58, 140); ctx.line_to(-58, 140); ctx.close_path(); ctx.clip()
        ctx.rectangle(-80, top, 160, 300); ctx.set_source_rgba(*PR, 0.35 * a); ctx.fill(); ctx.restore()
    rrect(ctx, -78, -170, 156, 50, 12); ctx.set_source_rgba(*WH, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*WH, 0.9 * a); ctx.set_line_width(4); ctx.stroke()
    rrect(ctx, -26, -205, 52, 36, 8); ctx.set_source_rgba(*WH, 0.9 * a); ctx.stroke()
    ctx.restore()


def dial(ctx, cx, cy, r, a, sector=0.0, col=None, hand=0.0):
    """reloj con un sector resaltado (fracción de hora) y una aguja"""
    col = col or TI
    if a <= 0: return
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*TI, 0.06 * a); ctx.fill_preserve(); ctx.set_source_rgba(*TI, 0.9 * a); ctx.set_line_width(6); ctx.stroke()
    for k in range(12):
        ang = k / 12 * 6.283 - math.pi / 2
        ctx.move_to(cx + math.cos(ang) * (r - 26), cy + math.sin(ang) * (r - 26)); ctx.line_to(cx + math.cos(ang) * (r - 8), cy + math.sin(ang) * (r - 8))
        ctx.set_source_rgba(*WH, 0.7 * a); ctx.set_line_width(4); ctx.stroke()
    if sector > 0:
        ctx.new_path(); ctx.move_to(cx, cy); ctx.arc(cx, cy, r - 12, -math.pi / 2, -math.pi / 2 + sector * 6.283); ctx.close_path()
        ctx.set_source_rgba(*col, 0.30 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    ang = -math.pi / 2 + hand * 6.283
    ctx.move_to(cx, cy); ctx.line_to(cx + math.cos(ang) * (r - 40), cy + math.sin(ang) * (r - 40)); ctx.set_source_rgba(*WH, a); ctx.set_line_width(7); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, 12, 0, 6.283); ctx.set_source_rgba(*WH, a); ctx.fill()


def scale_bal(ctx, cx, cy, tilt, a, left, right):
    if a <= 0: return
    ctx.move_to(cx, cy); ctx.line_to(cx, cy + 260); ctx.set_source_rgba(*WH, 0.8 * a); ctx.set_line_width(8); ctx.stroke()
    ctx.move_to(cx - 90, cy + 260); ctx.line_to(cx + 90, cy + 260); ctx.stroke()
    L = 300; ang = tilt
    lx, ly = cx - L * math.cos(ang), cy - L * math.sin(ang)
    rx, ry = cx + L * math.cos(ang), cy + L * math.sin(ang)
    ctx.move_to(lx, ly); ctx.line_to(rx, ry); ctx.set_line_width(8); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, 14, 0, 6.283); ctx.set_source_rgba(*WH, a); ctx.fill()
    for (px, py, (lab, col, sz)) in ((lx, ly, left), (rx, ry, right)):
        ctx.move_to(px, py); ctx.line_to(px, py + 70); ctx.set_source_rgba(*WH, 0.6 * a); ctx.set_line_width(3); ctx.stroke()
        rrect(ctx, px - 120, py + 70, 240, 34, 12); ctx.set_source_rgba(*col, 0.25 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
        for li, part in enumerate(lab.split("\n")):
            text(ctx, part, px, py + 168 + li * (sz + 6), F_BIG, sz, col, a, align="center")


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        shaker(ctx, 370, 800, 1.2, k, 0.75, t, shake=ease((u - 0.5) / 0.3))
        remain = max(0, 29 - int(u * 3))
        dial(ctx, 740, 790, 150, ease((u - 0.3) / 0.4), sector=0.5 * (remain / 30), col=RD, hand=(u * 0.6) % 1)
        text(ctx, "00:%02d" % remain, 740, 1020, F_MONO, 54, RD, ease((u - 0.3) / 0.4), align="center", bold=True)
    elif i == 1:
        dial(ctx, 540, 730, 200, k, sector=0.5 * ease((u - 0.6) / 1.4), col=PR, hand=0.5 * ease((u - 0.6) / 1.4))
        kq = easeb((u - lt(1) - 2.6) / 0.5)
        if kq > 0:
            ctx.save(); ctx.translate(540, 1110); ctx.scale(kq, kq)
            text(ctx, "¿Y SI LA PIERDES?", 0, 0, F_BIG, 70, RD, 1, align="center"); ctx.restore()
    elif i == 2:
        n = int(clamp((u - 0.2) / 1.8) * 23)
        for j in range(23):
            if j >= n: break
            col_ = j % 8; row = j // 8
            x = 205 + col_ * 85; y = 560 + row * 100
            rrect(ctx, x, y, 66, 84, 10); ctx.set_source_rgba(*CY, 0.15 * k); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.9 * k); ctx.set_line_width(3); ctx.stroke()
            for ln in range(3):
                ctx.move_to(x + 12, y + 22 + ln * 20); ctx.line_to(x + 54 - ln * 8, y + 22 + ln * 20); ctx.set_source_rgba(*WH, 0.5 * k); ctx.set_line_width(3); ctx.stroke()
        kb = easeb((u - lt(2) - 1.4) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 1010); ctx.scale(kb, kb)
            text(ctx, "23 ESTUDIOS", 0, 0, F_BIG, 90, AM, 1, align="center"); ctx.restore()
    elif i == 3:
        tilt = lerp(0.0, 0.32, ease((u - lt(3) - 1.4) / 1.2))
        scale_bal(ctx, 540, 560, tilt, k, ("HORARIO", TI, 54), ("PROTEÍNA\nTOTAL", PR, 54))
    elif i == 4:
        for j, (lab, col, cx, sec) in enumerate([("MINUTOS", TI, 330, 0.08), ("HORAS", PR, 750, 0.4)]):
            kj = easeb((u - 0.3 - j * 0.4) / 0.5)
            if kj <= 0: continue
            rrect(ctx, cx - 175, 560, 350, 320, 34); ctx.set_source_rgba(*col, 0.10 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(5); ctx.stroke()
            dial(ctx, cx, 690, 90, kj, sector=sec, col=col, hand=sec)
            text(ctx, lab, cx, 850, F_BIG, 58, col, kj, align="center")
        cur = "▌" if int(t * 2.5) % 2 == 0 else " "
        text(ctx, "COMENTA: MINUTOS U HORAS" + cur, 540, 990, F_MONO, 32, AM, ease((u - 1.2) / 0.4), align="center", bold=True)
    elif i == 5:
        # línea de tiempo: proteína ANTES vs DESPUÉS del entrenamiento
        for j, (lab, y, pos, col) in enumerate([("ANTES", 640, 0, TI), ("DESPUÉS", 900, 1, PR)]):
            kj = ease((u - 0.3 - j * 0.6) / 0.5)
            if kj <= 0: continue
            ctx.move_to(200, y); ctx.line_to(880, y); ctx.set_source_rgba(*WH, 0.5 * kj); ctx.set_line_width(3); ctx.stroke()
            rrect(ctx, 420, y - 40, 240, 80, 16); ctx.set_source_rgba(*CY, 0.20 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*CY, kj); ctx.set_line_width(3); ctx.stroke()
            text(ctx, "PESAS", 540, y + 14, F_BIG, 44, WH, kj, align="center")
            shaker(ctx, 340 if pos == 0 else 740, y - 6, 0.32, kj, 0.7)
            text(ctx, lab, 200, y - 60, F_MONO, 28, col, kj, bold=True)
        ke = easeb((u - lt(5) - 3.0) / 0.5)
        if ke > 0:
            ctx.save(); ctx.translate(540, 1080); ctx.scale(ke, ke)
            text(ctx, "MISMO RESULTADO", 0, 0, F_BIG, 70, GR, 1, align="center"); ctx.restore()
    elif i == 6:
        f = lambda x: 0.9 - 0.55 * x ** 1.3
        up = ease((u - 0.3) / 2.4)
        line_chart(ctx, 190, 540, 700, 420, [(f, GR, up, True)], [(0, "0 H"), (0.5, "12 H"), (1, "24 H")], "HORAS TRAS ENTRENAR", "EFECTO EN EL MÚSCULO", k)
    elif i == 7:
        ctx.move_to(170, 720); ctx.line_to(910, 720); ctx.set_source_rgba(*WH, 0.6 * k); ctx.set_line_width(4); ctx.stroke()
        meals = [(230, "DESAYUNO"), (430, "ALMUERZO"), (640, "MERIENDA"), (850, "CENA")]
        tot = 0
        for j, (x, lab) in enumerate(meals):
            kj = easeb((u - 0.3 - j * 0.45) / 0.5)
            if kj <= 0: continue
            tot += 1
            ctx.new_path(); ctx.arc(x, 720, 42 * kj, 0, 6.283); ctx.set_source_rgba(*PR, 0.35); ctx.fill_preserve(); ctx.set_source_rgba(*PR, 1); ctx.set_line_width(4); ctx.stroke()
            text(ctx, lab, x, 800, F_MONO, 22, WH, kj, align="center", bold=True)
        fill = ease((u - 0.5) / 2.6)
        rrect(ctx, 190, 900, 700, 70, 35); ctx.set_source_rgba(*PR, 0.10 * k); ctx.fill()
        rrect(ctx, 190, 900, max(70, 700 * fill), 70, 35); ctx.set_source_rgba(*PR, 0.40 * k); ctx.fill_preserve(); ctx.set_source_rgba(*PR, k); ctx.set_line_width(3); ctx.stroke()
        text(ctx, "PROTEÍNA TOTAL DEL DÍA", 540, 1040, F_BIG, 56, AM, ease((u - 1.0) / 0.4), align="center")
    elif i == 8:
        shaker(ctx, 540, 760, 1.0, k, 0.7, t)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1050); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, AM, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "MITO VS. REALIDAD · MÚSCULO", W / 2, 196, CY, k, 28)
        title(ctx, "¿CORRES POR TU BATIDO?", WH, 368, 96, k)
    elif i == 1:
        pill(ctx, "LA IDEA POPULAR", W / 2, 196, RD, k, 30, filled=True)
        title(ctx, "LA VENTANA DE 30 MINUTOS", WH, 368, 92, k)
    elif i == 2:
        pill(ctx, "METAANÁLISIS", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "LO PUSIERON A PRUEBA", WH, 368, 96, k)
        src(ctx, "Schoenfeld, Aragon y Krieger, JISSN 2013 · doi:10.1186/1550-2783-10-53", k, 1160)
    elif i == 3:
        pill(ctx, "RESULTADO", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "PESÓ EL TOTAL, NO LA HORA", WH, 368, 92, k)
        src(ctx, "Schoenfeld et al., 2013 · con proteína total igualada: sin diferencia", k, 1160)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿CUÁNTO ESPERAS PARA COMER?", WH, 368, 86, k)
    elif i == 5:
        pill(ctx, "ENSAYO · 10 SEMANAS", W / 2, 196, TI, k, 30, filled=True)
        title(ctx, "¿ANTES O DESPUÉS?", WH, 368, 100, k)
        src(ctx, "Schoenfeld et al., PeerJ 2017 · doi:10.7717/peerj.2825", k, 1160)
    elif i == 6:
        pill(ctx, "LA VENTANA ES ANCHA", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "DURA AL MENOS UN DÍA", WH, 368, 96, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1115, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Jäger et al., ISSN Position Stand 2017 · doi:10.1186/s12970-017-0177-8", k, 1160)
    elif i == 7:
        pill(ctx, "EN LA PRÁCTICA", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "REPARTIDA EN VARIAS COMIDAS", WH, 368, 86, k)
        src(ctx, "ISSN 2017 · dosis repartidas cada 3–4 h a lo largo del día", k, 1160)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 45 · MÚSCULO")
