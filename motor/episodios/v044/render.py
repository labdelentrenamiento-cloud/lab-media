"""v044 · ¿Las pesas te dejan rígido? (MITO VS. REALIDAD con pregunta antes del resultado, serie MOVILIDAD ·
paleta verde azulado profundo + magenta + ámbar + verde)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (0.98, 0.42, 0.80)   # magenta = movilidad


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.025, 0.12, 0.125], [0.004, 0.02, 0.025])
from engine_ext import *
CY = ACC
PE = AM                    # pesas = ámbar
ST = GR                    # estirar = verde


def title(ctx, s, color=WH, y=345, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1170):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def stamp(ctx, s, cx, cy, col, k, size=96, rot=-0.08):
    if k <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(k, k)
    font(ctx, F_BIG, size); tw = ctx.text_extents(s).x_advance
    rrect(ctx, -tw / 2 - 30, -size * 0.95, tw + 60, size * 1.25, 18); ctx.set_source_rgba(*col, 0.12); ctx.fill_preserve()
    ctx.set_source_rgba(*col, 1); ctx.set_line_width(6); ctx.stroke()
    text(ctx, s, 0, 0, F_BIG, size, col, 1, align="center")
    ctx.restore()


def bar(ctx, cx, cy, s, t, a, bob=True):
    """barra olímpica escalable (sin ondas)"""
    if a <= 0: return
    y = cy - (abs(math.sin(t * 2.4)) * 30 * s if bob else 0)
    ctx.save(); ctx.translate(cx, y); ctx.scale(s, s)
    ctx.move_to(-300, 0); ctx.line_to(300, 0); ctx.set_source_rgba(*WH, 0.9 * a); ctx.set_line_width(10); ctx.stroke()
    for sg in (-1, 1):
        for k, (h, w) in enumerate([(170, 34), (130, 26)]):
            x = sg * (215 + k * 40)
            rrect(ctx, x - w / 2, -h / 2, w, h, 8); ctx.set_source_rgba(*CY, 0.15 * a); ctx.fill_preserve()
            ctx.set_source_rgba(*CY, a); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def slr(ctx, hx, fy, s, theta, col, a, arc_col=None, load=False, arc=True):
    """figura acostada: elevación de pierna recta (prueba clásica de flexibilidad). theta en grados."""
    if a <= 0: return
    ctx.save(); ctx.translate(hx, fy); ctx.scale(s, s)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(-330, 18); ctx.line_to(330, 18); ctx.set_source_rgba(*MU, 0.6 * a); ctx.set_line_width(4); ctx.stroke()
    ctx.set_source_rgba(*col, a); ctx.set_line_width(16)
    ctx.move_to(0, 0); ctx.line_to(-230, 0); ctx.stroke()                    # tronco
    ctx.move_to(-120, 0); ctx.line_to(-60, -40); ctx.line_to(10, -30); ctx.stroke()  # brazo
    ctx.new_path(); ctx.arc(-275, -6, 40, 0, 6.283); ctx.set_line_width(10); ctx.stroke()
    ctx.set_line_width(16); ctx.move_to(0, 0); ctx.line_to(300, 0); ctx.stroke()   # pierna apoyada
    th = math.radians(theta); L = 300
    fx, fyy = L * math.cos(th), -L * math.sin(th)
    ctx.move_to(0, 0); ctx.line_to(fx, fyy); ctx.stroke()                        # pierna elevada
    if load:
        ctx.new_path(); ctx.arc(fx * 0.88, fyy * 0.88, 26, 0, 6.283); ctx.set_source_rgba(*PE, 0.5 * a); ctx.fill_preserve()
        ctx.set_source_rgba(*PE, a); ctx.set_line_width(5); ctx.stroke()
    ctx.set_line_cap(cairo.LINE_CAP_BUTT)
    if arc and theta > 1:
        ac = arc_col or CY
        ctx.new_path(); ctx.move_to(0, 0); ctx.arc_negative(0, 0, 170, 0, -th); ctx.close_path()
        ctx.set_source_rgba(*ac, 0.22 * a); ctx.fill_preserve(); ctx.set_source_rgba(*ac, a); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        bar(ctx, 540, 580, 0.9, t, k)
        slr(ctx, 560, 1060, 0.8, 40 + 8 * math.sin(t * 1.5), CY, ease((u - 0.4) / 0.5))
        stamp(ctx, "55 ESTUDIOS", 540, 790, AM, easeb((u - lt(0) - 2.6) / 0.5), 70)
    elif i == 1:
        th = lerp(70, 35, ease((u - 0.8) / 2.2))
        slr(ctx, 560, 960, 0.95, th, CY, k, arc_col=RD)
        kq = easeb((u - 2.6) / 0.5)
        if kq > 0:
            ctx.save(); ctx.translate(540, 620); ctx.scale(kq, kq)
            text(ctx, "¿MENOS MOVIMIENTO?", 0, 0, F_BIG, 76, RD, 1, align="center"); ctx.restore()
    elif i == 2:
        for j, (lab, col, cx) in enumerate([("PESAS", PE, 330), ("ESTIRAR", ST, 750)]):
            kj = easeb((u - 0.3 - j * 0.4) / 0.5)
            if kj <= 0: continue
            rrect(ctx, cx - 175, 580, 350, 280, 34); ctx.set_source_rgba(*col, 0.10 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(5); ctx.stroke()
            if j == 0:
                bar(ctx, cx, 690, 0.42, t, kj)
            else:
                slr(ctx, cx + 30, 720, 0.38, 75, ST, kj, arc=False)
            text(ctx, lab, cx, 830, F_BIG, 58, col, kj, align="center")
        cur = "▌" if int(t * 2.5) % 2 == 0 else " "
        text(ctx, "COMENTA TU APUESTA" + cur, 540, 980, F_MONO, 34, AM, ease((u - 1.2) / 0.4), align="center", bold=True)
    elif i == 3:
        th = lerp(35, 72, ease((u - 0.6) / 2.4))
        slr(ctx, 560, 980, 0.95, th, PE, k, arc_col=GR, load=True)
        kp = easeb((u - lt(3) - 1.8) / 0.5)
        if kp > 0:
            ctx.save(); ctx.translate(540, 600); ctx.scale(kp, kp)
            text(ctx, "+ RANGO DE MOVIMIENTO", 0, 0, F_BIG, 70, GR, 1, align="center"); ctx.restore()
    elif i == 4:
        kl = ease((u - 0.2) / 0.5); kr = ease((u - 0.8) / 0.5)
        slr(ctx, 300, 900, 0.5, 68 * kl, PE, kl, arc_col=PE, load=True)
        slr(ctx, 790, 900, 0.5, 68 * kr, ST, kr, arc_col=ST)
        text(ctx, "PESAS", 300, 1000, F_BIG, 60, PE, kl, align="center")
        text(ctx, "ESTIRAR", 790, 1000, F_BIG, 60, ST, kr, align="center")
        ke = easeb((u - lt(4) - 1.4) / 0.5)
        if ke > 0:
            ctx.save(); ctx.translate(545, 680); ctx.scale(ke, ke)
            text(ctx, "=", 0, 30, F_BIG, 150, WH, 1, align="center"); ctx.restore()
    elif i == 5:
        kk = ease((u - 0.3) / 1.6)
        vbars(ctx, [("YA\nENTRENADOS", 0.41, CY), ("SIN\nENTRENAR", 1.0, GR)], 270, 1000, 220, 100, 360, kk, 1.0, 26)
        kv = ease((u - 1.6) / 0.4)
        text(ctx, "0,43", 380, 1000 - 360 * 0.41 - 24, F_BIG, 52, CY, kv, align="center")
        text(ctx, "1,04", 700, 1000 - 360 - 24, F_BIG, 52, GR, kv, align="center")
        text(ctx, "TAMAÑO DEL EFECTO (MAYOR = MÁS RANGO GANADO)", 540, 500, F_MONO, 22, MU, kv, align="center", bold=True)
    elif i == 6:
        kl = ease((u - 0.2) / 0.5); kr = ease((u - lt(6) - 2.8) / 0.5)
        slr(ctx, 300, 880, 0.5, 50, MU, kl, arc_col=MU)
        slr(ctx, 790, 880, 0.5, 68, PE, kr, arc_col=GR, load=True)
        text(ctx, "SOLO PESO", 300, 980, F_BIG, 50, MU, kl, align="center")
        text(ctx, "CORPORAL", 300, 1040, F_BIG, 50, MU, kl, align="center")
        text(ctx, "CON CARGA", 790, 1010, F_BIG, 54, PE, kr, align="center")
        stamp(ctx, "NO SIGNIFICATIVO", 300, 640, RD, easeb((u - lt(6) - 1.6) / 0.5), 40, -0.05)
        stamp(ctx, "SÍ MEJORA", 790, 640, GR, easeb((u - lt(6) - 3.6) / 0.5), 48, -0.05)
    elif i == 7:
        th = 60 + 10 * math.sin(t * 1.4)
        slr(ctx, 560, 1010, 0.95, th, PE, k, arc_col=GR, load=True)
        kb = ease((u - 1.0) / 0.5)
        bar(ctx, 540, 560, 0.75, t, kb)
    elif i == 8:
        slr(ctx, 560, 820, 0.8, 62 + 10 * math.sin(t * 1.6), PE, k, arc_col=GR, load=True)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1010); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, AM, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "MITOS DEL GIMNASIO · MOVILIDAD", W / 2, 196, CY, k, 28)
        title(ctx, "¿LAS PESAS TE DEJAN RÍGIDO?", WH, 368, 90, k)
    elif i == 1:
        pill(ctx, "EL MIEDO", W / 2, 196, RD, k, 30, filled=True)
        title(ctx, "MÁS MÚSCULO, MENOS RANGO", WH, 368, 92, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1150, F_MONO, 22, AM, k, align="center", bold=True)
    elif i == 2:
        pill(ctx, "COMENTA ANTES DEL RESULTADO", W / 2, 196, AM, k, 28, filled=True)
        title(ctx, "¿QUÉ GANA?", WH, 368, 110, k)
    elif i == 3:
        pill(ctx, "METAANÁLISIS · 55 ESTUDIOS", W / 2, 196, GR, k, 28, filled=True)
        title(ctx, "LAS PESAS SUMAN FLEXIBILIDAD", WH, 368, 86, k)
        src(ctx, "Alizadeh et al., Sports Med 2023 · doi:10.1007/s40279-022-01804-x", k, 1150)
    elif i == 4:
        pill(ctx, "PESAS VS. ESTIRAR", W / 2, 196, AM, k, 30, filled=True)
        title(ctx, "SIN DIFERENCIA", WH, 368, 110, k)
        src(ctx, "Alizadeh et al., Sports Med 2023 · Afonso et al., Healthcare 2021", k, 1130)
        src(ctx, "doi:10.3390/healthcare9040427", k, 1165)
    elif i == 5:
        pill(ctx, "QUIÉN GANA MÁS", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "LOS QUE RECIÉN EMPIEZAN", WH, 368, 96, k)
        src(ctx, "Alizadeh et al., 2023 · subgrupos por nivel de actividad", k, 1160)
    elif i == 6:
        pill(ctx, "DETALLE CLAVE", W / 2, 196, CY, k, 30, filled=True)
        title(ctx, "LA CARGA IMPORTA", WH, 368, 104, k)
        src(ctx, "Alizadeh et al., 2023 · solo peso corporal: mejora no significativa", k, 1160)
    elif i == 7:
        pill(ctx, "EN LA PRÁCTICA", W / 2, 196, GR, k, 30, filled=True)
        title(ctx, "LA FUERZA TAMBIÉN SUMA RANGO", WH, 368, 86, k)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 368, 80, k)


run_episode(neon, txt, "EXPEDIENTE 44 · MOVILIDAD")
