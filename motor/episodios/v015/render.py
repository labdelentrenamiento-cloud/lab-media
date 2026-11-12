"""v015 · ¿Entrenar de noche arruina el sueño? (serie SUEÑO · paleta azul luna + ámbar)
Uso: copiar a la carpeta del episodio (con timeline.json) y correr
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

# ---- paleta de la serie SUEÑO (acento azul luna, fondo azul medianoche)
ACC = (0.48, 0.72, 1.0)
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.05, 0.07, 0.20], [0.006, 0.01, 0.04])
from engine_ext import *
CY = ACC
MOON = (1.0, 0.86, 0.52)


def moon(ctx, cx, cy, r, t, a):
    ctx.save()
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283)
    ctx.new_sub_path(); ctx.arc_negative(cx + r * 0.45, cy - r * 0.25, r * 0.85, 6.283, 0)
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    ctx.clip()
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283)
    ctx.set_source_rgba(*MOON, 0.35 * a); ctx.fill_preserve(); ctx.set_source_rgba(*MOON, a); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()
    for j, (dx, dy, s) in enumerate([(-1.6, -0.9, 10), (1.5, -1.3, 7), (1.9, 0.6, 9), (-1.9, 0.9, 6)]):
        tw = 0.5 + 0.5 * math.sin(t * 3 + j * 1.7)
        star(ctx, cx + dx * r, cy + dy * r, s * (0.8 + 0.4 * tw), MOON, a * (0.5 + 0.5 * tw))


def star(ctx, x, y, s, col, a):
    ctx.new_path()
    for k in range(8):
        ang = k * math.pi / 4; rr = s if k % 2 == 0 else s * 0.35
        ctx.line_to(x + math.cos(ang) * rr, y + math.sin(ang) * rr)
    ctx.close_path(); ctx.set_source_rgba(*col, a); ctx.fill()


def docs(ctx, n, k, a, x0=150, y0=560, cols=6):
    sz = 130
    for d in range(n):
        r, c = divmod(d, cols)
        x = x0 + c * sz; y = y0 + r * 140
        kk = ease((k * n - d) / 2)
        if kk <= 0: continue
        rrect(ctx, x, y, 96, 120, 10)
        ctx.set_source_rgba(*CY, 0.12 * kk * a); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.8 * kk * a); ctx.set_line_width(3); ctx.stroke()
        for li in range(3):
            ctx.move_to(x + 18, y + 32 + li * 26); ctx.line_to(x + 78 - li * 10, y + 32 + li * 26)
            ctx.set_source_rgba(*WH, 0.5 * kk * a); ctx.set_line_width(4); ctx.stroke()


def hypnogram(ctx, x0, y0, w, h, k, deep, a):
    # esquema de etapas: 0 = despierto, 1 = REM, 2 = ligero, 3 = profundo
    seq = [0, 2, 3, 3, 2, 1, 2, 3, 2, 1, 2, 2, 1, 2, 1, 0]
    levels = ["DESPIERTO", "REM", "LIGERO", "PROFUNDO"]
    for li, lab in enumerate(levels):
        yy = y0 + li * h / 3
        ctx.move_to(x0, yy); ctx.line_to(x0 + w, yy); ctx.set_source_rgba(*CY, 0.12 * a); ctx.set_line_width(2); ctx.stroke()
        text(ctx, lab, x0 - 16, yy + 8, F_MONO, 20, MU, a, align="right")
    n = len(seq); sw = w / n
    upto = k * n
    for j, s in enumerate(seq):
        if j > upto: break
        x = x0 + j * sw; yy = y0 + s * h / 3
        frac = clamp(upto - j)
        if s == 3 and deep > 0:
            rrect(ctx, x, yy - 22, sw * frac, 44, 8); ctx.set_source_rgba(*GR, 0.35 * deep * a); ctx.fill()
        ctx.move_to(x, yy); ctx.line_to(x + sw * frac, yy)
        if j + 1 < n and frac >= 1:
            ctx.line_to(x + sw, y0 + seq[j + 1] * h / 3)
        ctx.set_source_rgba(*(GR if s == 3 else CY), a); ctx.set_line_width(6); ctx.stroke()


def night_bar(ctx, y, k, a, ex_end, ex_len, col, bed=23.0, h0=17.0, h1=24.0, win=None, wincol=GR):
    x0, x1 = 120, 960
    X = lambda hh: x0 + (hh - h0) / (h1 - h0) * (x1 - x0)
    rrect(ctx, x0, y, x1 - x0, 70, 35); ctx.set_source_rgba(*CY, 0.08 * a); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.6 * a); ctx.set_line_width(3); ctx.stroke()
    for hh in range(int(h0), int(h1) + 1):
        text(ctx, "%d:00" % hh, X(hh), y + 120, F_MONO, 22, MU, a, align="center")
    if win:
        ww = ease(k)
        rrect(ctx, X(win[0]), y - 16, (X(win[1]) - X(win[0])) * ww, 102, 18)
        ctx.set_source_rgba(*wincol, 0.18 * a); ctx.fill_preserve(); ctx.set_source_rgba(*wincol, 0.9 * a); ctx.set_line_width(3); ctx.stroke()
    kk = ease(k * 1.4)
    if kk > 0:
        s = ex_end - ex_len
        rrect(ctx, X(s), y + 8, (X(ex_end) - X(s)) * kk, 54, 27); ctx.set_source_rgba(*col, 0.5 * a); ctx.fill_preserve()
        ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
    moon(ctx, X(bed), y - 70, 34, 0, a)


def wrist(ctx, cx, cy, s, t, a):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    rrect(ctx, -70, -230, 140, 460, 60); ctx.set_source_rgba(*CY, 0.06 * a); ctx.fill_preserve()
    ctx.set_source_rgba(*CY, 0.5 * a); ctx.set_line_width(4); ctx.stroke()
    rrect(ctx, -95, -80, 190, 160, 30); ctx.set_source_rgba(*CY, 0.16 * a); ctx.fill_preserve()
    ctx.set_source_rgba(*CY, a); ctx.set_line_width(6); ctx.stroke()
    ctx.new_path()
    for i in range(41):
        x = -70 + i * 3.5; ph = (i / 40 + t * 0.6) % 1
        y = -40 * math.exp(-((ph - 0.5) / 0.04) ** 2) + 18 * math.exp(-((ph - 0.6) / 0.03) ** 2)
        ctx.line_to(x, y)
    ctx.set_source_rgba(*RD, a); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def arrow_row(ctx, y, label, up, col, a):
    ax = 200
    if up:
        ctx.move_to(ax, y + 30); ctx.line_to(ax, y - 30); ctx.move_to(ax - 22, y - 8); ctx.line_to(ax, y - 30); ctx.line_to(ax + 22, y - 8)
    else:
        ctx.move_to(ax, y - 30); ctx.line_to(ax, y + 30); ctx.move_to(ax - 22, y + 8); ctx.line_to(ax, y + 30); ctx.line_to(ax + 22, y + 8)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    text(ctx, label, 270, y + 18, F_BIG, 58, col, a)


def check(ctx, cx, cy, r, k, a, col=GR):
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*col, 0.12 * a); ctx.fill_preserve()
    ctx.set_source_rgba(*col, a); ctx.set_line_width(6); ctx.stroke()
    kk = ease(k)
    if kk > 0:
        p = [(cx - r * 0.45, cy), (cx - r * 0.1, cy + r * 0.35), (cx + r * 0.5, cy - r * 0.35)]
        ctx.move_to(*p[0]); ctx.line_to(*p[1]); ctx.line_to(p[1][0] + (p[2][0] - p[1][0]) * kk, p[1][1] + (p[2][1] - p[1][1]) * kk)
        ctx.set_source_rgba(*col, a); ctx.set_line_width(12); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        moon(ctx, 540, 760, 170, t, k)
        barbell_icon(ctx, 540, 1060, t, a=ease((u - 0.6) / 0.4))
    elif i == 1:
        docs(ctx, 23, ease((u - 0.2) / 2.6), k, x0=165, y0=500)
        big(ctx, "23 ESTUDIOS", 540, 1200, 100, CY, ease((u - 2.4) / 0.5))
    elif i == 2:
        hypnogram(ctx, 260, 600, 720, 420, ease((u - 0.1) / 1.6), ease((u - 1.0) / 0.6), k)
        big(ctx, "+1,3 PUNTOS", 540, 1200, 90, GR, ease((u - 1.2) / 0.4))
    elif i == 3:
        night_bar(ctx, 760, ease((u - 0.3) / 1.6), k, 22.5, 1.0, RD, bed=23.0)
        big(ctx, "≤ 1 H", 540, 1110, 150, RD, ease((u - 1.8) / 0.4))
    elif i == 4:
        wrist(ctx, 270, 830, 1.0, t, k)
        n1 = int(14689 * ease((u - 0.8) / 2.0)); n2 = int(4084354 * ease((u - 2.4) / 2.4))
        a1 = ease((u - 0.8) / 0.3); a2 = ease((u - 2.4) / 0.3)
        big(ctx, f"{n1:,}".replace(",", "."), 720, 740, 110, CY, a1, maxw=560)
        big(ctx, f"{n2:,}".replace(",", "."), 720, 1000, 96, AM, a2, maxw=560)
    elif i == 5:
        arrow_row(ctx, 620, "SE DUERMEN MÁS TARDE", True, AM, ease((u - 1.6) / 0.4))
        arrow_row(ctx, 800, "DUERMEN MENOS", False, AM, ease((u - 3.0) / 0.4))
        arrow_row(ctx, 980, "PULSO NOCTURNO", True, RD, ease((u - 4.6) / 0.4))
    elif i == 6:
        night_bar(ctx, 760, ease((u - 0.3) / 1.6), k, 19.0, 1.0, GR, bed=23.0, win=(19.0, 23.0))
        check(ctx, 540, 1080, 80, (u - 2.2) / 0.6, ease((u - 1.8) / 0.4))
    elif i == 7:
        moon(ctx, 540, 730, 130, t, k)
        check(ctx, 540, 1030, 70, (u - 0.8) / 0.6, ease((u - 0.5) / 0.4))
    elif i == 8:
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 820); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 190, CY, 1, align="center"); ctx.restore()


def src(ctx, s, k, y=1290):
    text(ctx, s, W / 2, y, F_MONO, 21, MU, k, align="center")


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "MITO VS. REALIDAD · SUEÑO", W / 2, 196, CY, k, 28)
        title(ctx, "¿ENTRENAR DE NOCHE ARRUINA TU SUEÑO?", WH, 350, 84, k)
    elif i == 1:
        pill(ctx, "METAANÁLISIS · SPORTS MED 2019", W / 2, 196, CY, k, 28)
        title(ctx, "NO EMPEORA EL SUEÑO", GR, 345, 96, k)
        src(ctx, "adultos sanos · 1 sesión de ejercicio vs. sin ejercicio · Stutz et al., 2019", k)
    elif i == 2:
        pill(ctx, "SUEÑO PROFUNDO", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "SUBIÓ UN POCO", GR, 345, 100, k)
        text(ctx, "esquema ilustrativo de etapas del sueño", W / 2, 1080, F_MONO, 20, MU, k, align="center")
        src(ctx, "+1,3 puntos porcentuales de sueño profundo · Stutz et al., Sports Med 2019", k, 1275)
    elif i == 3:
        pill(ctx, "LA EXCEPCIÓN", W / 2, 196, RD, k, 30)
        title(ctx, "INTENSO JUSTO ANTES DE DORMIR", WH, 345, 84, k)
        text(ctx, "ENTRENAMIENTO INTENSO", 120, 720, F_MONO, 24, RD, k, bold=True)
        src(ctx, "puede costar más dormirse y dormir menos · Stutz et al., 2019 · esquema", k, 1240)
    elif i == 4:
        pill(ctx, "ESTUDIO OBSERVACIONAL · NAT COMMUN 2025", W / 2, 196, CY, k, 26)
        title(ctx, "4 MILLONES DE NOCHES", WH, 345, 92, k)
        text(ctx, "PERSONAS", 720, 800, F_MONO, 30, CY, ease((u - 0.8) / 0.3), align="center", bold=True)
        text(ctx, "NOCHES", 720, 1055, F_MONO, 30, AM, ease((u - 2.4) / 0.3), align="center", bold=True)
        src(ctx, "pulsera biométrica · 1 año · Leota et al., Nat Commun 2025", k, 1240)
    elif i == 5:
        pill(ctx, "MÁS INTENSO + MÁS TARDE", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "PEOR NOCHE", AM, 345, 100, k)
        src(ctx, "asociación, no prueba causa · Leota et al., Nat Commun 2025", k, 1240)
    elif i == 6:
        pill(ctx, "TERMINAR ≥ 4 H ANTES", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "SIN CAMBIOS EN EL SUEÑO", GR, 345, 92, k)
        text(ctx, "VENTANA DE 4 H", 540, 730, F_MONO, 24, GR, k, align="center", bold=True)
        src(ctx, "sin importar la intensidad · Leota et al., Nat Commun 2025", k, 1240)
    elif i == 7:
        pill(ctx, "VEREDICTO", W / 2, 196, CY, k, 30)
        title(ctx, "MITO A MEDIAS", WH, 345, 100, k)
        a = ease((u - 1.4) / 0.4); b = ease((u - 2.6) / 0.4)
        pill(ctx, "NOCHE: SÍ", 330, 1200, GR, a, 34, filled=True)
        pill(ctx, "LO INTENSO: ANTES", 720, 1200, AM, b, 34, filled=True)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)
        a = ease((u - 0.8) / 0.4)
        if a > 0:
            pulse = 1 + 0.04 * math.sin(t * 7)
            ctx.save(); ctx.translate(540, 1000); ctx.scale(pulse, pulse)
            rrect(ctx, -170, -50, 340, 100, 50); ctx.set_source_rgba(*RD, a); ctx.fill()
            text(ctx, "SEGUIR", 0, 18, F_UI, 50, WH, a, align="center", bold=True); ctx.restore()


run_episode(neon, txt, "EXPEDIENTE 15 · SUEÑO")
