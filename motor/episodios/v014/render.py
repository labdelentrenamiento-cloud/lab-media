"""v014 · ¿Qué pasa si dejas de entrenar 3 semanas? (serie RECUPERACIÓN · paleta cian clásica + ámbar)
Uso: copiar a la carpeta del episodio (con timeline.json) y correr
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
from engine_ext import *


def calendar(ctx, x0, y0, k, t, a):
    sz = 104
    for d in range(21):
        r, c = divmod(d, 7)
        x = x0 + c * sz; y = y0 + r * sz
        rrect(ctx, x, y, sz - 14, sz - 14, 12)
        ctx.set_source_rgba(*CY, 0.07 * a); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.6 * a); ctx.set_line_width(2.5); ctx.stroke()
        kk = ease((k * 21 - d) / 1.5)
        if kk > 0:
            m = 22; e = sz - 14 - m
            ctx.move_to(x + m, y + m); ctx.line_to(x + m + (e - m) * kk, y + m + (e - m) * kk)
            ctx.move_to(x + e, y + m); ctx.line_to(x + e - (e - m) * kk, y + m + (e - m) * kk)
            ctx.set_source_rgba(*AM, a); ctx.set_line_width(6); ctx.stroke()


def heart(ctx, cx, cy, s, t, a, col=RD):
    beat = 1 + 0.06 * max(0, math.sin(t * 7)) ** 8
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s * beat, s * beat)
    ctx.move_to(0, 60); ctx.curve_to(-120, -20, -80, -120, 0, -60); ctx.curve_to(80, -120, 120, -20, 0, 60); ctx.close_path()
    ctx.set_source_rgba(*col, 0.15 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5 / s); ctx.stroke()
    ctx.restore()


def blocks(ctx, k, a, y=640):
    seq = [(6, GR, "6"), (3, AM, "3"), (6, GR, "6"), (3, AM, "3"), (6, GR, "6")]
    x = 110; unit = 860 / 24; acc = 0
    for j, (w, col, lab) in enumerate(seq):
        kk = clamp((k * 24 - acc) / w)
        if kk > 0:
            rrect(ctx, x, y, max(10, w * unit * kk - 8), 120, 14)
            ctx.set_source_rgba(*col, 0.22 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
            if kk > 0.6:
                text(ctx, lab, x + w * unit / 2 - 4, y + 82, F_BIG, 64, col, a * ease((kk - 0.6) / 0.4), align="center")
        x += w * unit; acc += w


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        calendar(ctx, 180, 520, ease((u - 0.3) / 2.4), t, k)
        big(ctx, "21 DÍAS", 540, 1000, 120, AM, ease((u - 1.8) / 0.4))
    elif i == 1:
        vbars(ctx, [("ANTES", 1.0, CY), ("3 SEMANAS\nDESPUÉS", 0.95, GR)], 290, 1040, 210, 90, 460, (u - 0.3) / 1.6, a=k, label_size=26)
    elif i == 2:
        heart(ctx, 300, 720, 1.25, t, k)
        v = 7 * ease((u - 1.6) / 1.6)
        big(ctx, "−%d %%" % round(v), 760, 760, 170, AM, ease((u - 1.4) / 0.4), maxw=420)
        f = lambda x: 0.85 - 0.07 * 0.85 * ease(x / 0.9)
        line_chart(ctx, 160, 900, 760, 240, [(f, AM, ease((u - 1.6) / 2.4), True)],
                   [(0, "0"), (0.5, "10"), (1.0, "21")], "DÍAS SIN ENTRENAR", "VO2 MÁX", a=k)
    elif i == 3:
        blocks(ctx, ease((u - 0.3) / 4.0), k)
        barbell_icon(ctx, 540, 960, t, a=k)
    elif i == 4:
        f1 = lambda x: 0.10 + 0.75 * (1 - math.exp(-x * 2.6)) / (1 - math.exp(-2.6))
        def f2(x):
            base = f1(x)
            for s0 in (6 / 24, 15 / 24):
                if s0 <= x < s0 + 3 / 24: base -= 0.05 * math.sin((x - s0) / (3 / 24) * math.pi)
            return base
        up = ease((u - 0.2) / 2.6)
        line_chart(ctx, 130, 540, 820, 520, [(f1, CY, up, False), (f2, AM, up, False)],
                   [(0, "0"), (0.25, "6"), (0.5, "12"), (0.75, "18"), (1.0, "24")], "SEMANAS", "MÚSCULO Y FUERZA", a=k)
    elif i == 5:
        f1 = lambda x: 0.92 - 0.05 * x - 0.30 * x ** 2.2
        f2 = lambda x: 0.92 - 0.10 * x - 0.48 * x ** 1.8
        up = ease((u - 0.2) / 2.6)
        line_chart(ctx, 130, 540, 820, 520, [(f1, CY, up, False), (f2, RD, ease((u - 2.0) / 2.6), False)],
                   [(0, "0"), (1 / 3, "4"), (2 / 3, "8"), (1.0, "12+")], "SEMANAS SIN ENTRENAR", "FUERZA", a=k)
    elif i == 6:
        clock(ctx, 540, 780, 200, t, back=ease((u - 0.3) / 2.5), a=k)
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
        pill(ctx, "EXPEDIENTE · RECUPERACIÓN", W / 2, 196, CY, k, 28)
        title(ctx, "¿3 SEMANAS SIN ENTRENAR?", WH, 350, 92, k)
    elif i == 1:
        pill(ctx, "FUERZA", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "CASI NO CAMBIA", GR, 345, 100, k)
        src(ctx, "pausas < 4 semanas · esquema ilustrativo", k, 1200)
        text(ctx, "Mujika y Padilla, Sports Med 2000 · Bosquet et al., Scand J Med Sci Sports 2013", W / 2, 1240, F_MONO, 18, MU, k, align="center")
    elif i == 2:
        pill(ctx, "CARDIO · VO2 MÁX", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "BAJA PRIMERO", AM, 345, 100, k)
        text(ctx, "EN 3 SEMANAS", 760, 840, F_MONO, 30, AM, ease((u - 1.4) / 0.4), align="center", bold=True)
        src(ctx, "7 atletas de resistencia · Coyle et al., J Appl Physiol 1984", k)
    elif i == 3:
        pill(ctx, "ENSAYO · EUR J APPL PHYSIOL 2013", W / 2, 196, CY, k, 28)
        title(ctx, "ENTRENAR · PARAR · VOLVER", WH, 345, 88, k)
        text(ctx, "SEMANAS:  ENTRENO", 110, 610, F_MONO, 26, GR, k, bold=True)
        text(ctx, "PAUSA", 640, 610, F_MONO, 26, AM, k, bold=True)
        src(ctx, "14 hombres jóvenes · press de banca · Ogasawara et al., 2013", k)
    elif i == 4:
        pill(ctx, "RESULTADO A LAS 24 SEMANAS", W / 2, 196, GR, k, 28, filled=True)
        title(ctx, "MISMA GANANCIA", GR, 345, 100, k)
        a = ease((u - 0.8) / 0.4)
        text(ctx, "— SIN PAUSAS", 160, 1180, F_MONO, 28, CY, a, bold=True)
        text(ctx, "— CON PAUSAS", 560, 1180, F_MONO, 28, AM, a, bold=True)
        src(ctx, "esquema ilustrativo · Ogasawara et al., Eur J Appl Physiol 2013", k, 1250)
    elif i == 5:
        pill(ctx, "PAUSAS LARGAS", W / 2, 196, RD, k, 30)
        title(ctx, "MÁS TIEMPO, MÁS PÉRDIDA", WH, 345, 90, k)
        a = ease((u - 0.8) / 0.4)
        text(ctx, "— MENORES DE 65", 160, 1180, F_MONO, 28, CY, a, bold=True)
        text(ctx, "— 65+", 640, 1180, F_MONO, 28, RD, ease((u - 2.0) / 0.4), bold=True)
        src(ctx, "esquema ilustrativo · 103 estudios · Bosquet et al., 2013", k, 1250)
    elif i == 6:
        pill(ctx, "LA CLAVE", W / 2, 196, GR, k, 30)
        title(ctx, "VOLVER A ENTRENAR", GR, 345, 100, k)
    elif i == 7:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)
        a = ease((u - 0.8) / 0.4)
        if a > 0:
            pulse = 1 + 0.04 * math.sin(t * 7)
            ctx.save(); ctx.translate(540, 1000); ctx.scale(pulse, pulse)
            rrect(ctx, -170, -50, 340, 100, 50); ctx.set_source_rgba(*RD, a); ctx.fill()
            text(ctx, "SEGUIR", 0, 18, F_UI, 50, WH, a, align="center", bold=True); ctx.restore()


run_episode(neon, txt, "EXPEDIENTE 14 · PAUSA")
