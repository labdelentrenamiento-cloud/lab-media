"""v036 · ¿Sentadilla en la pared para bajar la presión? (ESTUDIO EXPLICADO + COMPARACIÓN, serie CORAZÓN ·
paleta azul petróleo + coral + verde + ámbar)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (1.0, 0.42, 0.52)   # coral = corazón


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.02, 0.10, 0.12], [0.004, 0.02, 0.03])
from engine_ext import *
CY = ACC
TE = (0.30, 0.85, 0.95)   # turquesa = cardio


def title(ctx, s, color=WH, y=345, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1270):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def badge(ctx, cx, cy, num, unit, col, a, w=300):
    if a <= 0: return
    rrect(ctx, cx - w / 2, cy - 150, w, 290, 26); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    big(ctx, num, cx, cy + 30, 120, col, a, maxw=w - 40)
    for li, part in enumerate(unit.split("\n")):
        text(ctx, part, cx, cy + 85 + li * 30, F_MONO, 23, WH, a, align="center", bold=True)


def heart(ctx, cx, cy, s, t, col, a, fill=0.15, bpm=70):
    if a <= 0: return
    ph = (t * bpm / 60.0) % 1.0
    beat = 1 + 0.08 * math.exp(-((ph - 0.05) / 0.05) ** 2) + 0.05 * math.exp(-((ph - 0.25) / 0.05) ** 2)
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s * beat, s * beat)
    ctx.new_path(); ctx.move_to(0, 70)
    ctx.curve_to(-110, 0, -90, -100, 0, -45)
    ctx.curve_to(90, -100, 110, 0, 0, 70); ctx.close_path()
    ctx.set_source_rgba(*col, fill * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5 / s); ctx.stroke()
    ctx.restore()


def ecg(ctx, x0, x1, y, t, col, a, amp=60):
    ctx.new_path()
    n = 220; per = 260.0; off = (t * 160) % per
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        q = ((x - x0 + off) % per) / per
        v = 0
        if 0.40 < q < 0.44: v = -0.25
        elif 0.44 < q < 0.48: v = 1.0
        elif 0.48 < q < 0.52: v = -0.45
        elif 0.62 < q < 0.72: v = 0.18 * math.sin((q - 0.62) / 0.10 * math.pi)
        yy = y - v * amp
        (ctx.move_to if i == 0 else ctx.line_to)(x, yy)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()


def wall_squat(ctx, wx, fy, s, col, a, t=0.0, effort=0.0, wall=True):
    """figura en sentadilla isométrica apoyada en la pared (rodillas a ~90°). wx = pared, fy = suelo"""
    if a <= 0: return
    sh = effort * 2.0 * math.sin(t * 40)
    ctx.save(); ctx.translate(wx, fy); ctx.scale(s, s)
    if wall:
        ctx.move_to(0, 10); ctx.line_to(0, -560); ctx.set_source_rgba(*MU, 0.8 * a); ctx.set_line_width(6); ctx.stroke()
        for j in range(9):
            ctx.move_to(0, -40 - j * 60); ctx.line_to(-26, -64 - j * 60); ctx.set_source_rgba(*MU, 0.45 * a); ctx.set_line_width(3); ctx.stroke()
        ctx.move_to(-40, 10); ctx.line_to(330, 10); ctx.set_source_rgba(*MU, 0.8 * a); ctx.set_line_width(6); ctx.stroke()
    ctx.translate(sh, 0)
    hip = (46, -210); knee = (236, -210); ankle = (236, 0); sho = (46, -440); head = (56, -500)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(14); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(*sho); ctx.line_to(*hip); ctx.line_to(*knee); ctx.line_to(*ankle); ctx.stroke()
    ctx.move_to(ankle[0], ankle[1]); ctx.line_to(ankle[0] + 50, ankle[1]); ctx.stroke()
    ctx.move_to(46, -400); ctx.line_to(110, -310); ctx.line_to(170, -300); ctx.stroke()   # brazo
    ctx.new_path(); ctx.arc(*head, 40, 0, 6.283); ctx.set_line_width(10); ctx.stroke()
    # cuádriceps encendido
    if effort > 0:
        ctx.new_path(); ctx.move_to(70, -224); ctx.curve_to(120, -240, 170, -238, 214, -222)
        ctx.line_to(214, -200); ctx.curve_to(160, -196, 110, -196, 70, -198); ctx.close_path()
        ctx.set_source_rgba(*AM, 0.75 * effort * a); ctx.fill()
    ctx.set_line_cap(cairo.LINE_CAP_BUTT)
    # ángulo 90°
    ctx.new_path(); ctx.arc(knee[0], knee[1], 46, math.pi / 2, math.pi); ctx.set_source_rgba(*WH, 0.7 * a); ctx.set_line_width(3); ctx.stroke()
    ctx.restore()


def hbar(ctx, x, y, w, h, frac, col, a, label, val):
    rrect(ctx, x, y, w, h, h / 2); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill()
    if frac > 0:
        rrect(ctx, x, y, max(h, w * frac), h, h / 2); ctx.set_source_rgba(*col, 0.35 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
    text(ctx, label, x, y - 14, F_MONO, 26, col, a, bold=True)
    text(ctx, val, x + w, y - 14, F_MONO, 26, WH, a, align="right", bold=True)


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        wall_squat(ctx, 200, 1030, 1.0, GR, k, t, effort=ease((u - 0.6) / 0.8))
        heart(ctx, 760, 720, 1.25, t, CY, ease((u - 0.3) / 0.5), bpm=78)
        kq = easeb((u - 1.2) / 0.5)
        if kq > 0: big(ctx, "?", 760, 960, 130 * kq, AM, kq, maxw=200)
    elif i == 1:
        badge(ctx, 360, 760, "270", "ENSAYOS\nALEATORIZADOS", AM, ease((u - 0.1) / 0.4))
        badge(ctx, 720, 760, "15.827", "PERSONAS", CY, ease((u - 1.4) / 0.4))
        ecg(ctx, 160, 920, 1080, t, CY, 0.7 * ease((u - 0.5) / 0.5), amp=50)
    elif i == 2:
        wall_squat(ctx, 170, 1050, 0.95, GR, k, t, effort=1.0)
        kn = easeb((u - lt(2) - 4.4) / 0.5)
        if kn > 0:
            ctx.save(); ctx.translate(740, 720); ctx.scale(kn, kn)
            text(ctx, "−8", 0, 0, F_BIG, 190, GR, 1, align="center")
            text(ctx, "mmHg", 0, 70, F_MONO, 40, WH, 1, align="center", bold=True); ctx.restore()
    elif i == 3:
        kk = ease((u - 0.2) / 1.6)
        rows = [("ISOMÉTRICO", 8.24, GR, "−8,2"), ("COMBINADO", 6.04, AM, "−6,0"), ("PESAS", 4.55, VI, "−4,6"),
                ("CARDIO", 4.49, TE, "−4,5"), ("HIIT", 4.08, TE, "−4,1")]
        for j, (lab, v, col, s) in enumerate(rows):
            kj = ease((kk - j * 0.12) / 0.5)
            if kj <= 0: continue
            hbar(ctx, 170, 600 + j * 108, 740, 44, v / 8.24 * kj, col, kj, lab, s)
        text(ctx, "BAJA DE PRESIÓN SISTÓLICA (mmHg)", 540, 1150, F_MONO, 24, MU, k, align="center", bold=True)
    elif i == 4:
        wall_squat(ctx, 200, 1000, 0.8, GR, k, t, effort=0.6)
        secs = int(clamp((u - 0.4) / max(d - 0.6, 0.1)) * 60)
        kc = ease((u - 0.3) / 0.4)
        rrect(ctx, 560, 560, 360, 200, 30); ctx.set_source_rgba(*AM, 0.10 * kc); ctx.fill_preserve(); ctx.set_source_rgba(*AM, kc); ctx.set_line_width(4); ctx.stroke()
        text(ctx, "0:%02d" % secs, 740, 700, F_BIG, 120, AM, kc, align="center")
        text(ctx, "TU TIEMPO", 740, 820, F_MONO, 28, WH, kc, align="center", bold=True)
    elif i == 5:
        for j in range(4):
            kj = easeb((u - 0.2 - j * 0.25) / 0.45)
            if kj <= 0: continue
            x = 150 + j * 205
            rrect(ctx, x, 560, 160, 200, 22); ctx.set_source_rgba(*GR, 0.16 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*GR, kj); ctx.set_line_width(4); ctx.stroke()
            text(ctx, "2", x + 80, 680, F_BIG, 96, GR, kj, align="center")
            text(ctx, "MIN", x + 80, 730, F_MONO, 26, WH, kj, align="center", bold=True)
        days = ["L", "M", "M", "J", "V", "S", "D"]; on = (0, 2, 4)
        kd = ease((u - lt(5) - 3.2) / 0.5)
        for j, dd in enumerate(days):
            x = 210 + j * 110
            ctx.new_path(); ctx.arc(x, 940, 40, 0, 6.283)
            if j in on: ctx.set_source_rgba(*AM, 0.85 * kd); ctx.fill_preserve()
            ctx.set_source_rgba(*AM, kd); ctx.set_line_width(3); ctx.stroke()
            text(ctx, dd, x, 952, F_MONO, 30, (0.02, 0.05, 0.1) if j in on else WH, kd, align="center", bold=True)
    elif i == 6:
        kk = ease((u - 0.3) / 1.2)
        for j, (lab, v, col) in enumerate((("ISOMÉTRICO", 0.62, GR), ("CARDIO", 0.58, TE), ("PESAS", 0.57, VI), ("COMBINADO", 0.60, AM))):
            kj = ease((kk - j * 0.12) / 0.5)
            if kj <= 0: continue
            x = 190 + j * 190; h = 380 * v * kj
            rrect(ctx, x, 1000 - h, 130, h, 14); ctx.set_source_rgba(*col, 0.22 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(3); ctx.stroke()
            text(ctx, lab, x + 65, 1042, F_MONO, 22, col, kj, align="center", bold=True)
        kp = easeb((u - lt(6) - 4.2) / 0.5)
        if kp > 0:
            ctx.save(); ctx.translate(540, 560); ctx.scale(kp, kp)
            text(ctx, "+", 0, 60, F_BIG, 230, AM, 1, align="center"); ctx.restore()
    elif i == 7:
        # respiración: ondas suaves + cruz médica
        kb = ease((u - 0.1) / 0.5)
        for j in range(3):
            ph = math.sin(t * 2.2 - j * 0.7)
            ctx.new_path(); ctx.arc(330, 760, 90 + j * 46 + 14 * ph, 0, 6.283)
            ctx.set_source_rgba(*TE, (0.7 - j * 0.2) * kb); ctx.set_line_width(4); ctx.stroke()
        text(ctx, "RESPIRA", 330, 772, F_MONO, 30, WH, kb, align="center", bold=True)
        kc = easeb((u - lt(7) - 2.4) / 0.5)
        if kc > 0:
            ctx.save(); ctx.translate(760, 760); ctx.scale(kc, kc)
            rrect(ctx, -110, -110, 220, 220, 30); ctx.set_source_rgba(*CY, 0.12); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 1); ctx.set_line_width(4); ctx.stroke()
            rrect(ctx, -26, -76, 52, 152, 8); ctx.set_source_rgba(*CY, 0.9); ctx.fill()
            rrect(ctx, -76, -26, 152, 52, 8); ctx.fill()
            ctx.restore()
            text(ctx, "TU MÉDICO", 760, 920, F_MONO, 30, WH, kc, align="center", bold=True)
    elif i == 8:
        heart(ctx, 540, 640, 1.4, t, CY, k, bpm=66)
        ecg(ctx, 160, 920, 820, t, GR, 0.6 * k, amp=40)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 980); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 120, AM, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "ESTUDIO EXPLICADO · CORAZÓN", W / 2, 196, CY, k, 28)
        title(ctx, "¿QUIETO PARA BAJAR LA PRESIÓN?", WH, 368, 92, k)
    elif i == 1:
        pill(ctx, "METAANÁLISIS EN RED · 2023", W / 2, 196, AM, k, 28, filled=True)
        title(ctx, "5 TIPOS DE EJERCICIO, CARA A CARA", WH, 368, 88, k)
        src(ctx, "Edwards et al., Br J Sports Med 2023 · doi:10.1136/bjsports-2022-106503", k, 1170)
    elif i == 2:
        pill(ctx, "ISOMÉTRICO", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "EL QUE MÁS LA BAJÓ", WH, 368, 104, k)
        text(ctx, "PRESIÓN SISTÓLICA EN REPOSO", 740, 880, F_MONO, 24, AM, ease((u - lt(2) - 4.6) / 0.4), align="center", bold=True)
        src(ctx, "Edwards et al., 2023 · −8,24 mmHg vs. grupo control", k, 1170)
    elif i == 3:
        pill(ctx, "COMPARACIÓN", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "CASI EL DOBLE", WH, 368, 110, k)
        src(ctx, "Edwards et al., 2023 · 270 ensayos, 15.827 personas", k, 1200)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿CUÁNTO AGUANTAS EN LA PARED?", WH, 368, 90, k)
    elif i == 5:
        pill(ctx, "EL PROTOCOLO DE LOS ESTUDIOS", W / 2, 196, GR, k, 28, filled=True)
        title(ctx, "4 × 2 MINUTOS", WH, 368, 110, k)
        text(ctx, "2 MIN DE DESCANSO ENTRE SERIES", W / 2, 830, F_MONO, 26, MU, ease((u - 1.4) / 0.4), align="center", bold=True)
        src(ctx, "Cohen et al., J Clin Hypertens 2023 · doi:10.1111/jch.14621", k, 1150)
    elif i == 6:
        pill(ctx, "EVIDENCIA 2026", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "MÁS PAREJO DE LO QUE PARECÍA", WH, 368, 88, k)
        text(ctx, "ESQUEMA ILUSTRATIVO · SIN UN GANADOR CLARO", W / 2, 1110, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Etayo-Urtasun et al., Hypertens Res 2026 · Yuan et al., Maturitas 2026", k, 1155)
    elif i == 7:
        pill(ctx, "SEGURIDAD", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "SIN AGUANTAR EL AIRE", WH, 368, 100, k)
        text(ctx, "¿PRESIÓN ALTA? CONSÚLTALO ANTES", W / 2, 1060, F_MONO, 28, AM, ease((u - lt(7) - 2.6) / 0.4), align="center", bold=True)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 36 · CORAZÓN")
