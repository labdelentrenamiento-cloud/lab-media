"""v020 · ¿Qué pasa si subes escaleras a toda prisa 3 veces al día? (serie CORAZÓN · paleta rubí + oro)
Uso: copiar a la carpeta del episodio (con timeline.json) y correr
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

# ---- paleta de la serie CORAZÓN (acento rubí, fondo vino profundo, datos en oro)
ACC = (1.0, 0.33, 0.42)
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.17, 0.03, 0.06], [0.03, 0.004, 0.012])
from engine_ext import *
CY = ACC
GO = (1.0, 0.80, 0.36)   # oro para datos
SK = (0.45, 0.85, 1.0)   # celeste para contraste


def heart(ctx, cx, cy, s, t, a=1.0, col=CY, bpm=72, fill=0.10):
    beat = (t * bpm / 60.0) % 1.0
    p = 1 + 0.07 * math.exp(-((beat - 0.08) / 0.05) ** 2) + 0.04 * math.exp(-((beat - 0.28) / 0.05) ** 2)
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s * p, s * p)
    ctx.new_path()
    for j in range(121):
        th = j / 120 * 2 * math.pi
        x = 16 * math.sin(th) ** 3
        y = -(13 * math.cos(th) - 5 * math.cos(2 * th) - 2 * math.cos(3 * th) - math.cos(4 * th))
        (ctx.move_to if j == 0 else ctx.line_to)(x * 9, y * 9)
    ctx.close_path()
    ctx.set_source_rgba(*col, fill * a); ctx.fill_preserve()
    ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(5 / s); ctx.stroke()
    # vasos / detalle holograma
    ctx.set_line_width(3 / s)
    for (x0, y0, x1, y1) in [(-30, -95, -40, -150), (5, -100, 10, -165), (40, -95, 55, -140)]:
        ctx.move_to(x0, y0); ctx.curve_to(x0, y0 - 25, x1, y1 + 20, x1, y1); ctx.set_source_rgba(*col, 0.7 * a); ctx.stroke()
    for r in (40, 75, 110):
        ctx.new_path(); ctx.arc(0, 10, r, 0, 6.283); ctx.set_source_rgba(*col, 0.12 * a); ctx.stroke()
    ctx.restore()


def ecg(ctx, x0, y0, w, t, a=1.0, col=GO, amp=70, bpm=72):
    per = 220.0
    ctx.new_path()
    head = (t * 360) % (w + 200)
    for xi in range(0, int(w), 3):
        ph = (xi % per) / per
        y = 0
        if 0.30 < ph < 0.36: y = -0.15 * math.sin((ph - 0.30) / 0.06 * math.pi)
        elif 0.40 < ph < 0.42: y = 0.18 * (ph - 0.40) / 0.02
        elif 0.42 <= ph < 0.45: y = 0.18 - 1.18 * (ph - 0.42) / 0.03
        elif 0.45 <= ph < 0.48: y = -1.0 + 1.3 * (ph - 0.45) / 0.03
        elif 0.48 <= ph < 0.50: y = 0.3 - 0.3 * (ph - 0.48) / 0.02
        elif 0.60 < ph < 0.72: y = -0.28 * math.sin((ph - 0.60) / 0.12 * math.pi)
        aa = a * clamp(1 - abs(xi - head) / 520) if xi <= head else a * 0.15
        (ctx.move_to if xi == 0 else ctx.line_to)(x0 + xi, y0 + y * amp)
    ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(4); ctx.stroke()
    hx = min(head, w)
    ctx.new_path(); ctx.arc(x0 + hx, y0, 9, 0, 6.283); ctx.set_source_rgba(1, 1, 1, a * 0.9); ctx.fill()


def stairs(ctx, x0, y0, n, sw, sh, a=1.0, col=CY, climb=0.0, t=0.0):
    ctx.new_path(); ctx.move_to(x0, y0)
    for j in range(n):
        ctx.line_to(x0 + j * sw, y0 - (j + 1) * sh); ctx.line_to(x0 + (j + 1) * sw, y0 - (j + 1) * sh)
    ctx.line_to(x0 + n * sw, y0); ctx.close_path()
    ctx.set_source_rgba(*col, 0.08 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(4); ctx.stroke()
    if climb > 0:
        f = climb * n
        j = min(int(f), n - 1); fr = f - j
        px = x0 + (j + 0.5) * sw + fr * sw * 0.5
        py = y0 - (j + 1) * sh - 34 - 10 * abs(math.sin(t * 9))
        ctx.new_path(); ctx.arc(px, py, 22, 0, 6.283); ctx.set_source_rgba(*GO, a); ctx.fill()
        for k in range(1, 5):
            ctx.new_path(); ctx.arc(px - k * 26, py + k * 10, 14 - k * 2.5, 0, 6.283); ctx.set_source_rgba(*GO, a * (0.5 - k * 0.1)); ctx.fill()


def bag(ctx, cx, cy, a=1.0, col=SK):
    rrect(ctx, cx - 70, cy - 50, 140, 130, 18)
    ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(5); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy - 50, 40, math.pi, 0); ctx.set_line_width(7); ctx.stroke()


def wrist(ctx, cx, cy, t, a=1.0, col=GO):
    rrect(ctx, cx - 60, cy - 170, 120, 340, 40); ctx.set_source_rgba(*col, 0.06 * a); ctx.fill_preserve()
    ctx.set_source_rgba(*col, 0.6 * a); ctx.set_line_width(3); ctx.stroke()
    rrect(ctx, cx - 95, cy - 85, 190, 170, 34); ctx.set_source_rgba(0.03, 0.01, 0.02, 0.8 * a); ctx.fill_preserve()
    ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(5); ctx.stroke()
    for k in range(3):
        ph = (t * 1.2 + k / 3) % 1
        ctx.new_path(); ctx.arc(cx, cy, 20 + 140 * ph, 0, 6.283); ctx.set_source_rgba(*col, a * (1 - ph) * 0.6); ctx.set_line_width(3); ctx.stroke()
    ecg(ctx, cx - 75, cy + 5, 150, t, a, col=CY, amp=35)


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        stairs(ctx, 330, 1080, 5, 120, 78, k, col=CY, climb=ease((u - 0.6) / 3.8), t=t)
        heart(ctx, 290, 620, 0.62, t, ease((u - 0.3) / 0.5), bpm=120)
    elif i == 1:
        wrist(ctx, 540, 700, t, k)
        n = int(25241 * ease((u - 0.5) / 1.8))
        big(ctx, "{:,}".format(n).replace(",", "."), 540, 1090, 150, GO, ease((u - 0.4) / 0.4))
    elif i == 2:
        a0 = ease((u - 1.6) / 0.4); a1 = ease((u - 2.6) / 0.4); a2 = ease((u - 3.5) / 0.4)
        stairs(ctx, 90, 900, 3, 70, 60, a0 * k, col=CY, climb=ease((u - 1.6) / 2.0), t=t)
        bag(ctx, 540, 830, a1 * k)
        footprints(ctx, 720, 1000, 850, t, 3.0, a=a2 * k, col=GO)
    elif i == 3:
        heart(ctx, 540, 760, 1.25, t, k, bpm=72)
        ecg(ctx, 120, 1060, 840, t, ease((u - 0.4) / 0.4), col=GO)
    elif i == 4:
        items = [("SIN\nRÁFAGAS", 1.0, MU), ("3 RÁFAGAS\nAL DÍA", 0.61, GO)]
        kb = ease((u - 0.3) / 1.6)
        vbars(ctx, items, 300, 1080, 190, 100, 560, kb, k, label_size=24)
        text(ctx, "1,00", 395, 1080 - 560 * kb - 18, F_MONO, 30, WH, k * clamp(kb * 2 - 1), align="center", bold=True)
        text(ctx, "≈0,61", 685, 1080 - 560 * 0.61 * kb - 18, F_MONO, 30, WH, k * clamp(kb * 2 - 1), align="center", bold=True)
    elif i == 5:
        heart(ctx, 540, 720, 1.0, t, k, col=CY, bpm=66)
        big(ctx, "−45 %", 540, 1090, 150, GO, ease((u - 3.4) / 0.5))
    elif i == 6:
        for j, (lab, col, x) in enumerate((("RÁFAGAS", GO, 300), ("SALUD", CY, 780))):
            kk = ease((u - 0.3 - j * 0.6) / 0.5)
            ctx.new_path(); ctx.arc(x, 800, 150, 0, 6.283); ctx.set_source_rgba(*col, 0.10 * kk * k); ctx.fill_preserve()
            ctx.set_source_rgba(*col, kk * k); ctx.set_line_width(5); ctx.stroke()
            text(ctx, lab, x, 812, F_MONO, 32, col, kk * k, align="center", bold=True)
        ka = ease((u - 1.6) / 0.5)
        ctx.set_dash([18, 14]); ctx.move_to(470, 800); ctx.line_to(610, 800)
        ctx.set_source_rgba(1, 1, 1, ka * k); ctx.set_line_width(5); ctx.stroke(); ctx.set_dash([])
        big(ctx, "?", 540, 720, 110, RD, ka * k)
    elif i == 7:
        stairs(ctx, 170, 1060, 5, 140, 88, k, col=CY, climb=ease((u - 0.3) / 3.6), t=t)
        kb = ease((u - 2.6) / 0.4)
        rrect(ctx, 120, 560, 400, 120, 40); ctx.set_source_rgba(*GO, 0.12 * kb); ctx.fill_preserve()
        ctx.set_source_rgba(*GO, kb); ctx.set_line_width(4); ctx.stroke()
        ctx.move_to(260, 680); ctx.line_to(230, 740); ctx.line_to(320, 680); ctx.stroke()
        text(ctx, "UF… CUESTA HABLAR", 320, 634, F_MONO, 30, GO, kb, align="center", bold=True)
    elif i == 8:
        heart(ctx, 540, 600, 0.75, t, k, bpm=72)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1000); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 170, CY, 1, align="center"); ctx.restore()


def src(ctx, s, k, y=1290):
    text(ctx, s, W / 2, y, F_MONO, 21, MU, k, align="center")


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "QUÉ PASA SI… · CORAZÓN", W / 2, 196, CY, k, 28)
        title(ctx, "ESCALERAS A TODA PRISA", WH, 350, 96, k)
        text(ctx, "1–2 MIN · 3 VECES AL DÍA", W / 2, 1170, F_MONO, 34, GO, ease((u - 2.6) / 0.4), align="center", bold=True)
    elif i == 1:
        pill(ctx, "NATURE MEDICINE · 2022", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "ADULTOS QUE NO ENTRENABAN", WH, 345, 88, k)
        text(ctx, "SENSOR EN LA MUÑECA", W / 2, 470, F_MONO, 30, GO, ease((u - 3.8) / 0.4), align="center", bold=True)
        text(ctx, "PERSONAS · UK BIOBANK", W / 2, 1150, F_MONO, 30, GO, ease((u - 1.0) / 0.4), align="center", bold=True)
        src(ctx, "Stamatakis et al., Nat Med 2022 · doi:10.1038/s41591-022-02100-x", k, 1225)
    elif i == 2:
        pill(ctx, "VILPA", W / 2, 196, GO, k, 30, filled=True)
        title(ctx, "RÁFAGAS DE LA VIDA DIARIA", WH, 345, 90, k)
        text(ctx, "ACTIVIDAD VIGOROSA INTERMITENTE", W / 2, 450, F_MONO, 28, MU, k, align="center", bold=True)
        for lab, x, a0 in (("ESCALERAS", 195, 1.6), ("BOLSAS", 540, 2.6), ("PASO RÁPIDO", 875, 3.5)):
            text(ctx, lab, x, 1050, F_MONO, 28, WH, ease((u - a0) / 0.4), align="center", bold=True)
        text(ctx, "≈ 1–2 MIN CADA UNA", W / 2, 1150, F_MONO, 32, GO, ease((u - 4.0) / 0.4), align="center", bold=True)
    elif i == 3:
        pill(ctx, "MORTALIDAD CARDIOVASCULAR", W / 2, 196, CY, k, 28)
        title(ctx, "CASI LA MITAD", GO, 345, 110, ease((u - 3.2) / 0.4))
        text(ctx, "−48 a −49 %", W / 2, 1180, F_BIG, 90, WH, ease((u - 3.4) / 0.4), align="center")
        src(ctx, "vs. 0 ráfagas · riesgo relativo · Stamatakis et al., Nat Med 2022", k, 1255)
    elif i == 4:
        pill(ctx, "MORTALIDAD TOTAL", W / 2, 196, GO, k, 30, filled=True)
        title(ctx, "−38 A −40 %", WH, 350, 120, ease((u - 1.8) / 0.4))
        src(ctx, "riesgo relativo (HR ≈ 0,60–0,62) · Stamatakis et al., Nat Med 2022", k, 1255)
    elif i == 5:
        pill(ctx, "MUJERES · BJSM 2025", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "≈ 3,5 MIN AL DÍA", WH, 345, 104, k)
        text(ctx, "INFARTO · INSUF. CARDÍACA · ACV", W / 2, 1170, F_MONO, 28, MU, ease((u - 4.6) / 0.4), align="center", bold=True)
        src(ctx, "HR 0,55 · Stamatakis et al., Br J Sports Med 2025", k, 1235)
    elif i == 6:
        pill(ctx, "OJO", W / 2, 196, RD, k, 30)
        title(ctx, "ASOCIACIÓN NO ES CAUSA", WH, 350, 92, k)
        text(ctx, "ESTUDIOS OBSERVACIONALES", W / 2, 1050, F_MONO, 32, AM, ease((u - 0.8) / 0.4), align="center", bold=True)
        src(ctx, "posible causalidad inversa · Koemel et al., IJBNPA 2026", k, 1140)
    elif i == 7:
        pill(ctx, "PRUÉBALO", W / 2, 196, GO, k, 30, filled=True)
        title(ctx, "INTENSO, PERO CORTO", WH, 345, 100, k)
        text(ctx, "¿CONDICIÓN CARDÍACA? CONSULTA ANTES", W / 2, 1160, F_MONO, 28, MU, ease((u - 1.0) / 0.4), align="center", bold=True)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)


run_episode(neon, txt, "EXPEDIENTE 20 · CORAZÓN")
