from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio.v2 as imageio
import numpy as np

SHOWCASE_ROOT = Path(r'D:\VS Code\SintegraPro-Showcase')
SOURCE_ROOT = Path(r'D:\VS Code\Imagens para o GitHub')
IMG_DIR = SHOWCASE_ROOT / 'assets' / 'imagens'
GIF_DIR = SHOWCASE_ROOT / 'assets' / 'gifs'
VIDEO_DIR = SHOWCASE_ROOT / 'assets' / 'video-demo'
IMG_DIR.mkdir(parents=True, exist_ok=True)
GIF_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

FONT_REG = r'C:\Windows\Fonts\segoeui.ttf'
FONT_SEMI = r'C:\Windows\Fonts\seguisb.ttf'
FONT_BOLD = r'C:\Windows\Fonts\segoeuib.ttf'

OUTPUTS = {
    'login': {
        'source': SOURCE_ROOT / 'Login.png',
        'output': IMG_DIR / 'acesso-login.png',
        'title': 'Acesso seguro',
        'subtitle': 'Tela de entrada do sistema, com shell visual alinhado ao instalador.',
        'redactions': [
            (1210, 447, 478, 46),
            (1207, 531, 498, 42),
            (1570, 594, 138, 38),
        ],
    },
    'dashboard': {
        'source': SOURCE_ROOT / 'Dashboard.png',
        'output': IMG_DIR / 'dashboard-overview.png',
        'title': 'Visão operacional',
        'subtitle': 'Resumo diário, atalhos rápidos e leitura imediata do ambiente.',
        'redactions': [
            (1707, 76, 150, 42),
        ],
    },
    'process': {
        'source': SOURCE_ROOT / 'Processar SINTEGRA.png',
        'output': IMG_DIR / 'processar-sintegra.png',
        'title': 'Processamento guiado',
        'subtitle': 'Seleção do arquivo, destino e resultado em um fluxo direto.',
        'redactions': [
            (1707, 76, 150, 42),
        ],
    },
    'history': {
        'source': SOURCE_ROOT / 'Histórico.png',
        'output': IMG_DIR / 'historico-operacional.png',
        'title': 'Histórico rastreável',
        'subtitle': 'Consultas rápidas com filtros e visão consolidada das execuções.',
        'redactions': [
            (1707, 76, 150, 42),
        ],
    },
    'settings': {
        'source': SOURCE_ROOT / 'Configurações.png',
        'output': IMG_DIR / 'configuracao-estacao.png',
        'title': 'Configuração por papel',
        'subtitle': 'Estação conectada ao servidor com parâmetros claros e status resumido.',
        'redactions': [
            (1707, 76, 150, 42),
            (324, 365, 206, 44),
        ],
    },
    'help': {
        'source': SOURCE_ROOT / 'Ajuda.png',
        'output': IMG_DIR / 'ajuda-operacional.png',
        'title': 'Ajuda contextual',
        'subtitle': 'Guia rápido, FAQ e suporte reunidos em um único lugar.',
        'redactions': [
            (1707, 76, 150, 42),
        ],
    },
}


def load_font(path, size):
    return ImageFont.truetype(path, size)


def blur_region(im, box, radius=24):
    x, y, w, h = box
    region = im.crop((x, y, x + w, y + h)).filter(ImageFilter.GaussianBlur(radius))
    im.paste(region, (x, y))
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle((x, y, x + w, y + h), radius=12, outline=(102, 196, 255), width=1)


def sanitize_image(source_path, output_path, redactions):
    im = Image.open(source_path).convert('RGB')
    for box in redactions:
        blur_region(im, box)
    im.save(output_path, quality=96)
    return im


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
    shot = resize_cover(screenshot, (w, h))
    card = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    shadow = Image.new('RGBA', (w + 30, h + 30), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((15, 15, w + 15, h + 15), radius=34, fill=(0, 0, 0, 125))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas.alpha_composite(shadow, (x - 15, y - 10))

    mask = rounded_rect_mask((w, h), 30)
    card.paste(shot, (0, 0), mask)
    card.alpha_composite(Image.new('RGBA', (w, h), (9, 24, 44, 24)))
    border = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border)
    border_draw.rounded_rectangle((1, 1, w - 2, h - 2), radius=30, outline=(91, 177, 255, 110), width=2)
    card.alpha_composite(border)
    canvas.alpha_composite(card, (x, y))

    draw = ImageDraw.Draw(canvas)
    font_title = load_font(FONT_BOLD, 24)
    font_sub = load_font(FONT_REG, 16)
    text_y = y + h - 88
    draw.rounded_rectangle((x + 18, text_y - 10, x + w - 18, y + h - 18), radius=22, fill=(8, 21, 38, 180))
    draw.text((x + 34, text_y), title, font=font_title, fill=(238, 245, 255))
    draw.text((x + 34, text_y + 34), subtitle, font=font_sub, fill=(169, 189, 219))


def build_social_preview(images):
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
    draw.text((72, 54), 'SintegraPro · Showcase', font=font_kicker, fill=(100, 197, 255))
    draw.text((72, 88), 'Processamento, correção e validação de arquivos fiscais', font=font_title, fill=(237, 245, 255))
    draw.text((72, 152), 'Capturas reais do produto, sanitizadas para apresentação pública.', font=font_sub, fill=(181, 199, 224))

    add_card(canvas, images['dashboard'], (72, 224, 540, 320), OUTPUTS['dashboard']['title'], OUTPUTS['dashboard']['subtitle'])
    add_card(canvas, images['process'], (668, 224, 540, 320), OUTPUTS['process']['title'], OUTPUTS['process']['subtitle'])
    canvas.convert('RGB').save(IMG_DIR / 'social-preview.png', quality=95)


def fit_for_video(im, size=(1280, 720)):
    return resize_cover(im.convert('RGB'), size)


def draw_overlay(frame, title, subtitle, progress=None):
    overlay = Image.new('RGBA', frame.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = frame.size
    draw.rounded_rectangle((44, h - 170, w - 44, h - 40), radius=28, fill=(8, 20, 36, 192))
    draw.text((72, h - 150), title, font=load_font(FONT_BOLD, 34), fill=(240, 246, 255))
    draw.text((72, h - 104), subtitle, font=load_font(FONT_REG, 20), fill=(176, 193, 217))
    if progress is not None:
        bar_x1, bar_y1, bar_x2, bar_y2 = 72, h - 62, w - 72, h - 50
        draw.rounded_rectangle((bar_x1, bar_y1, bar_x2, bar_y2), radius=8, fill=(38, 55, 85))
        fill_x = int(bar_x1 + (bar_x2 - bar_x1) * progress)
        draw.rounded_rectangle((bar_x1, bar_y1, fill_x, bar_y2), radius=8, fill=(78, 199, 255))
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


def make_sequence(images, order):
    frames = []
    for idx, key in enumerate(order):
        frames.extend(hold_frames(images[key], 16, OUTPUTS[key]['title'], OUTPUTS[key]['subtitle']))
        if idx < len(order) - 1:
            next_key = order[idx + 1]
            frames.extend(crossfade(images[key], images[next_key], 10, OUTPUTS[next_key]['title'], OUTPUTS[next_key]['subtitle']))
    return frames


def save_gif(path, frames, fps=8, size=(960, 540)):
    processed = [np.array(frame.resize(size, Image.LANCZOS)) for frame in frames]
    imageio.mimsave(path, processed, format='GIF', duration=1/fps, loop=0)


def save_mp4(path, frames, fps=12):
    with imageio.get_writer(path, fps=fps, codec='libx264', quality=8, macro_block_size=1) as writer:
        for frame in frames:
            writer.append_data(np.array(frame))


def main():
    sanitized = {}
    for key, meta in OUTPUTS.items():
        sanitized[key] = sanitize_image(meta['source'], meta['output'], meta['redactions'])

    build_social_preview(sanitized)
    main_frames = make_sequence(sanitized, ['login', 'dashboard', 'process', 'history'])
    support_frames = make_sequence(sanitized, ['settings', 'help', 'dashboard'])
    save_gif(GIF_DIR / 'fluxo-principal.gif', main_frames, fps=10)
    save_gif(GIF_DIR / 'configuracao-e-ajuda.gif', support_frames, fps=10)
    save_mp4(VIDEO_DIR / 'sintegrapro-showcase.mp4', main_frames + support_frames, fps=12)
    print('showcase media regenerated from sanitized real screenshots')


if __name__ == '__main__':
    main()
