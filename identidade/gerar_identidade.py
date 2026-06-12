from PIL import Image, ImageDraw, ImageFont
import os, math

FONTS = "/Users/jessicagregorio/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/4de4bdeb-9118-47dd-a7f9-0c3df3ef70fc/41e6c620-7e74-4cf6-9af2-fcd17229ba4c/skills/canvas-design/canvas-fonts"
OUT  = "/Users/jessicagregorio/Oca Propaganda/identidade"
os.makedirs(OUT, exist_ok=True)

Y  = (255, 222, 33)     # amarelo
BK = (10,  10,  10)     # preto
OW = (245, 245, 240)    # off-white
MG = (68,  68,  68)     # mid-gray
LG = (160, 160, 160)    # light-gray
WH = (255, 255, 255)

def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

def text_w(draw, txt, f):
    bb = draw.textbbox((0,0), txt, font=f)
    return bb[2] - bb[0]

def text_h(draw, txt, f):
    bb = draw.textbbox((0,0), txt, font=f)
    return bb[3] - bb[1]

# ─────────────────────────────────────────────────────────────
# 01  LOGOTIPO PRINCIPAL (3600×2400 px — landscape)
# ─────────────────────────────────────────────────────────────
def make_logo():
    W, H = 3600, 2400
    img = Image.new("RGB", (W, H), BK)
    d   = ImageDraw.Draw(img)

    # barra amarela esquerda
    d.rectangle([0, 0, 80, H], fill=Y)

    # "PROPAGANDA" — BigShoulders Bold
    f_big = font("BigShoulders-Bold.ttf", 320)
    f_med = font("BigShoulders-Bold.ttf", 420)
    f_mono = font("DMMono-Regular.ttf", 38)
    f_body = font("InstrumentSans-Regular.ttf", 52)

    tx = 160
    ty = 520
    d.text((tx, ty), "PROPAGANDA", font=f_big, fill=Y)

    # linha horizontal amarela
    lx1, ly = tx, ty + 345
    lx2 = W - 160
    d.rectangle([lx1, ly, lx2, ly + 6], fill=Y)

    # "OCA" com espaçamento manual
    oca_f = font("BigShoulders-Bold.ttf", 420)
    chars = list("OCA")
    spacing = 80
    cx = tx
    for ch in chars:
        d.text((cx, ly + 30), ch, font=oca_f, fill=Y)
        cx += text_w(d, ch, oca_f) + spacing

    # tagline
    d.text((tx, ly + 510), "Marketing que funciona de verdade.", font=f_body, fill=LG)

    # bloco inferior — dados
    d.rectangle([0, H - 180, W, H], fill=Y)
    f_foot = font("DMMono-Regular.ttf", 34)
    items = ["propagandaoca.com.br", "oi@propagandaoca.com.br", "(11) 9 5912-5935", "Bom Jesus dos Perdões · SP"]
    item_spacing = (W - 320) // (len(items) - 1)
    for i, item in enumerate(items):
        ix = 160 + i * item_spacing
        iw = text_w(d, item, f_foot)
        d.text((ix - iw//2, H - 115), item, font=f_foot, fill=BK)

    # marca d'agua geométrica — círculo vazio canto direito
    d.ellipse([W-520, 200, W-80, 640], outline=Y, width=3)
    d.ellipse([W-460, 260, W-140, 580], outline=(40,40,40), width=1)

    # label BRANDBOOK
    f_label = font("DMMono-Regular.ttf", 30)
    d.text((tx, ly + 460), "// IDENTIDADE VISUAL  2025", font=f_label, fill=MG)

    img.save(os.path.join(OUT, "01_logotipo.png"), dpi=(300,300))
    print("01 done")

# ─────────────────────────────────────────────────────────────
# 02  PALETA DE CORES (3600×2400)
# ─────────────────────────────────────────────────────────────
def make_paleta():
    W, H = 3600, 2400
    img = Image.new("RGB", (W, H), OW)
    d   = ImageDraw.Draw(img)

    f_title  = font("BigShoulders-Bold.ttf", 100)
    f_name   = font("BigShoulders-Bold.ttf", 72)
    f_hex    = font("DMMono-Regular.ttf", 46)
    f_small  = font("DMMono-Regular.ttf", 32)
    f_label  = font("InstrumentSans-Regular.ttf", 36)

    # header strip
    d.rectangle([0, 0, W, 220], fill=BK)
    d.text((120, 58), "IDENTIDADE VISUAL", font=f_title, fill=Y)
    d.text((W - 500, 90), "02 / CORES", font=f_small, fill=MG)

    cores = [
        (Y,  "#FFDE21", "255 · 222 · 33",  "0 · 13 · 87 · 0",  "AMARELO",      "Cor de identidade", BK),
        (BK, "#0A0A0A", "10 · 10 · 10",    "0 · 0 · 0 · 96",   "PRETO",        "Fundos e texto",    Y),
        (OW, "#F5F5F0", "245 · 245 · 240",  "0 · 0 · 2 · 4",    "OFF-WHITE",    "Fundos secundários",BK),
        ((26,26,26), "#1A1A1A","26 · 26 · 26","0 · 0 · 0 · 90",  "CINZA ESCURO", "Texto secundário",  LG),
    ]

    pad  = 100
    gap  = 60
    sw   = (W - 2*pad - 3*gap) // 4
    sh   = 900
    sy   = 320

    for i, (col, hex_, rgb, cmyk, name, uso, tx_col) in enumerate(cores):
        x = pad + i*(sw+gap)
        d.rectangle([x, sy, x+sw, sy+sh], fill=col)
        if col == OW:
            d.rectangle([x, sy, x+sw, sy+sh], outline=LG, width=2)

        # nome dentro do swatch
        d.text((x+40, sy+50), name, font=f_name, fill=tx_col)
        d.text((x+40, sy+140), hex_, font=f_hex, fill=tx_col)

        # dados abaixo
        by = sy + sh + 50
        d.text((x, by),      "RGB",  font=f_small, fill=MG)
        d.text((x, by+48),   rgb,    font=f_small, fill=BK)
        d.text((x, by+120),  "CMYK", font=f_small, fill=MG)
        d.text((x, by+168),  cmyk,   font=f_small, fill=BK)
        d.text((x, by+260),  uso,    font=f_label, fill=MG)

    # linha decorativa
    d.rectangle([pad, sy+sh-4, W-pad, sy+sh], fill=Y)

    # rodapé
    f_foot = font("DMMono-Regular.ttf", 28)
    d.text((120, H-70), "PROPAGANDA OCA  —  BRANDBOOK 2025", font=f_foot, fill=LG)

    img.save(os.path.join(OUT, "02_paleta.png"), dpi=(300,300))
    print("02 done")

# ─────────────────────────────────────────────────────────────
# 03  TIPOGRAFIA (3600×2400)
# ─────────────────────────────────────────────────────────────
def make_tipo():
    W, H = 3600, 2400
    img = Image.new("RGB", (W, H), BK)
    d   = ImageDraw.Draw(img)

    f_hd    = font("BigShoulders-Bold.ttf", 100)
    f_small = font("DMMono-Regular.ttf", 32)
    f_foot  = font("DMMono-Regular.ttf", 28)

    # header
    d.rectangle([0, 0, W, 220], fill=Y)
    d.text((120, 58), "TIPOGRAFIA", font=f_hd, fill=BK)
    d.text((W-400, 90), "03 / TYPE", font=f_small, fill=BK)

    # 3 blocos de fonte
    entries = [
        ("BigShoulders-Bold.ttf",    "TÍTULOS E DISPLAY",
         "BigShoulders", 220,
         "Força, impacto, presença. Para quando a marca precisa tomar espaço.",
         Y, BK),
        ("InstrumentSans-Regular.ttf","CORPO E SUBTÍTULOS",
         "Instrument Sans", 100,
         "Clareza, fluidez, leitura. Para quando o conteúdo precisa respirar.",
         OW, MG),
        ("DMMono-Regular.ttf",        "DADOS E DESTAQUES",
         "DM Mono", 80,
         "Precisão, técnica, referência. Para números, códigos e labels.",
         LG, MG),
    ]

    bh   = 600
    bpad = 100
    gap  = 2
    bw   = (W - 2*bpad - 2*gap) // 3
    by   = 280

    for i, (fname, role, sample_txt, sample_sz, desc, bg_c, txt_c) in enumerate(entries):
        bx = bpad + i*(bw+gap)
        d.rectangle([bx, by, bx+bw, by+bh], fill=(20,20,20) if bg_c == OW else BK)

        # role label
        f_role = font("DMMono-Regular.ttf", 30)
        d.text((bx+40, by+40), role, font=f_role, fill=Y)

        # amostra grande
        f_sample = font(fname, sample_sz)
        tw = text_w(d, sample_txt, f_sample)
        # se não couber, reduzir
        while tw > bw - 80 and sample_sz > 40:
            sample_sz -= 10
            f_sample = font(fname, sample_sz)
            tw = text_w(d, sample_txt, f_sample)
        d.text((bx+40, by+110), sample_txt, font=f_sample, fill=bg_c)

        # descrição
        f_desc = font("InstrumentSans-Regular.ttf", 36)
        d.text((bx+40, by+bh-120), desc, font=f_desc, fill=MG)

    # alphabet strip abaixo
    strip_y = by + bh + 80
    d.rectangle([0, strip_y, W, strip_y+200], fill=Y)
    f_alpha = font("BigShoulders-Bold.ttf", 160)
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ax = 60
    for ch in alpha:
        d.text((ax, strip_y+20), ch, font=f_alpha, fill=BK)
        ax += text_w(d, ch, f_alpha) + 8
        if ax > W - 60:
            break

    # numeral strip
    num_y = strip_y + 220
    d.rectangle([0, num_y, W, num_y+200], fill=(20,20,20))
    f_num = font("DMMono-Regular.ttf", 140)
    nums = "0123456789 .,:;%×→"
    nx = 60
    for ch in nums:
        cw2 = text_w(d, ch, f_num)
        d.text((nx, num_y+30), ch, font=f_num, fill=Y)
        nx += cw2 + 18
        if nx > W - 60:
            break

    # nota de rodapé
    d.text((120, H-70), "PROPAGANDA OCA  —  BRANDBOOK 2025", font=f_foot, fill=MG)

    img.save(os.path.join(OUT, "03_tipografia.png"), dpi=(300,300))
    print("03 done")

# ─────────────────────────────────────────────────────────────
# 04  MANIFESTO VISUAL (3600×2400) — página de arte principal
# ─────────────────────────────────────────────────────────────
def make_manifesto():
    W, H = 3600, 2400
    img = Image.new("RGB", (W, H), BK)
    d   = ImageDraw.Draw(img)

    # ── grid de linhas finas verticais decorativas ──
    for x in range(160, W, 220):
        opacity_col = (25, 25, 25)
        d.line([(x, 0), (x, H)], fill=opacity_col, width=1)

    # bloco amarelo massivo — canto superior direito
    d.rectangle([W//2 + 200, 0, W, H//2 - 100], fill=Y)

    # círculo geométrico no bloco amarelo
    cx, cy, r = W//2 + 200 + (W//2 - 200)//2, (H//2-100)//2, 280
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=BK)
    d.ellipse([cx-r+40, cy-r+40, cx+r-40, cy+r-40], outline=Y, width=4)

    # "PROPAGANDA" vertical — left column, massive
    f_vert = font("BigShoulders-Bold.ttf", 260)
    chars_p = list("PROPAGANDA")
    vy = 80
    for ch in chars_p:
        d.text((40, vy), ch, font=f_vert, fill=Y)
        vy += text_h(d, ch, f_vert) + 10

    # "OCA" horizontal — enorme no meio
    f_oca = font("BigShoulders-Bold.ttf", 520)
    oca_x, oca_y = 360, H//2 - 80
    d.text((oca_x, oca_y), "OCA", font=f_oca, fill=WH)

    # linha de corte amarela
    d.rectangle([360, oca_y - 12, W//2 + 160, oca_y - 6], fill=Y)

    # bloco de texto manifesto — canto inferior direito
    manifesto_lines = [
        "Marketing que funciona de verdade.",
        "Feito no interior. Para o interior.",
        "Sem jargão. Sem template. Sem enrolação.",
    ]
    f_mani = font("InstrumentSans-Regular.ttf", 56)
    f_mani_b = font("InstrumentSans-Bold.ttf", 56)
    mx, my = W//2 + 230, H//2 + 80
    for i, line in enumerate(manifesto_lines):
        d.text((mx, my + i*90), line,
               font=f_mani_b if i == 0 else f_mani,
               fill=BK if i == 0 else (30, 30, 30))

    # métricas — bloco inferior esquerdo
    metrics = [("+120", "EMPRESAS"), ("3×", "MAIS LEADS"), ("87%", "RETENÇÃO"), ("5", "ANOS")]
    f_mnum = font("BigShoulders-Bold.ttf", 180)
    f_mlbl = font("DMMono-Regular.ttf", 36)
    mpad   = 360
    mw     = (W//2 - mpad - 60) // 4
    base_y = H - 420
    d.rectangle([0, base_y - 40, W//2 + 100, H], fill=(16,16,16))
    for i, (num, lbl) in enumerate(metrics):
        mx2 = mpad + i*mw + (i * 20)
        d.text((mx2, base_y), num, font=f_mnum, fill=Y)
        d.text((mx2, base_y + 200), lbl, font=f_mlbl, fill=LG)

    # linha inferior amarela
    d.rectangle([0, H-8, W, H], fill=Y)

    # label bottom-right
    f_foot = font("DMMono-Regular.ttf", 28)
    d.text((W-700, H-60), "PROPAGANDA OCA  —  2025", font=f_foot, fill=MG)

    img.save(os.path.join(OUT, "04_manifesto.png"), dpi=(300,300))
    print("04 done")

# ─────────────────────────────────────────────────────────────
# 05  SISTEMA DE GRADE / APLICAÇÕES (3600×2400)
# ─────────────────────────────────────────────────────────────
def make_sistema():
    W, H = 3600, 2400
    img = Image.new("RGB", (W, H), OW)
    d   = ImageDraw.Draw(img)

    f_hd    = font("BigShoulders-Bold.ttf", 100)
    f_small = font("DMMono-Regular.ttf", 32)
    f_body  = font("InstrumentSans-Regular.ttf", 42)
    f_foot  = font("DMMono-Regular.ttf", 28)

    # header
    d.rectangle([0, 0, W, 220], fill=BK)
    d.text((120, 58), "SISTEMA DE APLICAÇÃO", font=f_hd, fill=Y)
    d.text((W-500, 90), "05 / GRID", font=f_small, fill=MG)

    # ── CARTÃO DE VISITA mockup ──
    cv_x, cv_y = 120, 300
    cv_w, cv_h = 1400, 860

    # frente — preto
    d.rectangle([cv_x, cv_y, cv_x+cv_w, cv_y+cv_h], fill=BK)
    d.rectangle([cv_x, cv_y, cv_x+50, cv_y+cv_h], fill=Y)
    f_card = font("BigShoulders-Bold.ttf", 80)
    d.text((cv_x+80, cv_y+80), "PROPAGANDA", font=f_card, fill=Y)
    f_card2 = font("BigShoulders-Bold.ttf", 100)
    d.text((cv_x+80, cv_y+165), "O  C  A",    font=f_card2, fill=Y)
    f_cn = font("InstrumentSans-Bold.ttf", 44)
    f_ct = font("InstrumentSans-Regular.ttf", 36)
    d.text((cv_x+80, cv_y+cv_h-280), "Jéssica Gregório", font=f_cn, fill=WH)
    d.text((cv_x+80, cv_y+cv_h-230), "Diretora · Propaganda Oca", font=f_ct, fill=LG)
    d.line([(cv_x+80, cv_y+cv_h-180), (cv_x+cv_w-80, cv_y+cv_h-180)], fill=(40,40,40), width=1)
    d.text((cv_x+80, cv_y+cv_h-140), "(11) 9 5912-5935", font=f_ct, fill=LG)
    d.text((cv_x+80, cv_y+cv_h-90),  "oi@propagandaoca.com.br", font=f_ct, fill=LG)

    # verso — amarelo
    vx = cv_x + cv_w + 60
    d.rectangle([vx, cv_y, vx+cv_w, cv_y+cv_h], fill=Y)
    f_cv = font("BigShoulders-Bold.ttf", 110)
    tw = text_w(d, "PROPAGANDA", f_cv)
    d.text((vx + (cv_w - tw)//2, cv_y+240), "PROPAGANDA", font=f_cv, fill=BK)
    tw2 = text_w(d, "O  C  A", f_cv)
    d.text((vx + (cv_w - tw2)//2, cv_y+355), "O  C  A", font=f_cv, fill=BK)

    # label
    f_lbl = font("DMMono-Regular.ttf", 30)
    d.text((cv_x, cv_y + cv_h + 30), "CARTÃO DE VISITA — FRENTE",  font=f_lbl, fill=MG)
    d.text((vx,   cv_y + cv_h + 30), "CARTÃO DE VISITA — VERSO",   font=f_lbl, fill=MG)

    # ── POST INSTAGRAM mockup ──
    ig_x = 120
    ig_y = cv_y + cv_h + 120
    ig_w = ig_h = 880

    d.rectangle([ig_x, ig_y, ig_x+ig_w, ig_y+ig_h], fill=BK)
    f_ig_big = font("BigShoulders-Bold.ttf", 200)
    f_ig_sm  = font("DMMono-Regular.ttf", 36)
    d.text((ig_x+60, ig_y+80),  "3×",        font=f_ig_big, fill=Y)
    d.text((ig_x+60, ig_y+320), "MAIS",      font=f_ig_big, fill=WH)
    d.text((ig_x+60, ig_y+540), "LEADS",     font=f_ig_big, fill=WH)
    d.rectangle([ig_x, ig_y+ig_h-120, ig_x+ig_w, ig_y+ig_h], fill=Y)
    d.text((ig_x+40, ig_y+ig_h-90), "@propaganda.oca", font=f_ig_sm, fill=BK)
    d.text((ig_x, ig_y+ig_h+30), "POST INSTAGRAM 1:1", font=f_lbl, fill=MG)

    # ── PAPEL TIMBRADO mockup (A4 proporcional) ──
    pt_x = ig_x + ig_w + 80
    pt_w = 620; pt_h = 878
    pt_y = ig_y
    d.rectangle([pt_x, pt_y, pt_x+pt_w, pt_y+pt_h], fill=WH, outline=LG, width=2)
    d.rectangle([pt_x, pt_y, pt_x+pt_w, pt_y+100], fill=BK)
    d.rectangle([pt_x, pt_y, pt_x+22, pt_y+100], fill=Y)
    f_pt = font("BigShoulders-Bold.ttf", 48)
    d.text((pt_x+32, pt_y+10), "PROPAGANDA", font=f_pt, fill=Y)
    d.text((pt_x+32, pt_y+55), "OCA",        font=f_pt, fill=Y)
    d.rectangle([pt_x, pt_y+pt_h-60, pt_x+pt_w, pt_y+pt_h], fill=Y)
    f_ptf = font("DMMono-Regular.ttf", 20)
    d.text((pt_x+10, pt_y+pt_h-38), "propagandaoca.com.br  ·  (11) 9 5912-5935", font=f_ptf, fill=BK)
    for k in range(8):
        ly = pt_y + 130 + k*78
        d.line([(pt_x+20, ly), (pt_x+pt_w-20, ly)], fill=(220,220,220), width=1)
    d.text((pt_x, pt_y+pt_h+30), "PAPEL TIMBRADO A4", font=f_lbl, fill=MG)

    # ── STORY INSTAGRAM mockup ──
    st_x = pt_x + pt_w + 80
    st_w = 500; st_h = 888
    st_y = ig_y
    d.rectangle([st_x, st_y, st_x+st_w, st_y+st_h], fill=Y)
    f_st = font("BigShoulders-Bold.ttf", 130)
    d.text((st_x+40, st_y+140),  "MARKET-",  font=f_st, fill=BK)
    d.text((st_x+40, st_y+270),  "ING QUE",  font=f_st, fill=BK)
    d.text((st_x+40, st_y+400),  "FUNCIO-",  font=f_st, fill=BK)
    d.text((st_x+40, st_y+530),  "NA.",       font=f_st, fill=BK)
    d.rectangle([st_x, st_y+st_h-100, st_x+st_w, st_y+st_h], fill=BK)
    d.text((st_x+20, st_y+st_h-72), "@propaganda.oca", font=f_ig_sm, fill=Y)
    d.text((st_x, st_y+st_h+30), "STORY 9:16", font=f_lbl, fill=MG)

    # rodapé
    d.text((120, H-70), "PROPAGANDA OCA  —  BRANDBOOK 2025", font=f_foot, fill=LG)

    img.save(os.path.join(OUT, "05_sistema.png"), dpi=(300,300))
    print("05 done")

# ─────────────────────────────────────────────────────────────
# 06  PÁGINA DE ARTE — Tom de Voz visual (3600×2400)
# ─────────────────────────────────────────────────────────────
def make_tom():
    W, H = 3600, 2400
    img = Image.new("RGB", (W, H), OW)
    d   = ImageDraw.Draw(img)

    f_hd    = font("BigShoulders-Bold.ttf", 100)
    f_small = font("DMMono-Regular.ttf", 32)
    f_body  = font("InstrumentSans-Regular.ttf", 48)
    f_bold  = font("InstrumentSans-Bold.ttf", 48)
    f_foot  = font("DMMono-Regular.ttf", 28)
    f_lbl   = font("DMMono-Regular.ttf", 34)

    # header
    d.rectangle([0, 0, W, 220], fill=Y)
    d.text((120, 58), "TOM DE VOZ", font=f_hd, fill=BK)
    d.text((W-400, 90), "04 / VOZ", font=f_small, fill=BK)

    # coluna esquerda — atributos
    attrs = [
        ("DIRETO",    "Vai direto ao ponto. Sem rodeios.\nO empresário não tem tempo a perder."),
        ("REGIONAL",  "Fala como quem conhece a cidade.\nMenciona lugares e contextos locais."),
        ("CONCRETO",  "Sempre com números e resultados reais.\nNunca promessas vagas."),
        ("PARCEIRO",  "Tom de quem está do lado, não de\nquem vende. Sem pedantismo."),
    ]
    f_attr = font("BigShoulders-Bold.ttf", 90)
    ay = 280
    for att, desc in attrs:
        d.rectangle([80, ay, 80+14, ay+90], fill=Y)
        d.text((120, ay), att, font=f_attr, fill=BK)
        for i, line in enumerate(desc.split("\n")):
            d.text((120, ay+100+i*56), line, font=f_body, fill=MG)
        ay += 280

    # divisória vertical
    d.rectangle([W//2 - 4, 240, W//2, H-80], fill=LG)

    # coluna direita — SIM vs NÃO
    d.text((W//2+60, 260), "COMO FALAMOS", font=f_hd, fill=BK)
    d.rectangle([W//2+60, 362, W//2+60+200, 368], fill=Y)

    pares = [
        ("A gente entende o seu mercado.",
         "Potencialize seus KPIs com\nsoluções omnichannel."),
        ("Sem enrolação, sem template.",
         "Desenvolvemos estratégias\ncustomizadas e escaláveis."),
        ("Resultado em 4 meses.\nNúmero real, cliente real.",
         "ROI otimizado a longo prazo\ncom metodologias ágeis."),
        ("Feito para Bom Jesus dos Perdões.",
         "Atendemos empresas de todos\nos portes e segmentos."),
    ]

    py = 420
    col_w = (W - W//2 - 120) // 2 - 30
    sx = W//2 + 60
    nx = sx + col_w + 40

    # headers
    d.rectangle([sx, py, sx+col_w, py+70], fill=(234,243,222))
    d.text((sx+20, py+10), "SIM", font=f_lbl, fill=(39,80,10))
    d.rectangle([nx, py, nx+col_w, py+70], fill=(252,235,235))
    d.text((nx+20, py+10), "NÃO", font=f_lbl, fill=(163,45,45))
    py += 90

    f_sim = font("InstrumentSans-Regular.ttf", 40)
    for sim, nao in pares:
        sh_lines = sim.split("\n"); nh_lines = nao.split("\n")
        box_h = max(len(sh_lines), len(nh_lines)) * 54 + 40

        d.rectangle([sx, py, sx+col_w, py+box_h], fill=(245,252,240))
        for i, l in enumerate(sh_lines):
            d.text((sx+20, py+20+i*54), l, font=f_sim, fill=(39,80,10))

        d.rectangle([nx, py, nx+col_w, py+box_h], fill=(255,245,245))
        for i, l in enumerate(nh_lines):
            d.text((nx+20, py+20+i*54), l, font=f_sim, fill=(163,45,45))

        py += box_h + 16

    # rodapé
    d.text((120, H-70), "PROPAGANDA OCA  —  BRANDBOOK 2025", font=f_foot, fill=LG)

    img.save(os.path.join(OUT, "06_tom_de_voz.png"), dpi=(300,300))
    print("06 done")

# ─────────────────────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────────────────────
make_logo()
make_paleta()
make_tipo()
make_manifesto()
make_sistema()
make_tom()
print("\nIdentidade visual completa em:", OUT)
