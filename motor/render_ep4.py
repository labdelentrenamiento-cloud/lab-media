import sys, math
sys.path.insert(0, "/home/claude/lab")
from engine_ext import *


def two_people(ctx, t, a, glowL=0.0):
    ctx.save(); ctx.translate(320, 0); ctx.scale(0.82, 1); ctx.translate(-320, 0)
    skeleton(ctx, 320, 470, 0.62, t, hl={"arms": (GR, glowL), "legs": (GR, glowL)} if glowL else None, base_a=0.85 * a, scan=False)
    ctx.restore()
    ctx.save(); ctx.translate(770, 0); ctx.scale(1.38, 1); ctx.translate(-770, 0)
    skeleton(ctx, 770, 455, 0.64, t, base_a=0.6 * a, scan=False)
    ctx.restore()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        two_people(ctx, t, k, glowL=ease((u - 1.2) / 0.6))
        ctx.save(); ctx.translate(320, 430); ctx.scale(0.42, 0.42); barbell_icon(ctx, 0, 0, t, a=k); ctx.restore()
    elif i == 1:
        cx, cy, r = 540, 690, 170
        ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*AM, 0.08 * k); ctx.fill_preserve()
        ctx.set_source_rgba(*AM, 0.9 * k); ctx.set_line_width(4); ctx.stroke()
        rnd = 0
        for ring in range(1, 6):
            n = ring * 7
            for j in range(n):
                ang = j / n * 6.283 + ring
                rr = ring * 28
                ctx.new_path(); ctx.arc(cx + math.cos(ang) * rr, cy + math.sin(ang) * rr, 10, 0, 6.283)
                ctx.set_source_rgba(*AM, 0.6 * k); ctx.set_line_width(2); ctx.stroke()
    elif i == 2:
        brain(ctx, 300, 570, 0.95, t, a=k, fire=ease((u - 0.8) / 0.5))
        act = 0.15 + 0.8 * ease((u - lt(2) - 1.6) / 2.4)
        nerve(ctx, [(330, 740), (330, 820), (520, 900), (600, 940)], t, a=k, rate=0.6 + 1.6 * act, n=3 + int(act * 4))
        fiber_bundle(ctx, 600, 820, 380, 360, 8, act, t, a=k)
    elif i == 3:
        brain(ctx, 540, 520, 0.45, t, a=k, fire=0.8)
        nerve(ctx, [(520, 560), (420, 640), (350, 700)], t, a=k, col=GR)
        ka = ease((u - lt(3) - 3.2) / 0.6)
        nerve(ctx, [(560, 560), (660, 640), (730, 700)], t, a=k * (0.3 + 0.7 * ka), col=CY)
        leg(ctx, 350, 700, 0.62, a=k, col=GR, fill=0.28)
        leg(ctx, 730, 700, 0.62, a=k, col=CY, fill=0.05 + 0.2 * ka)
        if ka > 0:
            big(ctx, "+12 %", 915, 905, 105 * (0.8 + 0.2 * easeb(ka)), GR, ka, maxw=300)
    elif i == 4:
        for j, (x, smooth, lab_col) in enumerate([(290, 0.0, RD), (790, 1.0, GR)]):
            rrect(ctx, x - 200, 480, 400, 680, 26); ctx.set_source_rgba(*lab_col, 0.05 * k); ctx.fill_preserve()
            ctx.set_source_rgba(*lab_col, 0.6 * k); ctx.set_line_width(3); ctx.stroke()
            pts = []
            for s in range(61):
                yy = 1080 - s * 9.5
                wob = (1 - smooth) * (55 * math.sin(s * 0.45) + 25 * math.sin(s * 1.3 + 1))
                pts.append((x + wob, yy))
            ctx.new_path(); ctx.move_to(*pts[0])
            for p in pts[1:]: ctx.line_to(*p)
            ctx.set_source_rgba(*lab_col, 0.85 * k); ctx.set_line_width(5); ctx.set_dash([10, 8]); ctx.stroke(); ctx.set_dash([])
            f = (math.sin(t * 2.2) * 0.5 + 0.5)
            px, py = pts[int(f * 60)]
            ctx.new_path(); ctx.arc(px, py, 34, 0, 6.283); ctx.set_source_rgba(*WH, 0.15 * k); ctx.fill_preserve()
            ctx.set_source_rgba(*WH, k); ctx.set_line_width(5); ctx.stroke()
    elif i == 5:
        up = ease((u - 0.3) / 3.2)
        wfn = lambda f: (0.35 + 0.65 * f) * 0.9
        sfn = lambda f: 0.9 * 0.35 * ((0.35 + 0.65 * f) / 0.35) ** (2 / 3)
        line_chart(ctx, 130, 560, 820, 500, [(wfn, AM, up, False), (sfn, CY, up, True)],
                   [(0, "LIVIANO"), (1, "PESADO")], "TAMAÑO DEL CUERPO →", "", a=k)
        if up > 0.98:
            text(ctx, "PESO", 960, 560 + 500 - wfn(1) * 500 - 18, F_MONO, 30, AM, 1, align="right", bold=True)
            text(ctx, "FUERZA", 960, 560 + 500 - sfn(1) * 500 + 52, F_MONO, 30, CY, 1, align="right", bold=True)
    elif i == 6:
        vbars(ctx, [("LIVIANO", 1.0, GR), ("MEDIO", 0.91, CY), ("PESADO", 0.82, AM)], 180, 1110, 200, 70, 560, u / 1.0, a=k, label_size=28)
    elif i == 7:
        two_people(ctx, t, k, glowL=1.0)
    elif i == 8:
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 820); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 190, CY, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "EXPEDIENTE · FUERZA", W / 2, 196, CY, k, 28)
        title(ctx, "¿FLACO PERO MÁS FUERTE?", WH, 350, 92, k)
        a = ease((u - 1.2) / 0.4)
        text(ctx, "FLACO", 320, 1160, F_MONO, 34, GR, a, align="center", bold=True)
        text(ctx, "GRANDE", 770, 1160, F_MONO, 34, MU, a, align="center", bold=True)
    elif i == 1:
        pill(ctx, "ANÁLISIS", W / 2, 196, AM, k, 28)
        title(ctx, "LA FUERZA NO ES SOLO TAMAÑO", WH, 345, 84, k)
        text(ctx, "CORTE DEL MÚSCULO", W / 2, 905, F_MONO, 26, AM, k, align="center", bold=True)
        items = [("TAMAÑO", AM), ("NERVIOS", VI), ("TÉCNICA", CY), ("FÍSICA", GR)]
        for j, (s, c) in enumerate(items):
            a = ease((u - 0.9 - j * 0.35) / 0.3)
            if a > 0:
                x = 300 + (j % 2) * 480; y = 990 + (j // 2) * 100
                pill(ctx, s, x, y, c, a, 34)
        a = ease((u - 2.5) / 0.3)
        if a > 0: text(ctx, "+", 540, 1048, F_UI, 56, WH, a, align="center", bold=True)
    elif i == 2:
        pill(ctx, "FACTOR 01", W / 2, 196, VI, k, 30, filled=True)
        title(ctx, "TU SISTEMA NERVIOSO", WH, 345, 90, k)
        text(ctx, "FIBRAS ACTIVAS", 790, 800, F_MONO, 26, GR, k, align="center", bold=True)
        text(ctx, "esquema ilustrativo", W / 2, 1265, F_MONO, 20, MU, k, align="center")
    elif i == 3:
        pill(ctx, "LA PRUEBA · EDUCACIÓN CRUZADA", W / 2, 196, GR, k, 28)
        title(ctx, "ENTRENAS UNA PIERNA…", WH, 345, 88, k)
        text(ctx, "ENTRENADA", 350, 1125, F_MONO, 28, GR, k, align="center", bold=True)
        text(ctx, "SIN ENTRENAR", 730, 1125, F_MONO, 28, CY, k, align="center", bold=True)
        text(ctx, "Manca et al., 2017 · metaanálisis de 31 estudios", W / 2, 1265, F_MONO, 20, MU, k, align="center")
    elif i == 4:
        pill(ctx, "FACTOR 02", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "LA TÉCNICA SE APRENDE", WH, 345, 90, k)
        text(ctx, "REPETICIÓN 1", 290, 1215, F_MONO, 28, RD, k, align="center", bold=True)
        text(ctx, "REPETICIÓN 100", 790, 1215, F_MONO, 28, GR, k, align="center", bold=True)
    elif i == 5:
        pill(ctx, "FACTOR 03", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "LA FÍSICA DEL TAMAÑO", WH, 345, 90, k)
        text(ctx, "FUERZA ∝ MASA^(2/3)", W / 2, 470, F_MONO, 34, CY, k, align="center", bold=True)
        text(ctx, "Escalamiento alométrico (ley de los 2/3)", W / 2, 1265, F_MONO, 20, MU, k, align="center")
    elif i == 6:
        pill(ctx, "RESULTADO", W / 2, 196, GR, k, 30)
        title(ctx, "MÁS FUERZA POR KILO", GR, 345, 92, k)
        text(ctx, "FUERZA RELATIVA AL PESO CORPORAL", W / 2, 470, F_MONO, 28, WH, k, align="center", bold=True)
        text(ctx, "según la ley de los 2/3 · esquema", W / 2, 1265, F_MONO, 20, MU, k, align="center")
    elif i == 7:
        title(ctx, "NO JUZGUES POR EL TAMAÑO", WH, 345, 90, k)
        a = ease((u - 0.5) / 0.4)
        text(ctx, "=", 545, 830, F_BIG, 150, CY, a, align="center")
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)
        a = ease((u - 0.8) / 0.4)
        if a > 0:
            pulse = 1 + 0.04 * math.sin(t * 7)
            ctx.save(); ctx.translate(540, 1000); ctx.scale(pulse, pulse)
            rrect(ctx, -170, -50, 340, 100, 50); ctx.set_source_rgba(*RD, a); ctx.fill()
            text(ctx, "SEGUIR", 0, 18, F_UI, 50, WH, a, align="center", bold=True); ctx.restore()


run_episode(neon, txt, "EXPEDIENTE 04 · FUERZA")
