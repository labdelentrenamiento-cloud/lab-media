"""v016 · Si quisieras vivir más con pesas: ¿cuántos minutos? (serie LONGEVIDAD-FUERZA · paleta coral)
Uso: copiar a la carpeta del episodio (con timeline.json) y correr
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

# ---- paleta de la serie LONGEVIDAD-FUERZA (acento coral, fondo vino profundo)
ACC = (1.0, 0.56, 0.44)
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.20, 0.05, 0.09], [0.03, 0.006, 0.015])
from engine_ext import *
CY = ACC
TL = (0.36, 0.95, 0.85)   # turquesa para datos


def hourglass(ctx, cx, cy, s, t, a):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.move_to(-110, -170); ctx.line_to(110, -170); ctx.line_to(14, 0); ctx.line_to(110, 170); ctx.line_to(-110, 170); ctx.line_to(-14, 0); ctx.close_path()
    ctx.set_source_rgba(*CY, 0.08 * a); ctx.fill_preserve(); ctx.set_source_rgba(*CY, a); ctx.set_line_width(6); ctx.stroke()
    for y in (-185, 185):
        rrect(ctx, -135, y - 12, 270, 24, 10); ctx.set_source_rgba(*AM, a); ctx.fill()
    f = (t * 0.15) % 1
    top = 1 - f
    ctx.move_to(-90 * top, -150 + 140 * (1 - top)); ctx.line_to(90 * top, -150 + 140 * (1 - top)); ctx.line_to(0, -10); ctx.close_path()
    ctx.set_source_rgba(*AM, 0.7 * a); ctx.fill()
    hb = 150 * f
    ctx.move_to(-100 * min(1, f + 0.3), 165); ctx.line_to(100 * min(1, f + 0.3), 165); ctx.line_to(0, 165 - hb); ctx.close_path()
    ctx.set_source_rgba(*AM, 0.7 * a); ctx.fill()
    for j in range(6):
        yy = -5 + ((t * 2.5 + j / 6) % 1) * (160 - hb)
        ctx.new_path(); ctx.arc(0, yy, 3, 0, 6.283); ctx.set_source_rgba(*AM, a); ctx.fill()
    ctx.restore()


def risk(x):
    """esquema: riesgo relativo vs minutos/semana (0..150) – curva en J, mínimo ~60 min = 0.73"""
    m = x * 150
    if m <= 60:
        return 1.0 - 0.27 * (1 - (1 - m / 60) ** 2)
    return 0.73 + 0.10 * ((m - 60) / 90) ** 1.6


def jcurve(ctx, x0, y0, w, h, upto, a, mark=0.0, shade=0.0):
    lo, hi = 0.6, 1.05
    Y = lambda r: y0 + h - (r - lo) / (hi - lo) * h
    ctx.set_line_width(2)
    for i in range(5):
        yy = y0 + h - i * h / 4
        ctx.move_to(x0, yy); ctx.line_to(x0 + w, yy); ctx.set_source_rgba(*CY, 0.12 * a); ctx.stroke()
    ctx.move_to(x0, y0); ctx.line_to(x0, y0 + h); ctx.line_to(x0 + w, y0 + h); ctx.set_source_rgba(*CY, 0.6 * a); ctx.set_line_width(3); ctx.stroke()
    for m in (0, 30, 60, 90, 120, 150):
        text(ctx, str(m), x0 + m / 150 * w, y0 + h + 40, F_MONO, 24, MU, a, align="center")
    text(ctx, "MIN/SEMANA DE FUERZA", x0 + w, y0 + h + 82, F_MONO, 22, MU, a, align="right")
    text(ctx, "RIESGO DE MORIR", x0, y0 - 18, F_MONO, 22, MU, a)
    # línea base 1.0
    ctx.move_to(x0, Y(1.0)); ctx.line_to(x0 + w, Y(1.0)); ctx.set_dash([10, 10]); ctx.set_source_rgba(*WH, 0.35 * a); ctx.stroke(); ctx.set_dash([])
    if shade > 0:
        xs = x0 + 60 / 150 * w
        rrect(ctx, xs, y0, (x0 + w - xs) * shade, h, 10); ctx.set_source_rgba(*AM, 0.12 * a); ctx.fill()
    n = max(2, int(100 * upto))
    pts = [(x0 + (i / 100) * w, Y(risk(i / 100))) for i in range(n + 1)]
    ctx.new_path(); ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    ctx.set_source_rgba(*TL, a); ctx.set_line_width(7); ctx.stroke()
    ctx.new_path(); ctx.arc(*pts[-1], 10, 0, 6.283); ctx.set_source_rgba(*WH, a); ctx.fill()
    if mark > 0:
        mx, my = x0 + 60 / 150 * w, Y(0.73)
        ctx.new_path(); ctx.arc(mx, my, 18 + 4 * math.sin(mark * 9), 0, 6.283); ctx.set_source_rgba(*GR, 0.9 * mark * a); ctx.set_line_width(5); ctx.stroke()
        ctx.move_to(mx, my + 24); ctx.line_to(mx, y0 + h); ctx.set_dash([6, 8]); ctx.set_source_rgba(*GR, 0.7 * mark * a); ctx.set_line_width(3); ctx.stroke(); ctx.set_dash([])


def week(ctx, k, a, days=(1, 3), y=640):
    labs = ["L", "M", "M", "J", "V", "S", "D"]
    sz = 122
    x0 = (W - 7 * sz + 14) / 2
    for d in range(7):
        x = x0 + d * sz
        on = d in days and ease((k - days.index(d) * 0.3) / 0.4) > 0 if d in days else False
        kk = ease((k - (days.index(d) * 0.3 if d in days else 0)) / 0.4) if d in days else 0
        rrect(ctx, x, y, sz - 14, 260, 18)
        col = GR if on else CY
        ctx.set_source_rgba(*col, (0.06 + 0.2 * kk) * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, (0.5 + 0.5 * kk) * a); ctx.set_line_width(3); ctx.stroke()
        text(ctx, labs[d], x + (sz - 14) / 2, y + 60, F_BIG, 48, WH, a, align="center")
        if on:
            ctx.save(); ctx.translate(x + (sz - 14) / 2, y + 150); ctx.scale(0.3, 0.3)
            ctx.move_to(-150, 0); ctx.line_to(150, 0); ctx.set_source_rgba(*GR, kk * a); ctx.set_line_width(16); ctx.stroke()
            for sgn in (-1, 1):
                rrect(ctx, sgn * 110 - 18, -70, 36, 140, 8); ctx.set_source_rgba(*GR, kk * a); ctx.fill()
            ctx.restore()
            text(ctx, "20–30'", x + (sz - 14) / 2, y + 225, F_MONO, 24, GR, kk * a, align="center", bold=True)


def neq(ctx, k, a):
    for j, (lab, col, x) in enumerate((("ASOCIACIÓN", TL, 290), ("CAUSA", AM, 790))):
        kk = ease((k - j * 0.35) / 0.4)
        ctx.new_path(); ctx.arc(x, 800, 150, 0, 6.283); ctx.set_source_rgba(*col, 0.1 * kk * a); ctx.fill_preserve()
        ctx.set_source_rgba(*col, kk * a); ctx.set_line_width(5); ctx.stroke()
        big(ctx, lab, x, 820, 54, col, kk * a, maxw=260)
    ka = ease((k - 0.8) / 0.3) * a
    if ka > 0:
        for dy in (-22, 22):
            ctx.move_to(500, 800 + dy); ctx.line_to(580, 800 + dy)
        ctx.move_to(560, 740); ctx.line_to(520, 860)
        ctx.set_source_rgba(*WH, ka); ctx.set_line_width(14); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        hourglass(ctx, 540, 720, 1.0, t, k)
        barbell_icon(ctx, 540, 1070, t, a=ease((u - 0.8) / 0.4))
    elif i == 1:
        big(ctx, "30–60", 540, 860, 260, TL, easeb((u - 0.2) / 0.5) * k, maxw=900)
        big(ctx, "MIN / SEMANA", 540, 1000, 90, CY, ease((u - 0.9) / 0.4))
    elif i == 2:
        v = 10 + 7 * ease((u - 0.8) / 1.4)
        big(ctx, "−10 a −%d %%" % round(v), 540, 700, 150, GR, ease((u - 0.5) / 0.4), maxw=900)
    elif i == 3:
        jcurve(ctx, 150, 560, 800, 460, ease((u - 0.2) / 2.2), k, mark=ease((u - 2.2) / 0.4))
        big(ctx, "−27 %", 540, 1200, 110, GR, ease((u - 2.4) / 0.4))
    elif i == 4:
        jcurve(ctx, 150, 560, 800, 460, 1.0, k, mark=1.0, shade=ease((u - 0.4) / 1.0))
    elif i == 5:
        neq(ctx, ease((u - 0.2) / 1.6), k)
    elif i == 6:
        week(ctx, ease((u - 0.6) / 2.2), k)
    elif i == 7:
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 820); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 190, CY, 1, align="center"); ctx.restore()


def src(ctx, s, k, y=1290):
    text(ctx, s, W / 2, y, F_MONO, 21, MU, k, align="center")


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "SI QUISIERAS… · LONGEVIDAD", W / 2, 196, CY, k, 28)
        title(ctx, "¿CUÁNTA FUERZA PARA VIVIR MÁS?", WH, 350, 88, k)
    elif i == 1:
        pill(ctx, "LA RESPUESTA", W / 2, 196, TL, k, 30, filled=True)
        title(ctx, "MENOS DE LO QUE CREES", WH, 345, 92, k)
        src(ctx, "Momma et al., Br J Sports Med 2022 · Shailendra et al., Am J Prev Med 2022", k, 1240)
    elif i == 2:
        pill(ctx, "METAANÁLISIS · 16 ESTUDIOS", W / 2, 196, CY, k, 28)
        title(ctx, "MENOS RIESGO DE…", WH, 345, 96, k)
        for j, (lab, col) in enumerate((("MORIR POR CUALQUIER CAUSA", GR), ("ENFERMEDAD CARDIOVASCULAR", TL), ("CÁNCER", AM), ("DIABETES", CY))):
            a = ease((u - 2.0 - j * 1.3) / 0.4)
            pill(ctx, lab, W / 2, 830 + j * 92, col, a, 34, filled=(j == 0))
        src(ctx, "cohortes de adultos · Momma et al., Br J Sports Med 2022", k, 1250)
    elif i == 3:
        pill(ctx, "OTRO METAANÁLISIS · AM J PREV MED 2022", W / 2, 196, CY, k, 26)
        title(ctx, "MÁXIMO CERCA DE 60 MIN", GR, 345, 92, k)
        src(ctx, "esquema ilustrativo · Shailendra et al., 2022", k, 1265)
    elif i == 4:
        pill(ctx, "MÁS DE 60 MIN", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "SIN BENEFICIO EXTRA", AM, 345, 96, k)
        text(ctx, "ZONA > 60 MIN", 760, 600, F_MONO, 26, AM, ease((u - 0.6) / 0.4), align="center", bold=True)
        src(ctx, "esquema ilustrativo · curva en J · Momma 2022 y Shailendra 2022", k, 1200)
    elif i == 5:
        pill(ctx, "OJO", W / 2, 196, RD, k, 30)
        title(ctx, "ESTUDIOS OBSERVACIONALES", WH, 345, 88, k)
        src(ctx, "los que entrenan fuerza pueden diferir en otros hábitos", k, 1150)
    elif i == 6:
        pill(ctx, "PARA EMPEZAR", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "2 SESIONES POR SEMANA", GR, 345, 92, k)
        a = ease((u - 2.4) / 0.4)
        text(ctx, "GRANDES GRUPOS MUSCULARES", W / 2, 1010, F_MONO, 30, WH, a, align="center", bold=True)
        src(ctx, "OMS 2020: fuerza ≥ 2 días/semana · Bull et al., Br J Sports Med 2020", k, 1240)
    elif i == 7:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)
        a = ease((u - 0.8) / 0.4)
        if a > 0:
            pulse = 1 + 0.04 * math.sin(t * 7)
            ctx.save(); ctx.translate(540, 1000); ctx.scale(pulse, pulse)
            rrect(ctx, -170, -50, 340, 100, 50); ctx.set_source_rgba(*RD, a); ctx.fill()
            text(ctx, "SEGUIR", 0, 18, F_UI, 50, WH, a, align="center", bold=True); ctx.restore()


run_episode(neon, txt, "EXPEDIENTE 16 · LONGEVIDAD")
