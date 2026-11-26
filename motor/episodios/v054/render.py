"""v054 · ¿Ejercicio antes, durante o después de estudiar? (3 MOMENTOS / ESTUDIO EXPLICADO, serie CEREBRO ·
paleta violeta profundo + magenta + cian)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (1.0, 0.42, 0.86)   # magenta


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.10, 0.03, 0.14], [0.02, 0.005, 0.03])
from engine_ext import *
CY = ACC
BR = (0.61, 0.55, 1.0)       # cerebro = violeta
C2 = (0.24, 0.94, 1.0)       # cian


def title(ctx, s, color=WH, y=380, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1110):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def book(ctx, cx, cy, s, a, col=C2):
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.set_line_width(5); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    for sx in (-1, 1):
        ctx.move_to(0, -60); ctx.curve_to(sx * 40, -80, sx * 90, -80, sx * 120, -60); ctx.line_to(sx * 120, 70)
        ctx.curve_to(sx * 90, 50, sx * 40, 50, 0, 70); ctx.close_path()
        ctx.set_source_rgba(*col, 0.12 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.stroke()
        for j in range(3):
            y = -35 + j * 30
            ctx.move_to(sx * 25, y); ctx.line_to(sx * 95, y - 8); ctx.set_source_rgba(*col, 0.5 * a); ctx.set_line_width(3); ctx.stroke()
        ctx.set_line_width(5)
    ctx.restore()


def bike(ctx, cx, cy, s, a, t, col=GR):
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.set_line_width(6); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgba(*col, a)
    ctx.move_to(-110, 90); ctx.line_to(110, 90); ctx.stroke()                       # base
    ctx.move_to(-60, 90); ctx.line_to(-20, -40); ctx.line_to(60, -40); ctx.line_to(30, 90); ctx.stroke()  # cuadro
    ctx.move_to(-40, -40); ctx.line_to(-10, -40); ctx.stroke()                      # asiento
    ctx.move_to(60, -40); ctx.line_to(80, -90); ctx.line_to(105, -90); ctx.stroke()  # manubrio
    ctx.new_path(); ctx.arc(20, 30, 34, 0, 6.283); ctx.set_source_rgba(*col, 0.15 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.stroke()
    ang = t * 6
    for sgn in (1, -1):
        px, py = 20 + math.cos(ang) * 30 * sgn, 30 + math.sin(ang) * 30 * sgn
        ctx.move_to(20, 30); ctx.line_to(px, py); ctx.stroke()
        ctx.move_to(px - 12, py); ctx.line_to(px + 12, py); ctx.stroke()
    ctx.restore()


def clock_icon(ctx, cx, cy, r, a, t, lab=None, col=AM):
    if a <= 0: return
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    for ang, ln in ((t * 0.8, r * 0.7), (t * 0.07, r * 0.45)):
        ctx.move_to(cx, cy); ctx.line_to(cx + math.sin(ang) * ln, cy - math.cos(ang) * ln)
        ctx.set_source_rgba(*WH, a); ctx.set_line_width(5); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    if lab:
        text(ctx, lab, cx, cy + r + 50, F_BIG, 48, col, a, align="center")


def check(ctx, x, y, a, col=GR):
    ctx.move_to(x - 20, y); ctx.line_to(x - 5, y + 16); ctx.line_to(x + 22, y - 18)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def cross(ctx, x, y, a, col=RD):
    ctx.move_to(x - 18, y - 18); ctx.line_to(x + 18, y + 18); ctx.move_to(x + 18, y - 18); ctx.line_to(x - 18, y + 18)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def moments(ctx, u, t, states, k):
    """tres tarjetas: ANTES / DURANTE / DESPUÉS; states = [(alpha, mark)] mark: 'ok','no',None"""
    labs = ["ANTES", "DURANTE", "DESPUÉS"]
    for j, lab in enumerate(labs):
        cx = 250 + j * 290
        ka, mark = states[j]
        a = k * (0.35 + 0.65 * ka)
        col = GR if mark == "ok" else RD if mark == "no" else BR
        rrect(ctx, cx - 125, 560, 250, 400, 30); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
        text(ctx, lab, cx, 630, F_BIG, 48, WH, a, align="center")
        if j == 1:
            book(ctx, cx, 760, 0.55, a); bike(ctx, cx, 850, 0.45, a, t)
        else:
            if j == 0:
                bike(ctx, cx, 730, 0.5, a, t); book(ctx, cx, 850, 0.5, a)
            else:
                book(ctx, cx, 730, 0.5, a); bike(ctx, cx, 860, 0.5, a, t)
        if mark and ka > 0:
            kk = easeb(ka)
            ctx.new_path(); ctx.arc(cx, 1020, 40, 0, 6.283); ctx.set_source_rgba(*col, 0.2 * kk); ctx.fill_preserve(); ctx.set_source_rgba(*col, kk); ctx.set_line_width(4); ctx.stroke()
            (check if mark == "ok" else cross)(ctx, cx, 1020, kk, col)


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        brain(ctx, 540, 760, 1.25, t, k, BR, fire=0.5)
        kq = easeb((u - lt(0) - 2.6) / 0.5)
        if kq > 0:
            ctx.save(); ctx.translate(540, 1040); ctx.scale(kq, kq)
            text(ctx, "¿CUÁNDO MOVERTE?", 0, 0, F_BIG, 84, AM, 1, align="center"); ctx.restore()
    elif i == 1:
        n = int(clamp((u - 0.2) / 2.2) * 42)
        for j in range(n):
            c = j % 7; r = j // 7
            x = 225 + c * 105; y = 540 + r * 64
            rrect(ctx, x - 38, y, 76, 46, 10); ctx.set_source_rgba(*BR, 0.18 * k); ctx.fill_preserve(); ctx.set_source_rgba(*BR, 0.9 * k); ctx.set_line_width(3); ctx.stroke()
        kb = easeb((u - lt(1) - 1.6) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 1050); ctx.scale(kb, kb)
            text(ctx, "42 EXPERIMENTOS", 0, 0, F_BIG, 80, AM, 1, align="center"); ctx.restore()
    elif i == 2:
        moments(ctx, u, t, [(ease((u - 0.4) / 0.5), "ok"), (0, None), (0, None)], k)
    elif i == 3:
        moments(ctx, u, t, [(1, "ok"), (ease((u - 0.4) / 0.5), "no"), (0, None)], k)
    elif i == 4:
        moments(ctx, u, t, [(1, "ok"), (1, "no"), (ease((u - 0.4) / 0.5), "ok")], k)
    elif i == 5:
        for j, (lab, col, cx) in enumerate([("ANTES", C2, 330), ("DESPUÉS", ACC, 750)]):
            kj = easeb((u - 0.3 - j * 0.4) / 0.5)
            if kj <= 0: continue
            rrect(ctx, cx - 185, 600, 370, 260, 34); ctx.set_source_rgba(*col, 0.10 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(5); ctx.stroke()
            sz = fit_size(ctx, lab, F_BIG, 100, 320)
            text(ctx, lab, cx, 770, F_BIG, sz, col, kj, align="center")
        cur = "▌" if int(t * 2.5) % 2 == 0 else " "
        text(ctx, "COMENTA: ANTES O DESPUÉS" + cur, 540, 980, F_MONO, 32, AM, ease((u - 1.0) / 0.4), align="center", bold=True)
    elif i == 6:
        # línea de tiempo: aprender -> 4 h -> pedalear -> 48 h -> prueba
        y = 760
        kk = ease((u - 0.2) / 3.0)
        x0, x1 = 170, 910
        ctx.move_to(x0, y); ctx.line_to(x0 + (x1 - x0) * kk, y); ctx.set_source_rgba(*WH, 0.6 * k); ctx.set_line_width(4); ctx.stroke()
        pts = [(170, "APRENDER", C2, 0.0), (480, "+4 H: PEDALEAR", GR, 0.42), (910, "+2 DÍAS: PRUEBA", AM, 1.0)]
        for x, lab, col, f in pts:
            kp = easeb((kk - f + 0.05) / 0.1) if f > 0 else k
            if kp <= 0: continue
            ctx.new_path(); ctx.arc(x, y, 18, 0, 6.283); ctx.set_source_rgba(*col, kp); ctx.fill()
            sz = fit_size(ctx, lab, F_MONO, 26, 300, True)
            al = "left" if x < 300 else "right" if x > 800 else "center"
            text(ctx, lab, x if al == "center" else x - 10 if al == "left" else x + 10, y - 50, F_MONO, sz, col, kp, align=al, bold=True)
        book(ctx, 170, 620 + 300, 0.55, k)
        bike(ctx, 480, 930, 0.6, easeb((kk - 0.37) / 0.1), t)
        kr = easeb((u - lt(6) - 4.6) / 0.5)
        if kr > 0:
            rrect(ctx, 640, 870, 290, 120, 24); ctx.set_source_rgba(*RD, 0.10 * kr); ctx.fill_preserve(); ctx.set_source_rgba(*RD, kr); ctx.set_line_width(4); ctx.stroke()
            text(ctx, "JUSTO DESPUÉS:", 785, 920, F_MONO, 22, WH, kr, align="center", bold=True)
            text(ctx, "SIN EFECTO", 785, 968, F_BIG, 44, RD, kr, align="center")
    elif i == 7:
        brain(ctx, 540, 740, 1.05, t, k, BR, fire=0.6, hippo=(ACC, k))
        kb = easeb((u - lt(7) - 1.2) / 0.5)
        text(ctx, "EFECTO PEQUEÑO, PERO SUMA", 540, 1040, F_BIG, 60, GR, kb, align="center")
    elif i == 8:
        brain(ctx, 540, 700, 1.1, t, k, BR, fire=0.8, hippo=(ACC, k))
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1010); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, AM, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "3 MOMENTOS · CEREBRO", W / 2, 214, CY, k, 28)
        title(ctx, "¿EJERCICIO Y ESTUDIO?", WH, 380, 94, k)
    elif i == 1:
        pill(ctx, "METAANÁLISIS", W / 2, 214, CY, k, 30, filled=True)
        title(ctx, "UNA SESIÓN Y TU MEMORIA", WH, 380, 90, k)
        src(ctx, "Qazi et al., Frontiers in Cognition 2024 · memoria episódica a largo plazo", k, 1130)
    elif i in (2, 3, 4):
        pill(ctx, ["ANTES DE APRENDER", "MIENTRAS APRENDES", "DESPUÉS DE APRENDER"][i - 2], W / 2, 214, [GR, RD, GR][i - 2], k, 30, filled=True)
        title(ctx, ["MEJORÓ UN POCO", "NO CAMBIÓ NADA", "TAMBIÉN AYUDÓ"][i - 2], WH, 380, 96, k)
        src(ctx, "Qazi et al., 2024 · 42 experimentos · doi:10.3389/fcogn.2024.1367569", k, 1130)
    elif i == 5:
        pill(ctx, "COMENTA", W / 2, 214, AM, k, 32, filled=True)
        title(ctx, "¿ENTRENAS ANTES O DESPUÉS?", WH, 380, 88, k)
    elif i == 6:
        pill(ctx, "OTRO ESTUDIO", W / 2, 214, CY, k, 30, filled=True)
        title(ctx, "EL TRUCO DE LAS 4 HORAS", WH, 380, 92, k)
        src(ctx, "van Dongen et al., Current Biology 2016 · 72 personas · doi:10.1016/j.cub.2016.04.071", k, 1110)
    elif i == 7:
        pill(ctx, "CONCLUSIÓN", W / 2, 214, GR, k, 30, filled=True)
        title(ctx, "MUÉVETE ANTES O UN RATO DESPUÉS", WH, 380, 80, k)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 380, 80, k)


run_episode(neon, txt, "EXPEDIENTE 54 · CEREBRO")
