#!/usr/bin/env python3
"""Gera carrossel de apresentação da Propaganda Oca (6 slides 1080x1080)."""

from PIL import Image, ImageDraw, ImageFont
import os

# Paths
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "carrossel")
FONTS = "/Users/jessicagregorio/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/4de4bdeb-9118-47dd-a7f9-0c3df3ef70fc/41e6c620-7e74-4cf6-9af2-fcd17229ba4c/skills/canvas-design/canvas-fonts"
LOGO = "/Users/jessicagregorio/Oca Propaganda/logo.png"

os.makedirs(OUT, exist_ok=True)

# Cores
YELLOW  = "#FFDE21"
BLACK   = "#0A0A0A"
OFFWHITE = "#F5F5F0"
WHITE   = "#FFFFFF"
GRAY    = "#888888"
DARK    = "#1A1A1A"

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def font(name, size):
    path = os.path.join(FONTS, name)
    return ImageFont.truetype(path, size)

def load_logo(size):
    """Carrega logo original (amarelo/preto sobre transparente) e redimensiona."""
    img = Image.open(LOGO).convert("RGBA")
    img.thumbnail((size, size), Image.LANCZOS)
    return img

def paste_logo(canvas, size, x, y, invert=False):
    """Cola logo na posição. invert=True faz logo branca (para fundo escuro)."""
    logo = load_logo(size)
    if invert:
        r, g, b, a = logo.split()
        rgb = Image.merge("RGB", (r, g, b))
        # Inverte apenas os pixels não-transparentes deixando amarelo → amarelo (mantém)
        # Na verdade, a logo tem fundo transparente com pixels amarelos e pretos.
        # Para fundo escuro, queremos deixar o logo com cores originais (amarelo+preto)
        # sem inversão — mas o preto some no fundo preto.
        # Solução: recolorir pixels escuros como branco, pixels amarelos permanecem.
        pixels = logo.load()
        w, h = logo.size
        for py in range(h):
            for px in range(w):
                pr, pg, pb, pa = pixels[px, py]
                if pa > 10:  # pixel visível
                    brightness = (pr + pg + pb) / 3
                    if brightness < 100:  # pixel escuro → branco
                        pixels[px, py] = (255, 255, 255, pa)
    canvas.paste(logo, (x, y), logo)

def draw_logo_small(canvas, invert=False, corner="topright"):
    """Logo pequena no canto (60px)."""
    size = 60
    logo = load_logo(size)
    if invert:
        pixels = logo.load()
        w, h = logo.size
        for py in range(h):
            for px in range(w):
                pr, pg, pb, pa = pixels[px, py]
                if pa > 10:
                    brightness = (pr + pg + pb) / 3
                    if brightness < 100:
                        pixels[px, py] = (255, 255, 255, pa)
    if corner == "topright":
        x = 1080 - size - 40
        y = 40
    elif corner == "bottomright":
        x = 1080 - size - 40
        y = 1080 - size - 40
    elif corner == "bottomleft":
        x = 40
        y = 1080 - size - 40
    canvas.paste(logo, (x, y), logo)

def draw_counter(draw, num, total, color=GRAY):
    """Número do slide no canto inferior direito."""
    f = font("DMMono-Regular.ttf", 22)
    text = f"{num:02d} / {total:02d}"
    draw.text((1080 - 40, 1080 - 40), text, font=f, fill=color, anchor="rb")

def draw_rule(draw, y, color=BLACK, width=1080, margin=60):
    draw.line([(margin, y), (width - margin, y)], fill=color, width=1)

# ─── SLIDE 01: CAPA ───────────────────────────────────────────────────────────
def slide01():
    img = Image.new("RGB", (1080, 1080), hex2rgb(BLACK))
    d = ImageDraw.Draw(img)

    # Logo no topo esquerdo (com pixels escuros → branco)
    paste_logo(img, 90, 40, 40, invert=True)

    # Título principal
    f_title = font("BigShoulders-Bold.ttf", 160)
    d.text((60, 300), "PROPAGANDA", font=f_title, fill=WHITE)
    d.text((60, 460), "OCA", font=f_title, fill=hex2rgb(YELLOW))

    # Barra amarela inferior
    d.rectangle([(0, 780), (1080, 1080)], fill=hex2rgb(YELLOW))

    # Tagline na barra
    f_tag = font("BigShoulders-Bold.ttf", 56)
    d.text((60, 820), "MARKETING QUE", font=f_tag, fill=hex2rgb(BLACK))
    d.text((60, 882), "FUNCIONA DE VERDADE.", font=f_tag, fill=hex2rgb(BLACK))

    # Rodapé da barra
    f_mono = font("DMMono-Regular.ttf", 20)
    d.text((60, 1040), "AGÊNCIA DE MARKETING  ·  BOM JESUS DOS PERDÕES, SP", font=f_mono, fill=hex2rgb(DARK))
    draw_counter(d, 1, 6, color=DARK)

    img.save(os.path.join(OUT, "01_capa.png"))
    print("✓ 01_capa.png")

# ─── SLIDE 02: QUEM SOMOS ─────────────────────────────────────────────────────
def slide02():
    img = Image.new("RGB", (1080, 1080), hex2rgb(OFFWHITE))
    d = ImageDraw.Draw(img)

    # Header negro
    d.rectangle([(0, 0), (1080, 160)], fill=hex2rgb(BLACK))
    f_head = font("BigShoulders-Bold.ttf", 90)
    d.text((60, 30), "QUEM SOMOS", font=f_head, fill=WHITE)

    # Logo pequena no header
    draw_logo_small(img, invert=True, corner="topright")

    # 4 seções
    sections = [
        ("01 / CONCEITO",    "A Oca representa a base, o acolhimento\ne a construção sólida."),
        ("02 / REGIONALISMO", "Feito no interior. Para o interior.\nFalamos a língua do empresário local."),
        ("03 / PERFORMANCE",  "Criatividade não é arte, é negócio.\nTodo trabalho é guiado por resultados reais."),
        ("04 / PARCERIA",     "Transparência absoluta. Sem enrolação.\nSem template pronto."),
    ]

    f_label = font("DMMono-Regular.ttf", 22)
    f_body  = font("InstrumentSans-Regular.ttf", 30)

    y = 185
    for label, body in sections:
        # Tag amarela
        bbox = d.textbbox((0, 0), label, font=f_label)
        tw = bbox[2] - bbox[0]
        d.rectangle([(60, y), (60 + tw + 16, y + 30)], fill=hex2rgb(YELLOW))
        d.text((68, y + 3), label, font=f_label, fill=hex2rgb(BLACK))

        # Texto
        d.text((60, y + 42), body, font=f_body, fill=hex2rgb(BLACK))

        # Linha divisória
        y_rule = y + 42 + 80
        draw_rule(d, y_rule, color="#CCCCCC")
        y = y_rule + 18

    draw_counter(d, 2, 6, color=GRAY)

    img.save(os.path.join(OUT, "02_quem_somos.png"))
    print("✓ 02_quem_somos.png")

# ─── SLIDE 03: SERVIÇOS ───────────────────────────────────────────────────────
def slide03():
    img = Image.new("RGB", (1080, 1080), hex2rgb(BLACK))
    d = ImageDraw.Draw(img)

    # Header amarelo
    d.rectangle([(0, 0), (1080, 140)], fill=hex2rgb(YELLOW))
    f_head = font("BigShoulders-Bold.ttf", 90)
    d.text((60, 20), "O QUE A OCA FAZ", font=f_head, fill=hex2rgb(BLACK))

    services = [
        "INBOUND MARKETING",
        "MARKETING DE CONTEÚDO",
        "SEO LOCAL",
        "CUSTOMER MARKETING",
        "GERAÇÃO DE DEMANDA",
        "AUTOMAÇÃO",
    ]

    f_num  = font("DMMono-Regular.ttf", 22)
    f_serv = font("BigShoulders-Bold.ttf", 62)
    f_arr  = font("BigShoulders-Bold.ttf", 50)

    y = 170
    row_h = 138
    for i, svc in enumerate(services):
        num = f"0{i+1}"
        # Linha divisória superior
        draw_rule(d, y, color="#333333")
        # Número
        d.text((60, y + 18), num, font=f_num, fill=hex2rgb(YELLOW))
        # Nome do serviço
        d.text((115, y + 10), svc, font=f_serv, fill=WHITE)
        # Seta
        d.text((1080 - 60, y + 10), "↗", font=f_arr, fill=hex2rgb(YELLOW), anchor="ra")
        y += row_h

    # Última linha
    draw_rule(d, y, color="#333333")

    # Logo pequena embaixo
    draw_logo_small(img, invert=True, corner="bottomright")

    draw_counter(d, 3, 6, color=GRAY)

    img.save(os.path.join(OUT, "03_servicos.png"))
    print("✓ 03_servicos.png")

# ─── SLIDE 04: NÚMEROS ────────────────────────────────────────────────────────
def slide04():
    img = Image.new("RGB", (1080, 1080), hex2rgb(YELLOW))
    d = ImageDraw.Draw(img)

    # Header negro
    d.rectangle([(0, 0), (1080, 140)], fill=hex2rgb(BLACK))
    f_head = font("BigShoulders-Bold.ttf", 90)
    d.text((60, 20), "NOSSOS NÚMEROS", font=f_head, fill=WHITE)

    stats = [
        ("+120", "EMPRESAS ATENDIDAS"),
        ("3×",   "MAIS LEADS EM MÉDIA"),
        ("87%",  "TAXA DE RETENÇÃO"),
        ("5",    "ANOS NO MERCADO REGIONAL"),
    ]

    f_big  = font("BigShoulders-Bold.ttf", 130)
    f_sub  = font("DMMono-Regular.ttf", 22)

    pad = 20
    box_w = (1080 - pad * 3) // 2
    box_h = (1080 - 140 - pad * 3) // 2

    positions = [
        (pad,           140 + pad),
        (pad * 2 + box_w, 140 + pad),
        (pad,           140 + pad * 2 + box_h),
        (pad * 2 + box_w, 140 + pad * 2 + box_h),
    ]

    for (stat, label), (bx, by) in zip(stats, positions):
        d.rectangle([(bx, by), (bx + box_w, by + box_h)], fill=hex2rgb(BLACK))
        # Número grande
        bbox = d.textbbox((0, 0), stat, font=f_big)
        tx = bx + (box_w - (bbox[2] - bbox[0])) // 2
        d.text((tx, by + 40), stat, font=f_big, fill=hex2rgb(YELLOW))
        # Label
        lbbox = d.textbbox((0, 0), label, font=f_sub)
        lx = bx + (box_w - (lbbox[2] - lbbox[0])) // 2
        d.text((lx, by + box_h - 55), label, font=f_sub, fill=hex2rgb(GRAY))

    # Logo pequena
    draw_logo_small(img, invert=False, corner="bottomright")

    draw_counter(d, 4, 6, color=DARK)

    img.save(os.path.join(OUT, "04_numeros.png"))
    print("✓ 04_numeros.png")

# ─── SLIDE 05: TOM DE VOZ ─────────────────────────────────────────────────────
def slide05():
    img = Image.new("RGB", (1080, 1080), hex2rgb(OFFWHITE))
    d = ImageDraw.Draw(img)

    # Header negro
    d.rectangle([(0, 0), (1080, 140)], fill=hex2rgb(BLACK))
    f_head = font("BigShoulders-Bold.ttf", 90)
    d.text((60, 20), "COMO FALAMOS", font=f_head, fill=WHITE)

    attrs = [
        ("DIRETO",    "Sem rodeios. O empresário não tem\ntempo a perder. Direto ao ponto."),
        ("REGIONAL",  "Falamos como quem conhece a\ncidade. Autenticidade do interior."),
        ("CONCRETO",  "Sempre com números reais. Nunca\npromessas vagas."),
        ("PARCEIRO",  "Tom de quem está do lado.\nSem pedantismo ou jargões."),
    ]

    f_label = font("DMMono-Regular.ttf", 22)
    f_body  = font("InstrumentSans-Regular.ttf", 29)

    pad = 20
    box_w = (1080 - pad * 3) // 2
    # Rodapé vai ter uma faixa preta com regra, então a área útil é menor
    footer_h = 60
    area_h = 1080 - 140 - footer_h
    box_h = (area_h - pad * 3) // 2

    positions = [
        (pad,           140 + pad),
        (pad * 2 + box_w, 140 + pad),
        (pad,           140 + pad * 2 + box_h),
        (pad * 2 + box_w, 140 + pad * 2 + box_h),
    ]

    for (tag, body), (bx, by) in zip(attrs, positions):
        d.rectangle([(bx, by), (bx + box_w, by + box_h)], fill=hex2rgb(DARK))

        # Tag amarela
        bbox_t = d.textbbox((0, 0), tag, font=f_label)
        tw = bbox_t[2] - bbox_t[0]
        d.rectangle([(bx + 20, by + 20), (bx + 20 + tw + 16, by + 20 + 30)], fill=hex2rgb(YELLOW))
        d.text((bx + 28, by + 23), tag, font=f_label, fill=hex2rgb(BLACK))

        # Texto
        d.text((bx + 20, by + 68), body, font=f_body, fill=WHITE)

    # Rodapé negro com regra
    footer_y = 1080 - footer_h
    d.rectangle([(0, footer_y), (1080, 1080)], fill=hex2rgb(BLACK))
    f_rule = font("DMMono-Regular.ttf", 18)
    d.text((60, footer_y + 18),
           "REGRA: SE NÃO DIRIA OLHANDO NOS OLHOS, NÃO COLOCA NO CONTEÚDO.",
           font=f_rule, fill=hex2rgb(YELLOW))

    draw_counter(d, 5, 6, color=GRAY)

    img.save(os.path.join(OUT, "05_tom_de_voz.png"))
    print("✓ 05_tom_de_voz.png")

# ─── SLIDE 06: CTA ────────────────────────────────────────────────────────────
def slide06():
    img = Image.new("RGB", (1080, 1080), hex2rgb(YELLOW))
    d = ImageDraw.Draw(img)

    # Texto principal
    f_big = font("BigShoulders-Bold.ttf", 145)
    lines = ["PRONTOS", "PARA O", "PRÓXIMO", "NÍVEL?"]
    y = 60
    for line in lines:
        d.text((60, y), line, font=f_big, fill=hex2rgb(BLACK))
        y += 168

    # Faixa preta no rodapé
    footer_y = 820
    d.rectangle([(0, footer_y), (1080, 1080)], fill=hex2rgb(BLACK))

    # 3 colunas de contato
    contacts = [
        ("E-MAIL", "oi@propagandaoca.com.br"),
        ("WEB",    "propagandaoca.com.br"),
        ("LOCAL",  "Bom Jesus dos Perdões, SP"),
    ]

    f_label = font("DMMono-Regular.ttf", 18)
    f_val   = font("InstrumentSans-Regular.ttf", 24)
    col_w = 1080 // 3

    for i, (label, val) in enumerate(contacts):
        cx = i * col_w + 30
        # Divisor vertical
        if i > 0:
            d.line([(i * col_w, footer_y + 20), (i * col_w, 1080 - 20)], fill="#333333", width=1)

        # Tag
        bbox_t = d.textbbox((0, 0), label, font=f_label)
        tw = bbox_t[2] - bbox_t[0]
        d.rectangle([(cx, footer_y + 22), (cx + tw + 14, footer_y + 22 + 26)], fill=hex2rgb(YELLOW))
        d.text((cx + 7, footer_y + 25), label, font=f_label, fill=hex2rgb(BLACK))

        # Valor
        d.text((cx, footer_y + 62), val, font=f_val, fill=WHITE)

    draw_counter(d, 6, 6, color=GRAY)

    img.save(os.path.join(OUT, "06_cta.png"))
    print("✓ 06_cta.png")

# ─── EXECUTA ─────────────────────────────────────────────────────────────────
slide01()
slide02()
slide03()
slide04()
slide05()
slide06()
print("\nCarrossel gerado em:", OUT)
