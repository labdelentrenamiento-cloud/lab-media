"""v030 · ¿La creatina hace caer el pelo? Mito vs. realidad (serie SUPLEMENTOS-RENDIMIENTO · paleta azul acero + oro + coral)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (1.0, 0.80, 0.30)   # oro
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.04, 0.10, 0.15], [0.005, 0.015, 0.028])
from engine_ext import *
CY = ACC
CO = (1.0, 0.45, 0.42)    # coral
IC = (0.55, 0.92, 1.0)    # hielo


def title(ctx, s, color=WH, y=345, size=86, a=1.0):
    """título centrado que no invade los 140 px de botones a la derecha"""
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def head(ctx, cx, cy, s, col, a, hair=1.0, fall=0.0, t=0.0):
    """cabeza de perfil frontal con mechones; fall = mechones cayendo (0–1)."""
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 150, 0, 6.283)
    ctx.set_source_rgba(*col, 0.08 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    ctx.move_to(-70, 135); ctx.line_to(-80, 230); ctx.move_to(70, 135); ctx.line_to(80, 230)
    ctx.move_to(-220, 330); ctx.curve_to(-200, 250, -120, 230, -80, 230); ctx.move_to(220, 330); ctx.curve_to(200, 250, 120, 230, 80, 230)
    ctx.stroke()
    for j in range(15):
        ang = math.pi + 0.12 + j * (math.pi - 0.24) / 14
        bx, by = math.cos(ang) * 150, math.sin(ang) * 150
        L = 60 * hair
        if L < 2: continue
        dropped = fall > 0 and j % 3 == 1
        oy = 0
        if dropped:
            oy = 420 * ease(fall); ctx.set_source_rgba(*CO, a * (1 - 0.6 * ease(fall)))
        else:
            ctx.set_source_rgba(*IC, 0.9 * a)
        sw = math.sin(t * 2 + j) * 6
        ctx.move_to(bx, by + oy); ctx.curve_to(bx * 1.15 + sw, by * 1.15 + oy, bx * 1.2, by * 1.25 + oy - 10, bx * 1.1 + sw, by + oy - L)
        ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def jar(ctx, cx, cy, s, col, a, label="CREATINA"):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    rrect(ctx, -95, -150, 190, 50, 12); ctx.set_source_rgba(*col, 0.25 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    rrect(ctx, -115, -95, 230, 260, 34); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    rrect(ctx, -95, -20, 190, 90, 10); ctx.set_source_rgba(*col, 0.25 * a); ctx.fill()
    text(ctx, label, 0, 40, F_MONO, 30, WH, a, align="center", bold=True)
    ctx.restore()


def person(ctx, x, y, s, col, a):
    ctx.new_path(); ctx.arc(x, y - 30 * s, 16 * s, 0, 6.283); ctx.set_source_rgba(*col, a); ctx.fill()
    ctx.new_path(); ctx.move_to(x - 26 * s, y + 40 * s); ctx.curve_to(x - 26 * s, y - 8 * s, x + 26 * s, y - 8 * s, x + 26 * s, y + 40 * s); ctx.close_path(); ctx.fill()


def follicle(ctx, x, y, h, col, a, k=1.0):
    ctx.new_path(); ctx.arc(x, y + h, 22, 0, 6.283); ctx.set_source_rgba(*col, 0.3 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
    ctx.move_to(x, y + h - 22); ctx.curve_to(x + 10, y + h * 0.6, x - 10, y + h * 0.3, x + 4, y + h - (h * k))
    ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()


def src(ctx, s, k, y=1270):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        jar(ctx, 300, 800, 1.0, CY, k)
        head(ctx, 760, 760, 0.95, IC, ease((u - 0.3) / 0.4), fall=ease((u - 1.2) / 2.0), t=t)
        kq = easeb((u - 2.0) / 0.5)
        if kq > 0: big(ctx, "?", 540, 640, 200 * kq, CO, kq, maxw=300)
    elif i == 1:
        for r in range(4):
            for c in range(5):
                j = r * 5 + c
                kk = ease((u - 0.1 - j * 0.05) / 0.3)
                if kk > 0: person(ctx, 260 + c * 140, 560 + r * 135, 1.25, CY, kk)
        for w_ in range(3):
            kk = ease((u - 1.6 - w_ * 0.4) / 0.4)
            rrect(ctx, 230 + w_ * 215, 1120, 190, 40, 12); ctx.set_source_rgba(*IC, 0.2 * kk); ctx.fill_preserve(); ctx.set_source_rgba(*IC, kk); ctx.set_line_width(3); ctx.stroke()
            text(ctx, "SEM %d" % (w_ + 1), 325 + w_ * 215, 1150, F_MONO, 24, WH, kk, align="center", bold=True)
    elif i == 2:
        vbars(ctx, [("ANTES", 0.50, IC), ("7 DÍAS", 0.78, CO)], 280, 1000, 220, 80, 460, ease((u - 0.1) / 1.2), k, label_size=28)
        kb = easeb((u - 1.3) / 0.5)
        if kb > 0: big(ctx, "+56 %", 650, 560, 120 * kb, CO, kb, maxw=420)
        kx = ease((u - lt(2) - 3.6) / 0.4)
        if kx > 0:
            rrect(ctx, 240, 1100, 600, 80, 18); ctx.set_source_rgba(*RD, 0.15 * kx); ctx.fill_preserve(); ctx.set_source_rgba(*RD, kx); ctx.set_line_width(4); ctx.stroke()
            text(ctx, "PELO: NO SE MIDIÓ", 540, 1155, F_MONO, 36, WH, kx, align="center", bold=True)
    elif i == 3:
        for j, (lab, col, x) in enumerate((("SÍ", CY, 330), ("NO", CO, 750))):
            kk = easeb((u - 0.2 - j * 0.25) / 0.5)
            if kk <= 0: continue
            ctx.save(); ctx.translate(x, 800); ctx.scale(kk, kk)
            ctx.new_path(); ctx.arc(0, 0, 150, 0, 6.283); ctx.set_source_rgba(*col, 0.14); ctx.fill_preserve(); ctx.set_source_rgba(*col, 1); ctx.set_line_width(6); ctx.stroke()
            text(ctx, lab, 0, 55, F_BIG, 150, col, 1, align="center"); ctx.restore()
    elif i == 4:
        jar(ctx, 300, 700, 0.9, CY, k, "5 g/DÍA")
        jar(ctx, 780, 700, 0.9, MU, ease((u - 0.5) / 0.4), "PLACEBO")
        kt = ease((u - 1.5) / 3.0)
        x0, x1, y = 170, 910, 1010
        ctx.move_to(x0, y); ctx.line_to(x0 + (x1 - x0) * kt, y); ctx.set_source_rgba(*IC, 0.9); ctx.set_line_width(6); ctx.stroke()
        for w_ in range(13):
            xx = x0 + (x1 - x0) * w_ / 12
            if w_ / 12 <= kt + 1e-6:
                ctx.move_to(xx, y - 14); ctx.line_to(xx, y + 14); ctx.set_source_rgba(*IC, 0.9); ctx.set_line_width(3); ctx.stroke()
        text(ctx, "12 SEMANAS", 540, 1080, F_MONO, 30, WH, ease((u - 2.5) / 0.4), align="center", bold=True)
        kf = ease((u - lt(4) - 5.0) / 0.5)
        if kf > 0:
            ctx.new_path(); ctx.arc(540, 1160, 45, 0, 6.283); ctx.set_source_rgba(*GR, kf); ctx.set_line_width(5); ctx.stroke()
            ctx.move_to(572, 1192); ctx.line_to(605, 1225); ctx.set_line_width(9); ctx.stroke()
            follicle(ctx, 540, 1128, 50, GR, kf)
    elif i == 5:
        for g, (lab, col, x) in enumerate((("CREATINA", CY, 320), ("PLACEBO", MU, 760))):
            kk = ease((u - 0.1 - g * 0.3) / 0.5)
            for f in range(4):
                follicle(ctx, x - 120 + f * 80, 600, 260, col if g == 0 else IC, kk, k=0.6 + 0.4 * ease((u - 0.6) / 1.0))
            text(ctx, lab, x, 960, F_MONO, 30, col if g == 0 else IC, kk, align="center", bold=True)
        ke = easeb((u - 1.6) / 0.5)
        if ke > 0: big(ctx, "=", 540, 820, 160 * ke, GR, ke, maxw=200)
    elif i == 6:
        ka = easeb((u - 0.1) / 0.5)
        if ka > 0:
            ctx.save(); ctx.translate(540, 640); ctx.scale(ka, ka)
            ctx.move_to(0, -130); ctx.line_to(140, 110); ctx.line_to(-140, 110); ctx.close_path()
            ctx.set_source_rgba(*AM, 0.15); ctx.fill_preserve(); ctx.set_source_rgba(*AM, 1); ctx.set_line_width(7); ctx.stroke()
            text(ctx, "!", 0, 80, F_BIG, 150, AM, 1, align="center"); ctx.restore()
        tags = [("38 COMPLETARON EL ESTUDIO", 0.9), ("HOMBRES DE 18 A 40 AÑOS", 2.0), ("QUE YA ENTRENABAN", 3.0)]
        for j, (s, t0) in enumerate(tags):
            kk = ease((u - lt(6) - t0) / 0.4)
            if kk <= 0: continue
            rrect(ctx, 180, 870 + j * 105, 720, 80, 20); ctx.set_source_rgba(*AM, 0.10 * kk); ctx.fill_preserve(); ctx.set_source_rgba(*AM, kk); ctx.set_line_width(3); ctx.stroke()
            text(ctx, s, 540, 922 + j * 105, F_MONO, 30, WH, kk, align="center", bold=True)
    elif i == 7:
        head(ctx, 540, 760, 1.1, IC, k, fall=0.0, t=t)
        kc = easeb((u - 0.8) / 0.5)
        if kc > 0:
            ctx.save(); ctx.translate(800, 560); ctx.scale(kc, kc)
            ctx.new_path(); ctx.arc(0, 0, 80, 0, 6.283); ctx.set_source_rgba(*GR, 0.18); ctx.fill_preserve(); ctx.set_source_rgba(*GR, 1); ctx.set_line_width(6); ctx.stroke()
            ctx.move_to(-38, 2); ctx.line_to(-10, 32); ctx.line_to(42, -30); ctx.set_line_width(10); ctx.stroke(); ctx.restore()
    elif i == 8:
        jar(ctx, 540, 640, 1.0, CY, k)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1000); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 150, CY, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "MITO VS. REALIDAD · SUPLEMENTOS", W / 2, 196, CY, k, 28)
        title(ctx, "¿LA CREATINA DA CALVICIE?", WH, 368, 96, k)
    elif i == 1:
        pill(ctx, "EL ORIGEN DEL MITO · 2009", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "20 JUGADORES DE RUGBY", WH, 368, 100, k)
        src(ctx, "van der Merwe et al., Clin J Sport Med 2009 · doi:10.1097/JSM.0b013e3181b8b52f", k, 1240)
    elif i == 2:
        pill(ctx, "DHT EN SANGRE", W / 2, 196, CO, k, 30, filled=True)
        title(ctx, "SUBIÓ UNA HORMONA…", WH, 368, 100, k)
        src(ctx, "van der Merwe et al., 2009 · tras 7 días de carga (25 g/día)", k, 1240)
    elif i == 3:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿CONOCÍAS ESTE MITO?", WH, 368, 100, k)
        text(ctx, "ESCRIBE SÍ O NO", W / 2, 1090, F_MONO, 34, AM, ease((u - 0.8) / 0.4), align="center", bold=True)
    elif i == 4:
        pill(ctx, "ENSAYO CON PLACEBO · 2025", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "ESTA VEZ MIDIERON EL PELO", WH, 368, 92, k)
        src(ctx, "Lak et al., J Int Soc Sports Nutr 2025 · doi:10.1080/15502783.2025.2495229", k, 1300)
    elif i == 5:
        pill(ctx, "RESULTADO", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "SIN DIFERENCIAS", WH, 368, 110, k)
        text(ctx, "ESQUEMA · DHT, DENSIDAD Y GROSOR DEL PELO", W / 2, 1060, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Lak et al., JISSN 2025", k, 1105)
    elif i == 6:
        pill(ctx, "LÍMITES DEL ESTUDIO", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "OJO: FALTAN MÁS", WH, 368, 110, k)
    elif i == 7:
        pill(ctx, "LO QUE SABEMOS HOY", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "SIN PRUEBAS DE CALVICIE", WH, 368, 96, k)
        src(ctx, "Antonio et al., J Int Soc Sports Nutr 2021 · doi:10.1186/s12970-021-00412-w", k, 1180)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 30 · SUPLEMENTOS")
