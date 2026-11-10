"""LAB engine: renders a tech/HUD style vertical Short from a timeline + scene spec."""
import cairo, math, json, random, sys, os, subprocess
import numpy as np
from PIL import Image, ImageFilter

W, H, FPS = 1080, 1920, 30
CY = (0.24, 0.94, 1.0); GR = (0.35, 0.95, 0.60); RD = (1.0, 0.36, 0.45)
AM = (1.0, 0.76, 0.29); VI = (0.61, 0.55, 1.0); WH = (1, 1, 1); MU = (0.55, 0.60, 0.77)
F_BIG = "Anton"; F_UI = "Inter Display"; F_MONO = "DejaVu Sans Mono"


def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def easeb(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def lerp(a, b, k): return a + (b - a) * k


# ---------------------------------------------------------------- background
def make_bg():
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt(((x - W / 2) / W) ** 2 + ((y - H * 0.42) / H) ** 2)
    c0 = np.array([0.055, 0.10, 0.24]); c1 = np.array([0.008, 0.016, 0.05])
    k = np.clip(d / 0.75, 0, 1)[..., None]
    rgb = c0 * (1 - k) + c1 * k
    img = np.zeros((H, W, 4), np.float32)
    img[..., 2] = rgb[..., 0]; img[..., 1] = rgb[..., 1]; img[..., 0] = rgb[..., 2]; img[..., 3] = 1
    return img


BG = make_bg()
random.seed(5)
PARTS = [(random.uniform(0, W), random.uniform(0, H), random.uniform(0.6, 2.4), random.uniform(6, 22), random.uniform(0, 6.28)) for _ in range(90)]


def draw_grid(ctx, t):
    # perspective floor
    hy = 1250; vx = W / 2
    ctx.set_line_width(1.5)
    for i in range(-14, 15):
        ctx.move_to(vx + i * 26, hy); ctx.line_to(vx + i * 260, H + 40)
        ctx.set_source_rgba(*CY, 0.07); ctx.stroke()
    off = (t * 0.35) % 1
    for j in range(14):
        z = (j + off) / 14
        y = hy + (H - hy) * (z ** 2.2)
        ctx.move_to(0, y); ctx.line_to(W, y)
        ctx.set_source_rgba(*CY, 0.03 + 0.07 * z); ctx.stroke()
    # faint upper grid
    for gx in range(0, W, 90):
        ctx.move_to(gx, 0); ctx.line_to(gx, hy); ctx.set_source_rgba(*CY, 0.025); ctx.stroke()
    for gy in range(0, hy, 90):
        ctx.move_to(0, gy); ctx.line_to(W, gy); ctx.set_source_rgba(*CY, 0.025); ctx.stroke()
    for (x, y, r, sp, ph) in PARTS:
        yy = (y - t * sp) % H
        a = 0.25 + 0.25 * math.sin(t * 1.3 + ph)
        ctx.arc(x + 6 * math.sin(t * 0.5 + ph), yy, r, 0, 6.283); ctx.set_source_rgba(*CY, a * 0.5); ctx.fill()


# ---------------------------------------------------------------- text helpers
def font(ctx, fam, size, bold=False):
    ctx.select_font_face(fam, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)


def text(ctx, s, x, y, fam, size, col, a=1.0, align="left", bold=False, track=0.0):
    font(ctx, fam, size, bold)
    if track:
        widths = [ctx.text_extents(c).x_advance + track for c in s]
        tw = sum(widths) - track
    else:
        tw = ctx.text_extents(s).x_advance
    x0 = x - tw / 2 if align == "center" else (x - tw if align == "right" else x)
    ctx.set_source_rgba(*col, a)
    if track:
        xx = x0
        for c, wv in zip(s, widths):
            ctx.move_to(xx, y); ctx.show_text(c); xx += wv
    else:
        ctx.move_to(x0, y); ctx.show_text(s)
    return tw


def fit_size(ctx, s, fam, size, maxw, bold=False):
    font(ctx, fam, size, bold)
    while ctx.text_extents(s).x_advance > maxw and size > 10:
        size -= 2; font(ctx, fam, size, bold)
    return size


def rrect(ctx, x, y, w, h, r):
    ctx.new_sub_path(); ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); ctx.close_path()


def pill(ctx, s, cx, y, col, a=1.0, size=30, filled=False):
    font(ctx, F_MONO, size, True)
    tw = ctx.text_extents(s).x_advance; pw = tw + 48; ph = size + 26
    rrect(ctx, cx - pw / 2, y, pw, ph, ph / 2)
    if filled:
        ctx.set_source_rgba(*col, 0.95 * a); ctx.fill()
        ctx.set_source_rgba(0.02, 0.05, 0.1, a)
    else:
        ctx.set_source_rgba(*col, 0.12 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.85 * a); ctx.set_line_width(2.5); ctx.stroke()
        ctx.set_source_rgba(*col, a)
    ctx.move_to(cx - tw / 2, y + ph / 2 + size * 0.36); ctx.show_text(s)
    return pw, ph


# ---------------------------------------------------------------- HUD
def hud(ctx, t, scene_i, n_scenes, prog, label):
    L = 46; m = 34
    ctx.set_line_width(4); ctx.set_source_rgba(*CY, 0.8)
    for (x, y, dx, dy) in [(m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)]:
        ctx.move_to(x, y + dy * L); ctx.line_to(x, y); ctx.line_to(x + dx * L, y); ctx.stroke()
    ctx.arc(90, 101, 9, 0, 6.283); ctx.set_source_rgba(*CY, 0.95); ctx.fill()
    ctx.arc(90, 101, 15, 0, 6.283); ctx.set_source_rgba(*CY, 0.6); ctx.set_line_width(2); ctx.stroke()
    text(ctx, "LAB · CIENCIA DEL ENTRENAMIENTO", 116, 112, F_UI, 30, CY, 0.95, bold=True, track=1.5)
    blink = 1.0 if (t % 1.0) < 0.6 else 0.25
    ctx.arc(W - 200, 101, 9, 0, 6.283); ctx.set_source_rgba(*RD, blink); ctx.fill()
    text(ctx, "REC", W - 182, 112, F_MONO, 28, RD, 0.9, bold=True)
    text(ctx, "T+%05.1f" % t, W - 78, 150, F_MONO, 24, MU, 0.9, align="right")
    text(ctx, label, 78, 150, F_MONO, 24, MU, 0.9)
    ctx.move_to(78, 172); ctx.line_to(W - 78, 172); ctx.set_source_rgba(*CY, 0.25); ctx.set_line_width(1.5); ctx.stroke()
    # progress
    gap = 8; x0 = 78; x1 = W - 78; segw = (x1 - x0 - gap * (n_scenes - 1)) / n_scenes; y = 1830
    for i in range(n_scenes):
        xs = x0 + i * (segw + gap)
        rrect(ctx, xs, y, segw, 8, 4); ctx.set_source_rgba(*CY, 0.18); ctx.fill()
        f = 1 if i < scene_i else (prog if i == scene_i else 0)
        if f > 0:
            rrect(ctx, xs, y, max(8, segw * f), 8, 4); ctx.set_source_rgba(*CY, 0.95); ctx.fill()


# ---------------------------------------------------------------- skeleton
def bone(ctx, pts, w, col, a, fill_a):
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    ctx.set_source_rgba(*col, a); ctx.set_line_width(w + 5); ctx.stroke_preserve()
    ctx.set_source_rgba(0.02, 0.06, 0.12, 1); ctx.set_line_width(w - 2); ctx.stroke_preserve()
    ctx.set_source_rgba(*col, fill_a); ctx.set_line_width(w - 2); ctx.stroke()


def skeleton(ctx, cx, top, sc, t, hl=None, base_a=0.85, scan=True, load=0.0):
    hl = hl or {}
    def C(region):
        if region in hl:
            col, k = hl[region]
            pulse = 0.65 + 0.35 * math.sin(t * 6)
            return col, 0.95, 0.35 * k * pulse + 0.05
        return CY, base_a, 0.06
    ctx.save(); ctx.translate(cx, top); ctx.scale(sc, sc)
    # skull
    col, a, fa = C("skull")
    ctx.save(); ctx.translate(0, 70); ctx.scale(52, 64); ctx.arc(0, 0, 1, 0, 6.283); ctx.restore()
    ctx.set_source_rgba(*col, fa); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    for s in (-1, 1):
        ctx.save(); ctx.translate(s * 20, 68); ctx.scale(13, 11); ctx.arc(0, 0, 1, 0, 6.283); ctx.restore()
        ctx.set_source_rgba(*col, a * 0.8); ctx.set_line_width(3); ctx.stroke()
    ctx.move_to(-28, 112); ctx.curve_to(-20, 140, 20, 140, 28, 112); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
    # neck + spine
    col, a, fa = C("spine")
    for i in range(22):
        y = 140 + i * 15.5
        w = 18 + (i > 4) * 6 + (i > 14) * 6
        rrect(ctx, -w / 2, y, w, 11, 4)
        ctx.set_source_rgba(*col, fa * 2.2); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(2.5); ctx.stroke()
    # clavicles, sternum, ribs
    col, a, fa = C("ribs")
    for s in (-1, 1):
        bone(ctx, [(s * 8, 196), (s * 60, 186), (s * 112, 182)], 10, col, a, fa)
    rrect(ctx, -9, 205, 18, 120, 6); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
    for i in range(10):
        y = 210 + i * 21
        wmax = 98 - abs(i - 4) * 4 - max(0, i - 7) * 8
        for s in (-1, 1):
            ctx.move_to(s * 14, y); ctx.curve_to(s * (wmax + 10), y - 14, s * (wmax + 6), y + 30, s * (wmax - 30), y + 46)
            ctx.set_source_rgba(*col, a * 0.85); ctx.set_line_width(4); ctx.stroke()
    # pelvis
    col, a, fa = C("hips")
    for s in (-1, 1):
        ctx.move_to(s * 16, 478); ctx.curve_to(s * 70, 455, s * 128, 470, s * 120, 505)
        ctx.curve_to(s * 112, 545, s * 82, 585, s * 40, 595); ctx.curve_to(s * 22, 585, s * 16, 560, s * 16, 478)
        ctx.close_path(); ctx.set_source_rgba(*col, fa * 1.6); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(4); ctx.stroke()
        ctx.arc(s * 50, 560, 15, 0, 6.283); ctx.set_source_rgba(*col, a * 0.7); ctx.set_line_width(3); ctx.stroke()
        # femur head + neck (hip)
        ctx.arc(s * 84, 552, 17, 0, 6.283); ctx.set_source_rgba(*col, fa * 2); ctx.fill_preserve(); ctx.set_source_rgba(*col, a); ctx.set_line_width(3.5); ctx.stroke()
    # legs
    col, a, fa = C("legs")
    for s in (-1, 1):
        bone(ctx, [(s * 96, 575), (s * 80, 690), (s * 62, 790)], 20, col, a, fa)
        ctx.arc(s * 61, 803, 12, 0, 6.283); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
        bone(ctx, [(s * 60, 818), (s * 56, 900), (s * 52, 975)], 16, col, a, fa)
        bone(ctx, [(s * 76, 822), (s * 72, 970)], 7, col, a * 0.8, fa)
        ctx.move_to(s * 44, 985); ctx.line_to(s * 92, 1000); ctx.line_to(s * 40, 1004); ctx.close_path()
        ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
    # arms
    col, a, fa = C("arms")
    for s in (-1, 1):
        ctx.arc(s * 116, 190, 13, 0, 6.283); ctx.set_source_rgba(*col, a); ctx.set_line_width(3); ctx.stroke()
        bone(ctx, [(s * 120, 200), (s * 130, 300), (s * 138, 385)], 15, col, a, fa)
    colw, aw, faw = C("wrists")
    for s in (-1, 1):
        bone(ctx, [(s * 138, 395), (s * 146, 470), (s * 150, 520)], 8, col, a, fa)
        bone(ctx, [(s * 128, 398), (s * 134, 470), (s * 140, 522)], 7, col, a, fa)
        ctx.arc(s * 146, 528, 13, 0, 6.283); ctx.set_source_rgba(*colw, faw * 2.5); ctx.fill_preserve()
        ctx.set_source_rgba(*colw, aw); ctx.set_line_width(3); ctx.stroke()
        for k in range(5):
            ang = math.radians(80 + (k - 2) * 9) if s > 0 else math.radians(100 - (k - 2) * 9)
            ctx.move_to(s * 146, 540); ctx.line_to(s * 146 + math.cos(ang) * 4 * s, 540 + 52 - abs(k - 2) * 6)
            ctx.set_source_rgba(*col, a * 0.8); ctx.set_line_width(3); ctx.stroke()
    # load arrows
    if load > 0:
        for s in (-1, 0, 1):
            for k in range(3):
                ph = ((t * 1.4 + k / 3) % 1)
                y = -120 + ph * 90 + (0 if s == 0 else 150)
                x = s * 116
                al = load * (1 - ph)
                ctx.move_to(x - 22, y); ctx.line_to(x, y + 22); ctx.line_to(x + 22, y)
                ctx.set_source_rgba(*GR, al); ctx.set_line_width(6); ctx.stroke()
    # scanline
    if scan:
        sy = ((t * 0.45) % 1) * 1040 - 20
        g = cairo.LinearGradient(0, sy - 60, 0, sy)
        g.add_color_stop_rgba(0, *CY, 0); g.add_color_stop_rgba(1, *CY, 0.22)
        ctx.rectangle(-200, sy - 60, 400, 60); ctx.set_source(g); ctx.fill()
        ctx.move_to(-210, sy); ctx.line_to(210, sy); ctx.set_source_rgba(*CY, 0.9); ctx.set_line_width(2.5); ctx.stroke()
    ctx.restore()


def callout(ctx, x, y, tx, ty, label, col, a=1.0, sub=None):
    ctx.arc(x, y, 7, 0, 6.283); ctx.set_source_rgba(*col, a); ctx.fill()
    ctx.arc(x, y, 16, 0, 6.283); ctx.set_source_rgba(*col, a * 0.5); ctx.set_line_width(2); ctx.stroke()
    ctx.move_to(x, y); ctx.line_to(tx, ty); ctx.line_to(tx + (60 if tx > x else -60), ty)
    ctx.set_source_rgba(*col, a * 0.9); ctx.set_line_width(2.5); ctx.stroke()
    align = "left" if tx > x else "right"
    xx = tx + (70 if tx > x else -70)
    text(ctx, label, xx, ty + 11, F_MONO, 30, col, a, align=align, bold=True)
    if sub:
        text(ctx, sub, xx, ty + 46, F_MONO, 22, MU, a, align=align)


# ---------------------------------------------------------------- icons
def orbit_icon(ctx, cx, cy, r, t, a=1.0):
    ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*CY, 0.08 * a); ctx.fill_preserve()
    ctx.set_source_rgba(*CY, 0.9 * a); ctx.set_line_width(4); ctx.stroke()
    for k in (-0.45, 0, 0.45):
        ctx.save(); ctx.translate(cx, cy); ctx.scale(1, 1); ctx.move_to(-r, k * r * 1.2); ctx.curve_to(-r * 0.4, k * r * 1.2 + 18, r * 0.4, k * r * 1.2 + 18, r, k * r * 1.2)
        ctx.restore(); ctx.set_source_rgba(*CY, 0.35 * a); ctx.set_line_width(2); ctx.stroke()
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.35); ctx.scale(1, 0.32)
    ctx.arc(0, 0, r * 1.75, 0, 6.283); ctx.restore(); ctx.set_source_rgba(*VI, 0.8 * a); ctx.set_line_width(3); ctx.stroke()
    ang = t * 1.6
    sx = cx + math.cos(ang) * r * 1.75 * math.cos(-0.35) - math.sin(ang) * r * 1.75 * 0.32 * math.sin(-0.35)
    sy = cy + math.cos(ang) * r * 1.75 * math.sin(-0.35) + math.sin(ang) * r * 1.75 * 0.32 * math.cos(-0.35)
    # satellite / station
    ctx.rectangle(sx - 26, sy - 5, 52, 10); ctx.set_source_rgba(*WH, a); ctx.fill()
    ctx.rectangle(sx - 8, sy - 12, 16, 24); ctx.set_source_rgba(*AM, a); ctx.fill()


def barbell_icon(ctx, cx, cy, t, a=1.0):
    bob = -abs(math.sin(t * 2.4)) * 40
    y = cy + bob
    ctx.move_to(cx - 300, y); ctx.line_to(cx + 300, y); ctx.set_source_rgba(*WH, 0.9 * a); ctx.set_line_width(10); ctx.stroke()
    for s in (-1, 1):
        for k, (h, w) in enumerate([(170, 34), (130, 26)]):
            x = cx + s * (215 + k * 40)
            rrect(ctx, x - w / 2, y - h / 2, w, h, 8); ctx.set_source_rgba(*CY, 0.15 * a); ctx.fill_preserve()
            ctx.set_source_rgba(*CY, a); ctx.set_line_width(4); ctx.stroke()
    # impact waves below
    for k in range(3):
        ph = ((t * 1.2 + k / 3) % 1)
        rr = 40 + ph * 260
        ctx.save(); ctx.translate(cx, cy + 230); ctx.scale(1, 0.25); ctx.arc(0, 0, rr, 0, 6.283); ctx.restore()
        ctx.set_source_rgba(*GR, (1 - ph) * a); ctx.set_line_width(4); ctx.stroke()


def chair_icon(ctx, cx, cy, a=1.0, col=MU):
    ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_source_rgba(*col, a)
    ctx.move_to(cx - 90, cy - 170); ctx.line_to(cx - 90, cy + 140)
    ctx.move_to(cx - 90, cy + 10); ctx.line_to(cx + 100, cy + 10); ctx.line_to(cx + 100, cy + 140)
    ctx.move_to(cx - 90, cy + 10); ctx.line_to(cx - 90, cy + 140); ctx.stroke()


# ---------------------------------------------------------------- chart (bone mass vs age)
def bone_curve(age, female=True):
    rise = 1 / (1 + math.exp(-(age - 14) / 4.0))
    m = 0.25 + 0.75 * rise
    if age > 30: m -= 0.0025 * (age - 30)
    if female and age > 50:
        drop = min(age - 50, 7) / 7 * 0.20 * m
        m -= drop + 0.003 * max(0, age - 57)
    return m


def chart(ctx, x0, y0, w, h, upto, t, mark_peak=0.0, mark_meno=0.0, a=1.0):
    ctx.set_line_width(2)
    for i in range(5):
        y = y0 + h - i * h / 4
        ctx.move_to(x0, y); ctx.line_to(x0 + w, y); ctx.set_source_rgba(*CY, 0.12 * a); ctx.stroke()
    ctx.move_to(x0, y0); ctx.line_to(x0, y0 + h); ctx.line_to(x0 + w, y0 + h); ctx.set_source_rgba(*CY, 0.6 * a); ctx.set_line_width(3); ctx.stroke()
    for ag in range(0, 81, 10):
        xx = x0 + ag / 80 * w
        text(ctx, str(ag), xx, y0 + h + 40, F_MONO, 24, MU, a, align="center")
    text(ctx, "EDAD (AÑOS)", x0 + w, y0 + h + 82, F_MONO, 22, MU, a, align="right")
    text(ctx, "MASA ÓSEA", x0, y0 - 18, F_MONO, 22, MU, a)
    def P(ag): return x0 + ag / 80 * w, y0 + h - bone_curve(ag) * h * 0.95
    n = int(upto * 4)
    if n >= 2:
        # fill
        ctx.move_to(x0, y0 + h)
        for i in range(n + 1): ctx.line_to(*P(i / 4))
        ctx.line_to(P(n / 4)[0], y0 + h); ctx.close_path()
        g = cairo.LinearGradient(0, y0, 0, y0 + h); g.add_color_stop_rgba(0, *CY, 0.25 * a); g.add_color_stop_rgba(1, *CY, 0.0)
        ctx.set_source(g); ctx.fill()
        ctx.move_to(*P(0))
        for i in range(1, n + 1): ctx.line_to(*P(i / 4))
        ctx.set_source_rgba(*CY, a); ctx.set_line_width(6); ctx.stroke()
        hx, hy = P(n / 4)
        ctx.arc(hx, hy, 10, 0, 6.283); ctx.set_source_rgba(*WH, a); ctx.fill()
    if mark_peak > 0 and upto >= 30:
        px, py = P(30)
        ctx.move_to(px, py); ctx.line_to(px, y0 + h); ctx.set_source_rgba(*AM, 0.7 * mark_peak); ctx.set_dash([8, 8]); ctx.set_line_width(3); ctx.stroke(); ctx.set_dash([])
        ctx.arc(px, py, 16 + 6 * math.sin(t * 5), 0, 6.283); ctx.set_source_rgba(*AM, mark_peak); ctx.set_line_width(4); ctx.stroke()
        pill(ctx, "PICO ≈ 30 AÑOS", px, py - 100, AM, mark_peak, 28, filled=True)
    if mark_meno > 0 and upto >= 57:
        x50 = P(50)[0]; x57 = P(57)[0]
        ctx.rectangle(x50, y0, x57 - x50, h); ctx.set_source_rgba(*RD, 0.16 * mark_meno); ctx.fill()
        ctx.move_to(x50, y0); ctx.line_to(x50, y0 + h); ctx.move_to(x57, y0); ctx.line_to(x57, y0 + h)
        ctx.set_source_rgba(*RD, 0.8 * mark_meno); ctx.set_line_width(2.5); ctx.stroke()
        pill(ctx, "MENOPAUSIA", x57 + 120, y0 - 70, RD, mark_meno, 26)


# ---------------------------------------------------------------- captions
def captions(ctx, words, t, y=1415):
    # pick current chunk of up to ~4 words / 26 chars
    chunks = []; cur = []; ln = 0
    for w in words:
        if cur and (ln + len(w["w"]) > 22 or len(cur) >= 4):
            chunks.append(cur); cur = []; ln = 0
        cur.append(w); ln += len(w["w"]) + 1
        if w["w"][-1] in ".,:?!…": chunks.append(cur); cur = []; ln = 0
    if cur: chunks.append(cur)
    act = None
    for ch in chunks:
        if ch[0]["s"] - 0.05 <= t <= ch[-1]["e"] + 0.25: act = ch
    if not act: return
    size = 92
    font(ctx, F_BIG, size)
    toks = [w["w"].upper() for w in act]
    space = ctx.text_extents(" ").x_advance + 18
    widths = [ctx.text_extents(s).x_advance for s in toks]
    tot = sum(widths) + space * (len(toks) - 1)
    while tot > W - 120:
        size -= 4; font(ctx, F_BIG, size)
        space = ctx.text_extents(" ").x_advance + 18
        widths = [ctx.text_extents(s).x_advance for s in toks]; tot = sum(widths) + space * (len(toks) - 1)
    x = (W - tot) / 2
    k_in = ease((t - act[0]["s"] + 0.05) / 0.15)
    for wd, s, wv in zip(act, toks, widths):
        on = wd["s"] <= t
        now = wd["s"] <= t <= wd["e"] + 0.05
        col = CY if now else (WH if on else (0.75, 0.8, 0.95))
        a = 1.0 if on else 0.55
        sc = 1.08 if now else 1.0
        ctx.save(); ctx.translate(x + wv / 2, y - size * 0.35); ctx.scale(sc, sc); ctx.translate(-(x + wv / 2), -(y - size * 0.35))
        ctx.move_to(x, y + (1 - k_in) * 30); ctx.text_path(s)
        ctx.set_source_rgba(0, 0.02, 0.06, 0.85 * a); ctx.set_line_width(14); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
        ctx.set_source_rgba(*col, a * k_in); ctx.fill()
        ctx.restore()
        x += wv + space


# ---------------------------------------------------------------- composite
def glow_composite(base, neon, gain=1.35):
    n = neon.astype(np.float32) / 255.0
    rgb = Image.fromarray(np.ascontiguousarray(neon[..., :3]), "RGB")
    small = rgb.resize((W // 3, H // 3), Image.BILINEAR).filter(ImageFilter.GaussianBlur(7))
    g = np.asarray(small.resize((W, H), Image.BICUBIC)).astype(np.float32) / 255.0
    out = base[..., :3] * (1 - n[..., 3:4]) + n[..., :3]
    out += g * gain
    return np.clip(out, 0, 1)


def surf_from(arr):
    s = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_ARGB32, W, H)
    return s, cairo.Context(s)
