"""v024 · ¿Solo aprovechas 30 g de proteína por comida? Estudio explicado (serie MÚSCULO-NUTRICIÓN · paleta tinta + mantequilla + cobalto)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (1.0, 0.83, 0.32)   # mantequilla
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.035, 0.055, 0.13], [0.006, 0.01, 0.03])
from engine_ext import *
CY = ACC
IC = (0.45, 0.70, 1.0)   # cobalto para datos


def glass(ctx, cx, base, h, lvl, a=1.0, col=None, label=None, t=0.0):
    col = col or IC
    wt, wb = h * 0.62, h * 0.48
    def outline():
        ctx.new_path(); ctx.move_to(cx - wt / 2, base - h); ctx.line_to(cx - wb / 2, base); ctx.line_to(cx + wb / 2, base); ctx.line_to(cx + wt / 2, base - h)
    # liquid
    if lvl > 0:
        ly = base - h * lvl
        wl = wb + (wt - wb) * lvl
        ctx.new_path(); ctx.move_to(cx - wb / 2, base); ctx.line_to(cx - wl / 2, ly)
        for s in range(21):
            xx = cx - wl / 2 + wl * s / 20
            ctx.line_to(xx, ly + 4 * math.sin(t * 4 + s * 0.8))
        ctx.line_to(cx + wb / 2, base); ctx.close_path()
        ctx.set_source_rgba(*col, 0.30 * a); ctx.fill()
    outline(); ctx.set_source_rgba(1, 1, 1, 0.85 * a); ctx.set_line_width(5); ctx.stroke()
    if label:
        text(ctx, label, cx, base + 62, F_BIG, 58, col, a, align="center")


def amino(ctx, x, y, r, col, a):
    ctx.new_path()
    for k in range(6):
        ang = k * math.pi / 3 + math.pi / 6
        (ctx.move_to if k == 0 else ctx.line_to)(x + math.cos(ang) * r, y + math.sin(ang) * r)
    ctx.close_path(); ctx.set_source_rgba(*col, 0.25 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()


def flame(ctx, cx, cy, s, a, col=RD, t=0.0):
    fl = 1 + 0.06 * math.sin(t * 9)
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s * fl)
    ctx.new_path(); ctx.move_to(0, -90); ctx.curve_to(50, -30, 60, 20, 0, 60); ctx.curve_to(-60, 20, -50, -30, 0, -90)
    ctx.restore(); ctx.set_source_rgba(*col, 0.15 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(5); ctx.stroke()


def src(ctx, s, k, y=1270):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        glass(ctx, 540, 1080, 460, 0.25 + 0.55 * ease((u - 0.3) / 2.0), k, t=t)
        ka = ease((u - 2.2) / 0.4)
        y30 = 1080 - 460 * 0.32
        ctx.set_dash([20, 14]); ctx.move_to(200, y30); ctx.line_to(960, y30)
        ctx.set_source_rgba(*RD, ka); ctx.set_line_width(5); ctx.stroke(); ctx.set_dash([])
        text(ctx, "¿LÍMITE 30 g?", 960, y30 - 22, F_MONO, 30, RD, ka, align="right", bold=True)
    elif i == 1:
        glass(ctx, 330, 1060, 300, 0.25 * ease((u - 0.3) / 0.8), k, label="25 g", t=t)
        glass(ctx, 750, 1060, 420, 0.95 * ease((u - 1.6) / 1.4), k, col=CY, label="100 g", t=t)
        pass
    elif i == 2:
        # vaso → sangre → músculo
        glass(ctx, 190, 900, 220, 0.7, k, t=t)
        pts = [(260, 760), (420, 640), (620, 700), (760, 820)]
        ctx.new_path(); ctx.move_to(*pts[0])
        for p in pts[1:]: ctx.line_to(*p)
        ctx.set_source_rgba(*RD, 0.35 * k); ctx.set_line_width(26); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        for j in range(9):
            f = ((t * 0.35 + j / 9) % 1)
            x, y = polyline_point(pts, f)
            amino(ctx, x, y, 14, CY, k * ease((u - 0.5) / 0.5))
        fiber_bundle(ctx, 700, 840, 300, 230, 7, ease((u - 2.0) / 1.2), t, k, col_on=CY, col_off=IC)
        clock(ctx, 300, 1150, 70, t, back=0, a=ease((u - 3.4) / 0.4), col=IC)
        text(ctx, "12 h", 420, 1170, F_BIG, 64, WH, ease((u - 3.4) / 0.4))
    elif i == 3:
        f25 = lambda x: 0.55 * math.exp(-((x - 0.17) / 0.14) ** 2) + 0.05
        f100 = lambda x: 0.12 + 0.68 * (1 - math.exp(-x / 0.12)) * (1 - 0.25 * x)
        up = ease((u - 0.3) / 2.4)
        line_chart(ctx, 170, 600, 740, 420, [(f25, IC, up, False), (f100, CY, up, True)],
                   [(0, "0 h"), (0.5, "6 h"), (1, "12 h")], "", "SÍNTESIS PROTEICA", k)
        ka = ease((u - 2.6) / 0.4)
        text(ctx, "100 g", 880, 690, F_MONO, 30, CY, ka, align="right", bold=True)
        text(ctx, "25 g", 880, 960, F_MONO, 30, IC, ka, align="right", bold=True)
    elif i == 4:
        flame(ctx, 540, 820, 1.6, k * 0.6, col=RD, t=t)
        gauge(ctx, 540, 840, 210, 0.12 + 0.02 * math.sin(t * 3), ease((u - 0.8) / 0.4), col=IC)
        for j in range(6):
            amino(ctx, 250 + j * 116, 1140, 18, CY, ease((u - 1.6 - j * 0.12) / 0.4))
    elif i == 5:
        glass(ctx, 300, 1000, 260, 0.8, k, col=CY, label="1 COMIDA", t=t)
        ka = ease((u - 2.0) / 0.4)
        rrect(ctx, 610, 700, 300, 300, 26); ctx.set_source_rgba(*MU, 0.08 * ka); ctx.fill_preserve(); ctx.set_source_rgba(*MU, 0.8 * ka); ctx.set_line_width(4); ctx.stroke()
        for r in range(4):
            for c in range(5):
                ctx.new_path(); ctx.arc(650 + c * 55, 770 + r * 60, 12, 0, 6.283); ctx.set_source_rgba(*MU, 0.6 * ka); ctx.fill()
        big(ctx, "?", 760, 1090, 110, RD, ease((u - 2.6) / 0.4))
    elif i == 6:
        def fb(x):
            g = x * 2.6  # g/kg en eje 0–2,6
            return 0.12 + 0.62 * min(g, 1.62) / 1.62
        line_chart(ctx, 170, 620, 740, 400, [(fb, CY, ease((u - 0.4) / 2.6), True)],
                   [(0, "0"), (0.385, "1"), (0.623, "1,6"), (0.77, "2"), (1, "2,6")], "g / kg / día", "MASA MAGRA GANADA", k)
        ka = ease((u - 4.4) / 0.4)
        x16 = 170 + 0.623 * 740
        ctx.set_dash([14, 10]); ctx.move_to(x16, 620); ctx.line_to(x16, 1020); ctx.set_source_rgba(*IC, ka); ctx.set_line_width(4); ctx.stroke(); ctx.set_dash([])
        text(ctx, "≈1,6", x16, 600, F_BIG, 56, IC, ka, align="center")
    elif i == 7:
        hk = ease((u - 0.6) / 0.6)
        skeleton(ctx, 380, 520, 0.55, t, hl={"arms": (CY, hk), "legs": (CY, hk), "spine": (CY, hk)}, base_a=0.75 * k)
        items = [("DES", 0.45, IC), ("ALM", 0.65, IC), ("CENA", 0.55, IC)]
        vbars(ctx, items, 640, 1060, 80, 30, 380, ease((u - 1.6) / 1.0), k, label_size=22)
        text(ctx, "= TOTAL DIARIO", 790, 1160, F_MONO, 28, CY, ease((u - 3.0) / 0.4), align="center", bold=True)
    elif i == 8:
        glass(ctx, 540, 820, 300, 0.75, k, col=CY, t=t)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1010); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 150, CY, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "ESTUDIO EXPLICADO · PROTEÍNA", W / 2, 196, CY, k, 28)
        title(ctx, "¿SOLO 30 g POR COMIDA?", WH, 350, 100, k)
    elif i == 1:
        pill(ctx, "MAASTRICHT · 2023", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "25 g VS. 100 g", WH, 345, 110, k)
        text(ctx, "HOMBRES JÓVENES SANOS · TRAS ENTRENAR FUERZA", W / 2, 440, F_MONO, 24, MU, k, align="center", bold=True)
        src(ctx, "Trommelen et al., Cell Rep Med 2023 · doi:10.1016/j.xcrm.2023.101324", ease((u - 1.0) / 0.4), 1250)
    elif i == 2:
        pill(ctx, "ISÓTOPOS MARCADOS", W / 2, 196, IC, k, 28, filled=True)
        title(ctx, "SEGUIR CADA AMINOÁCIDO", WH, 345, 92, k)
        text(ctx, "SANGRE → MÚSCULO", W / 2, 1270, F_MONO, 28, MU, ease((u - 1.4) / 0.4), align="center", bold=True)
    elif i == 3:
        pill(ctx, "RESULTADO", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "MÁS Y POR MÁS TIEMPO", WH, 345, 100, k)
        text(ctx, "ESQUEMA ILUSTRATIVO · NO SON DATOS EXACTOS", W / 2, 1130, F_MONO, 22, AM, ease((u - 1.0) / 0.4), align="center", bold=True)
        src(ctx, "Trommelen et al., Cell Rep Med 2023", k, 1185)
    elif i == 4:
        pill(ctx, "¿SE DESPERDICIA?", W / 2, 196, RD, k, 30)
        title(ctx, "CASI NO SE QUEMÓ", WH, 345, 106, k)
        text(ctx, "OXIDACIÓN DE AMINOÁCIDOS ≈ IGUAL", W / 2, 1230, F_MONO, 28, IC, ease((u - 1.2) / 0.4), align="center", bold=True)
        src(ctx, "Trommelen et al., Cell Rep Med 2023", k, 1280)
    elif i == 5:
        pill(ctx, "OJO", W / 2, 196, RD, k, 30)
        title(ctx, "UNA COMIDA ≠ MESES", WH, 345, 104, k)
        text(ctx, "NO MIDIÓ GANANCIA DE MÚSCULO", W / 2, 1230, F_MONO, 28, AM, ease((u - 2.4) / 0.4), align="center", bold=True)
    elif i == 6:
        pill(ctx, "METAANÁLISIS · 49 ENSAYOS", W / 2, 196, IC, k, 28, filled=True)
        title(ctx, "MANDA EL TOTAL DEL DÍA", WH, 345, 94, k)
        text(ctx, "ESQUEMA DEL PUNTO DE QUIEBRE", W / 2, 1150, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Morton et al., Br J Sports Med 2018 · 1.863 personas · doi:10.1136/bjsports-2017-097608", k, 1200)
    elif i == 7:
        pill(ctx, "LA IDEA", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "TOTAL DIARIO + FUERZA", WH, 345, 100, k)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)


run_episode(neon, txt, "EXPEDIENTE 24 · PROTEÍNA")
