"""v021 · ¿El baño de hielo después de las pesas frena tu músculo? (serie RECUPERACIÓN · paleta hielo glaciar + naranja)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (0.62, 0.93, 1.0)   # hielo
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.03, 0.12, 0.20], [0.004, 0.018, 0.035])
from engine_ext import *
CY = ACC
OR = (1.0, 0.58, 0.26)   # naranja cálido para datos


def ice_cube(ctx, cx, cy, s, a=1.0, rot=0.0, col=CY):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -50, -50, 100, 100, 16)
    ctx.set_source_rgba(*col, 0.14 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(4 / s); ctx.stroke()
    ctx.move_to(-30, -32); ctx.line_to(-8, -32); ctx.set_source_rgba(1, 1, 1, 0.8 * a); ctx.set_line_width(5 / s); ctx.stroke()
    ctx.move_to(-32, -30); ctx.line_to(-32, -6); ctx.stroke()
    ctx.restore()


def tub(ctx, cx, cy, w, h, t, a=1.0):
    rrect(ctx, cx - w / 2, cy - h / 2, w, h, 40)
    ctx.set_source_rgba(*CY, 0.06 * a); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.9 * a); ctx.set_line_width(5); ctx.stroke()
    wy = cy - h / 2 + 70
    ctx.new_path()
    for xi in range(0, int(w) - 40, 6):
        x = cx - w / 2 + 20 + xi
        y = wy + 10 * math.sin(xi / 45 + t * 3)
        (ctx.move_to if xi == 0 else ctx.line_to)(x, y)
    ctx.set_source_rgba(*CY, 0.8 * a); ctx.set_line_width(4); ctx.stroke()
    for j, (dx, rr) in enumerate([(-0.3, 0.3), (0.05, -0.2), (0.32, 0.5)]):
        ice_cube(ctx, cx + dx * w, wy + 6 * math.sin(t * 2 + j), 0.75, a, rr + 0.05 * math.sin(t + j))


def thermo(ctx, x, y, a=1.0, lvl=0.25, col=CY, label="10–15 °C"):
    rrect(ctx, x - 22, y - 260, 44, 260, 22); ctx.set_source_rgba(*col, 0.1 * a); ctx.fill_preserve()
    ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(4); ctx.stroke()
    ctx.new_path(); ctx.arc(x, y + 20, 40, 0, 6.283); ctx.set_source_rgba(*col, 0.85 * a); ctx.fill()
    rrect(ctx, x - 10, y - 240 * lvl, 20, 240 * lvl + 10, 10); ctx.fill()
    text(ctx, label, x, y + 110, F_MONO, 26, col, a, align="center", bold=True)


def snow(ctx, t, a=1.0, n=26):
    for k in range(n):
        x = (k * 173.3) % W
        y = 360 + ((t * 60 + k * 97) % 900)
        ctx.new_path(); ctx.arc(x, y, 3 + (k % 3), 0, 6.283); ctx.set_source_rgba(1, 1, 1, 0.35 * a); ctx.fill()


def fiber_xs(ctx, cx, cy, r, a=1.0, col=OR, frost=0.0, t=0.0):
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283)
    ctx.set_source_rgba(*col, 0.16 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(5); ctx.stroke()
    for k in range(7):
        ang = k / 7 * 6.283 + 0.4
        ctx.new_path(); ctx.arc(cx + math.cos(ang) * r * 0.9, cy + math.sin(ang) * r * 0.9, 7, 0, 6.283)
        ctx.set_source_rgba(1, 1, 1, 0.8 * a); ctx.fill()
    if frost > 0:
        for k in range(6):
            ang = k / 6 * 6.283
            ctx.move_to(cx, cy); ctx.line_to(cx + math.cos(ang) * r * 0.55, cy + math.sin(ang) * r * 0.55)
        ctx.set_source_rgba(*CY, 0.7 * frost * a); ctx.set_line_width(4); ctx.stroke()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        snow(ctx, t, k)
        tub(ctx, 520, 820, 600, 380, t, k)
        thermo(ctx, 900, 900, ease((u - 0.8) / 0.5))
        barbell_icon(ctx, 540, 520, t, a=ease((u - 1.8) / 0.5) * 0.9)
    elif i == 1:
        tub(ctx, 540, 690, 520, 300, t, k)
        n = int(52 * ease((u - 0.8) / 1.6))
        big(ctx, str(n), 540, 1060, 170, OR, ease((u - 0.6) / 0.4))
    elif i == 2:
        for j in range(12):
            kk = ease((u - 0.5 - j * 0.25) / 0.3)
            x = 150 + (j % 6) * 136; y = 560 + (j // 6) * 136
            rrect(ctx, x, y, 112, 112, 16); ctx.set_source_rgba(*CY, 0.12 * kk * k); ctx.fill_preserve()
            ctx.set_source_rgba(*CY, kk * k); ctx.set_line_width(3); ctx.stroke()
            text(ctx, str(j + 1), x + 56, y + 70, F_MONO, 34, WH, kk * k, align="center", bold=True)
        ka = ease((u - 4.0) / 0.4)
        for j, (lab, col, x) in enumerate((("RECUPERACIÓN ACTIVA", OR, 300), ("AGUA FRÍA 10 MIN", CY, 780))):
            rrect(ctx, x - 215, 900, 430, 90, 45); ctx.set_source_rgba(*col, 0.12 * ka); ctx.fill_preserve()
            ctx.set_source_rgba(*col, ka); ctx.set_line_width(4); ctx.stroke()
            text(ctx, lab, x, 957, F_MONO, 26, col, ka, align="center", bold=True)
    elif i == 3:
        k1 = ease((u - 0.4) / 1.2); k2 = ease((u - 3.0) / 0.6)
        fiber_xs(ctx, 280, 780, 130 * (1 + 0.085 * k1), k, col=OR)
        ctx.set_dash([10, 10]); ctx.new_path(); ctx.arc(280, 780, 130, 0, 6.283); ctx.set_source_rgba(1, 1, 1, 0.35 * k); ctx.set_line_width(2); ctx.stroke(); ctx.set_dash([])
        fiber_xs(ctx, 740, 780, 130, k2, col=CY, frost=1.0, t=t)
        ctx.set_dash([10, 10]); ctx.new_path(); ctx.arc(740, 780, 130, 0, 6.283); ctx.set_source_rgba(1, 1, 1, 0.35 * k2); ctx.set_line_width(2); ctx.stroke(); ctx.set_dash([])
        big(ctx, "+17 %", 280, 1040, 110, OR, ease((u - 1.4) / 0.4), maxw=420)
        big(ctx, "≈ 0", 740, 1040, 110, CY, ease((u - 3.4) / 0.4), maxw=420)
    elif i == 4:
        fiber_bundle(ctx, 170, 640, 740, 300, 6, 0.0 if u > 2.2 else 1.0, t, k, col_on=OR, col_off=CY)
        nerve(ctx, [(120, 560), (360, 600), (620, 560), (960, 600)], t, k * (1 - 0.7 * ease((u - 1.8) / 0.6)), col=OR, rate=1.2)
        snow(ctx, t, ease((u - 1.6) / 0.6), n=18)
    elif i == 5:
        items = [("SOLO\nPESAS", 0.36 / 0.40, OR), ("PESAS +\nFRÍO", 0.14 / 0.40, CY)]
        kb = ease((u - 0.4) / 1.6)
        vbars(ctx, items, 300, 1060, 190, 100, 460, kb, k, label_size=24)
        text(ctx, "0,36", 395, 1060 - 460 * 0.9 * kb - 18, F_MONO, 32, WH, k * clamp(kb * 2 - 1), align="center", bold=True)
        text(ctx, "0,14", 685, 1060 - 460 * 0.35 * kb - 18, F_MONO, 32, WH, k * clamp(kb * 2 - 1), align="center", bold=True)
    elif i == 6:
        barbell_icon(ctx, 540, 560, t, a=k)
        ka = ease((u - 1.6) / 0.4)
        ice_cube(ctx, 540, 1000, 1.0, ka, 0.1)
        ctx.move_to(455, 915); ctx.line_to(625, 1085); ctx.move_to(625, 915); ctx.line_to(455, 1085)
        ctx.set_source_rgba(*RD, ka); ctx.set_line_width(12); ctx.stroke()
    elif i == 7:
        tub(ctx, 540, 720, 520, 300, t, k)
        ka = ease((u - 2.4) / 0.4)
        for j, (lab, col, x) in enumerate((("HOY", OR, 330), ("MAÑANA", GR, 750))):
            rrect(ctx, x - 140, 940, 280, 110, 24); ctx.set_source_rgba(*col, 0.12 * ka); ctx.fill_preserve()
            ctx.set_source_rgba(*col, ka); ctx.set_line_width(4); ctx.stroke()
            text(ctx, lab, x, 1008, F_MONO, 34, col, ka, align="center", bold=True)
        ctx.move_to(480, 995); ctx.line_to(600, 995); ctx.set_source_rgba(1, 1, 1, ka); ctx.set_line_width(5); ctx.stroke()
        ctx.move_to(585, 980); ctx.line_to(605, 995); ctx.line_to(585, 1010); ctx.stroke()
    elif i == 8:
        snow(ctx, t, k, n=14)
        ice_cube(ctx, 540, 610, 1.6, k, 0.15 * math.sin(t))
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1000); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 170, CY, 1, align="center"); ctx.restore()


def src(ctx, s, k, y=1290):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "MITO VS. REALIDAD · RECUPERACIÓN", W / 2, 196, CY, k, 28)
        title(ctx, "¿HIELO TRAS LAS PESAS?", WH, 350, 100, k)
        text(ctx, "¿TE RECUPERA O TE FRENA?", W / 2, 1160, F_MONO, 34, OR, ease((u - 2.6) / 0.4), align="center", bold=True)
    elif i == 1:
        pill(ctx, "SPORTS MEDICINE · 2022", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "PARA RECUPERARTE: SÍ", WH, 345, 100, k)
        text(ctx, "ESTUDIOS · MENOS DOLOR A LAS 24 H", W / 2, 1150, F_MONO, 30, OR, ease((u - 3.2) / 0.4), align="center", bold=True)
        src(ctx, "Moore et al., Sports Med 2022 · doi:10.1007/s40279-022-01644-9", k, 1225)
    elif i == 2:
        pill(ctx, "J PHYSIOL · 2015", W / 2, 196, OR, k, 30, filled=True)
        title(ctx, "12 SEMANAS DE FUERZA", WH, 345, 100, k)
        text(ctx, "21 HOMBRES ACTIVOS · 2 DÍAS/SEMANA", W / 2, 450, F_MONO, 28, MU, k, align="center", bold=True)
        text(ctx, "CON FRÍO: MENOS MÚSCULO Y FUERZA", W / 2, 1100, F_MONO, 32, CY, ease((u - 5.2) / 0.4), align="center", bold=True)
        src(ctx, "Roberts et al., J Physiol 2015 · doi:10.1113/JP270570", k, 1190)
    elif i == 3:
        pill(ctx, "FIBRAS TIPO II (RÁPIDAS)", W / 2, 196, OR, k, 28)
        title(ctx, "ÁREA DE LA FIBRA", WH, 345, 100, k)
        text(ctx, "SIN FRÍO", 280, 560, F_MONO, 32, OR, k, align="center", bold=True)
        text(ctx, "CON FRÍO", 740, 560, F_MONO, 32, CY, ease((u - 3.0) / 0.4), align="center", bold=True)
        text(ctx, "SIN AUMENTO SIGNIFICATIVO", 740, 1100, F_MONO, 19, MU, ease((u - 3.6) / 0.4), align="center")
        src(ctx, "esquema · Roberts et al., J Physiol 2015", k, 1190)
    elif i == 4:
        pill(ctx, "¿POR QUÉ?", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "EL FRÍO FRENA LA SEÑAL", WH, 345, 96, k)
        text(ctx, "SEÑAL DE CRECIMIENTO (p70S6K) ↓", W / 2, 1080, F_MONO, 30, OR, ease((u - 1.6) / 0.4), align="center", bold=True)
        text(ctx, "CÉLULAS SATÉLITE ↓", W / 2, 1135, F_MONO, 30, CY, ease((u - 3.4) / 0.4), align="center", bold=True)
        src(ctx, "esquema · Roberts et al., J Physiol 2015", k, 1210)
    elif i == 5:
        pill(ctx, "METAANÁLISIS · 8 ESTUDIOS", W / 2, 196, OR, k, 28, filled=True)
        title(ctx, "LA MISMA TENDENCIA", WH, 345, 100, k)
        text(ctx, "TAMAÑO DEL EFECTO EN HIPERTROFIA", W / 2, 450, F_MONO, 26, MU, k, align="center", bold=True)
        text(ctx, "EVIDENCIA LIMITADA · CALIDAD REGULAR-BAJA", W / 2, 1180, F_MONO, 26, AM, ease((u - 4.2) / 0.4), align="center", bold=True)
        src(ctx, "Piñero et al., Eur J Sport Sci 2024 · doi:10.1002/ejsc.12074", k, 1240)
    elif i == 6:
        pill(ctx, "META: MÚSCULO", W / 2, 196, OR, k, 30, filled=True)
        title(ctx, "SIN HIELO JUSTO DESPUÉS", WH, 345, 92, k)
        text(ctx, "SOBRE TODO SI ES RUTINA", W / 2, 1185, F_MONO, 30, MU, ease((u - 2.4) / 0.4), align="center", bold=True)
    elif i == 7:
        pill(ctx, "META: RECUPERAR RÁPIDO", W / 2, 196, GR, k, 28, filled=True)
        title(ctx, "AHÍ SÍ PUEDE SERVIR", WH, 345, 100, k)
        src(ctx, "Tornero-Aguilera et al., Exp Physiol 2026 · doi:10.1113/EP094042", k, 1190)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)


run_episode(neon, txt, "EXPEDIENTE 21 · RECUPERACIÓN")
