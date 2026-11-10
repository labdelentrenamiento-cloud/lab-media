import sys, math
sys.path.insert(0, "/home/claude/lab")
from engine_ext import *


def mass(age):
    if age <= 30: return 0.55 + 0.35 * (age - 20) / 10
    m = 0.90 - 0.0055 * (age - 30)
    if age > 60: m -= 0.0065 * (age - 60)
    return m


def chart(ctx, upto, k, accel=0.0):
    fn = lambda f: mass(20 + 70 * f)
    line_chart(ctx, 130, 560, 820, 500, [(fn, CY, upto, True)],
               [(i / 7, str(20 + 10 * i)) for i in range(8)], "EDAD (AÑOS)", "MASA MUSCULAR", a=k)
    if accel > 0:
        x60 = 130 + (40 / 70) * 820
        ctx.rectangle(x60, 560, 950 - x60, 500); ctx.set_source_rgba(*RD, 0.14 * accel); ctx.fill()
        ctx.move_to(x60, 560); ctx.line_to(x60, 1060); ctx.set_source_rgba(*RD, 0.8 * accel); ctx.set_line_width(3); ctx.stroke()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        skeleton(ctx, 380, 470, 0.72, t, hl={"legs": (CY, 0.6)}, base_a=0.8 * k)
        v = int(30 + 60 * ease((u - 0.4) / 1.6))
        big(ctx, str(v), 790, 800, 230, AM, k, maxw=420)
    elif i == 1:
        chart(ctx, ease((u - 0.2) / 3.6), k)
    elif i == 2:
        chart(ctx, 1.0, 1.0, accel=ease((u - 0.3) / 0.6))
    elif i == 3:
        rrect(ctx, 90, 440, 900, 780, 28)
        ctx.set_source_rgba(*CY, 0.06 * k); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.7 * k); ctx.set_line_width(3); ctx.stroke()
        rows = [("10 PERSONAS FRÁGILES", WH), ("≈ 90 AÑOS (HASTA 96)", WH), ("RESIDENTES DE UN HOGAR", WH), ("FUERZA DE ALTA INTENSIDAD", GR)]
        for r, (s, col) in enumerate(rows):
            ak = ease((u - 0.6 - r * 1.0) / 0.35)
            if ak <= 0: continue
            y = 545 + r * 112
            ctx.new_path(); ctx.arc(150, y - 12, 10, 0, 6.283); ctx.set_source_rgba(*col, ak); ctx.fill()
            sz = fit_size(ctx, s, F_MONO, 42, 760, True)
            text(ctx, s, 185 + (1 - ak) * 30, y, F_MONO, sz, col, ak, bold=True)
        mk = clamp((u - 4.6) / 2.0)
        if u > 4.3:
            a = ease((u - 4.3) / 0.4); cx, cy, r = 470, 1080, 70
            ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*CY, 0.18 * a); ctx.set_line_width(12); ctx.stroke()
            ctx.new_path(); ctx.arc(cx, cy, r, -math.pi / 2, -math.pi / 2 + 6.283 * mk); ctx.set_source_rgba(*AM, a); ctx.set_line_width(12); ctx.stroke()
            text(ctx, str(max(1, int(round(1 + 7 * mk)))), cx, cy + 22, F_BIG, 64, WH, a, align="center")
            text(ctx, "SEMANAS", cx + 110, cy + 12, F_MONO, 30, AM, a, bold=True)
    elif i == 4:
        v = int(174 * ease((u - 0.5) / 2.2))
        big(ctx, "+%d %%" % v, 540, 700, 200, GR, k)
        vbars(ctx, [("ANTES", 0.36, MU), ("DESPUÉS", 1.0, GR)], 300, 1150, 200, 80, 330, (u - 0.6) / 1.5, a=k, label_size=28)
    elif i == 5:
        ctx.save(); skeleton(ctx, 300, 470, 0.72, t, hl={"legs": (GR, 1.0)}, base_a=0.6 * k, scan=False); ctx.restore()
        g = ease((u - 0.4) / 1.4)
        cx, cy = 770, 680
        ctx.new_path(); ctx.arc(cx, cy, 150, 0, 6.283); ctx.set_source_rgba(*MU, 0.7 * k); ctx.set_line_width(3); ctx.set_dash([10, 8]); ctx.stroke(); ctx.set_dash([])
        rr = 150 * (1 + 0.0440 * g) + 6 * g
        ctx.new_path(); ctx.arc(cx, cy, rr, 0, 6.283); ctx.set_source_rgba(*GR, 0.18 * k); ctx.fill_preserve()
        ctx.set_source_rgba(*GR, k); ctx.set_line_width(5); ctx.stroke()
        big(ctx, "+9 %", cx, 1060, 140, GR, g, maxw=380)
    elif i == 6:
        v = 0.35 * (1 + 0.48 * ease((u - 0.3) / 1.5))
        gauge(ctx, 540, 740, 240, v, a=k)
        big(ctx, "+48 %", 540, 1035, 120, GR, ease((u - 0.8) / 0.4), maxw=420)
        footprints(ctx, 150, 930, 1170, t, 0.6 + 0.6 * ease((u - 0.3) / 1.5), a=k)
    elif i == 7:
        skeleton(ctx, 540, 450, 0.78, t, hl={"legs": (GR, 1), "arms": (GR, 1), "spine": (GR, 1), "hips": (GR, 1)}, base_a=0.8 * k)
    elif i == 8:
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 820); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 190, CY, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "EXPEDIENTE · MÚSCULO", W / 2, 196, CY, k, 28)
        title(ctx, "¿MÚSCULO A LOS 90 AÑOS?", WH, 350, 92, k)
        text(ctx, "AÑOS", 790, 870, F_MONO, 36, AM, k, align="center", bold=True)
    elif i == 1:
        pill(ctx, "SARCOPENIA", W / 2, 196, RD, k, 30)
        title(ctx, "−3 A −8 % POR DÉCADA", RD, 345, 92, k)
        text(ctx, "Pérdida de masa muscular desde los 30 años", W / 2, 1265, F_MONO, 20, MU, k, align="center")
    elif i == 2:
        pill(ctx, "DESPUÉS DE LOS 60", W / 2, 196, RD, k, 30)
        title(ctx, "LA PÉRDIDA SE ACELERA", WH, 345, 92, k)
        a = ease((u - 0.6) / 0.4)
        text(ctx, "MÁS RÁPIDO", 830, 620, F_MONO, 32, RD, a, align="center", bold=True)
        text(ctx, "esquema ilustrativo", W / 2, 1265, F_MONO, 20, MU, k, align="center")
    elif i == 3:
        pill(ctx, "ESTUDIO · JAMA 1990", W / 2, 196, GR, k, 30)
        title(ctx, "LO PUSIERON A PRUEBA", GR, 345, 92, k)
    elif i == 4:
        pill(ctx, "RESULTADO 01", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "FUERZA", WH, 345, 96, k)
        text(ctx, "aumento promedio · Fiatarone et al., JAMA 1990", W / 2, 1265, F_MONO, 20, MU, k, align="center")
    elif i == 5:
        pill(ctx, "RESULTADO 02", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "MÚSCULO DEL MUSLO", WH, 345, 92, k)
        text(ctx, "ÁREA DEL MÚSCULO", 770, 495, F_MONO, 26, GR, k, align="center", bold=True)
    elif i == 6:
        pill(ctx, "RESULTADO 03", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "VELOCIDAD AL CAMINAR", WH, 345, 92, k)
    elif i == 7:
        title(ctx, "A CUALQUIER EDAD", GR, 345, 100, k)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)
        a = ease((u - 0.8) / 0.4)
        if a > 0:
            pulse = 1 + 0.04 * math.sin(t * 7)
            ctx.save(); ctx.translate(540, 1000); ctx.scale(pulse, pulse)
            rrect(ctx, -170, -50, 340, 100, 50); ctx.set_source_rgba(*RD, a); ctx.fill()
            text(ctx, "SEGUIR", 0, 18, F_UI, 50, WH, a, align="center", bold=True); ctx.restore()


run_episode(neon, txt, "EXPEDIENTE 05 · MÚSCULO")
