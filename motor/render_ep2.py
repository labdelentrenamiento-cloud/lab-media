import sys, math
sys.path.insert(0, "/home/claude/lab")
from engine_ext import *


def hippo_chart(ctx, upto, k):
    fn = lambda f: 0.9 - 0.55 * f ** 1.3
    line_chart(ctx, 130, 560, 820, 500, [(fn, VI, upto, True)],
               [(i / 5, str(55 + 5 * i)) for i in range(6)], "EDAD (AÑOS)", "VOLUMEN DEL HIPOCAMPO", a=k)


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        brain(ctx, 540, 700, 1.45, t, a=k, fire=0.6, hippo=(GR, ease((u - 1.2) / 0.6)))
        footprints(ctx, 150, 930, 1130, t, 1.0, a=k, col=GR)
    elif i == 1:
        hk = ease((u - 0.4) / 0.5)
        brain(ctx, 470, 720, 1.5, t, a=k, hippo=(CY, hk))
        if hk > 0: callout(ctx, 470 + 30 * 1.5, 720 + 60 * 1.5, 760, 1040, "MEMORIA", CY, hk, sub="aprendizaje")
    elif i == 2:
        hippo_chart(ctx, ease((u - 0.2) / 3.0), k)
    elif i == 3:
        rrect(ctx, 90, 440, 900, 780, 28)
        ctx.set_source_rgba(*CY, 0.06 * k); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.7 * k); ctx.set_line_width(3); ctx.stroke()
        big(ctx, str(int(120 * ease((u - 0.3) / 1.2))), 540, 690, 220, CY, k, maxw=500)
        rows = [("ADULTOS MAYORES SEDENTARIOS", WH), ("SEGUIMIENTO DE 1 AÑO", WH), ("RESONANCIA MAGNÉTICA", GR)]
        for r, (s, col) in enumerate(rows):
            ak = ease((u - 1.4 - r * 0.9) / 0.35)
            if ak <= 0: continue
            y = 830 + r * 100
            ctx.new_path(); ctx.arc(170, y - 12, 10, 0, 6.283); ctx.set_source_rgba(*col, ak); ctx.fill()
            sz = fit_size(ctx, s, F_MONO, 40, 720, True)
            text(ctx, s, 205 + (1 - ak) * 30, y, F_MONO, sz, col, ak, bold=True)
    elif i == 4:
        for x, col in ((290, GR), (790, AM)):
            rrect(ctx, x - 210, 480, 420, 680, 26); ctx.set_source_rgba(*col, 0.05 * k); ctx.fill_preserve()
            ctx.set_source_rgba(*col, 0.6 * k); ctx.set_line_width(3); ctx.stroke()
        footprints(ctx, 110, 470, 820, t, 1.3, a=k, col=GR)
        # stretching: slow wave
        ctx.new_path()
        for s in range(61):
            xx = 620 + s * 5.7; yy = 820 + 60 * math.sin(s * 0.15 + t * 1.2)
            (ctx.move_to if s == 0 else ctx.line_to)(xx, yy)
        ctx.set_source_rgba(*AM, k); ctx.set_line_width(6); ctx.stroke()
    elif i == 5:
        brain(ctx, 540, 720, 1.45, t, a=k, fire=0.8, hippo=(GR, 1.0))
        big(ctx, "+2 %", 540, 1110, 150, GR, ease((u - 0.8) / 0.4), maxw=400)
    elif i == 6:
        zero = 820
        g = ease((u - 0.4) / 1.2)
        rrect(ctx, 260, zero - 300 * g, 200, max(2, 300 * g), 14); ctx.set_source_rgba(*GR, 0.25 * k); ctx.fill_preserve(); ctx.set_source_rgba(*GR, k); ctx.set_line_width(3); ctx.stroke()
        rrect(ctx, 620, zero, 200, max(2, 210 * g), 14); ctx.set_source_rgba(*RD, 0.25 * k); ctx.fill_preserve(); ctx.set_source_rgba(*RD, k); ctx.set_line_width(3); ctx.stroke()
        ctx.move_to(160, zero); ctx.line_to(920, zero); ctx.set_source_rgba(*WH, 0.7 * k); ctx.set_line_width(3); ctx.stroke()
        if g > 0.5:
            big(ctx, "+2,0 %", 360, zero - 330, 76, GR, g, maxw=300)
            big(ctx, "−1,4 %", 720, zero + 300, 76, RD, g, maxw=300)
    elif i == 7:
        clock(ctx, 540, 760, 220, t, back=ease((u - 0.2) / 2.5), a=k)
    elif i == 8:
        k2 = easeb((u - lt(8) - 1.9) / 0.5)
        brain(ctx, 540, 760, 1.1, t, a=k * (1 - ease((u - lt(8) - 1.8) / 0.3)), fire=1.0, hippo=(GR, 1))
        if k2 > 0:
            ctx.save(); ctx.translate(540, 820); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 190, CY, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "40 MIN · 3 VECES POR SEMANA", W / 2, 196, GR, k, 28)
        title(ctx, "CAMINAR HACE CRECER TU CEREBRO", WH, 350, 82, k)
    elif i == 1:
        pill(ctx, "ESCANEO CEREBRAL · ZONA 01", W / 2, 196, CY, k, 28)
        title(ctx, "HIPOCAMPO", CY, 350, 110, k)
    elif i == 2:
        pill(ctx, "ADULTOS MAYORES", W / 2, 196, RD, k, 30)
        title(ctx, "−1 A −2 % CADA AÑO", RD, 345, 96, k)
        text(ctx, "esquema · pérdida típica del hipocampo con la edad", W / 2, 1265, F_MONO, 20, MU, k, align="center")
    elif i == 3:
        pill(ctx, "ESTUDIO · PNAS 2011", W / 2, 196, GR, k, 30)
        title(ctx, "LO MIDIERON", GR, 345, 96, k)
    elif i == 4:
        pill(ctx, "DOS GRUPOS", W / 2, 196, CY, k, 30)
        title(ctx, "CAMINAR VS. ESTIRAR", WH, 345, 92, k)
        text(ctx, "CAMINATA RÁPIDA", 290, 1215, F_MONO, 28, GR, k, align="center", bold=True)
        text(ctx, "ESTIRAMIENTOS", 790, 1215, F_MONO, 28, AM, k, align="center", bold=True)
    elif i == 5:
        pill(ctx, "RESULTADO · 1 AÑO", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "LOS QUE CAMINARON", WH, 345, 92, k)
    elif i == 6:
        pill(ctx, "COMPARACIÓN", W / 2, 196, RD, k, 30)
        title(ctx, "LOS QUE SOLO ESTIRARON", WH, 345, 88, k)
        text(ctx, "CAMINATA", 360, 1150, F_MONO, 28, GR, k, align="center", bold=True)
        text(ctx, "ESTIRAMIENTOS", 720, 600, F_MONO, 28, RD, k, align="center", bold=True)
        text(ctx, "Erickson et al., PNAS 2011 · volumen del hipocampo", W / 2, 1265, F_MONO, 20, MU, k, align="center")
    elif i == 7:
        pill(ctx, "EQUIVALENCIA", W / 2, 196, GR, k, 30)
        title(ctx, "RETROCEDER 1 A 2 AÑOS", GR, 345, 92, k)
        text(ctx, "de pérdida de volumen del hipocampo por la edad", W / 2, 1100, F_MONO, 26, WH, k, align="center", bold=True)
    elif i == 8:
        title(ctx, "TU CEREBRO TAMBIÉN SE ENTRENA", WH, 345, 80, k)
        a = ease((u - lt(8) - 2.2) / 0.4)
        if a > 0:
            pulse = 1 + 0.04 * math.sin(t * 7)
            ctx.save(); ctx.translate(540, 1000); ctx.scale(pulse, pulse)
            rrect(ctx, -170, -50, 340, 100, 50); ctx.set_source_rgba(*RD, a); ctx.fill()
            text(ctx, "SEGUIR", 0, 18, F_UI, 50, WH, a, align="center", bold=True); ctx.restore()


run_episode(neon, txt, "EXPEDIENTE 02 · CEREBRO")
