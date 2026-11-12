"""v012 · ¿10.000 pasos? (serie LONGEVIDAD · paleta turquesa)
Uso: copiar a la carpeta del episodio (con timeline.json) y correr
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

# ---- paleta de la serie LONGEVIDAD (acento turquesa, fondo petróleo)
ACC = (0.28, 1.0, 0.80)
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.03, 0.13, 0.17], [0.005, 0.02, 0.035])
from engine_ext import *
CY = ACC


def counter(ctx, v, x, y, size, col, a):
    big(ctx, f"{v:,}".replace(",", "."), x, y, size, col, a, maxw=900)


def pedometer(ctx, cx, cy, s, a, t, val):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    rrect(ctx, -150, -200, 300, 400, 70)
    ctx.set_source_rgba(*CY, 0.08 * a); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.95 * a); ctx.set_line_width(6); ctx.stroke()
    rrect(ctx, -110, -150, 220, 120, 18); ctx.set_source_rgba(*CY, 0.16 * a); ctx.fill_preserve()
    ctx.set_source_rgba(*CY, 0.8 * a); ctx.set_line_width(3); ctx.stroke()
    text(ctx, f"{val:05d}", 0, -65, F_MONO, 64, WH, a, align="center", bold=True)
    ctx.new_path(); ctx.arc(0, 90, 55, 0, 6.283); ctx.set_source_rgba(*CY, 0.7 * a); ctx.set_line_width(5); ctx.stroke()
    ang = -math.pi / 2 + 0.6 * math.sin(t * 6)
    ctx.move_to(0, 90); ctx.line_to(math.cos(ang) * 45, 90 + math.sin(ang) * 45); ctx.set_source_rgba(*AM, a); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def dots(ctx, n, k, a, col=CY):
    cols = 8; sz = 70; x0 = 540 - (cols - 1) * sz / 2; y0 = 500
    for i in range(n):
        kk = ease((k * n - i) / 3)
        if kk <= 0: continue
        r, c = divmod(i, cols)
        x = x0 + c * sz; y = y0 + r * sz
        rrect(ctx, x - 24, y - 30, 48, 60, 8)
        ctx.set_source_rgba(*col, 0.18 * a * kk); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.9 * a * kk); ctx.set_line_width(2.5); ctx.stroke()
        for li in range(3):
            ctx.move_to(x - 14, y - 14 + li * 13); ctx.line_to(x + 14, y - 14 + li * 13)
            ctx.set_source_rgba(*WH, 0.5 * a * kk); ctx.set_line_width(2); ctx.stroke()


def risk(st):
    # esquema ilustrativo: curva inversa no lineal con inflexión ~5.000–7.000 (Ding 2025)
    x = st / 12000
    return 0.22 + 0.70 * math.exp(-x * 4.2)


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        v = int(10000 * ease((u - 0.2) / 1.8))
        counter(ctx, v, 540, 820, 230, CY, k)
        footprints(ctx, 120, 960, 1010, t, 1.0, a=k)
    elif i == 1:
        pedometer(ctx, 540, 760, 1.15, k, t, int(10000 * ease((u - 0.3) / 2.5)))
        a = ease((u - 1.4) / 0.4)
        big(ctx, "1965", 540, 1170, 120, AM, a)
    elif i == 2:
        dots(ctx, 57, ease((u - 0.2) / 3.0), k)
        a = ease((u - 3.2) / 0.4)
        big(ctx, "57", 540, 1150, 150, CY, a)
    elif i == 3:
        vbars(ctx, [("2.000\nPASOS", 1.0, MU), ("7.000\nPASOS", 0.53, CY)], 290, 960, 210, 90, 400, (u - 0.4) / 1.6, a=k, label_size=28)
        a = ease((u - 2.6) / 0.4)
        big(ctx, "−47 %", 540, 1225, 120, CY, a)
    elif i == 4:
        brain(ctx, 330, 760, 1.05, t, a=k, col=VI, fire=0.5 * k)
        a1 = ease((u - 0.6) / 0.4); a2 = ease((u - 2.6) / 0.4)
        big(ctx, "−38 %", 800, 700, 130, CY, a1, maxw=380)
        big(ctx, "−22 %", 800, 1010, 130, CY, a2, maxw=380)
    elif i == 5:
        up = ease((u - 0.2) / 2.6)
        line_chart(ctx, 130, 520, 820, 520, [(lambda f: risk(f * 12000), CY, up, True)],
                   [(j / 6, str(2 * j) + "k") for j in range(7)], "PASOS / DÍA", "RIESGO RELATIVO", a=k)
        a = ease((u - 2.0) / 0.5)
        x7 = 130 + 7 / 12 * 820
        ctx.move_to(x7, 520); ctx.line_to(x7, 1040); ctx.set_source_rgba(*AM, 0.8 * a); ctx.set_line_width(3); ctx.set_dash([12, 8]); ctx.stroke(); ctx.set_dash([])
    elif i == 6:
        for j, (lab, v, col) in enumerate([("7.000", 0.62, CY), ("10.000", 0.88, GR)]):
            aa = ease((u - 0.3 - j * 1.3) / 0.4)
            cx = 300 + j * 480; cy = 800
            ctx.new_path(); ctx.arc(cx, cy, 170, 0, 6.283); ctx.set_source_rgba(*col, 0.18 * aa); ctx.set_line_width(14); ctx.stroke()
            ctx.new_path(); ctx.arc(cx, cy, 170, -math.pi / 2, -math.pi / 2 + 6.283 * v * aa); ctx.set_source_rgba(*col, aa); ctx.set_line_width(14); ctx.stroke()
            big(ctx, lab, cx, cy + 35, 96, WH, aa, maxw=300)
    elif i == 7:
        skeleton(ctx, 540, 430, 0.74, t, hl={"legs": (CY, 0.8 + 0.2 * math.sin(t * 6))}, base_a=0.75 * k)
        footprints(ctx, 120, 960, 1200, t, 1.2, a=k)
    elif i == 8:
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 820); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 190, CY, 1, align="center"); ctx.restore()


def src(ctx, s, k):
    text(ctx, s, W / 2, 1290, F_MONO, 21, MU, k, align="center")


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "EXPEDIENTE · LONGEVIDAD", W / 2, 196, CY, k, 28)
        title(ctx, "¿10.000 PASOS AL DÍA?", WH, 350, 96, k)
        text(ctx, "PASOS", 540, 900, F_MONO, 36, CY, k, align="center", bold=True)
    elif i == 1:
        pill(ctx, "ORIGEN DE LA CIFRA", W / 2, 196, AM, k, 30)
        title(ctx, "PUBLICIDAD, NO CIENCIA", AM, 345, 92, k)
        src(ctx, "podómetro “manpo-kei” (10.000 pasos) · Japón, 1965", k)
        text(ctx, "Tudor-Locke y Bassett, Sports Med 2004 · Lee et al., JAMA Intern Med 2019", W / 2, 1325, F_MONO, 18, MU, k, align="center")
    elif i == 2:
        pill(ctx, "REVISIÓN · LANCET PUBLIC HEALTH 2025", W / 2, 196, CY, k, 28)
        title(ctx, "57 ESTUDIOS", WH, 345, 100, k)
        src(ctx, "pasos medidos con dispositivo · Ding et al., 2025", k)
    elif i == 3:
        pill(ctx, "MORTALIDAD POR CUALQUIER CAUSA", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "7.000 VS. 2.000 PASOS", WH, 345, 92, k)
        src(ctx, "HR 0,53 · 14 estudios · Ding et al., Lancet Public Health 2025", k)
    elif i == 4:
        pill(ctx, "CEREBRO Y ÁNIMO", W / 2, 196, VI, k, 30, filled=True)
        title(ctx, "7.000 PASOS VS. 2.000", WH, 345, 92, k)
        text(ctx, "DEMENCIA", 800, 770, F_MONO, 32, WH, ease((u - 0.6) / 0.4), align="center", bold=True)
        text(ctx, "SÍNTOMAS DEPRESIVOS", 800, 1080, F_MONO, 30, WH, ease((u - 2.6) / 0.4), align="center", bold=True)
        src(ctx, "Ding et al., Lancet Public Health 2025 (asociaciones)", k)
    elif i == 5:
        pill(ctx, "CURVA DOSIS-RESPUESTA", W / 2, 196, CY, k, 30)
        title(ctx, "EL GRAN SALTO: ANTES DE 7.000", WH, 345, 84, k)
        src(ctx, "esquema ilustrativo · inflexión ≈ 5.000–7.000 pasos (Ding 2025)", k)
    elif i == 6:
        pill(ctx, "META, NO MÍNIMO", W / 2, 196, GR, k, 30)
        title(ctx, "10.000 SIGUE SUMANDO", GR, 345, 92, k)
        src(ctx, "beneficio se estabiliza: 6–8 mil (60+) · 8–10 mil (<60) · Paluch et al., 2022", k)
    elif i == 7:
        pill(ctx, "ASOCIACIÓN ≠ CAUSA", W / 2, 196, AM, k, 30)
        title(ctx, "SI CAMINAS POCO, SUMA PASOS", WH, 345, 88, k)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)
        a = ease((u - 0.8) / 0.4)
        if a > 0:
            pulse = 1 + 0.04 * math.sin(t * 7)
            ctx.save(); ctx.translate(540, 1000); ctx.scale(pulse, pulse)
            rrect(ctx, -170, -50, 340, 100, 50); ctx.set_source_rgba(*RD, a); ctx.fill()
            text(ctx, "SEGUIR", 0, 18, F_UI, 50, WH, a, align="center", bold=True); ctx.restore()


run_episode(neon, txt, "EXPEDIENTE 12 · PASOS")
