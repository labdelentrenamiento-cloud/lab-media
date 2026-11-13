"""v019 · ¿Qué ejercicio ayuda más contra la depresión? (serie CEREBRO · paleta magenta + turquesa)
Uso: copiar a la carpeta del episodio (con timeline.json) y correr
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

# ---- paleta de la serie CEREBRO (acento magenta, fondo ciruela)
ACC = (1.0, 0.46, 0.80)
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.15, 0.04, 0.14], [0.022, 0.006, 0.024])
from engine_ext import *
CY = ACC
TL = (0.36, 0.95, 0.85)   # turquesa para datos


def badge(ctx, cx, cy, r, lab, col, a, check=0.0):
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve()
    ctx.set_source_rgba(*col, a); ctx.set_line_width(6); ctx.stroke()
    big(ctx, lab, cx, cy + 22, 64, col, a, maxw=r * 1.7)
    if check > 0:
        x, y = cx + r * 0.7, cy - r * 0.7
        ctx.new_path(); ctx.arc(x, y, 44, 0, 6.283); ctx.set_source_rgba(*GR, check * a); ctx.fill()
        ctx.move_to(x - 20, y); ctx.line_to(x - 5, y + 16); ctx.line_to(x + 22, y - 16)
        ctx.set_source_rgba(0.05, 0.05, 0.08, check * a); ctx.set_line_width(9); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        brain(ctx, 540, 800, 1.7, t, k, col=CY, fire=ease((u - 1.0) / 0.8))
    elif i == 1:
        n1 = int(218 * ease((u - 0.2) / 1.4)); n2 = int(14170 * ease((u - 0.9) / 1.6))
        big(ctx, str(n1), 540, 740, 200, CY, k)
        big(ctx, "{:,}".format(n2).replace(",", "."), 540, 1060, 150, TL, ease((u - 0.8) / 0.4))
    elif i == 2:
        items = [("CAMINAR\nTROTAR", 0.62, TL), ("YOGA", 0.55, CY), ("FUERZA", 0.49, AM), ("AERÓB.\nMIXTO", 0.43, MU), ("TAI CHI", 0.42, MU)]
        vbars(ctx, items, 162, 1050, 132, 24, 600, ease((u - 0.3) / 2.4), k, label_size=22)
        for j, (lab, v, col) in enumerate(items):
            kk = ease((ease((u - 0.3) / 2.4) - j * 0.15) / 0.7)
            if kk > 0.8:
                text(ctx, ("%.2f" % v).replace(".", ","), 162 + j * 156 + 66, 1050 - 600 * v - 18, F_MONO, 26, WH, k, align="center", bold=True)
    elif i == 3:
        line_chart(ctx, 150, 600, 780, 440, [(lambda f: 0.2 + 0.6 * f, TL, ease((u - 0.3) / 2.6), True)],
                   [(0.0, "SUAVE"), (0.5, "MODERADA"), (1.0, "INTENSA")], "INTENSIDAD INDICADA", "REDUCCIÓN DE SÍNTOMAS", k)
    elif i == 4:
        badge(ctx, 320, 820, 190, "FUERZA", AM, k, check=ease((u - 1.0) / 0.4))
        badge(ctx, 760, 820, 190, "YOGA", CY, ease((u - 0.5) / 0.4), check=ease((u - 1.4) / 0.4))
    elif i == 5:
        gauge(ctx, 540, 860, 220, 0.25 * ease((u - 0.4) / 1.2), a=k, col=RD)
    elif i == 6:
        for j, (lab, col, x, y) in enumerate((("PSICOTERAPIA", VI, 390, 720), ("ANTIDEPRESIVOS", TL, 690, 720), ("EJERCICIO", CY, 540, 960))):
            kk = ease((u - 0.3 - j * 0.9) / 0.5)
            ctx.new_path(); ctx.arc(x, y, 200, 0, 6.283); ctx.set_source_rgba(*col, 0.10 * kk * k); ctx.fill_preserve()
            ctx.set_source_rgba(*col, kk * k); ctx.set_line_width(5); ctx.stroke()
            text(ctx, lab, x + (-60 if j == 0 else 60 if j == 1 else 0), y + (-40 if j < 2 else 90), F_MONO, 28, col, kk * k, align="center", bold=True)
    elif i == 7:
        brain(ctx, 540, 760, 1.3, t, k, col=CY, fire=0.6)
        nerve(ctx, [(200, 1110), (540, 1060), (880, 1110)], t, a=ease((u - 0.6) / 0.4), col=TL)
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
        pill(ctx, "ESTUDIO EXPLICADO · CEREBRO", W / 2, 196, CY, k, 28)
        title(ctx, "EJERCICIO VS. DEPRESIÓN", WH, 350, 96, k)
        src(ctx, "Noetel et al., BMJ 2024 · metaanálisis en red", k, 1180)
    elif i == 1:
        pill(ctx, "METAANÁLISIS EN RED · BMJ 2024", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "ENSAYOS ALEATORIZADOS", WH, 345, 90, k)
        text(ctx, "ENSAYOS", W / 2, 830, F_MONO, 30, CY, k, align="center", bold=True)
        text(ctx, "PERSONAS CON DEPRESIÓN", W / 2, 1120, F_MONO, 30, TL, ease((u - 0.8) / 0.4), align="center", bold=True)
        src(ctx, "Noetel et al., BMJ 2024 · doi:10.1136/bmj-2023-075847", k, 1220)
    elif i == 2:
        pill(ctx, "TAMAÑO DEL EFECTO", W / 2, 196, TL, k, 30, filled=True)
        title(ctx, "EL PODIO", WH, 345, 104, k)
        src(ctx, "g de Hedges vs. controles activos · Noetel et al., BMJ 2024", k, 1260)
    elif i == 3:
        pill(ctx, "EFECTO MODERADO", W / 2, 196, CY, k, 30)
        title(ctx, "MÁS INTENSO, MÁS EFECTO", TL, 345, 92, k)
        src(ctx, "esquema ilustrativo · Noetel et al., BMJ 2024", k, 1250)
    elif i == 4:
        pill(ctx, "ADHERENCIA", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "LOS MEJOR TOLERADOS", WH, 345, 94, k)
        src(ctx, "Noetel et al., BMJ 2024", k, 1130)
    elif i == 5:
        pill(ctx, "OJO", W / 2, 196, RD, k, 30)
        title(ctx, "CERTEZA DE LA EVIDENCIA: BAJA", WH, 345, 80, k)
        text(ctx, "NO REEMPLAZA TU TRATAMIENTO", W / 2, 1140, F_MONO, 32, AM, ease((u - 2.4) / 0.4), align="center", bold=True)
        src(ctx, "solo 1 estudio con bajo riesgo de sesgo · CINeMA", k, 1220)
    elif i == 6:
        pill(ctx, "PROPUESTA DE LOS AUTORES", W / 2, 196, CY, k, 28)
        title(ctx, "UN TRATAMIENTO CENTRAL MÁS", WH, 345, 86, k)
        src(ctx, "junto a, no en lugar de · Noetel 2024 · Heissel et al., BJSM 2023", k, 1250)
    elif i == 7:
        pill(ctx, "SI TE SIENTES ASÍ", W / 2, 196, TL, k, 30, filled=True)
        title(ctx, "HABLA CON UN PROFESIONAL", WH, 345, 88, k)
        text(ctx, "MOVERTE PUEDE SER PARTE DEL PLAN", W / 2, 1190, F_MONO, 30, TL, ease((u - 1.8) / 0.4), align="center", bold=True)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)


run_episode(neon, txt, "EXPEDIENTE 19 · CEREBRO")
