"""v022 · Si quisieras rendir más con cafeína, harías esto (serie RENDIMIENTO · paleta espresso + menta + caramelo)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (0.42, 1.0, 0.80)   # menta
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.13, 0.075, 0.05], [0.02, 0.01, 0.008])
from engine_ext import *
CY = ACC
CA = (1.0, 0.72, 0.38)   # caramelo para datos


def cup(ctx, cx, cy, s, t, a=1.0, col=CA, fill=0.7):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.move_to(-110, -90); ctx.line_to(110, -90); ctx.line_to(90, 80); ctx.curve_to(80, 110, -80, 110, -90, 80); ctx.close_path()
    ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(5 / s); ctx.stroke()
    lv = -90 + 170 * (1 - fill)
    ctx.move_to(-108 + (lv + 90) * 0.12, lv); ctx.line_to(108 - (lv + 90) * 0.12, lv); ctx.set_source_rgba(*col, 0.6 * a); ctx.set_line_width(3 / s); ctx.stroke()
    ctx.new_path(); ctx.arc(125, -10, 42, -1.3, 1.3); ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(8 / s); ctx.stroke()
    ctx.save(); ctx.scale(1, 0.25); ctx.new_path(); ctx.arc(0, 480, 170, 0, 6.283); ctx.restore()
    ctx.set_source_rgba(*col, 0.5 * a); ctx.set_line_width(3 / s); ctx.stroke()
    for j in (-45, 0, 45):
        ph = (t * 0.6 + j / 90) % 1
        ctx.new_path()
        for z in range(30):
            yy = -110 - z * 5 - ph * 30
            xx = j + 14 * math.sin(z / 4 + t * 3 + j)
            (ctx.move_to if z == 0 else ctx.line_to)(xx, yy)
        ctx.set_source_rgba(*CY, 0.7 * a * (1 - ph * 0.5)); ctx.set_line_width(5 / s); ctx.stroke()
    ctx.restore()


def bolt(ctx, cx, cy, s, a=1.0, col=CY):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.move_to(10, -60); ctx.line_to(-30, 8); ctx.line_to(0, 8); ctx.line_to(-12, 60); ctx.line_to(32, -12); ctx.line_to(4, -12); ctx.close_path()
    ctx.set_source_rgba(*col, 0.25 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4 / s); ctx.stroke()
    ctx.restore()


def moon(ctx, cx, cy, r, a=1.0, col=CY):
    ctx.new_path(); ctx.arc(cx, cy, r, 0.9, 5.4); ctx.arc_negative(cx + r * 0.45, cy - r * 0.2, r * 0.8, 4.9, 1.3); ctx.close_path()
    ctx.set_source_rgba(*col, 0.15 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(5); ctx.stroke()


def wheel(ctx, cx, cy, r, t, a=1.0, col=CY):
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(6); ctx.stroke()
    for k in range(8):
        ang = k / 8 * 3.1416 + t * 4
        ctx.move_to(cx - math.cos(ang) * r, cy - math.sin(ang) * r); ctx.line_to(cx + math.cos(ang) * r, cy + math.sin(ang) * r)
    ctx.set_source_rgba(*col, 0.4 * a); ctx.set_line_width(2); ctx.stroke()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        cup(ctx, 540, 820, 1.35, t, k)
        ka = ease((u - 1.6) / 0.4)
        bolt(ctx, 840, 620, 1.5, ka); bolt(ctx, 240, 640, 1.1, ka * 0.8)
    elif i == 1:
        for j in range(21):
            kk = ease((u - 0.4 - j * 0.07) / 0.3)
            x = 230 + (j % 7) * 103; y = 560 + (j // 7) * 110
            ctx.new_path(); ctx.arc(x, y, 38, 0, 6.283); ctx.set_source_rgba(*CY, 0.12 * kk * k); ctx.fill_preserve()
            ctx.set_source_rgba(*CY, kk * k); ctx.set_line_width(3); ctx.stroke()
            text(ctx, "MA", x, y + 9, F_MONO, 22, WH, kk * k * 0.8, align="center", bold=True)
        for j, (lab, x) in enumerate((("RESISTENCIA", 245), ("FUERZA", 540), ("POTENCIA", 820))):
            ka = ease((u - 2.6 - j * 0.6) / 0.4)
            rrect(ctx, x - 118, 930, 236, 76, 38); ctx.set_source_rgba(*CA, 0.14 * ka); ctx.fill_preserve()
            ctx.set_source_rgba(*CA, ka); ctx.set_line_width(3); ctx.stroke()
            text(ctx, lab, x, 978, F_MONO, 23, CA, ka, align="center", bold=True)
    elif i == 2:
        footprints(ctx, 120, 960, 720, t, 2.5, a=k, col=CY)
        wheel(ctx, 380, 920, 110, t, ease((u - 2.6) / 0.4)); wheel(ctx, 700, 920, 110, t, ease((u - 2.6) / 0.4))
        ka = ease((u - 2.6) / 0.4)
        ctx.move_to(380, 920); ctx.line_to(520, 820); ctx.line_to(700, 920); ctx.move_to(520, 820); ctx.line_to(480, 760); ctx.move_to(520, 820); ctx.line_to(640, 790)
        ctx.set_source_rgba(*CY, ka); ctx.set_line_width(6); ctx.stroke()
    elif i == 3:
        big(ctx, "3–6", 540, 760, 230, CA, ease((u - 0.3) / 0.4))
        text(ctx, "MG / KG DE PESO", W / 2, 840, F_MONO, 40, WH, ease((u - 1.6) / 0.4), align="center", bold=True)
        clock(ctx, 540, 1010, 90, t, back=0.0, a=ease((u - 3.4) / 0.4), col=CY)
    elif i == 4:
        ka = ease((u - 0.3) / 0.4)
        rrect(ctx, 110, 560, 240, 150, 30); ctx.set_source_rgba(*CY, 0.12 * ka); ctx.fill_preserve(); ctx.set_source_rgba(*CY, ka); ctx.set_line_width(4); ctx.stroke()
        text(ctx, "70 KG", 230, 655, F_BIG, 64, WH, ka, align="center")
        text(ctx, "× 3 MG", 515, 655, F_MONO, 44, CA, ease((u - 1.4) / 0.4), align="center", bold=True)
        kb = ease((u - 2.4) / 0.4)
        rrect(ctx, 680, 560, 250, 150, 30); ctx.set_source_rgba(*CA, 0.14 * kb); ctx.fill_preserve(); ctx.set_source_rgba(*CA, kb); ctx.set_line_width(4); ctx.stroke()
        text(ctx, "≈210 MG", 805, 655, F_BIG, 56, WH, kb, align="center")
        kc = ease((u - 3.8) / 0.4)
        cup(ctx, 400, 960, 0.8, t, kc); cup(ctx, 680, 960, 0.8, t, kc)
    elif i == 5:
        v = 0.3 + 0.62 * ease((u - 0.8) / 2.6)
        gauge(ctx, 540, 860, 250, v, k, col=RD if v > 0.75 else CA)
        ctx.new_path(); ctx.arc(540, 860, 250, math.pi * (0.8 + 1.4 * 0.75), math.pi * 2.2); ctx.set_source_rgba(*RD, 0.6 * k); ctx.set_line_width(18); ctx.stroke()
        text(ctx, "3–6", 540 + math.cos(math.pi * 1.35) * 320, 860 + math.sin(math.pi * 1.35) * 320, F_MONO, 30, CA, k, align="center", bold=True)
        text(ctx, "9 MG/KG", 830, 700, F_MONO, 30, RD, ease((u - 2.6) / 0.4), align="center", bold=True)
    elif i == 6:
        moon(ctx, 540, 720, 170, k)
        for j in range(3):
            ph = (t * 0.4 + j / 3) % 1
            text(ctx, "z", 700 + j * 50, 600 - ph * 120, F_BIG, 60 - j * 10, CY, k * (1 - ph), align="center")
        big(ctx, "−45 MIN", 540, 1080, 140, CA, ease((u - 3.4) / 0.4))
    elif i == 7:
        clock(ctx, 540, 740, 190, t, back=0.0, a=k, col=CY)
        big(ctx, "≥ 9 H", 540, 1060, 130, CA, ease((u - 1.0) / 0.4))
    elif i == 8:
        cup(ctx, 540, 640, 0.95, t, k)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1000); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 170, CY, 1, align="center"); ctx.restore()


def src(ctx, s, k, y=1290):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "SI QUISIERAS… · RENDIMIENTO", W / 2, 196, CY, k, 28)
        title(ctx, "CAFEÍNA PARA RENDIR MÁS", WH, 350, 96, k)
        text(ctx, "LO QUE DICE LA EVIDENCIA", W / 2, 1170, F_MONO, 34, CA, ease((u - 2.4) / 0.4), align="center", bold=True)
    elif i == 1:
        pill(ctx, "BR J SPORTS MED · 2019", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "21 METAANÁLISIS", WH, 345, 104, k)
        text(ctx, "REVISIÓN PARAGUAS · CALIDAD MODERADA", W / 2, 450, F_MONO, 26, MU, k, align="center", bold=True)
        src(ctx, "Grgic et al., Br J Sports Med 2019 · doi:10.1136/bjsports-2018-100278", k, 1120)
    elif i == 2:
        pill(ctx, "POSTURA ISSN · 2021", W / 2, 196, CA, k, 28, filled=True)
        title(ctx, "MÁS CONSTANTE EN RESISTENCIA", WH, 345, 86, k)
        text(ctx, "CORRER · PEDALEAR", W / 2, 1140, F_MONO, 32, CY, ease((u - 2.6) / 0.4), align="center", bold=True)
        src(ctx, "Guest et al., J Int Soc Sports Nutr 2021 · doi:10.1186/s12970-020-00383-4", k, 1215)
    elif i == 3:
        pill(ctx, "LA DOSIS", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "LO QUE USAN LOS ESTUDIOS", WH, 345, 90, k)
        text(ctx, "≈ 60 MIN ANTES", W / 2, 1170, F_MONO, 34, CA, ease((u - 3.6) / 0.4), align="center", bold=True)
        src(ctx, "Guest et al., J Int Soc Sports Nutr 2021", k, 1235)
    elif i == 4:
        pill(ctx, "EJEMPLO", W / 2, 196, CA, k, 30, filled=True)
        title(ctx, "≈ 2 TAZAS DE CAFÉ", WH, 345, 104, k)
        text(ctx, "1 TAZA (250 ML) ≈ 100 MG · VARÍA MUCHO", W / 2, 1150, F_MONO, 26, MU, ease((u - 4.0) / 0.4), align="center", bold=True)
        src(ctx, "EFSA 2015: hasta 200 mg por dosis, sin riesgo en adultos sanos", k, 1215)
    elif i == 5:
        pill(ctx, "OJO", W / 2, 196, RD, k, 30)
        title(ctx, "MÁS NO ES MEJOR", WH, 345, 110, k)
        text(ctx, "MÁS EFECTOS SECUNDARIOS · SIN MÁS BENEFICIO", W / 2, 1160, F_MONO, 25, AM, ease((u - 2.8) / 0.4), align="center", bold=True)
        src(ctx, "Guest et al., J Int Soc Sports Nutr 2021", k, 1225)
    elif i == 6:
        pill(ctx, "SLEEP MED REV · 2023", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "CUIDA TU SUEÑO", WH, 345, 110, k)
        text(ctx, "MENOS SUEÑO TOTAL · 24 ESTUDIOS", W / 2, 1150, F_MONO, 28, MU, ease((u - 3.6) / 0.4), align="center", bold=True)
        src(ctx, "Gardiner et al., Sleep Med Rev 2023 · doi:10.1016/j.smrv.2023.101764", k, 1215)
    elif i == 7:
        pill(ctx, "ANTES DE DORMIR", W / 2, 196, CA, k, 28, filled=True)
        title(ctx, "CAFÉ: 8,8 H ANTES COMO MÍNIMO", WH, 345, 80, k)
        text(ctx, "¿EMBARAZO O CONDICIÓN MÉDICA? CONSULTA", W / 2, 1150, F_MONO, 26, AM, ease((u - 3.0) / 0.4), align="center", bold=True)
        src(ctx, "Gardiner et al., 2023 · EFSA 2015 (embarazo: máx. 200 mg/día)", k, 1215)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)


run_episode(neon, txt, "EXPEDIENTE 22 · RENDIMIENTO")
