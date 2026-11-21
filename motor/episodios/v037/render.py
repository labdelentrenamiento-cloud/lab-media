"""v037 · ¿Entrenas un brazo y el otro se hace más fuerte? (QUÉ PASA SI…, serie FUERZA/SISTEMA NERVIOSO ·
paleta violeta noche + violeta + verde + ámbar)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (0.66, 0.58, 1.0)   # violeta = sistema nervioso


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.07, 0.04, 0.15], [0.01, 0.005, 0.04])
from engine_ext import *
CY = ACC
TE = (0.30, 0.85, 0.95)


def title(ctx, s, color=WH, y=345, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1170):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def badge(ctx, cx, cy, num, unit, col, a, w=300):
    if a <= 0: return
    rrect(ctx, cx - w / 2, cy - 150, w, 290, 26); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    big(ctx, num, cx, cy + 30, 120, col, a, maxw=w - 40)
    for li, part in enumerate(unit.split("\n")):
        text(ctx, part, cx, cy + 85 + li * 30, F_MONO, 23, WH, a, align="center", bold=True)


def arm(ctx, sx, sy, side, s, col, a, curl=0.0, fill=0.08, dumb=False, cast=False, glow=0.0):
    """brazo de perfil frontal: hombro (sx,sy), side=+1 derecha / -1 izquierda; curl 0..1 flexiona el codo"""
    if a <= 0: return
    ctx.save(); ctx.translate(sx, sy); ctx.scale(s * side, s)
    elb = (40, 230)
    ang = math.radians(90 - 135 * curl)          # antebrazo: hacia abajo (90°) → arriba
    hand = (elb[0] + math.cos(ang) * 220, elb[1] + math.sin(ang) * 220)
    # brazo (bíceps)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for (p0, p1, wdt) in ((( 0, 0), elb, 78), (elb, hand, 60)):
        ctx.move_to(*p0); ctx.line_to(*p1)
        ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(wdt); ctx.stroke()
    for (p0, p1, wdt) in ((( 0, 0), elb, 78), (elb, hand, 60)):
        ctx.move_to(*p0); ctx.line_to(*p1); ctx.set_source_rgba(0.02, 0.02, 0.06, 0.9 * a); ctx.set_line_width(wdt - 10); ctx.stroke()
        ctx.move_to(*p0); ctx.line_to(*p1); ctx.set_source_rgba(*col, fill * a * 2); ctx.set_line_width(wdt - 10); ctx.stroke()
    if glow > 0:
        ctx.move_to(6, 40); ctx.line_to(36, 200); ctx.set_source_rgba(*GR, 0.8 * glow * a); ctx.set_line_width(36); ctx.stroke()
    ctx.new_path(); ctx.arc(*elb, 14, 0, 6.283); ctx.set_source_rgba(*col, 0.8 * a); ctx.fill()
    if cast:
        ctx.move_to(elb[0] + (hand[0] - elb[0]) * 0.1, elb[1] + (hand[1] - elb[1]) * 0.1)
        ctx.line_to(elb[0] + (hand[0] - elb[0]) * 0.9, elb[1] + (hand[1] - elb[1]) * 0.9)
        ctx.set_source_rgba(*WH, 0.85 * a); ctx.set_line_width(74); ctx.set_line_cap(cairo.LINE_CAP_BUTT); ctx.stroke()
        for j in range(5):
            f = 0.2 + j * 0.15
            px = elb[0] + (hand[0] - elb[0]) * f; py = elb[1] + (hand[1] - elb[1]) * f
            ctx.move_to(px - 36, py - 6); ctx.line_to(px + 36, py + 6); ctx.set_source_rgba(*MU, 0.7 * a); ctx.set_line_width(3); ctx.stroke()
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.new_path(); ctx.arc(*hand, 24, 0, 6.283); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    if dumb:
        ctx.save(); ctx.translate(*hand)
        ctx.move_to(-70, 0); ctx.line_to(70, 0); ctx.set_source_rgba(*AM, a); ctx.set_line_width(12); ctx.stroke()
        for xx in (-70, 70):
            rrect(ctx, xx - 16, -46, 32, 92, 8); ctx.set_source_rgba(*AM, 0.25 * a); ctx.fill_preserve(); ctx.set_source_rgba(*AM, a); ctx.set_line_width(4); ctx.stroke()
        ctx.restore()
    ctx.set_line_cap(cairo.LINE_CAP_BUTT)
    ctx.restore()


def torso(ctx, cx, top, col, a):
    ctx.new_path(); ctx.arc(cx, top - 60, 54, 0, 6.283); ctx.set_source_rgba(*col, 0.08 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    rrect(ctx, cx - 120, top + 10, 240, 330, 50); ctx.set_source_rgba(*col, 0.06 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(5); ctx.stroke()


def body(ctx, cx, top, t, a, curl_r=0.0, curl_l=0.0, glow_l=0.0, cast_l=False, dumb_l=False, col=None):
    col = col or CY
    torso(ctx, cx, top, col, a)
    arm(ctx, cx + 150, top + 40, +1, 1.0, col, a, curl=curl_r, dumb=True)   # derecha del espectador = brazo derecho de la figura
    arm(ctx, cx - 150, top + 40, -1, 1.0, col, a, curl=curl_l, glow=glow_l, cast=cast_l, dumb=dumb_l)


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    rep = 0.5 - 0.5 * math.cos(t * 3.2)
    if i == 0:
        body(ctx, 540, 640, t, k, curl_r=rep)
        kq = easeb((u - 1.6) / 0.5)
        if kq > 0: big(ctx, "?", 250, 640, 160 * kq, AM, kq, maxw=200)
        text(ctx, "ENTRENA", 820, 1268, F_MONO, 26, AM, k, align="center", bold=True)
        text(ctx, "NO ENTRENA", 250, 1268, F_MONO, 26, MU, k, align="center", bold=True)
    elif i == 1:
        badge(ctx, 360, 760, "31", "ENSAYOS\nCONTROLADOS", AM, ease((u - 0.1) / 0.4))
        badge(ctx, 720, 760, "785", "PERSONAS", CY, ease((u - 1.2) / 0.4))
    elif i == 2:
        ctx.save(); ctx.translate(590, 700); ctx.scale(0.8, 0.8); ctx.translate(-540, -700)
        body(ctx, 540, 600, t, k, curl_r=rep, glow_l=ease((u - 1.8) / 0.8)); ctx.restore()
        kn = easeb((u - lt(2) - 3.0) / 0.5)
        if kn > 0:
            ctx.save(); ctx.translate(215, 800); ctx.scale(kn, kn)
            text(ctx, "+12 %", 0, 0, F_BIG, 120, GR, 1, align="center"); ctx.restore()
    elif i == 3:
        brain(ctx, 540, 640, 1.25, t, k, col=CY, fire=ease((u - 0.6) / 0.6))
        kn = ease((u - 1.2) / 0.6)
        nerve(ctx, [(560, 760), (680, 880), (860, 1000)], t, kn, col=GR, rate=1.4)
        nerve(ctx, [(520, 760), (400, 880), (220, 1000)], t, kn * ease((u - lt(3) - 3.6) / 0.6), col=GR, rate=1.4)
        fiber_bundle(ctx, 760, 1000, 220, 90, 4, 0.75, t, kn)
        fiber_bundle(ctx, 100, 1000, 220, 90, 4, 0.5 * ease((u - lt(3) - 3.8) / 0.6), t, kn)
    elif i == 4:
        kk = ease((u - 0.2) / 0.4)
        for j, (lab, col, x) in enumerate((("IZQUIERDO", CY, 330), ("DERECHO", AM, 750))):
            kj = easeb((u - 0.3 - j * 0.3) / 0.45)
            if kj <= 0: continue
            rrect(ctx, x - 170, 600, 340, 300, 30); ctx.set_source_rgba(*col, 0.10 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(4); ctx.stroke()
            arm(ctx, x - 30 * (1 if j else -1), 640, 1 if j else -1, 0.5, col, kj, curl=0.8, dumb=False)
            text(ctx, lab, x, 950, F_MONO, 30, WH, kj, align="center", bold=True)
        text(ctx, "VS", 540, 770, F_BIG, 70, WH, kk, align="center")
    elif i == 5:
        body(ctx, 540, 620, t, k, curl_r=rep, cast_l=True, glow_l=0.0)
        ks = easeb((u - lt(5) - 3.8) / 0.5)
        if ks > 0:
            ctx.save(); ctx.translate(250, 560); ctx.scale(ks, ks)
            ctx.move_to(0, -70); ctx.line_to(60, -45); ctx.line_to(55, 20); ctx.curve_to(45, 60, 15, 80, 0, 90)
            ctx.curve_to(-15, 80, -45, 60, -55, 20); ctx.line_to(-60, -45); ctx.close_path()
            ctx.set_source_rgba(*GR, 0.18); ctx.fill_preserve(); ctx.set_source_rgba(*GR, 1); ctx.set_line_width(5); ctx.stroke()
            ctx.move_to(-22, 5); ctx.line_to(-4, 25); ctx.line_to(28, -15); ctx.set_line_width(7); ctx.stroke()
            ctx.restore()
    elif i == 6:
        kk = ease((u - 0.3) / 1.4)
        rows = [("SOLO INMOVILIZADO", 0.85, RD), ("+ ENTRENAR EL OTRO BRAZO", 0.55, GR)]
        for j, (lab, v, col) in enumerate(rows):
            kj = ease((kk - j * 0.25) / 0.5)
            if kj <= 0: continue
            y = 640 + j * 190
            text(ctx, lab, 170, y - 18, F_MONO, 28, col, kj, bold=True)
            rrect(ctx, 170, y, 740, 60, 30); ctx.set_source_rgba(*col, 0.10 * kj); ctx.fill()
            rrect(ctx, 170, y, max(60, 740 * v * kj), 60, 30); ctx.set_source_rgba(*col, 0.35 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(3); ctx.stroke()
        text(ctx, "PÉRDIDA DE FUERZA", 540, 1050, F_MONO, 26, MU, k, align="center", bold=True)
    elif i == 7:
        kb = ease((u - 0.1) / 0.5)
        gauge(ctx, 330, 800, 170, 0.5 * kb, kb, col=AM)
        text(ctx, "EFECTO MODERADO", 330, 1010, F_MONO, 26, WH, kb, align="center", bold=True)
        kc = easeb((u - lt(7) - 2.6) / 0.5)
        if kc > 0:
            ctx.save(); ctx.translate(760, 780); ctx.scale(kc, kc)
            rrect(ctx, -110, -110, 220, 220, 30); ctx.set_source_rgba(*CY, 0.12); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 1); ctx.set_line_width(4); ctx.stroke()
            rrect(ctx, -26, -76, 52, 152, 8); ctx.set_source_rgba(*CY, 0.9); ctx.fill()
            rrect(ctx, -76, -26, 152, 52, 8); ctx.fill()
            ctx.restore()
            text(ctx, "KINESIÓLOGO", 760, 1010, F_MONO, 26, WH, kc, align="center", bold=True)
    elif i == 8:
        brain(ctx, 540, 620, 1.05, t, k, col=CY, fire=0.8)
        nerve(ctx, [(560, 720), (700, 820), (860, 900)], t, k, col=GR, rate=1.2)
        nerve(ctx, [(520, 720), (380, 820), (220, 900)], t, k, col=GR, rate=1.2)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1010); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, AM, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "QUÉ PASA SI… · FUERZA", W / 2, 196, CY, k, 28)
        title(ctx, "¿ENTRENAS UN BRAZO Y EL OTRO GANA?", WH, 368, 88, k)
    elif i == 1:
        pill(ctx, "METAANÁLISIS · 2017", W / 2, 196, AM, k, 28, filled=True)
        title(ctx, "SE MIDIÓ EL LADO SIN ENTRENAR", WH, 368, 88, k)
        src(ctx, "Manca et al., Eur J Appl Physiol 2017 · doi:10.1007/s00421-017-3720-z", k, 1130)
    elif i == 2:
        pill(ctx, "EDUCACIÓN CRUZADA", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "EL OTRO LADO TAMBIÉN GANA", WH, 368, 96, k)
        for li, part in enumerate(("FUERZA DEL LADO", "NO ENTRENADO")):
            text(ctx, part, 215, 860 + li * 30, F_MONO, 22, WH, ease((u - lt(2) - 3.2) / 0.5), align="center", bold=True)
        src(ctx, "Manca et al., 2017 · 31 ensayos · +11,9 % (promedio)", k, 1170)
    elif i == 3:
        pill(ctx, "SISTEMA NERVIOSO", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "APRENDE EL CEREBRO, NO EL MÚSCULO", WH, 368, 86, k)
        src(ctx, "Hernando-Garijo et al., Physiother Theory Pract 2026 · sin cambio en grosor muscular", k, 1170)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 196, AM, k, 32, filled=True)
        title(ctx, "¿CUÁL ES TU LADO MÁS DÉBIL?", WH, 368, 92, k)
    elif i == 5:
        pill(ctx, "BRAZO INMOVILIZADO", W / 2, 196, GR, k, 28, filled=True)
        title(ctx, "ENTRENA EL LADO SANO", WH, 368, 104, k)
        text(ctx, "YESO", 250, 1268, F_MONO, 26, MU, k, align="center", bold=True)
        text(ctx, "ENTRENA", 820, 1268, F_MONO, 26, AM, k, align="center", bold=True)
    elif i == 6:
        pill(ctx, "METAANÁLISIS · 2026", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "MENOS FUERZA PERDIDA", WH, 368, 100, k)
        text(ctx, "ESQUEMA ILUSTRATIVO · 8 ESTUDIOS, 189 PERSONAS", W / 2, 1100, F_MONO, 22, AM, k, align="center", bold=True)
        src(ctx, "Rodríguez-Coloma et al., J Appl Physiol 2026 · doi:10.1152/japplphysiol.00081.2026", k, 1150)
    elif i == 7:
        pill(ctx, "OJO", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "SUMA, NO REEMPLAZA", WH, 368, 104, k)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 37 · FUERZA")
