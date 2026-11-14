"""v023 · ¿Qué dice la fuerza de tu mano sobre tu salud? Estudio PURE explicado (serie LONGEVIDAD · paleta grafito + naranja + hielo)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (1.0, 0.56, 0.26)   # naranja
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.09, 0.09, 0.12], [0.012, 0.012, 0.02])
from engine_ext import *
CY = ACC
IC = (0.50, 0.88, 1.0)   # celeste hielo para datos


def dynamometer(ctx, cx, cy, s, t, a=1.0, sq=0.0, val=0.0):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    # dial
    ctx.new_path(); ctx.arc(0, -150, 120, 0, 6.283); ctx.set_source_rgba(*CY, 0.08 * a); ctx.fill_preserve()
    ctx.set_source_rgba(*CY, 0.95 * a); ctx.set_line_width(6); ctx.stroke()
    for k in range(13):
        ang = math.pi * (0.75 + 1.5 * k / 12)
        ctx.move_to(math.cos(ang) * 92, -150 + math.sin(ang) * 92); ctx.line_to(math.cos(ang) * 108, -150 + math.sin(ang) * 108)
    ctx.set_source_rgba(1, 1, 1, 0.7 * a); ctx.set_line_width(3); ctx.stroke()
    ang = math.pi * (0.75 + 1.5 * val)
    ctx.move_to(0, -150); ctx.line_to(math.cos(ang) * 88, -150 + math.sin(ang) * 88)
    ctx.set_source_rgba(*IC, a); ctx.set_line_width(7); ctx.stroke()
    ctx.new_path(); ctx.arc(0, -150, 10, 0, 6.283); ctx.set_source_rgba(1, 1, 1, a); ctx.fill()
    # body + handles
    rrect(ctx, -40, -30, 80, 300, 24); ctx.set_source_rgba(*CY, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.9 * a); ctx.set_line_width(5); ctx.stroke()
    gx = 120 - 40 * sq
    rrect(ctx, gx - 20, 0, 40, 260, 20); ctx.set_source_rgba(*IC, 0.15 * a); ctx.fill_preserve(); ctx.set_source_rgba(*IC, 0.95 * a); ctx.stroke()
    ctx.move_to(40, 30); ctx.line_to(gx - 20, 30); ctx.move_to(40, 230); ctx.line_to(gx - 20, 230); ctx.set_source_rgba(*CY, 0.8 * a); ctx.stroke()
    # fingers
    for j in range(4):
        y = 30 + j * 62
        rrect(ctx, gx + 14, y, 70, 48, 22); ctx.set_source_rgba(1, 1, 1, 0.08 * a); ctx.fill_preserve(); ctx.set_source_rgba(1, 1, 1, 0.55 * a); ctx.set_line_width(3); ctx.stroke()
    ctx.restore()


def globe(ctx, cx, cy, r, t, a=1.0, n=17, kd=1.0):
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*CY, 0.06 * a); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.9 * a); ctx.set_line_width(4); ctx.stroke()
    for k in range(1, 4):
        ctx.save(); ctx.translate(cx, cy); ctx.scale(math.cos(t * 0.6 + k * 0.8), 1); ctx.new_path(); ctx.arc(0, 0, r, 0, 6.283); ctx.restore()
        ctx.set_source_rgba(*CY, 0.25 * a); ctx.set_line_width(2); ctx.stroke()
    for k in (-0.5, 0, 0.5):
        yy = cy + k * r; hw = math.sqrt(1 - k * k) * r
        ctx.move_to(cx - hw, yy); ctx.line_to(cx + hw, yy); ctx.set_source_rgba(*CY, 0.25 * a); ctx.stroke()
    for j in range(n):
        if j / n > kd: break
        ang = j * 2.4; rr = r * 0.85 * math.sqrt((j + 0.5) / n)
        x = cx + math.cos(ang) * rr; y = cy + math.sin(ang) * rr * 0.9
        ph = 0.6 + 0.4 * math.sin(t * 4 + j)
        ctx.new_path(); ctx.arc(x, y, 9, 0, 6.283); ctx.set_source_rgba(*IC, a * ph); ctx.fill()


def crowd(ctx, x0, y0, cols, rows, kd, a=1.0, sp=40):
    n = cols * rows
    for j in range(n):
        if j / n > kd: break
        x = x0 + (j % cols) * sp; y = y0 + (j // cols) * sp
        col = IC if (j // cols) % 2 == 0 else CY
        ctx.new_path(); ctx.arc(x, y - 9, 7, 0, 6.283); ctx.set_source_rgba(*col, 0.85 * a); ctx.fill()
        ctx.new_path(); ctx.arc(x, y + 9, 11, math.pi, 0); ctx.fill()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        sq = 0.5 + 0.5 * math.sin(t * 3)
        dynamometer(ctx, 540, 760, 1.15, t, k, sq=sq, val=0.25 + 0.5 * sq)
    elif i == 1:
        globe(ctx, 540, 760, 260, t, k, kd=ease((u - 0.6) / 2.0))
        n = int(139691 * ease((u - 0.5) / 2.2))
        big(ctx, "{:,}".format(n).replace(",", "."), 540, 1130, 120, IC, ease((u - 0.4) / 0.4))
    elif i == 2:
        v = 0.75 - 0.3 * ease((u - 0.6) / 1.6)
        dynamometer(ctx, 260, 790, 0.95, t, k, sq=0.4, val=v)
        ka = ease((u - 0.8) / 0.4)
        text(ctx, "−5 KG", 510, 720, F_BIG, 54, WH, ka, align="center")
        ctx.move_to(450, 760); ctx.line_to(570, 760); ctx.set_source_rgba(1, 1, 1, ka); ctx.set_line_width(6); ctx.stroke()
        ctx.move_to(550, 740); ctx.line_to(575, 760); ctx.line_to(550, 780); ctx.stroke()
        big(ctx, "+16 %", 735, 790, 120, CY, ease((u - 4.2) / 0.4), maxw=300)
        text(ctx, "RIESGO DE MORIR", 735, 850, F_MONO, 24, MU, ease((u - 4.2) / 0.4), align="center", bold=True)
    elif i == 3:
        dynamometer(ctx, 300, 820, 0.8, t, k, sq=0.5, val=0.6)
        ka = ease((u - 1.8) / 0.4)
        # brazalete de presión
        rrect(ctx, 640, 640, 240, 300, 40); ctx.set_source_rgba(*MU, 0.08 * ka); ctx.fill_preserve(); ctx.set_source_rgba(*MU, 0.8 * ka); ctx.set_line_width(4); ctx.stroke()
        gauge(ctx, 760, 760, 80, 0.55, ka * 0.8, col=MU)
        text(ctx, ">", 495, 830, F_BIG, 150, CY, ease((u - 2.6) / 0.4), align="center")
    elif i == 4:
        crowd(ctx, 150, 590, 20, 11, ease((u - 0.3) / 2.6), k, sp=40)
        ka = ease((u - 3.2) / 0.4)
        for j, (lab, col, x) in enumerate((("MUJERES +20 %", IC, 300), ("HOMBRES +16 %", CY, 740))):
            rrect(ctx, x - 175, 1050, 350, 84, 42); ctx.set_source_rgba(0.02, 0.02, 0.03, 0.85 * ka); ctx.fill_preserve()
            ctx.set_source_rgba(*col, ka); ctx.set_line_width(4); ctx.stroke()
            text(ctx, lab, x, 1104, F_MONO, 28, col, ka, align="center", bold=True)
    elif i == 5:
        for j, (lab, col, x) in enumerate((("AGARRE", IC, 300), ("SALUD", CY, 760))):
            kk = ease((u - 0.3 - j * 0.6) / 0.5)
            ctx.new_path(); ctx.arc(x, 800, 150, 0, 6.283); ctx.set_source_rgba(*col, 0.10 * kk * k); ctx.fill_preserve()
            ctx.set_source_rgba(*col, kk * k); ctx.set_line_width(5); ctx.stroke()
            text(ctx, lab, x, 812, F_MONO, 32, col, kk * k, align="center", bold=True)
        ka = ease((u - 1.6) / 0.5)
        ctx.set_dash([18, 14]); ctx.move_to(460, 800); ctx.line_to(600, 800)
        ctx.set_source_rgba(1, 1, 1, ka * k); ctx.set_line_width(5); ctx.stroke(); ctx.set_dash([])
        big(ctx, "?", 530, 720, 110, RD, ka * k)
    elif i == 6:
        dynamometer(ctx, 540, 800, 0.95, t, k, sq=0.5 + 0.5 * math.sin(t * 5), val=0.5)
        big(ctx, "?", 800, 640, 160, RD, ease((u - 1.4) / 0.4))
    elif i == 7:
        hk = ease((u - 0.6) / 0.6)
        skeleton(ctx, 540, 480, 0.6, t, hl={"arms": (CY, hk), "legs": (CY, hk), "spine": (CY, hk), "hips": (CY, hk)}, base_a=0.75 * k)
    elif i == 8:
        dynamometer(ctx, 540, 640, 0.7, t, k, sq=0.5 + 0.5 * math.sin(t * 3), val=0.7)
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
        pill(ctx, "ESTUDIO EXPLICADO · LONGEVIDAD", W / 2, 196, CY, k, 28)
        title(ctx, "TU MANO VS. TU PRESIÓN", WH, 350, 98, k)
        text(ctx, "FUERZA DE AGARRE", W / 2, 1170, F_MONO, 36, IC, ease((u - 1.6) / 0.4), align="center", bold=True)
    elif i == 1:
        pill(ctx, "THE LANCET · 2015", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "ESTUDIO PURE · 17 PAÍSES", WH, 345, 96, k)
        text(ctx, "ADULTOS DE 35 A 70 AÑOS", W / 2, 1185, F_MONO, 30, MU, ease((u - 2.4) / 0.4), align="center", bold=True)
        src(ctx, "Leong et al., Lancet 2015 · doi:10.1016/S0140-6736(14)62000-6", k, 1245)
    elif i == 2:
        pill(ctx, "POR CADA 5 KG MENOS", W / 2, 196, IC, k, 28, filled=True)
        title(ctx, "+16 % RIESGO DE MORIR", WH, 345, 100, ease((u - 4.0) / 0.4))
        text(ctx, "SEGUIMIENTO MEDIANO: 4 AÑOS", W / 2, 1185, F_MONO, 28, MU, k, align="center", bold=True)
        src(ctx, "HR 1,16 (IC95 % 1,13–1,20) · Leong et al., Lancet 2015", k, 1245)
    elif i == 3:
        pill(ctx, "MUERTE CARDIOVASCULAR", W / 2, 196, CY, k, 28)
        title(ctx, "MEJOR PREDICTOR", WH, 345, 110, k)
        text(ctx, "AGARRE", 300, 1120, F_MONO, 32, IC, k, align="center", bold=True)
        text(ctx, "PRESIÓN SISTÓLICA", 760, 1120, F_MONO, 28, MU, ease((u - 1.8) / 0.4), align="center", bold=True)
        src(ctx, "Leong et al., Lancet 2015", k, 1200)
    elif i == 4:
        pill(ctx, "BMJ · 2018", W / 2, 196, IC, k, 30, filled=True)
        title(ctx, "502.293 PERSONAS", WH, 345, 106, k)
        text(ctx, "UK BIOBANK · RIESGO POR CADA 5 KG MENOS", W / 2, 450, F_MONO, 25, MU, k, align="center", bold=True)
        src(ctx, "Celis-Morales et al., BMJ 2018 · doi:10.1136/bmj.k1651", k, 1210)
    elif i == 5:
        pill(ctx, "OJO", W / 2, 196, RD, k, 30)
        title(ctx, "ASOCIACIÓN NO ES CAUSA", WH, 350, 92, k)
        text(ctx, "EL AGARRE REFLEJA TU FUERZA GENERAL", W / 2, 1050, F_MONO, 28, AM, ease((u - 3.0) / 0.4), align="center", bold=True)
        src(ctx, "Soysal et al., J Sport Health Sci 2021 · 34 estudios, 1,8 millones", k, 1140)
    elif i == 6:
        pill(ctx, "AÚN NO PROBADO", W / 2, 196, RD, k, 30)
        title(ctx, "¿ENTRENAR SOLO EL AGARRE?", WH, 345, 90, k)
        text(ctx, "FALTAN ENSAYOS QUE LO DEMUESTREN", W / 2, 1150, F_MONO, 28, MU, ease((u - 1.0) / 0.4), align="center", bold=True)
        src(ctx, "Leong et al., Lancet 2015", k, 1215)
    elif i == 7:
        pill(ctx, "LA IDEA", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "FUERZA DE TODO EL CUERPO", WH, 345, 92, k)
        text(ctx, "≥ 2 DÍAS POR SEMANA", W / 2, 1190, F_MONO, 36, IC, ease((u - 3.0) / 0.4), align="center", bold=True)
        src(ctx, "OMS 2020 · Bull et al., Br J Sports Med 2020", k, 1250)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)


run_episode(neon, txt, "EXPEDIENTE 23 · LONGEVIDAD")
