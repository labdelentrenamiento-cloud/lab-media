import sys, os, json, math, subprocess
sys.path.insert(0, "/home/claude/lab")
from engine import *

TL = json.load(open("timeline.json"))
LINES = TL["lines"]
TOTAL = TL["total"]
STARTS = [0.0] + [l["start"] - 0.12 for l in LINES[1:]]
WORDS = [w for l in LINES for w in l["words"]]
LABEL = "EXPEDIENTE 03 · HUESOS"
BG8 = (np.clip(BG, 0, 1) * 255).astype(np.uint8)


def scene_at(t):
    i = max(k for k, s in enumerate(STARTS) if s <= t)
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    return i, t - STARTS[i], end - STARTS[i]


def title(ctx, s, color=WH, y=345, size=86, a=1.0):
    sz = fit_size(ctx, s, F_BIG, size, W - 150)
    text(ctx, s, W / 2, y, F_BIG, sz, color, a, align="center")


def lt(i):
    """local time of line i's speech start relative to scene start"""
    return LINES[i]["start"] - STARTS[i]


def neon_layer(ctx, i, u, d, t):
    k = ease(u / 0.35)
    if i == 0:
        hk = clamp((u - 0.6) / 0.8)
        skeleton(ctx, 540, 445, 0.76, t, hl={"hips": (RD, hk), "spine": (RD, hk), "wrists": (RD, hk)}, base_a=0.75 * k)
        if u > 1.4:
            a = ease((u - 1.4) / 0.4)
            callout(ctx, 540 + 84 * .76, 445 + 552 * .76, 820, 760, "CADERA", RD, a)
        if u > 1.9:
            a = ease((u - 1.9) / 0.4)
            callout(ctx, 540, 445 + 330 * .76, 250, 640, "COLUMNA", RD, a)
        if u > 2.4:
            a = ease((u - 2.4) / 0.4)
            callout(ctx, 540 - 146 * .76, 445 + 528 * .76, 230, 960, "MUÑECA", RD, a)
    elif i == 1:
        ld = clamp((u - lt(1) - 1.9) / 0.6)
        skeleton(ctx, 660, 470, 0.70, t, hl={"legs": (GR, ld), "spine": (GR, ld), "hips": (GR, ld)}, base_a=0.8 * k, load=ld)
        chair_icon(ctx, 240, 900, a=0.8 * k)
        xa = ease((u - 0.8) / 0.3)
        if xa > 0:
            ctx.set_line_width(12); ctx.set_source_rgba(*RD, xa)
            ctx.move_to(130, 720); ctx.line_to(130 + 220 * xa, 720 + 320 * xa); ctx.stroke()
            ctx.move_to(350, 720); ctx.line_to(350 - 220 * xa, 720 + 320 * xa); ctx.stroke()
    elif i == 2:
        orbit_icon(ctx, 540, 640, 150 * (0.8 + 0.2 * k), t, a=k)
        hk = ease((u - 1.2) / 0.5)
        if hk > 0:
            sz = fit_size(ctx, "−1 a −1,5 %", F_BIG, 150, W - 160)
            text(ctx, "−1 a −1,5 %", W / 2, 1000, F_BIG, sz, RD, hk, align="center")
        # monthly bars
        for m in range(6):
            ak = ease((u - 2.0 - m * 0.25) / 0.3)
            if ak <= 0: continue
            hgt = (150 - m * 15) * ak
            x = 270 + m * 95
            rrect(ctx, x, 1215 - hgt, 60, hgt, 8); ctx.set_source_rgba(*RD, 0.25 + 0.1 * (6 - m) / 6); ctx.fill_preserve()
            ctx.set_source_rgba(*RD, 0.9); ctx.set_line_width(2.5); ctx.stroke()
    elif i == 3:
        barbell_icon(ctx, 540, 700, t, a=k)
        a1 = ease((u - lt(3) - 2.6) / 0.4); a2 = ease((u - lt(3) - 3.0) / 0.4)
        if a1 > 0: pill(ctx, "FUERZA", 330, 1000, CY, a1, 38)
        if a2 > 0: pill(ctx, "IMPACTO", 750, 1000, GR, a2, 38)
    elif i in (4, 5):
        if i == 4:
            upto = 35 * ease((u - 0.3) / 3.4)
            mp = ease((u - lt(4) - 3.6) / 0.5)
            chart(ctx, 130, 560, 820, 520, max(upto, 0.5), t, mark_peak=mp, a=k if u < 0.4 else 1)
        else:
            upto = 35 + 45 * ease(u / 2.2)
            mm = ease((u - 1.8) / 0.5)
            chart(ctx, 130, 560, 820, 520, upto, t, mark_peak=1.0, mark_meno=mm)
    elif i == 6:
        rrect(ctx, 90, 440, 900, 780, 28)
        ctx.set_source_rgba(*CY, 0.06 * k); ctx.fill_preserve(); ctx.set_source_rgba(*CY, 0.7 * k); ctx.set_line_width(3); ctx.stroke()
        rows = [("101 MUJERES POSMENOPÁUSICAS", WH), ("CON BAJA MASA ÓSEA", WH), ("FUERZA INTENSA + IMPACTO", GR),
                ("SUPERVISADAS", GR), ("2 VECES / SEMANA · 30 MIN", CY)]
        for r, (s, col) in enumerate(rows):
            ak = ease((u - 0.6 - r * 1.05) / 0.35)
            if ak <= 0: continue
            y = 535 + r * 108
            ctx.arc(150, y - 12, 10, 0, 6.283); ctx.set_source_rgba(*col, ak); ctx.fill()
            sz = fit_size(ctx, s, F_MONO, 40, 760, True)
            text(ctx, s, 185 + (1 - ak) * 30, y, F_MONO, sz, col, ak, bold=True)
        # months ring
        mk = clamp((u - 6.0) / 3.2)
        if u > 5.6:
            a = ease((u - 5.6) / 0.4)
            cx, cy, r = 540, 1100, 70
            ctx.new_path(); ctx.arc(cx, cy, r, 0, 6.283); ctx.set_source_rgba(*CY, 0.18 * a); ctx.set_line_width(12); ctx.stroke()
            ctx.new_path(); ctx.arc(cx, cy, r, -math.pi / 2, -math.pi / 2 + 6.283 * mk); ctx.set_source_rgba(*AM, a); ctx.set_line_width(12); ctx.stroke()
            text(ctx, str(max(1, int(round(1 + 7 * mk)))), cx, cy + 22, F_BIG, 64, WH, a, align="center")
            text(ctx, "MESES", cx + 110, cy + 12, F_MONO, 30, AM, a, bold=True)
    elif i == 7:
        skeleton(ctx, 340, 470, 0.70, t, hl={"spine": (GR, 1.0), "hips": (GR, 1.0)}, base_a=0.75 * k)
        b1 = ease((u - 0.8) / 1.0); b2 = ease((u - 1.4) / 0.8)
        base = 1180
        for x, hh, col, kk in [(690, 470, GR, b1), (870, 150, MU, b2)]:
            if kk <= 0: continue
            h = hh * kk
            rrect(ctx, x, base - h, 120, h, 14); ctx.set_source_rgba(*col, 0.22); ctx.fill_preserve()
            ctx.set_source_rgba(*col, 0.95); ctx.set_line_width(3); ctx.stroke()
        if b1 > 0.95:
            text(ctx, "▲", 750, base - 470 - 26, F_UI, 54, GR, 1, align="center", bold=True)
    elif i == 8:
        k2 = easeb((u - lt(8) - 1.2) / 0.5)
        if k2 > 0:
            ctx.save(); ctx.translate(540, 820); ctx.scale(k2, k2)
            text(ctx, "SÍGUEME", 0, 0, F_BIG, 190, CY, 1, align="center"); ctx.restore()


def text_layer(ctx, i, u, d, t):
    k = ease(u / 0.3)
    if i == 0:
        pill(ctx, "EXPEDIENTE · HUESOS", W / 2, 200, CY, k, 28)
        title(ctx, "HUESOS FRÁGILES A LOS 65", WH, 350, 92, k)
        text(ctx, "INSTRUCCIONES (PARA NO SEGUIR)", W / 2, 405, F_MONO, 30, RD, k, align="center", bold=True)
    elif i in (1, 3, 4):
        n = {1: "01", 3: "02", 4: "03"}[i]
        pill(ctx, "ERROR " + n, W / 2, 196, RD, k, 32, filled=True)
        s = {1: "PASAR EL DÍA SIN MOVERTE", 3: "NUNCA LEVANTAR PESO NI SALTAR", 4: "CREER QUE TIENES TIEMPO"}[i]
        title(ctx, s, WH, 345, 84, k)
        if i == 1:
            a = ease((u - lt(1) - 2.0) / 0.4)
            if a > 0: pill(ctx, "CARGA = ESTÍMULO PARA EL HUESO", W / 2, 1240, GR, a, 30)
        if i == 3:
            a = ease((u - lt(3) - 3.4) / 0.4)
            if a > 0: text(ctx, "= EL ESTÍMULO QUE CONSTRUYE HUESO", W / 2, 1150, F_MONO, 32, WH, a, align="center", bold=True)
    elif i == 2:
        pill(ctx, "ASTRONAUTAS · NASA", W / 2, 196, VI, k, 30)
        title(ctx, "SIN CARGA, EL HUESO SE PIERDE", WH, 345, 80, k)
        a = ease((u - 1.5) / 0.4)
        text(ctx, "DE DENSIDAD ÓSEA · CADA MES", W / 2, 1065, F_MONO, 32, WH, a, align="center", bold=True)
        text(ctx, "Fuente: NASA · misiones de 4 a 6 meses", W / 2, 1268, F_MONO, 22, MU, a, align="center")
    elif i == 5:
        pill(ctx, "DESPUÉS DE LOS 50", W / 2, 196, RD, k, 30)
        title(ctx, "HASTA −20 % EN 5 A 7 AÑOS", RD, 345, 86, k)
        text(ctx, "Fuente: National Osteoporosis Foundation", W / 2, 1265, F_MONO, 22, MU, k, align="center")
    elif i == 6:
        pill(ctx, "ESTUDIO LIFTMOR · JBMR 2018", W / 2, 196, GR, k, 30)
        title(ctx, "LA BUENA NOTICIA", GR, 345, 92, k)
    elif i == 7:
        pill(ctx, "RESULTADO", W / 2, 196, GR, k, 30)
        title(ctx, "MÁS DENSIDAD EN COLUMNA Y CADERA", WH, 345, 80, k)
        a1 = ease((u - 1.0) / 0.4); a2 = ease((u - 1.5) / 0.4)
        text(ctx, "FUERZA +", 750, 1225, F_MONO, 24, GR, a1, align="center", bold=True)
        text(ctx, "IMPACTO", 750, 1255, F_MONO, 24, GR, a1, align="center", bold=True)
        text(ctx, "EJERCICIO", 930, 1225, F_MONO, 24, MU, a2, align="center", bold=True)
        text(ctx, "SUAVE", 930, 1255, F_MONO, 24, MU, a2, align="center", bold=True)
        text(ctx, "Watson et al., JBMR 2018 · esquema", W / 2, 1300, F_MONO, 20, MU, k, align="center")
    elif i == 8:
        title(ctx, "TUS HUESOS TAMBIÉN SE ENTRENAN", WH, 345, 80, k)
        a = ease((u - lt(8) - 1.5) / 0.4)
        if a > 0:
            text(ctx, "para más ciencia del entrenamiento", W / 2, 910, F_UI, 46, WH, a, align="center", bold=True)
            pulse = 1 + 0.04 * math.sin(t * 7)
            ctx.save(); ctx.translate(540, 1050); ctx.scale(pulse, pulse)
            rrect(ctx, -170, -50, 340, 100, 50); ctx.set_source_rgba(*RD, a); ctx.fill()
            text(ctx, "SEGUIR", 0, 18, F_UI, 50, WH, a, align="center", bold=True)
            ctx.restore()


def frame(t):
    i, u, d = scene_at(t)
    base = BG8.copy()
    bs, bctx = surf_from(base)
    draw_grid(bctx, t)
    bs.flush()
    neon = np.zeros((H, W, 4), np.uint8)
    ns, nctx = surf_from(neon)
    punch = 1 + 0.06 * (1 - ease(u / 0.35))
    nctx.translate(W / 2, 820); nctx.scale(punch, punch); nctx.translate(-W / 2, -820)
    neon_layer(nctx, i, u, d, t)
    ns.flush()
    comp = glow_composite(base.astype(np.float32) / 255.0, neon)
    out = np.zeros((H, W, 4), np.uint8)
    out[..., :3] = (comp * 255).astype(np.uint8); out[..., 3] = 255
    os_, octx = surf_from(out)
    octx.save(); octx.translate(W / 2, 820); octx.scale(punch, punch); octx.translate(-W / 2, -820)
    text_layer(octx, i, u, d, t)
    octx.restore()
    captions(octx, WORDS, t)
    hud(octx, t, i, len(LINES), clamp(u / d), LABEL)
    # cut flash
    if i > 0 and u < 0.22:
        f = 1 - u / 0.22
        sy = u / 0.22 * H
        g = cairo.LinearGradient(0, sy - 220, 0, sy)
        g.add_color_stop_rgba(0, *CY, 0); g.add_color_stop_rgba(1, *CY, 0.35 * f)
        octx.rectangle(0, sy - 220, W, 220); octx.set_source(g); octx.fill()
        octx.set_source_rgba(1, 1, 1, 0.18 * f); octx.paint()
    os_.flush()
    return out


def render(f0, f1, path):
    tmp = path + ".part.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fr in range(f0, f1):
        p.stdin.write(frame(fr / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, path)


if __name__ == "__main__":
    if sys.argv[1] == "preview":
        for tt in map(float, sys.argv[2:]):
            Image.fromarray(frame(tt)[..., [2, 1, 0]]).save(f"prev_{tt:05.2f}.png")
    elif sys.argv[1] == "part":
        i, n = int(sys.argv[2]), int(sys.argv[3]); tot = int(TOTAL * FPS)
        render(tot * i // n, tot * (i + 1) // n, f"part{i}.mp4")
    elif sys.argv[1] == "starts":
        print([round(s, 2) for s in STARTS], TOTAL)
