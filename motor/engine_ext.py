"""Extra LAB modules + generic episode runner."""
import sys, os, json, math, subprocess
from engine import *


# ---------------------------------------------------------------- generic runner
SHIFT_Y = 90   # baja el contenido para que quede centrado en el recorte 4:5 de Instagram (zona segura y 300–1620)


def share_cta(ctx, a, y=1205):
    """Llamado a compartir/guardar en la escena final (dibujado por el motor en todos los episodios)."""
    if a <= 0:
        return
    items = [("COMPÁRTELO CON QUIEN LO NECESITE", CY), ("GUÁRDALO PARA DESPUÉS", AM)]
    for k, (s, col) in enumerate(items):
        yy = y + k * 96
        font(ctx, F_UI, 34, True)
        tw = ctx.text_extents(s).x_advance; pw = tw + 120; ph = 70; x0 = W / 2 - pw / 2
        rrect(ctx, x0, yy, pw, ph, ph / 2)
        ctx.set_source_rgba(0.02, 0.05, 0.12, 0.88 * a); ctx.fill_preserve()
        ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(3); ctx.stroke()
        ix, iy = x0 + 42, yy + ph / 2
        ctx.set_source_rgba(*col, a); ctx.set_line_width(4)
        if k == 0:   # flecha de compartir
            ctx.move_to(ix - 12, iy + 12); ctx.line_to(ix + 12, iy - 12); ctx.stroke()
            ctx.move_to(ix - 2, iy - 13); ctx.line_to(ix + 13, iy - 13); ctx.line_to(ix + 13, iy + 2); ctx.stroke()
        else:        # marcador (guardar)
            ctx.move_to(ix - 10, iy - 15); ctx.line_to(ix + 10, iy - 15); ctx.line_to(ix + 10, iy + 15)
            ctx.line_to(ix, iy + 6); ctx.line_to(ix - 10, iy + 15); ctx.close_path(); ctx.stroke()
        ctx.set_source_rgba(1, 1, 1, a)
        ctx.move_to(x0 + 78, yy + ph / 2 + 12); ctx.show_text(s)


def run_episode(neon_fn, text_fn, label, focus_y=820):
    TL = json.load(open("timeline.json"))
    LINES = TL["lines"]; TOTAL = TL["total"]
    STARTS = [0.0] + [l["start"] - 0.12 for l in LINES[1:]]
    WORDS = []
    for l in LINES:
        for w in l["words"]:
            if WORDS and w["w"] in ("%", "%.", "%,") and WORDS[-1]["w"][-1].isdigit():
                WORDS[-1] = dict(WORDS[-1], w=WORDS[-1]["w"] + w["w"], e=w["e"])
            else:
                WORDS.append(dict(w))
    BG8 = (np.clip(BG, 0, 1) * 255).astype(np.uint8)

    def scene_at(t):
        i = max(k for k, s in enumerate(STARTS) if s <= t)
        end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
        return i, t - STARTS[i], end - STARTS[i]

    def lt(i): return LINES[i]["start"] - STARTS[i]

    def frame(t):
        i, u, d = scene_at(t)
        base = BG8.copy(); bs, bctx = surf_from(base); draw_grid(bctx, t); bs.flush()
        neon = np.zeros((H, W, 4), np.uint8); ns, nctx = surf_from(neon)
        punch = 1 + 0.06 * (1 - ease(u / 0.35))
        nctx.translate(0, SHIFT_Y)
        nctx.translate(W / 2, focus_y); nctx.scale(punch, punch); nctx.translate(-W / 2, -focus_y)
        neon_fn(nctx, i, u, d, t, lt); ns.flush()
        comp = glow_composite(base.astype(np.float32) / 255.0, neon)
        out = np.zeros((H, W, 4), np.uint8); out[..., :3] = (comp * 255).astype(np.uint8); out[..., 3] = 255
        os_, octx = surf_from(out)
        octx.save(); octx.translate(0, SHIFT_Y); octx.translate(W / 2, focus_y); octx.scale(punch, punch); octx.translate(-W / 2, -focus_y)
        text_fn(octx, i, u, d, t, lt); octx.restore()
        if i == len(LINES) - 1:
            share_cta(octx, clamp((u - 0.4) / 0.5))
        captions(octx, WORDS, t, y=1490)
        hud(octx, t, i, len(LINES), clamp(u / d), label)
        if i > 0 and u < 0.22:
            f = 1 - u / 0.22; sy = u / 0.22 * H
            g = cairo.LinearGradient(0, sy - 220, 0, sy); g.add_color_stop_rgba(0, *CY, 0); g.add_color_stop_rgba(1, *CY, 0.35 * f)
            octx.rectangle(0, sy - 220, W, 220); octx.set_source(g); octx.fill()
            octx.set_source_rgba(1, 1, 1, 0.18 * f); octx.paint()
        os_.flush()
        return out

    def render(f0, f1, path):
        tmp = path + ".part.mp4"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
               "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", tmp]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for fr in range(f0, f1): p.stdin.write(frame(fr / FPS).tobytes())
        p.stdin.close()
        if p.wait() == 0: os.replace(tmp, path)

    a = sys.argv
    if a[1] == "preview":
        for tt in map(float, a[2:]):
            Image.fromarray(frame(tt)[..., [2, 1, 0]]).save(f"prev_{tt:05.2f}.png")
    elif a[1] == "part":
        i, n = int(a[2]), int(a[3]); tot = int(TOTAL * FPS)
        render(tot * i // n, tot * (i + 1) // n, f"part{i}.mp4")
    elif a[1] == "starts":
        print([round(s, 2) for s in STARTS], TOTAL)


def title(ctx, s, color=WH, y=345, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 150)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


# ---------------------------------------------------------------- brain
def brain(ctx, cx, cy, s, t, a=1.0, col=VI, fire=0.0, hippo=None):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    # outer silhouette (side view)
    ctx.move_to(-150, 30)
    ctx.curve_to(-175, -60, -110, -150, -10, -150)
    ctx.curve_to(90, -155, 170, -95, 168, -10)
    ctx.curve_to(168, 50, 120, 85, 70, 80)
    ctx.curve_to(50, 110, 10, 110, -10, 90)
    ctx.curve_to(-60, 100, -140, 90, -150, 30)
    ctx.close_path()
    ctx.set_source_rgba(*col, 0.10 * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(5); ctx.stroke()
    # gyri
    ctx.set_line_width(3.5)
    for k, (x, y, r, a0, a1) in enumerate([(-80, -60, 45, 3.6, 6.0), (0, -90, 50, 3.4, 6.2), (80, -60, 45, 3.5, 6.1),
                                           (-70, 20, 40, 0.3, 3.0), (20, -10, 45, 3.8, 6.4), (100, 20, 35, 0.2, 2.9),
                                           (-120, -20, 30, 1.2, 4.4), (40, 50, 30, 3.5, 6.0)]):
        ctx.new_path(); ctx.arc(x, y, r, a0, a1); ctx.set_source_rgba(*col, 0.55 * a); ctx.stroke()
    # cerebellum + stem
    ctx.new_path(); ctx.arc(105, 95, 38, -0.2, 3.3); ctx.set_source_rgba(*col, 0.8 * a); ctx.stroke()
    ctx.move_to(40, 100); ctx.line_to(30, 175); ctx.set_line_width(14); ctx.set_source_rgba(*col, 0.8 * a); ctx.stroke()
    # hippocampus
    if hippo:
        hc, hk = hippo
        pulse = 0.7 + 0.3 * math.sin(t * 5)
        ctx.new_path(); ctx.move_to(-5, -5); ctx.curve_to(-18, 40, 20, 78, 62, 62); ctx.curve_to(84, 52, 80, 26, 60, 30)
        ctx.set_source_rgba(*hc, hk * a); ctx.set_line_width(20); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke_preserve()
        ctx.set_source_rgba(1, 1, 1, 0.5 * hk * a * pulse); ctx.set_line_width(6); ctx.stroke()
    # firing sparks
    if fire > 0:
        for k in range(14):
            ph = (t * 1.7 + k * 0.37) % 1
            x = math.sin(k * 12.9) * 120; y = math.cos(k * 7.7) * 70 - 40
            ctx.new_path(); ctx.arc(x, y, 4 + 10 * (1 - ph), 0, 6.283); ctx.set_source_rgba(*CY, fire * a * (1 - ph)); ctx.fill()
    ctx.restore()


def polyline_point(pts, f):
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    L = sum(seg); d = f * L
    for i, s in enumerate(seg):
        if d <= s:
            k = d / s if s else 0
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * k, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * k)
        d -= s
    return pts[-1]


def nerve(ctx, pts, t, a=1.0, col=CY, rate=1.0, n=4):
    ctx.new_path(); ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    ctx.set_source_rgba(*col, 0.35 * a); ctx.set_line_width(5); ctx.stroke()
    for k in range(n):
        f = (t * 0.9 * rate + k / n) % 1
        x, y = polyline_point(pts, f)
        ctx.new_path(); ctx.arc(x, y, 11, 0, 6.283); ctx.set_source_rgba(*WH, a); ctx.fill()
        ctx.new_path(); ctx.arc(x, y, 22, 0, 6.283); ctx.set_source_rgba(*col, 0.4 * a); ctx.fill()


def fiber_bundle(ctx, x, y, w, h, n, active, t, a=1.0, col_on=GR, col_off=CY):
    rr = h / n
    for i in range(n):
        yy = y + i * rr
        on = (i + 0.5) / n <= active
        col = col_on if on else col_off
        flick = 0.85 + 0.15 * math.sin(t * 18 + i * 2.3) if on else 1
        rrect(ctx, x, yy + 3, w, rr - 6, (rr - 6) / 2)
        ctx.set_source_rgba(*col, (0.35 if on else 0.06) * a * flick); ctx.fill_preserve()
        ctx.set_source_rgba(*col, (0.95 if on else 0.45) * a); ctx.set_line_width(2.5); ctx.stroke()
        for sx in range(int(x + 30), int(x + w - 10), 34):
            ctx.move_to(sx, yy + 8); ctx.line_to(sx, yy + rr - 8)
            ctx.set_source_rgba(*col, (0.5 if on else 0.15) * a); ctx.set_line_width(1.5); ctx.stroke()


def leg(ctx, cx, top, s, a=1.0, col=CY, fill=0.06, thick=1.0):
    ctx.save(); ctx.translate(cx, top); ctx.scale(s * thick, s)
    ctx.move_to(-60, 0); ctx.curve_to(-78, 120, -66, 240, -40, 330)   # thigh outer
    ctx.curve_to(-48, 380, -46, 430, -36, 560); ctx.line_to(-46, 600); ctx.line_to(48, 600); ctx.line_to(30, 560)
    ctx.curve_to(40, 430, 44, 380, 36, 330); ctx.curve_to(60, 240, 68, 120, 58, 0); ctx.close_path()
    ctx.set_source_rgba(*col, fill * a); ctx.fill_preserve(); ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(4 / max(thick, 0.5)); ctx.stroke()
    ctx.new_path(); ctx.arc(-2, 340, 14, 0, 6.283); ctx.set_source_rgba(*col, 0.7 * a); ctx.set_line_width(3); ctx.stroke()
    ctx.restore()


def gauge(ctx, cx, cy, r, v, a=1.0, col=GR):
    ctx.new_path(); ctx.arc(cx, cy, r, math.pi * 0.8, math.pi * 2.2); ctx.set_source_rgba(*CY, 0.2 * a); ctx.set_line_width(18); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, r, math.pi * 0.8, math.pi * (0.8 + 1.4 * v)); ctx.set_source_rgba(*col, a); ctx.set_line_width(18); ctx.stroke()
    for k in range(11):
        ang = math.pi * (0.8 + 1.4 * k / 10)
        ctx.move_to(cx + math.cos(ang) * (r - 34), cy + math.sin(ang) * (r - 34)); ctx.line_to(cx + math.cos(ang) * (r - 18), cy + math.sin(ang) * (r - 18))
        ctx.set_source_rgba(*WH, 0.6 * a); ctx.set_line_width(3); ctx.stroke()
    ang = math.pi * (0.8 + 1.4 * v)
    ctx.move_to(cx, cy); ctx.line_to(cx + math.cos(ang) * (r - 40), cy + math.sin(ang) * (r - 40))
    ctx.set_source_rgba(*WH, a); ctx.set_line_width(7); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, cy, 14, 0, 6.283); ctx.set_source_rgba(*WH, a); ctx.fill()


def footprints(ctx, x0, x1, y, t, speed, a=1.0, col=CY):
    step = 120
    off = (t * speed * 180) % step
    x = x0 - step + off; k = 0
    while x < x1:
        if x > x0 - 20:
            yy = y + (24 if k % 2 else -24)
            ctx.save(); ctx.translate(x, yy); ctx.scale(1.6, 0.8)
            ctx.new_path(); ctx.arc(0, 0, 18, 0, 6.283); ctx.restore()
            fa = clamp((x - x0) / 120) * clamp((x1 - x) / 120)
            ctx.set_source_rgba(*col, 0.85 * a * fa); ctx.fill()
        x += step; k += 1


def line_chart(ctx, x0, y0, w, h, series, xticks, xlabel, ylabel, a=1.0):
    ctx.set_line_width(2)
    for i in range(5):
        yy = y0 + h - i * h / 4
        ctx.move_to(x0, yy); ctx.line_to(x0 + w, yy); ctx.set_source_rgba(*CY, 0.12 * a); ctx.stroke()
    ctx.move_to(x0, y0); ctx.line_to(x0, y0 + h); ctx.line_to(x0 + w, y0 + h); ctx.set_source_rgba(*CY, 0.6 * a); ctx.set_line_width(3); ctx.stroke()
    for (fx, lab) in xticks:
        text(ctx, lab, x0 + fx * w, y0 + h + 40, F_MONO, 24, MU, a, align="center")
    if xlabel: text(ctx, xlabel, x0 + w, y0 + h + 82, F_MONO, 22, MU, a, align="right")
    if ylabel: text(ctx, ylabel, x0, y0 - 18, F_MONO, 22, MU, a)
    for (fn, col, upto, fill) in series:
        n = max(2, int(80 * upto))
        pts = [(x0 + (i / 80) * w, y0 + h - fn(i / 80) * h) for i in range(n + 1)]
        if fill:
            ctx.new_path(); ctx.move_to(pts[0][0], y0 + h)
            for p in pts: ctx.line_to(*p)
            ctx.line_to(pts[-1][0], y0 + h); ctx.close_path()
            g = cairo.LinearGradient(0, y0, 0, y0 + h); g.add_color_stop_rgba(0, *col, 0.25 * a); g.add_color_stop_rgba(1, *col, 0)
            ctx.set_source(g); ctx.fill()
        ctx.new_path(); ctx.move_to(*pts[0])
        for p in pts[1:]: ctx.line_to(*p)
        ctx.set_source_rgba(*col, a); ctx.set_line_width(6); ctx.stroke()
        ctx.new_path(); ctx.arc(*pts[-1], 10, 0, 6.283); ctx.set_source_rgba(*WH, a); ctx.fill()


def vbars(ctx, items, x0, base, bw, gap, maxh, k, a=1.0, label_size=24):
    for j, (lab, v, col) in enumerate(items):
        kk = ease((k - j * 0.15) / 0.7)
        if kk <= 0: continue
        x = x0 + j * (bw + gap); hgt = maxh * v * kk
        rrect(ctx, x, base - hgt, bw, hgt, 14); ctx.set_source_rgba(*col, 0.22 * a); ctx.fill_preserve()
        ctx.set_source_rgba(*col, 0.95 * a); ctx.set_line_width(3); ctx.stroke()
        for li, part in enumerate(lab.split("\n")):
            text(ctx, part, x + bw / 2, base + 40 + li * 30, F_MONO, label_size, col, a * kk, align="center", bold=True)


def big(ctx, s, x, y, size, col, a=1.0, maxw=W - 140):
    sz = fit_size(ctx, s, F_BIG, size, maxw)
    text(ctx, s, x, y, F_BIG, sz, col, a, align="center")


def clock(ctx, cx, cy, r, t, back=0.0, a=1.0, col=CY):
    ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*col, 0.08 * a); ctx.fill_preserve()
    ctx.set_source_rgba(*col, 0.9 * a); ctx.set_line_width(6); ctx.stroke()
    for k in range(12):
        ang = k / 12 * 6.283
        ctx.move_to(cx + math.cos(ang) * (r - 26), cy + math.sin(ang) * (r - 26)); ctx.line_to(cx + math.cos(ang) * (r - 8), cy + math.sin(ang) * (r - 8))
        ctx.set_source_rgba(*WH, 0.7 * a); ctx.set_line_width(4); ctx.stroke()
    am = -math.pi / 2 - back * 6.283 * 3
    ah = -math.pi / 2 + 1.1 - back * 6.283 * 0.25
    for ang, L, w in ((am, r * 0.78, 6), (ah, r * 0.5, 10)):
        ctx.move_to(cx, cy); ctx.line_to(cx + math.cos(ang) * L, cy + math.sin(ang) * L)
        ctx.set_source_rgba(*WH, a); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    # rewind arrow
    ctx.new_path(); ctx.arc_negative(cx, cy, r + 34, -0.3, -2.2); ctx.set_source_rgba(*GR, 0.9 * a); ctx.set_line_width(8); ctx.stroke()
    ex, ey = cx + math.cos(-2.2) * (r + 34), cy + math.sin(-2.2) * (r + 34)
    ctx.move_to(ex - 22, ey + 6); ctx.line_to(ex, ey - 4); ctx.line_to(ex + 8, ey + 24); ctx.set_source_rgba(*GR, 0.9 * a); ctx.stroke()


def tears(ctx, x, y, w, h, n, k, t, seed=3):
    import random as _r
    rg = _r.Random(seed); rr = h / n
    for j in range(9):
        i = rg.randrange(n); px = x + 60 + rg.random() * (w - 120)
        yy = y + i * rr + rr / 2
        kk = ease((k - j * 0.08) / 0.3)
        if kk <= 0: continue
        ctx.new_path(); ctx.move_to(px - 14, yy - rr * 0.35)
        for z in range(4): ctx.line_to(px + (8 if z % 2 == 0 else -8), yy - rr * 0.35 + (z + 1) * rr * 0.18)
        ctx.set_source_rgba(*RD, kk); ctx.set_line_width(5); ctx.stroke()
        fl = 0.5 + 0.5 * math.sin(t * 9 + j)
        ctx.new_path(); ctx.arc(px, yy, 14 + 6 * fl, 0, 6.283); ctx.set_source_rgba(*RD, 0.35 * kk); ctx.fill()
