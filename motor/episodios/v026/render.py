"""v026 · ¿El dolor muscular de los días siguientes es ácido láctico? Mito vs. realidad (serie RECUPERACIÓN · paleta ciruela + ámbar + lavanda)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (1.0, 0.70, 0.24)   # ámbar
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.10, 0.045, 0.13], [0.016, 0.007, 0.022])
from engine_ext import *
CY = ACC
LV = (0.74, 0.62, 1.0)   # lavanda para datos


def sore_spots(ctx, pts, t, a):
    for j, (x, y) in enumerate(pts):
        ph = 0.6 + 0.4 * math.sin(t * 5 + j)
        ctx.new_path(); ctx.arc(x, y, 30 * ph + 10, 0, 6.283); ctx.set_source_rgba(*RD, 0.35 * a); ctx.fill()
        ctx.new_path(); ctx.arc(x, y, 9, 0, 6.283); ctx.set_source_rgba(1, 1, 1, 0.9 * a); ctx.fill()


def treadmill(ctx, cx, cy, ang, t, a, col):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(ang)
    rrect(ctx, -300, -30, 600, 60, 30); ctx.set_source_rgba(*col, 0.12 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(5); ctx.stroke()
    off = (t * 120) % 60
    for x in range(-280, 280, 60):
        xx = x + off
        if -280 < xx < 280:
            ctx.move_to(xx, -20); ctx.line_to(xx, 20); ctx.set_source_rgba(*col, 0.5 * a); ctx.set_line_width(3); ctx.stroke()
    # corredor esquemático
    bob = -abs(math.sin(t * 6)) * 12
    ctx.new_path(); ctx.arc(0, -250 + bob, 30, 0, 6.283); ctx.set_source_rgba(1, 1, 1, 0.9 * a); ctx.set_line_width(5); ctx.stroke()
    ctx.move_to(0, -220 + bob); ctx.line_to(0, -120 + bob); ctx.stroke()
    s = math.sin(t * 6)
    ctx.move_to(0, -120 + bob); ctx.line_to(40 * s, -35); ctx.move_to(0, -120 + bob); ctx.line_to(-40 * s, -35)
    ctx.move_to(0, -200 + bob); ctx.line_to(-45 * s, -150 + bob); ctx.move_to(0, -200 + bob); ctx.line_to(45 * s, -150 + bob)
    ctx.stroke()
    ctx.restore()


def meter(ctx, x, y, w, v, lab, col, a):
    rrect(ctx, x, y, w, 46, 23); ctx.set_source_rgba(*col, 0.08 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.6 * a); ctx.set_line_width(3); ctx.stroke()
    if v > 0.02:
        rrect(ctx, x + 4, y + 4, (w - 8) * v, 38, 19); ctx.set_source_rgba(*col, 0.8 * a); ctx.fill()
    text(ctx, lab, x, y - 16, F_MONO, 26, col, a, bold=True)


def src(ctx, s, k, y=1270):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        leg(ctx, 400, 540, 0.95, k, col=LV)
        leg(ctx, 680, 540, 0.95, k, col=LV)
        sore_spots(ctx, [(385, 670), (415, 750), (690, 680), (665, 765)], t, ease((u - 1.0) / 0.5))
    elif i == 1:
        def lac(x):
            if x < 0.3: return 0.1 + 0.75 * (x / 0.3)
            return 0.1 + 0.75 * math.exp(-(x - 0.3) / 0.12)
        line_chart(ctx, 170, 600, 740, 420, [(lac, CY, ease((u - 0.3) / 3.0), True)],
                   [(0, "INICIO"), (0.3, "FIN"), (0.65, "+30 min"), (1, "+60 min")], "", "LACTATO EN SANGRE", k)
    elif i == 2:
        treadmill(ctx, 540, 840, 0.0, t, k, LV)
        ka = ease((u - 1.6) / 0.4)
        meter(ctx, 200, 1000, 300, 0.85 * ka, "LACTATO", CY, ka)
        kb = ease((u - 4.2) / 0.4)
        meter(ctx, 580, 1000, 300, 0.12 * kb, "DOLOR", RD, kb)
    elif i == 3:
        treadmill(ctx, 540, 820, 0.17, t, k, LV)
        ka = ease((u - 1.4) / 0.4)
        meter(ctx, 200, 1000, 300, 0.05, "LACTATO", CY, ka)
        kb = ease((u - 3.0) / 0.4)
        meter(ctx, 580, 1000, 300, 0.9 * kb, "DOLOR", RD, kb)
    elif i == 4:
        fiber_bundle(ctx, 170, 600, 680, 420, 7, 0.0, t, k, col_on=LV, col_off=LV)
        tears(ctx, 170, 600, 680, 420, 7, ease((u - 0.9) / 1.6), t, seed=5)
        ka = ease((u - 3.4) / 0.4)
        # flecha de frenado (fase excéntrica)
        ctx.move_to(905, 640); ctx.line_to(905, 980); ctx.set_source_rgba(*CY, ka); ctx.set_line_width(8); ctx.stroke()
        ctx.move_to(875, 940); ctx.line_to(905, 985); ctx.line_to(935, 940); ctx.stroke()
    elif i == 5:
        def soreness(x):
            h = x * 120
            return 0.05 + 0.75 * math.exp(-((h - 48) / 26) ** 2) * (h > 6)
        line_chart(ctx, 170, 600, 740, 420, [(soreness, RD, ease((u - 0.3) / 2.6), True)],
                   [(0, "0 h"), (0.2, "24 h"), (0.4, "48 h"), (0.6, "72 h"), (1, "5 d")], "", "DOLOR", k)
        ka = ease((u - 3.4) / 0.4)
        x0, x1 = 170 + 0.2 * 740, 170 + 0.6 * 740
        rrect(ctx, x0, 600, x1 - x0, 420, 12); ctx.set_source_rgba(*CY, 0.08 * ka); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.7 * ka); ctx.set_line_width(3); ctx.stroke()
    elif i == 6:
        vbars(ctx, [("CON DAÑO\nY DOLOR", 0.78, RD), ("SIN SEÑALES\nDE DAÑO", 0.75, LV)], 250, 1060, 220, 140, 400, ease((u - 0.6) / 1.6), k, label_size=24)
        ka = ease((u - 3.4) / 0.4)
        text(ctx, "+26 %", 360, 600, F_BIG, 70, RD, ka, align="center")
        text(ctx, "+25 %", 720, 612, F_BIG, 70, LV, ka, align="center")
    elif i == 7:
        vbars(ctx, [("1.ª SESIÓN", 0.85, RD), ("2.ª SESIÓN", 0.35, LV)], 250, 1060, 220, 140, 400, ease((u - 0.4) / 1.8), k, label_size=24)
        sore_spots(ctx, [(360, 780)], t, ease((u - 0.8) / 0.4))
    elif i == 8:
        leg(ctx, 540, 500, 0.62, k, col=LV)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1010); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 150, CY, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "MITO VS. REALIDAD · RECUPERACIÓN", W / 2, 196, CY, k, 28)
        title(ctx, "¿ES ÁCIDO LÁCTICO?", WH, 350, 104, k)
        text(ctx, "EL DOLOR DE 1–3 DÍAS DESPUÉS", W / 2, 1275, F_MONO, 28, LV, ease((u - 2.6) / 0.4), align="center", bold=True)
    elif i == 1:
        pill(ctx, "LACTATO", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "SE VA EN 30–60 MIN", WH, 345, 104, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1150, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Hospital for Special Surgery (HSS) · Cheung et al., Sports Med 2003", k, 1200)
    elif i == 2:
        pill(ctx, "EXPERIMENTO · 1983", W / 2, 196, LV, k, 28, filled=True)
        title(ctx, "CORRER EN PLANO", WH, 345, 110, k)
        src(ctx, "Schwane et al., Phys Sportsmed 1983 · doi:10.1080/00913847.1983.11708485", k, 1260)
    elif i == 3:
        pill(ctx, "MISMOS VOLUNTARIOS", W / 2, 196, LV, k, 28, filled=True)
        title(ctx, "CORRER CUESTA ABAJO", WH, 345, 104, k)
        src(ctx, "Schwane et al., Phys Sportsmed 1983 · dolor medido durante 72 h", k, 1260)
    elif i == 4:
        pill(ctx, "LA REALIDAD", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "MICROLESIONES + INFLAMACIÓN", WH, 345, 84, k)
        text(ctx, "FASE EXCÉNTRICA: EL MÚSCULO FRENA LA CARGA", W / 2, 1110, F_MONO, 24, CY, ease((u - 3.4) / 0.4), align="center", bold=True)
        src(ctx, "Cheung et al., Sports Med 2003 · doi:10.2165/00007256-200333020-00005", k, 1170)
    elif i == 5:
        pill(ctx, "DOLOR MUSCULAR TARDÍO", W / 2, 196, RD, k, 28)
        title(ctx, "MÁXIMO: 24–72 HORAS", WH, 345, 100, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1150, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Cheung et al., Sports Med 2003", k, 1200)
    elif i == 6:
        pill(ctx, "¿SIN DOLOR NO HAY MÚSCULO?", W / 2, 196, RD, k, 28)
        title(ctx, "MISMA FUERZA Y MÚSCULO", WH, 345, 94, k)
        text(ctx, "AUMENTO DE FUERZA EN 8 SEMANAS", W / 2, 1180, F_MONO, 24, MU, ease((u - 3.4) / 0.4), align="center", bold=True)
        src(ctx, "Flann et al., J Exp Biol 2011 · doi:10.1242/jeb.050112", k, 1230)
    elif i == 7:
        pill(ctx, "EFECTO DE LA SESIÓN REPETIDA", W / 2, 196, LV, k, 28, filled=True)
        title(ctx, "LA 2.ª VEZ DUELE MENOS", WH, 345, 98, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1170, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Hyldahl, Chen y Nosaka, Exerc Sport Sci Rev 2017 · doi:10.1249/JES.0000000000000095", k, 1220)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)


run_episode(neon, txt, "EXPEDIENTE 26 · RECUPERACIÓN")
