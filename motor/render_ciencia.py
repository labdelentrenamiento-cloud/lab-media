import sys, math
sys.path.insert(0, "/home/claude/lab")
from engine_ext import *


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        skeleton(ctx, 540, 480, 0.74, t, hl={"legs": (GR, ease((u - 0.8) / 0.6)), "hips": (GR, ease((u - 0.8) / 0.6))}, base_a=0.8 * k)
    elif i == 1:
        fiber_bundle(ctx, 140, 520, 800, 600, 9, 0.0, t, a=k)
        tears(ctx, 140, 520, 800, 600, 9, (u - lt(1) - 1.4) / 2.2, t)
    elif i == 2:
        pain = ease((u - 0.6) / 0.6)
        leg(ctx, 300, 500, 1.0, a=k, col=CY, fill=0.05)
        ctx.save(); ctx.translate(300, 500)
        ctx.new_path(); ctx.save(); ctx.translate(0, 170); ctx.scale(55, 140); ctx.arc(0, 0, 1, 0, 6.283); ctx.restore()
        ctx.set_source_rgba(*RD, (0.25 + 0.2 * math.sin(t * 6)) * pain); ctx.fill(); ctx.restore()
        for r in range(3):
            ph = (t * 0.8 + r / 3) % 1
            ctx.new_path(); ctx.arc(300, 670, 60 + ph * 140, 0, 6.283); ctx.set_source_rgba(*RD, (1 - ph) * 0.6 * pain); ctx.set_line_width(4); ctx.stroke()
        # time axis 0..96h
        x0, x1, y = 560, 990, 900
        ctx.move_to(x0, y); ctx.line_to(x1, y); ctx.set_source_rgba(*CY, 0.7 * k); ctx.set_line_width(3); ctx.stroke()
        for hh in (0, 24, 48, 72, 96):
            xx = x0 + (x1 - x0) * hh / 96
            ctx.move_to(xx, y - 10); ctx.line_to(xx, y + 10); ctx.stroke()
            text(ctx, f"{hh}h", xx, y + 46, F_MONO, 24, MU, k, align="center")
        z = ease((u - 0.9) / 0.6)
        xa = x0 + (x1 - x0) * 24 / 96; xb = x0 + (x1 - x0) * (24 + 48 * z) / 96
        rrect(ctx, xa, y - 140, max(4, xb - xa), 120, 14); ctx.set_source_rgba(*RD, 0.25 * k); ctx.fill_preserve()
        ctx.set_source_rgba(*RD, 0.9 * k); ctx.set_line_width(3); ctx.stroke()
        if z > 0.95: text(ctx, "PICO DE DOLOR", (xa + xb) / 2, y - 70, F_MONO, 26, WH, 1, align="center", bold=True)
    elif i == 3:
        vbars(ctx, [("3 h", 0.93, GR), ("24 h", 0.54, CY), ("48 h", 0.28, VI)], 170, 1120, 200, 90, 520, (u - 0.4) / 2.0, a=k, label_size=32)
        for j, (s, v, c) in enumerate([("+112 %", 0.93, GR), ("+65 %", 0.54, CY), ("+34 %", 0.28, VI)]):
            a = ease((u - 0.9 - j * 0.3) / 0.4)
            if a > 0: big(ctx, s, 270 + j * 290, 1120 - 520 * v - 30, 64, c, a, maxw=260)
    elif i == 4:
        vbars(ctx, [("FUERZA", 0.85, GR), ("TAMAÑO", 0.12, AM)], 250, 1110, 220, 140, 520, (u - 0.4) / 1.6, a=k, label_size=32)
    elif i == 5:
        brain(ctx, 300, 570, 0.95, t, a=k, fire=ease((u - 0.8) / 0.5))
        act = 0.15 + 0.8 * ease((u - lt(5) - 1.4) / 2.6)
        nerve(ctx, [(330, 740), (330, 820), (520, 900), (600, 940)], t, a=k, rate=0.6 + 1.6 * act, n=3 + int(act * 4))
        fiber_bundle(ctx, 600, 820, 380, 360, 8, act, t, a=k)
    elif i == 6:
        up = ease((u - 0.2) / 3.0)
        sfn = lambda f: 0.15 + 0.7 * (1 - math.exp(-f * 10 / 2.2)) * (0.6 + 0.4 * f)
        hfn = lambda f: 0.15 + (0.0 if f * 10 < 5 else 0.06 * (f * 10 - 5) ** 1.15)
        line_chart(ctx, 130, 560, 820, 500, [(sfn, GR, up, False), (hfn, AM, up, True)],
                   [(i / 10, str(i)) for i in range(0, 11, 2)], "SEMANAS", "", a=k)
        if up > 0.6:
            x6 = 130 + 0.6 * 820
            ctx.move_to(x6, 560); ctx.line_to(x6, 1060); ctx.set_source_rgba(*AM, 0.6); ctx.set_dash([8, 8]); ctx.set_line_width(3); ctx.stroke(); ctx.set_dash([])
    elif i == 7:
        brain(ctx, 540, 780, 1.6, t, a=k, fire=1.0)
    elif i == 8:
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 820); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 190, CY, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "EXPEDIENTE · FUERZA", W / 2, 196, CY, k, 28)
        title(ctx, "SI EMPIEZAS A ENTRENAR HOY…", WH, 350, 88, k)
        a = ease((u - 1.6) / 0.4)
        text(ctx, "ESTO LE PASA A TU CUERPO", W / 2, 410, F_MONO, 32, GR, a, align="center", bold=True)
    elif i == 1:
        pill(ctx, "DÍA 1", W / 2, 196, CY, k, 32, filled=True)
        title(ctx, "MICROLESIONES", RD, 350, 100, k)
        text(ctx, "FIBRAS MUSCULARES", W / 2, 490, F_MONO, 26, CY, k, align="center", bold=True)
    elif i == 2:
        pill(ctx, "24 – 72 HORAS", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "DOLOR MUSCULAR TARDÍO", WH, 345, 88, k)
        text(ctx, "Pico de dolor entre las 24 y 72 h", W / 2, 1265, F_MONO, 20, MU, k, align="center")
    elif i == 3:
        pill(ctx, "HASTA 48 HORAS", W / 2, 196, GR, k, 32, filled=True)
        title(ctx, "TU MÚSCULO SE REPARA", WH, 345, 88, k)
        text(ctx, "SÍNTESIS DE PROTEÍNA SOBRE EL REPOSO", W / 2, 470, F_MONO, 26, WH, k, align="center", bold=True)
        text(ctx, "Phillips et al., 1997 · Am J Physiol", W / 2, 1265, F_MONO, 20, MU, k, align="center")
    elif i == 4:
        pill(ctx, "SEMANAS 1 – 4", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "MÁS FUERTE… SIN CRECER", WH, 345, 90, k)
        text(ctx, "esquema ilustrativo", W / 2, 1265, F_MONO, 20, MU, k, align="center")
    elif i == 5:
        pill(ctx, "¿CÓMO?", W / 2, 196, VI, k, 32, filled=True)
        title(ctx, "TU SISTEMA NERVIOSO APRENDE", WH, 345, 84, k)
        text(ctx, "FIBRAS ACTIVAS", 790, 800, F_MONO, 26, GR, k, align="center", bold=True)
        text(ctx, "esquema ilustrativo", W / 2, 1265, F_MONO, 20, MU, k, align="center")
    elif i == 6:
        pill(ctx, "SEMANA 6 +", W / 2, 196, GR, k, 32, filled=True)
        title(ctx, "AHORA SÍ: EL MÚSCULO CRECE", WH, 345, 86, k)
        text(ctx, "FUERZA", 940, 600, F_MONO, 28, GR, k, align="right", bold=True)
        text(ctx, "TAMAÑO", 940, 900, F_MONO, 28, AM, k, align="right", bold=True)
        text(ctx, "esquema · cambios medibles de grosor tras ~6 semanas", W / 2, 1265, F_MONO, 20, MU, k, align="center")
    elif i == 7:
        pill(ctx, "NO TE RINDAS", W / 2, 196, GR, k, 32, filled=True)
        title(ctx, "TU CEREBRO YA ESTÁ ENTRENANDO", GR, 345, 82, k)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)
        a = ease((u - 0.8) / 0.4)
        if a > 0:
            pulse = 1 + 0.04 * math.sin(t * 7)
            ctx.save(); ctx.translate(540, 1000); ctx.scale(pulse, pulse)
            rrect(ctx, -170, -50, 340, 100, 50); ctx.set_source_rgba(*RD, a); ctx.fill()
            text(ctx, "SEGUIR", 0, 18, F_UI, 50, WH, a, align="center", bold=True); ctx.restore()


run_episode(neon, txt, "EXPEDIENTE 01 · MÚSCULO")
