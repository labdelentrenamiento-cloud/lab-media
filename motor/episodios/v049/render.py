"""v049 · ¿Qué pasa si duermes siesta antes de entrenar? ("QUÉ PASA SI…", serie SUEÑO Y RENDIMIENTO ·
paleta violeta noche + lavanda + ámbar + verde)
Uso: en la carpeta del episodio (con timeline.json):
  python3 render.py preview 2 8 ...   |   python3 render.py part 0 2
"""
import sys, math
sys.path.insert(0, "/home/claude/lab")
import numpy as np
import engine, engine_ext

ACC = (0.72, 0.64, 1.0)   # lavanda


def _bg(c0, c1):
    y, x = np.mgrid[0:engine.H, 0:engine.W]
    d = np.sqrt(((x - engine.W / 2) / engine.W) ** 2 + ((y - engine.H * 0.42) / engine.H) ** 2)
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = np.array(c0) * (1 - k) + np.array(c1) * k
    img = np.zeros((engine.H, engine.W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


engine.CY = engine_ext.CY = ACC
engine.BG = engine_ext.BG = _bg([0.075, 0.04, 0.17], [0.01, 0.006, 0.04])
from engine_ext import *
CY = ACC
SL = ACC          # sueño = lavanda
EN = AM           # energía = ámbar


def title(ctx, s, color=WH, y=368, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 300)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def src(ctx, s, k, y=1150):
    sz = fit_size(ctx, s, F_MONO, 21, W - 300)
    text(ctx, s, W / 2, y, F_MONO, sz, MU, k, align="center")


def moon(ctx, cx, cy, r, a, col=SL):
    """luna creciente (círculo menos círculo desplazado)"""
    if a <= 0: return
    ox, oy, r2 = cx + r * 0.48, cy - r * 0.28, r * 0.86
    ctx.push_group()
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*col, 0.22 * a); ctx.fill_preserve()
    ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    ctx.set_operator(cairo.OPERATOR_CLEAR); ctx.new_path(); ctx.arc(ox, oy, r2, 0, 6.283); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.save(); ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.clip()
    ctx.new_path(); ctx.arc(ox, oy, r2, 0, 6.283); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke(); ctx.restore()
    ctx.pop_group_to_source(); ctx.paint()


def zzz(ctx, x, y, t, a, col=SL):
    for j in range(3):
        ph = (t * 0.6 + j * 0.33) % 1
        text(ctx, "Z", x + j * 34 + ph * 30, y - j * 46 - ph * 40, F_BIG, 40 + j * 14, col, a * (1 - ph) * 0.95, align="center")


def sleeper(ctx, cx, cy, s, a, col=SL, t=0.0):
    """persona durmiendo en una cama (vista lateral)"""
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    rrect(ctx, -230, 20, 460, 40, 12); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(-230, 60); ctx.line_to(-230, 110); ctx.move_to(230, 60); ctx.line_to(230, 110); ctx.move_to(-230, -60); ctx.line_to(-230, 20); ctx.stroke()
    rrect(ctx, -215, -18, 90, 38, 16); ctx.set_source_rgba(*WH, 0.12 * a); ctx.fill_preserve(); ctx.set_source_rgba(*WH, 0.7 * a); ctx.stroke()
    br = 1 + 0.04 * math.sin(t * 2.2)
    ctx.new_path(); ctx.arc(-150, -38, 30, 0, 6.283); ctx.set_source_rgba(*col, 0.12 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(5); ctx.stroke()
    ctx.move_to(-115, -10); ctx.curve_to(-40, -40 * br, 120, -40 * br, 215, -8); ctx.line_to(215, 18); ctx.line_to(-115, 18); ctx.close_path()
    ctx.set_source_rgba(*col, 0.16 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.stroke()
    ctx.restore()


def dumbbell(ctx, cx, cy, s, a, col=EN):
    if a <= 0: return
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    ctx.move_to(-60, 0); ctx.line_to(60, 0); ctx.set_source_rgba(*WH, 0.9 * a); ctx.set_line_width(10); ctx.stroke()
    for sx in (-1, 1):
        rrect(ctx, sx * 70 - 18, -48, 36, 96, 8); ctx.set_source_rgba(*col, 0.15 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def card(ctx, x, y, w, h, col, a, lab, arrow_up=True, sub=None):
    if a <= 0: return
    rrect(ctx, x, y, w, h, 28); ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    ax, ay = x + 80, y + h / 2
    d = -1 if arrow_up else 1
    ctx.move_to(ax, ay - d * 34); ctx.line_to(ax, ay + d * 34); ctx.move_to(ax - 26, ay + d * 10); ctx.line_to(ax, ay + d * 38); ctx.line_to(ax + 26, ay + d * 10)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(9); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    sz = fit_size(ctx, lab, F_BIG, 58, w - 180)
    text(ctx, lab, x + 150, y + h / 2 + 22, F_BIG, sz, WH, a)


def person(ctx, x, y, s, a, col):
    ctx.new_path(); ctx.arc(x, y - 30 * s, 15 * s, 0, 6.283); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(x - 24 * s, y + 30 * s); ctx.curve_to(x - 24 * s, y - 8 * s, x + 24 * s, y - 8 * s, x + 24 * s, y + 30 * s); ctx.stroke()


def neon(ctx, i, u, d, t, lt):
    k = ease(u / 0.35)
    if i == 0:
        moon(ctx, 760, 600, 70, k)
        sleeper(ctx, 480, 820, 1.0, k, t=t)
        zzz(ctx, 360, 730, t, k)
        kd = easeb((u - 1.0) / 0.5)
        if kd > 0:
            dumbbell(ctx, 780, 1000, 0.9, kd)
            text(ctx, "→", 610, 1022, F_BIG, 80, EN, kd, align="center")
    elif i == 1:
        n = int(clamp((u - 0.2) / 1.8) * 22)
        for j in range(n):
            ang = math.pi * (0.1 + 0.8 * j / 21)
            x = 540 - math.cos(ang) * 300; y = 900 - math.sin(ang) * 300
            ctx.new_path(); ctx.arc(x, y, 24, 0, 6.283); ctx.set_source_rgba(*SL, 0.18 * k); ctx.fill_preserve(); ctx.set_source_rgba(*SL, k); ctx.set_line_width(3); ctx.stroke()
            moon(ctx, x, y, 11, k, WH)
        kb = easeb((u - lt(1) - 2.0) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 900); ctx.scale(kb, kb)
            text(ctx, "22", 0, 0, F_BIG, 170, EN, 1, align="center")
            text(ctx, "ENSAYOS", 0, 62, F_MONO, 34, WH, 1, align="center", bold=True); ctx.restore()
    elif i == 2:
        items = [("RENDIMIENTO FÍSICO", GR, True, 0.6), ("ATENCIÓN", CY, True, 2.0), ("CANSANCIO", RD, False, 3.6)]
        for j, (lab, col, up, t0) in enumerate(items):
            kj = easeb((u - t0) / 0.5)
            card(ctx, 200, 540 + j * 175, 680, 135, col, kj, lab, up)
    elif i == 3:
        cx, cy, r = 540, 800, 220
        ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*SL, 0.06 * k); ctx.fill_preserve(); ctx.set_source_rgba(*SL, 0.7 * k); ctx.set_line_width(5); ctx.stroke()
        for m in range(12):
            ang = -math.pi / 2 + m / 12 * 6.283
            ctx.move_to(cx + math.cos(ang) * (r - 24), cy + math.sin(ang) * (r - 24)); ctx.line_to(cx + math.cos(ang) * (r - 6), cy + math.sin(ang) * (r - 6))
            ctx.set_source_rgba(*WH, 0.7 * k); ctx.set_line_width(4); ctx.stroke()
        g = ease((u - lt(3) - 1.0) / 1.6)
        if g > 0:
            a0 = -math.pi / 2 + math.pi          # 30 min
            a1 = a0 + math.pi * g                 # hasta 60 min
            ctx.new_path(); ctx.arc(cx, cy, r + 36, a0, a1); ctx.set_source_rgba(*EN, 0.95); ctx.set_line_width(26); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        text(ctx, "0", cx, cy - r + 62, F_MONO, 30, MU, k, align="center", bold=True)
        text(ctx, "30", cx, cy + r - 34, F_MONO, 30, MU, k, align="center", bold=True)
        kb = easeb((u - lt(3) - 2.4) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(cx, cy + 30); ctx.scale(kb, kb)
            text(ctx, "30–60", 0, 0, F_BIG, 110, EN, 1, align="center")
            text(ctx, "MINUTOS", 0, 54, F_MONO, 30, WH, 1, align="center", bold=True); ctx.restore()
    elif i == 4:
        for j, (lab, col, cx) in enumerate([("SÍ", EN, 330), ("NO", SL, 750)]):
            kj = easeb((u - 0.3 - j * 0.4) / 0.5)
            if kj <= 0: continue
            rrect(ctx, cx - 175, 560, 350, 320, 34); ctx.set_source_rgba(*col, 0.10 * kj); ctx.fill_preserve(); ctx.set_source_rgba(*col, kj); ctx.set_line_width(5); ctx.stroke()
            text(ctx, lab, cx, 790, F_BIG, 150, col, kj, align="center")
        cur = "▌" if int(t * 2.5) % 2 == 0 else " "
        text(ctx, "COMENTA: SÍ O NO" + cur, 540, 990, F_MONO, 34, EN, ease((u - 1.0) / 0.4), align="center", bold=True)
    elif i == 5:
        y = 820
        g = ease((u - 0.4) / 2.4)
        ctx.move_to(220, y); ctx.line_to(220 + 640 * g, y); ctx.set_source_rgba(*SL, 0.9); ctx.set_line_width(6); ctx.set_dash([18, 12]); ctx.stroke(); ctx.set_dash([])
        moon(ctx, 220, y - 110, 50, k)
        text(ctx, "DESPERTAR", 220, y + 70, F_MONO, 28, SL, k, align="center", bold=True)
        if g > 0.45:
            kk = easeb((g - 0.45) / 0.2)
            pill(ctx, "+1 HORA", 540, y - 120, EN, kk, 34, filled=True)
        if g > 0.95:
            kk = easeb((u - 2.9) / 0.4)
            dumbbell(ctx, 860, y - 110, 0.75, kk, GR)
            text(ctx, "PRUEBA", 860, y + 70, F_MONO, 28, GR, kk, align="center", bold=True)
            ctx.new_path(); ctx.arc(860, y, 14, 0, 6.283); ctx.set_source_rgba(*GR, kk); ctx.fill()
    elif i == 6:
        kb = ease((u - 0.3) / 0.4)
        vbars(ctx, [("FUERZA\nMÁXIMA", 0.42, MU), ("CARRERAS\nREPETIDAS", 0.78, GR)], 270, 1010, 220, 100, 420, ease((u - 0.3) / 1.6), kb, 26)
        if u > 1.8:
            kk = easeb((u - 1.8) / 0.4)
            text(ctx, "=", 380, 540, F_BIG, 80, MU, kk, align="center")
            text(ctx, "↑", 700, 540, F_BIG, 80, GR, kk, align="center")
    elif i == 7:
        for j in range(10):
            kj = ease((u - 0.2 - j * 0.08) / 0.4)
            if kj <= 0: continue
            x = 220 + (j % 5) * 160; y = 640 + (j // 5) * 170
            person(ctx, x, y, 1.6, kj, SL)
        kb = easeb((u - lt(7) - 2.6) / 0.5)
        if kb > 0:
            ctx.save(); ctx.translate(540, 1030); ctx.scale(kb, kb)
            text(ctx, "FALTA PROBARLO EN MÁS PERSONAS", 0, 0, F_BIG, 58, EN, 1, align="center"); ctx.restore()
    elif i == 8:
        moon(ctx, 740, 560, 50, k)
        sleeper(ctx, 520, 760, 0.8, k, t=t)
        zzz(ctx, 420, 700, t, k)
        k2 = easeb((u - 0.3) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 1020); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 110, EN, 1, align="center"); ctx.restore()


def txt(ctx, i, u, d, t, lt):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "QUÉ PASA SI… · SUEÑO Y RENDIMIENTO", W / 2, 214, CY, k, 26)
        title(ctx, "¿SIESTA ANTES DE ENTRENAR?", WH, 380, 88, k)
    elif i == 1:
        pill(ctx, "REVISIÓN DE ENSAYOS", W / 2, 214, EN, k, 30, filled=True)
        title(ctx, "LO PUSIERON A PRUEBA", WH, 380, 96, k)
        src(ctx, "Mesas et al., Br J Sports Med 2023 · 22 ensayos aleatorizados · doi:10.1136/bjsports-2022-106355", k, 1130)
    elif i == 2:
        pill(ctx, "RESULTADO", W / 2, 214, GR, k, 30, filled=True)
        title(ctx, "TRAS UNA NOCHE NORMAL", WH, 380, 92, k)
        src(ctx, "Mesas et al., 2023 · siesta vs. sin siesta", k, 1120)
    elif i == 3:
        pill(ctx, "DURACIÓN", W / 2, 214, EN, k, 30, filled=True)
        title(ctx, "NI MUY CORTA NI ETERNA", WH, 380, 92, k)
        src(ctx, "Mesas et al., 2023 · mayor beneficio con siestas de 30 a <60 min", k, 1120)
    elif i == 4:
        pill(ctx, "COMENTA", W / 2, 214, EN, k, 32, filled=True)
        title(ctx, "¿DUERMES SIESTA?", WH, 380, 100, k)
    elif i == 5:
        pill(ctx, "EL DETALLE", W / 2, 214, SL, k, 30, filled=True)
        title(ctx, "DATE TIEMPO PARA DESPERTAR", WH, 380, 88, k)
        src(ctx, "Mesas et al., 2023 · efecto mayor con >1 h entre despertar y prueba", k, 1080)
    elif i == 6:
        pill(ctx, "OTRA REVISIÓN", W / 2, 214, GR, k, 30, filled=True)
        title(ctx, "NO TE HACE MÁS FUERTE", WH, 380, 92, k)
        text(ctx, "ESQUEMA ILUSTRATIVO", W / 2, 1110, F_MONO, 22, EN, k, align="center", bold=True)
        src(ctx, "Boukhris et al., Sports Med 2024 · doi:10.1007/s40279-023-01920-2", k, 1150)
    elif i == 7:
        pill(ctx, "LÍMITES", W / 2, 214, RD, k, 30, filled=True)
        title(ctx, "¿QUIÉNES PARTICIPARON?", WH, 380, 94, k)
        src(ctx, "Mesas et al., 2023 · 291 hombres de 18 a 35 años", k, 1130)
    elif i == 8:
        title(ctx, "MÁS CIENCIA DEL ENTRENAMIENTO", WH, 380, 80, k)


run_episode(neon, txt, "EXPEDIENTE 49 · SUEÑO")
