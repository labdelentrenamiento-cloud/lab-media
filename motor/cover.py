#!/usr/bin/env python3
"""Portada LAB para Reels/Shorts/TikTok.

Uso:
  python3 cover.py VIDEO.mp4 "LÍNEA 1|LÍNEA *2*|LÍNEA 3" SALIDA.mp4 [--png portada.png] [--t 0.42]

- Las líneas se separan con "|". Las palabras entre *asteriscos* van en ámbar.
- Crea una portada 1080x1920 de alto contraste (fondo = cuadro del video, oscurecido,
  con acentos cálidos) y la antepone como los primeros 0,2 s del video. Instagram y TikTok
  usan el primer cuadro como portada por defecto; YouTube también lo ofrece.
- Todo el texto queda dentro de la zona central 3:4 (y 260–1660) para que se lea en la grilla
  del perfil de Instagram.
"""
import os, subprocess, sys, tempfile, json
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

W, H = 1080, 1920
AMBER = (255, 194, 75)
CORAL = (255, 93, 115)
CYAN = (62, 240, 255)
WHITE = (255, 255, 255)


def font(cands, size):
    for c in cands:
        for p in [os.path.expanduser('~/.fonts/' + c), '/usr/share/fonts/truetype/' + c, c]:
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    # fc-match como respaldo
    name = cands[0].split('/')[-1].split('.')[0]
    path = subprocess.run(['fc-match', '-f', '%{file}', name], capture_output=True, text=True).stdout
    return ImageFont.truetype(path, size)


ANTON = ['Anton-Regular.ttf', 'anton/Anton-Regular.ttf']
INTER = ['/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf', '/usr/share/fonts/opentype/inter/Inter-Bold.otf']


def duration(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                         capture_output=True, text=True).stdout.strip()
    return float(out)


def grab(video, t):
    tmp = tempfile.mktemp(suffix='.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', video, '-frames:v', '1', tmp], check=True)
    im = Image.open(tmp).convert('RGB').resize((W, H))
    os.remove(tmp)
    return im


def parse(line):
    """'¿PESAS *LIGERAS*?' -> [('¿PESAS ', False), ('LIGERAS', True), ('?', False)]"""
    parts, hl, buf = [], False, ''
    for ch in line:
        if ch == '*':
            if buf:
                parts.append((buf, hl))
            buf, hl = '', not hl
        else:
            buf += ch
    if buf:
        parts.append((buf, hl))
    return parts


def fit(lines, maxw, start=150, minsize=90):
    size = start
    while size > minsize:
        f = font(ANTON, size)
        if all(f.getlength(''.join(t for t, _ in parse(l))) <= maxw for l in lines):
            return f, size
        size -= 6
    return font(ANTON, minsize), minsize


def make_cover(video, text, rel_t=0.42, estilo='video'):
    d = duration(video)
    bg = grab(video, max(0.5, d * rel_t))
    if estilo == 'video':
        return make_cover_video(video, text, bg, d, rel_t)
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(16))).enhance(0.5)
    bg = ImageEnhance.Contrast(bg).enhance(1.2)
    # tinte cálido diagonal (coral -> ámbar) para que la portada no se vea azul
    tint = Image.new('RGB', (W, H))
    td = ImageDraw.Draw(tint)
    for y in range(H):
        k = y / H
        td.line([(0, y), (W, y)], fill=(int(120 + 100 * k), int(40 + 50 * (1 - k)), int(70 - 30 * k)))
    bg = Image.blend(bg, tint, 0.38)
    img = bg.convert('RGBA')

    # Viñeta y degradados cálidos para separar del azul
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for y in range(H):
        a = 0
        if y < 520:
            a = int(150 * (1 - y / 520))
        elif y > H - 620:
            a = int(170 * ((y - (H - 620)) / 620))
        od.line([(0, y), (W, y)], fill=(8, 6, 18, a))
    img = Image.alpha_composite(img, ov)
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-260, 980, 760, 2100], fill=(255, 120, 60, 110))
    gd.ellipse([520, -200, 1400, 760], fill=(255, 194, 75, 90))
    gd.ellipse([140, 560, 940, 1360], fill=(62, 240, 255, 40))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(160)))

    # Visual nítido del video (zona central del holograma) con borde difuminado
    frame = grab(video, max(0.5, d * rel_t))
    crop = frame.crop((140, 520, 940, 1320)).resize((700, 700))
    crop = ImageEnhance.Brightness(crop).enhance(1.35)
    crop = ImageEnhance.Color(crop).enhance(1.3)
    mask = Image.new('L', (700, 700), 0)
    ImageDraw.Draw(mask).ellipse([40, 40, 660, 660], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(60))
    img.paste(crop, (190, 400), mask)

    dr = ImageDraw.Draw(img)
    # Insignia superior
    f_b = font(INTER, 34)
    badge = 'LAB · CIENCIA DEL ENTRENAMIENTO'
    bw = f_b.getlength(badge) + 64
    x0 = (W - bw) / 2
    dr.rounded_rectangle([x0, 280, x0 + bw, 350], radius=35, fill=(10, 14, 30, 230), outline=CYAN, width=3)
    dr.text((W / 2, 315), badge, font=f_b, fill=CYAN, anchor='mm')

    # Titular
    lines = [l.strip() for l in text.split('|') if l.strip()]
    f, size = fit(lines, W - 120)
    asc, desc = f.getmetrics()
    lh = asc + int(desc * 0.25)
    total = lh * len(lines)
    y = min(1130, 1545 - total)
    for l in lines:
        parts = parse(l)
        tw = sum(f.getlength(t) for t, _ in parts)
        x = (W - tw) / 2
        for t, hl in parts:
            col = AMBER if hl else WHITE
            # sombra dura + contorno para que se lea sobre cualquier fondo
            dr.text((x + 6, y + 8), t, font=f, fill=(0, 0, 0, 200))
            dr.text((x, y), t, font=f, fill=col, stroke_width=5, stroke_fill=(10, 8, 20))
            x += f.getlength(t)
        y += lh

    # Barra inferior
    f_s = font(INTER, 40)
    tag = 'LO QUE DICE LA CIENCIA  ▶'
    tw = f_s.getlength(tag) + 70
    x0 = (W - tw) / 2
    yb = y + 22
    dr.rounded_rectangle([x0, yb, x0 + tw, yb + 84], radius=42, fill=CORAL)
    dr.text((W / 2, yb + 42), tag, font=f_s, fill=WHITE, anchor='mm')
    return img.convert('RGB')


def make_cover_video(video, text, frame, d, rel_t):
    """Portada con la MISMA estética del video: fondo azul noche con grilla, holograma nítido,
    neón cian/verde/ámbar. Contenido centrado en la zona 4:5 / 3:4 que muestra Instagram."""
    base = grab(video, 0.35)  # fondo + grilla del propio video (después de una portada previa)
    img = ImageEnhance.Brightness(base.filter(ImageFilter.GaussianBlur(10))).enhance(0.9).convert('RGBA')
    # holograma nítido, más grande y centrado
    crop = frame.crop((90, 470, 990, 1370)).resize((820, 820))
    crop = ImageEnhance.Brightness(crop).enhance(1.25)
    crop = ImageEnhance.Color(crop).enhance(1.2)
    mask = Image.new('L', (820, 820), 0)
    ImageDraw.Draw(mask).rounded_rectangle([30, 30, 790, 790], radius=120, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(45))
    img.paste(crop, (130, 330), mask)
    # franja oscura suave bajo el titular para legibilidad
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for y in range(1020, 1720):
        a = int(170 * min(1, (y - 1020) / 160))
        od.line([(0, y), (W, y)], fill=(4, 8, 24, a))
    img = Image.alpha_composite(img, ov)
    dr = ImageDraw.Draw(img)
    f_b = font(INTER, 34)
    badge = 'LAB · CIENCIA DEL ENTRENAMIENTO'
    bw = f_b.getlength(badge) + 64; x0 = (W - bw) / 2
    dr.rounded_rectangle([x0, 270, x0 + bw, 340], radius=35, fill=(6, 12, 30, 235), outline=CYAN, width=3)
    dr.text((W / 2, 305), badge, font=f_b, fill=CYAN, anchor='mm')
    lines = [l.strip() for l in text.split('|') if l.strip()]
    f, size = fit(lines, W - 120)
    asc, desc = f.getmetrics(); lh = asc + int(desc * 0.25); total = lh * len(lines)
    y = min(1120, 1545 - total)
    # brillo neón detrás del texto
    gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
    yy = y
    for l in lines:
        parts = parse(l); tw = sum(f.getlength(t) for t, _ in parts); x = (W - tw) / 2
        for t, hl in parts:
            gd.text((x, yy), t, font=f, fill=(AMBER if hl else CYAN) + (200,))
            x += f.getlength(t)
        yy += lh
    img = Image.alpha_composite(img, gl.filter(ImageFilter.GaussianBlur(18)))
    dr = ImageDraw.Draw(img)
    for l in lines:
        parts = parse(l); tw = sum(f.getlength(t) for t, _ in parts); x = (W - tw) / 2
        for t, hl in parts:
            dr.text((x, y), t, font=f, fill=AMBER if hl else WHITE, stroke_width=4, stroke_fill=(4, 8, 24))
            x += f.getlength(t)
        y += lh
    f_s = font(INTER, 38)
    tag = 'LO QUE DICE LA CIENCIA  ▶'
    tw = f_s.getlength(tag) + 70; x0 = (W - tw) / 2; yb = y + 22
    dr.rounded_rectangle([x0, yb, x0 + tw, yb + 80], radius=40, fill=(6, 12, 30, 235), outline=(88, 242, 154), width=3)
    dr.text((W / 2, yb + 40), tag, font=f_s, fill=(88, 242, 154), anchor='mm')
    return img.convert('RGB')


def prepend(video, cover_png, out, secs=0.2):
    fps = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate',
                          '-of', 'csv=p=0', video], capture_output=True, text=True).stdout.strip() or '30/1'
    ar = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=sample_rate',
                         '-of', 'csv=p=0', video], capture_output=True, text=True).stdout.strip() or '44100'
    cmd = ['ffmpeg', '-v', 'error', '-y',
           '-loop', '1', '-framerate', fps, '-t', str(secs), '-i', cover_png,
           '-f', 'lavfi', '-t', str(secs), '-i', f'anullsrc=r={ar}:cl=stereo',
           '-i', video,
           '-filter_complex',
           f'[0:v]scale={W}:{H},format=yuv420p,setsar=1[c];[2:v]scale={W}:{H},format=yuv420p,setsar=1[v];'
           f'[2:a]aformat=sample_rates={ar}:channel_layouts=stereo[a];'
           '[c][1:a][v][a]concat=n=2:v=1:a=1[ov][oa]',
           '-map', '[ov]', '-map', '[oa]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
           '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True)


if __name__ == '__main__':
    args = sys.argv[1:]
    png = None
    rel = 0.42
    estilo = 'video'
    if '--estilo' in args:
        i = args.index('--estilo'); estilo = args[i + 1]; del args[i:i + 2]
    if '--png' in args:
        i = args.index('--png'); png = args[i + 1]; del args[i:i + 2]
    if '--t' in args:
        i = args.index('--t'); rel = float(args[i + 1]); del args[i:i + 2]
    video, text, out = args
    png = png or os.path.splitext(out)[0] + '_portada.png'
    make_cover(video, text, rel, estilo).save(png)
    tmp = out + '.tmp.mp4'
    prepend(video, png, tmp)
    os.replace(tmp, out)
    print(json.dumps({'out': out, 'png': png, 'duration': duration(out)}))
