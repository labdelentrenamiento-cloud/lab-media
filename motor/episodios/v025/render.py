"""v025 · ¿Intervalos (HIIT) o cardio continuo? Cochrane los comparó (serie CORAZÓN-RENDIMIENTO · paleta petróleo + verde eléctrico + fucsia)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (0.36, 1.0, 0.58)   # verde eléctrico
def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img
engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.02, 0.085, 0.09], [0.004, 0.016, 0.018])
from engine_ext import *
CY = ACC
PK = (1.0, 0.38, 0.62)   # fucsia = intervalos


def heart(ctx, cx, cy, s, a, col, t=0.0, beat=True):
    sc = s * (1 + (0.06 * max(0, math.sin(t * 7)) if beat else 0))
    ctx.save(); ctx.translate(cx, cy); ctx.scale(sc, sc)
    ctx.new_path(); ctx.move_to(0, 60)
    ctx.curve_to(-110, -10, -90, -110, -10, -90); ctx.curve_to(0, -86, 0, -70, 0, -62)
    ctx.curve_to(0, -70, 0, -86, 10, -90); ctx.curve_to(90, -110, 110, -10, 0, 60)
    ctx.close_path(); ctx.restore()
    ctx.set_source_rgba(*col, 0.14 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(5); ctx.stroke()


def pulse_line(ctx, x0, x1, y, t, a, col, spiky=True):
    ctx.new_path()
    n = 120
    for j in range(n + 1):
        x = x0 + (x1 - x0) * j / n
        ph = (j / n * 4 - t * 0.8) % 1
        if spiky:
            v = (ph < 0.5) * 1.0
            yy = y - 120 * v
        else:
            yy = y - 50 - 6 * math.sin(j * 0.5 + t * 3)
        (ctx.move_to if j == 0 else ctx.line_to)(x, yy)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(6); ctx.stroke()


def balance(ctx, cx, cy, tilt, a, t):
    ctx.move_to(cx, cy); ctx.line_to(cx, cy + 330); ctx.set_source_rgba(1, 1, 1, 0.8 * a); ctx.set_line_width(8); ctx.stroke()
    ctx.move_to(cx - 120, cy + 330); ctx.line_to(cx + 120, cy + 330); ctx.stroke()
    ang = tilt
    lx, ly = cx - 300 * math.cos(ang), cy - 300 * math.sin(ang) * -1
    rx, ry = cx + 300 * math.cos(ang), cy + 300 * math.sin(ang) * -1
    ly = cy + 300 * math.sin(ang); ry = cy - 300 * math.sin(ang)
    ctx.move_to(lx, ly); ctx.line_to(rx, ry); ctx.set_line_width(7); ctx.stroke()
    for (px, py, col, lab) in ((lx, ly, CY, "CONTINUO"), (rx, ry, PK, "INTERVALOS")):
        ctx.move_to(px, py); ctx.line_to(px - 70, py + 120); ctx.move_to(px, py); ctx.line_to(px + 70, py + 120)
        ctx.set_source_rgba(1, 1, 1, 0.5 * a); ctx.set_line_width(3); ctx.stroke()
        ctx.new_path(); ctx.arc(px, py + 120, 90, 0, math.pi); ctx.set_source_rgba(*col, 0.2 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
        text(ctx, lab, px, py + 250, F_MONO, 26, col, a, align="center", bold=True)
    ctx.new_path(); ctx.arc(cx, cy, 14, 0, 6.283); ctx.set_source_rgba(1, 1, 1, a); ctx.fill()


def src(ctx, s, k, y=1270):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        heart(ctx, 540, 640, 1.1, k, PK, t)
        pulse_line(ctx, 120, 500, 1040, t, ease((u - 0.6) / 0.4), PK, True)
        pulse_line(ctx, 580, 960, 1040, t, ease((u - 1.2) / 0.4), CY, False)
        text(ctx, "INTERVALOS", 310, 1110, F_MONO, 28, PK, ease((u - 0.6) / 0.4), align="center", bold=True)
        text(ctx, "CONTINUO", 770, 1110, F_MONO, 28, CY, ease((u - 1.2) / 0.4), align="center", bold=True)
    elif i == 1:
        n = 22 * 12; kd = ease((u - 0.3) / 2.6)
        for j in range(n):
            if j / n > kd: break
            x = 140 + (j % 22) * 38; y = 560 + (j // 22) * 40
            col = PK if (j * 7) % 3 == 0 else CY
            ctx.new_path(); ctx.arc(x, y - 8, 7, 0, 6.283); ctx.set_source_rgba(*col, 0.85 * k); ctx.fill()
            ctx.new_path(); ctx.arc(x, y + 9, 11, math.pi, 0); ctx.fill()
        cnt = int(2075 * ease((u - 0.3) / 2.6))
        big(ctx, "{:,}".format(cnt).replace(",", "."), 540, 1150, 120, WH, ease((u - 0.3) / 0.4))
    elif i == 2:
        vbars(ctx, [("SIN\nENTRENAR", 0.06, MU), ("INTERVALOS", 0.85, PK)], 250, 1080, 220, 140, 420, ease((u - 0.4) / 1.4), k, label_size=26)
        big(ctx, "+6", 720, 690, 120, PK, ease((u - 3.0) / 0.4), maxw=260)
        heart(ctx, 360, 700, 0.6, ease((u - 1.0) / 0.4), MU, t, beat=False)
    elif i == 3:
        balance(ctx, 540, 640, -0.07 * ease((u - 1.6) / 1.2), k, t)
        big(ctx, "+1,4", 540, 1180, 100, PK, ease((u - 4.0) / 0.4))
    elif i == 4:
        for j, lab in enumerate(("CINTURA", "PRESIÓN", "TRIGLICÉRIDOS")):
            kk = ease((u - 0.3 - j * 0.7) / 0.5)
            y = 640 + j * 190
            rrect(ctx, 140, y - 70, 800, 140, 70); ctx.set_source_rgba(*CY, 0.07 * kk); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.8 * kk); ctx.set_line_width(4); ctx.stroke()
            text(ctx, lab, 200, y + 14, F_MONO, 34, WH, kk, bold=True)
            text(ctx, "=", 870, y + 30, F_BIG, 90, CY, kk, align="center")
    elif i == 5:
        gauge(ctx, 540, 820, 230, 0.22, k, col=AM)
        for j in range(5):
            x = 300 + j * 120
            ctx.new_path(); ctx.arc(x, 1130, 26, 0, 6.283); ctx.set_source_rgba(*MU, 0.7 * ease((u - 1.8 - j * 0.1) / 0.4)); ctx.set_line_width(4); ctx.stroke()
    elif i == 6:
        clock(ctx, 540, 650, 140, t, back=0, a=k, col=CY)
        ka = ease((u - 1.6) / 0.5)
        rrect(ctx, 200, 900, 200, 120, 22); ctx.set_source_rgba(*PK, 0.25 * ka); ctx.fill_preserve(); ctx.set_source_rgba(*PK, ka); ctx.set_line_width(4); ctx.stroke()
        text(ctx, "1 MIN", 300, 975, F_BIG, 50, PK, ka, align="center")
        text(ctx, "=", 470, 990, F_BIG, 90, WH, ka, align="center")
        for j in range(2):
            kb = ease((u - 2.4 - j * 0.3) / 0.4)
            rrect(ctx, 540 + j * 200, 900, 180, 120, 22); ctx.set_source_rgba(*CY, 0.18 * kb); ctx.fill_preserve(); ctx.set_source_rgba(*CY, kb); ctx.stroke()
            text(ctx, "1 MIN", 630 + j * 200, 975, F_BIG, 50, CY, kb, align="center")
        text(ctx, "VIGOROSO", 300, 1070, F_MONO, 24, PK, ka, align="center", bold=True)
        text(ctx, "MODERADOS", 730, 1070, F_MONO, 24, CY, ease((u - 2.6) / 0.4), align="center", bold=True)
    elif i == 7:
        days = ["L", "M", "X", "J", "V", "S", "D"]
        for j, dname in enumerate(days):
            x = 165 + j * 125; kk = ease((u - 0.3 - j * 0.15) / 0.4)
            rrect(ctx, x - 50, 700, 100, 120, 18); ctx.set_source_rgba(*CY, 0.07 * kk); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.7 * kk); ctx.set_line_width(3); ctx.stroke()
            text(ctx, dname, x, 750, F_MONO, 30, WH, kk, align="center", bold=True)
            if j in (0, 2, 4, 5):
                col = PK if j in (2, 5) else CY
                kc = ease((u - 1.6 - j * 0.15) / 0.3)
                ctx.move_to(x - 22, 785); ctx.line_to(x - 4, 803); ctx.line_to(x + 26, 768); ctx.set_source_rgba(*col, kc); ctx.set_line_width(6); ctx.stroke()
        heart(ctx, 540, 1000, 0.8, ease((u - 2.6) / 0.4), CY, t)
    elif i == 8:
        heart(ctx, 540, 700, 1.0, k, PK, t)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1010); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 150, CY, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "COMPARACIÓN · CORAZÓN", W / 2, 196, CY, k, 28)
        title(ctx, "INTERVALOS VS. CONTINUO", WH, 350, 96, k)
    elif i == 1:
        pill(ctx, "REVISIÓN COCHRANE · 2026", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "58 ENSAYOS", WH, 345, 116, k)
        text(ctx, "ADULTOS SANOS PERO SEDENTARIOS · ≥ 4 SEMANAS", W / 2, 445, F_MONO, 24, MU, k, align="center", bold=True)
        src(ctx, "Strauss et al., Cochrane 2026 · doi:10.1002/14651858.CD013617.pub2", k, 1240)
    elif i == 2:
        pill(ctx, "VS. NO ENTRENAR", W / 2, 196, PK, k, 28, filled=True)
        title(ctx, "VO2 MÁX: +6 ml/kg/min", WH, 345, 96, k)
        text(ctx, "CERTEZA MODERADA · 16 ESTUDIOS", W / 2, 1230, F_MONO, 26, MU, ease((u - 1.4) / 0.4), align="center", bold=True)
        src(ctx, "DM 5,98 (IC95 % 4,66–7,30) · Strauss et al., Cochrane 2026", k, 1280)
    elif i == 3:
        pill(ctx, "VS. CARDIO CONTINUO MODERADO", W / 2, 196, CY, k, 28, filled=True)
        title(ctx, "GANA, PERO POR POCO", WH, 345, 104, k)
        src(ctx, "DM 1,39 ml/kg/min (IC95 % 0,44–2,34) · 37 estudios · certeza baja", ease((u - 4.0) / 0.4), 1250)
    elif i == 4:
        pill(ctx, "INTERVALOS VS. CONTINUO", W / 2, 196, CY, k, 28)
        title(ctx, "SIN DIFERENCIA CLARA", WH, 345, 100, k)
        src(ctx, "Strauss et al., Cochrane 2026", k, 1210)
    elif i == 5:
        pill(ctx, "OJO", W / 2, 196, RD, k, 30)
        title(ctx, "CERTEZA BAJA", WH, 345, 116, k)
        text(ctx, "ESTUDIOS PEQUEÑOS Y SUPERVISADOS", W / 2, 1230, F_MONO, 28, AM, ease((u - 1.6) / 0.4), align="center", bold=True)
    elif i == 6:
        pill(ctx, "OMS · 2020", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "LA VENTAJA: EL TIEMPO", WH, 345, 100, k)
        text(ctx, "75–150 MIN VIGOROSOS ≈ 150–300 MODERADOS", W / 2, 1180, F_MONO, 25, MU, ease((u - 2.8) / 0.4), align="center", bold=True)
        src(ctx, "Bull et al., Br J Sports Med 2020 · doi:10.1136/bjsports-2020-102955", k, 1240)
    elif i == 7:
        pill(ctx, "LA IDEA", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "EL QUE PUEDAS REPETIR", WH, 345, 100, k)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 345, 80, k)


run_episode(neon, txt, "EXPEDIENTE 25 · CORAZÓN")
