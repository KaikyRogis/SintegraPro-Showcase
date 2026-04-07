from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio.v2 as imageio
import numpy as np

ROOT = Path(r'D:\VS Code\SintegraPro-Showcase')
IMG_DIR = ROOT / 'assets' / 'imagens'
GIF_DIR = ROOT / 'assets' / 'gifs'
VIDEO_DIR = ROOT / 'assets' / 'video-demo'
GIF_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

FONT_REG = r'C:\Windows\Fonts\segoeui.ttf'
FONT_SEMI = r'C:\Windows\Fonts\seguisb.ttf'
FONT_BOLD = r'C:\Windows\Fonts\segoeuib.ttf'

SCREENS = {
    'login': IMG_DIR / 'acesso-login.png',
    'dashboard': IMG_DIR / 'dashboard-overview.png',
    'process': IMG_DIR / 'processar-sintegra.png',
    'history': IMG_DIR / 'historico-operacional.png',
    'settings': IMG_DIR / 'configuracao-estacao.png',
    'help': IMG_DIR / 'ajuda-operacional.png',
}

TITLES = {
    'login': ('Acesso seguro', 'Entrada controlada com shell visual alinhado ao instalador.'),
    'dashboard': ('Visão operacional', 'Resumo diário, atalhos rápidos e leitura imediata do ambiente.'),
    'process': ('Processamento guiado', 'Seleção do arquivo, destino e resultado em um fluxo direto.'),
    'history': ('Histórico rastreável', 'Consultas rápidas com filtros e visão consolidada das execuções.'),
    'settings': ('Configuração por papel', 'Servidor e estação com parâmetros claros e status resumido.'),
    'help': ('Ajuda contextual', 'Guia rápido, FAQ e suporte organizados em um único lugar.'),
}


def load_font(path, size):
    return ImageFont.truetype(path, size)


def rounded_rect_mask(size, radius):
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask


def resize_cover(im, size):
    src_w, src_h = im.size
    dst_w, dst_h = size
    src_ratio = src_w / src_h
    dst_ratio = dst_w / dst_h
    if src_ratio > dst_ratio:
        new_h = dst_h
        new_w = int(new_h * src_ratio)
    else:
        new_w = dst_w
        new_h = int(new_w / src_ratio)
    resized = im.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - dst_w) // 2
    top = (new_h - dst_h) // 2
    return resized.crop((left, top, left + dst_w, top + dst_h))


def add_card(canvas, screenshot, box, title, subtitle):
    x, y, w, h = box
    shot = Image.open(screenshot).convert('RGB')
    shot = resize_cover(shot, (w, h))
    card = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    shadow = Image.new('RGBA', (w + 28, h + 28), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((14, 14, w + 14, h + 14), radius=34, fill=(0, 0, 0, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas.alpha_composite(shadow, (x - 14, y - 10))

    mask = rounded_rect_mask((w, h), 30)
    card.paste(shot, (0, 0), mask)
    overlay = Image.new('RGBA', (w, h), (11, 27, 48, 20))
    card.alpha_composite(overlay)
    border = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border)
    border_draw.rounded_rectangle((1, 1, w - 2, h - 2), radius=30, outline=(91, 177, 255, 110), width=2)
    card.alpha_composite(border)
    canvas.alpha_composite(card, (x, y))

    draw = ImageDraw.Draw(canvas)
    font_title = load_font(FONT_BOLD, 24)
    font_sub = load_font(FONT_REG, 16)
    text_y = y + h - 88
    draw.rounded_rectangle((x + 18, text_y - 10, x + w - 18, y + h - 18), radius=22, fill=(8, 21, 38, 176))
    draw.text((x + 34, text_y), title, font=font_title, fill=(238, 245, 255, 255))
    draw.text((x + 34, text_y + 34), subtitle, font=font_sub, fill=(169, 189, 219, 255))


def build_social_preview():
    canvas = Image.new('RGBA', (1280, 640), (7, 21, 37, 255))
    bg = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(bg)
    draw.ellipse((-120, -80, 520, 520), fill=(64, 148, 255, 46))
    draw.ellipse((880, 260, 1320, 760), fill=(54, 205, 171, 40))
    bg = bg.filter(ImageFilter.GaussianBlur(40))
    canvas.alpha_composite(bg)

    draw = ImageDraw.Draw(canvas)
    font_kicker = load_font(FONT_SEMI, 20)
    font_title = load_font(FONT_BOLD, 50)
    font_sub = load_font(FONT_REG, 22)
    draw.text((72, 54), 'SintegraPro · Showcase', font=font_kicker, fill=(100, 197, 255, 255))
    draw.text((72, 88), 'Processamento, correção e validação de arquivos fiscais', font=font_title, fill=(237, 245, 255, 255))
    draw.text((72, 152), 'Interface desktop com shell moderno, operação local e suporte a servidor/estação.', font=font_sub, fill=(181, 199, 224, 255))

    add_card(canvas, SCREENS['dashboard'], (72, 224, 540, 320), *TITLES['dashboard'])
    add_card(canvas, SCREENS['process'], (668, 224, 540, 320), *TITLES['process'])

    canvas.convert('RGB').save(IMG_DIR / 'social-preview.png', quality=95)


def fit_for_video(im, size=(1280, 720)):
    return resize_cover(im.convert('RGB'), size)


def draw_overlay(frame, title, subtitle, progress=None):
    overlay = Image.new('RGBA', frame.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = frame.size
    draw.rounded_rectangle((44, h - 170, w - 44, h - 40), radius=28, fill=(8, 20, 36, 190))
    draw.text((72, h - 150), title, font=load_font(FONT_BOLD, 34), fill=(240, 246, 255, 255))
    draw.text((72, h - 104), subtitle, font=load_font(FONT_REG, 20), fill=(176, 193, 217, 255))
    if progress is not None:
        bar_x1, bar_y1, bar_x2, bar_y2 = 72, h - 62, w - 72, h - 50
        draw.rounded_rectangle((bar_x1, bar_y1, bar_x2, bar_y2), radius=8, fill=(38, 55, 85, 255))
        fill_x = int(bar_x1 + (bar_x2 - bar_x1) * progress)
        draw.rounded_rectangle((bar_x1, bar_y1, fill_x, bar_y2), radius=8, fill=(78, 199, 255, 255))
    return Image.alpha_composite(frame.convert('RGBA'), overlay).convert('RGB')


def hold_frames(im, count, title, subtitle):
    frames = []
    base = fit_for_video(im)
    for i in range(count):
        frames.append(draw_overlay(base, title, subtitle, progress=min(1.0, (i + 1) / max(count, 1))))
    return frames


def crossfade(a, b, steps, title, subtitle):
    frames = []
    a = fit_for_video(a)
    b = fit_for_video(b)
    for i in range(steps):
        alpha = i / max(steps - 1, 1)
        blend = Image.blend(a, b, alpha)
        frames.append(draw_overlay(blend, title, subtitle))
    return frames


def make_sequence(order):
    frames = []
    images = [Image.open(SCREENS[key]).convert('RGB') for key in order]
    for idx, key in enumerate(order):
        title, subtitle = TITLES[key]
        frames.extend(hold_frames(images[idx], 16, title, subtitle))
        if idx < len(order) - 1:
            next_key = order[idx + 1]
            next_title, next_subtitle = TITLES[next_key]
            frames.extend(crossfade(images[idx], images[idx + 1], 10, next_title, next_subtitle))
    return frames


def save_gif(path, frames, fps=8, size=(960, 540)):
    processed = []
    for frame in frames:
        processed.append(np.array(frame.resize(size, Image.LANCZOS)))
    imageio.mimsave(path, processed, format='GIF', duration=1/fps, loop=0)


def save_mp4(path, frames, fps=12):
    with imageio.get_writer(path, fps=fps, codec='libx264', quality=8, macro_block_size=1) as writer:
        for frame in frames:
            writer.append_data(np.array(frame))


build_social_preview()
main_frames = make_sequence(['login', 'dashboard', 'process', 'history'])
support_frames = make_sequence(['settings', 'help', 'dashboard'])
save_gif(GIF_DIR / 'fluxo-principal.gif', main_frames, fps=10)
save_gif(GIF_DIR / 'configuracao-e-ajuda.gif', support_frames, fps=10)
save_mp4(VIDEO_DIR / 'sintegrapro-showcase.mp4', main_frames + support_frames, fps=12)
print('media generated')
