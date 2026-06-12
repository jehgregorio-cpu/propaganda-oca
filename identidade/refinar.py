from PIL import Image, ImageDraw, ImageFont
import os

FONTS = "/Users/jessicagregorio/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/4de4bdeb-9118-47dd-a7f9-0c3df3ef70fc/41e6c620-7e74-4cf6-9af2-fcd17229ba4c/skills/canvas-design/canvas-fonts"
OUT  = "/Users/jessicagregorio/Oca Propaganda/identidade"

Y  = (255, 222, 33)
BK = (10,  10,  10)
OW = (245, 245, 240)
MG = (80,  80,  80)
LG = (155, 155, 155)
WH = (255, 255, 255)
D20= (20,  20,  20)
D16= (16,  16,  16)

def f(name, size): return ImageFont.truetype(os.path.join(FONTS, name), size)
def tw(d, t, ft):
    bb = d.textbbox((0,0), t, font=ft); return bb[2]-bb[0]
def th(d, t, ft):
    bb = d.textbbox((0,0), t, font=ft); return bb[3]-bb[1]

# ─────────────────────────────────────────────────────────────
# 01 LOGOTIPO  — fix: label e tagline separados, mais espaço
# ─────────────────────────────────────────────────────────────
def make_logo():
    W, H = 3600, 2400
    img = Image.new("RGB", (W, H), BK)
    d   = ImageDraw.Draw(img)

    # barra amarela esquerda
    d.rectangle([0, 0, 72, H], fill=Y)

    f_title = f("CactusClassical-Regular.ttf", 300)
    f_oca   = f("OfertaDoDia-Regular.ttf", 520)
    f_tag   = f("DMMono-Regular.ttf", 34)
    f_body  = f("InstrumentSans-Regular.ttf", 56)
    f_foot  = f("DMMono-Regular.ttf", 34)

    TX = 175
    # "PROPAGANDA" em Cactus Classical Serif
    d.text((TX, 480), "PROPAGANDA", font=f_title, fill=Y)

    # linha amarela
    line_y = 810
    d.rectangle([TX, line_y, W - 175, line_y + 5], fill=Y)

    # "OCA" em Oferta do Dia
    oca_y = line_y + 30
    d.text((TX, oca_y), "OCA", font=f_oca, fill=Y)

    # label técnico — acima da tagline, com espaço claro
    oca_h = f_oca.getbbox("OCA")[3] - f_oca.getbbox("OCA")[1]
    label_y = oca_y + oca_h + 40
    d.text((TX, label_y), "// IDENTIDADE VISUAL  ·  2025", font=f_tag, fill=MG)

    # tagline — abaixo do label, com respiro
    tag_y = label_y + 60
    d.text((TX, tag_y), "Marketing que funciona de verdade.", font=f_body, fill=LG)

    # elemento geométrico — canto superior direito
    cx2, cy2, r = W - 340, 340, 260
    d.ellipse([cx2-r, cy2-r, cx2+r, cy2+r], outline=Y, width=4)
    d.ellipse([cx2-r+52, cy2-r+52, cx2+r-52, cy2+r-52], outline=(35,35,35), width=2)
    # ponto no centro
    d.ellipse([cx2-8, cy2-8, cx2+8, cy2+8], fill=Y)

    # cross marker canto inferior direito
    mx, my = W-340, H-340
    d.line([(mx-40, my), (mx+40, my)], fill=(35,35,35), width=2)
    d.line([(mx, my-40), (mx, my+40)], fill=(35,35,35), width=2)

    # rodapé amarelo
    d.rectangle([0, H-160, W, H], fill=Y)
    items = ["propagandaoca.com.br", "oi@propagandaoca.com.br",
             "(11) 9 5912-5935", "Bom Jesus dos Perdões · SP"]
    slot_w = (W - 2*TX) // len(items)
    for i, item in enumerate(items):
        ix = TX + i * slot_w + slot_w // 2
        iw = tw(d, item, f_foot)
        d.text((ix - iw//2, H - 105), item, font=f_foot, fill=BK)

    img.save(os.path.join(OUT, "01_logotipo.png"), dpi=(300,300))
    print("01 done")

# ─────────────────────────────────────────────────────────────
# 02 PALETA — fix: swatches maiores, preencher espaço vazio
# ─────────────────────────────────────────────────────────────
def make_paleta():
    W, H = 3600, 2400
    img = Image.new("RGB", (W, H), OW)
    d   = ImageDraw.Draw(img)

    f_hd   = f("BigShoulders-Bold.ttf", 100)
    f_name = f("BigShoulders-Bold.ttf", 80)
    f_hex  = f("DMMono-Regular.ttf", 48)
    f_sm   = f("DMMono-Regular.ttf", 34)
    f_uso  = f("InstrumentSans-Regular.ttf", 38)
    f_foot = f("DMMono-Regular.ttf", 28)

    # header
    d.rectangle([0, 0, W, 220], fill=BK)
    d.text((120, 55), "IDENTIDADE VISUAL", font=f_hd, fill=Y)
    d.text((W-460, 90), "02 / CORES", font=f_sm, fill=MG)

    pad = 100; gap = 50
    sw  = (W - 2*pad - 3*gap) // 4
    sh  = 1100
    sy  = 280

    cores = [
        (Y,  "#FFDE21", "255 · 222 · 33",  "0 · 13 · 87 · 0",  "AMARELO",     "Cor de identidade.\nDestaques, CTAs, assinaturas.", BK),
        (BK, "#0A0A0A", "10 · 10 · 10",    "0 · 0 · 0 · 96",   "PRETO",       "Fundos principais.\nTexto sobre fundo claro.",     Y),
        (OW, "#F5F5F0", "245 · 245 · 240",  "0 · 0 · 2 · 4",    "OFF-WHITE",   "Fundos secundários.\nPapelaria e apresentações.", BK),
        ((26,26,26), "#1A1A1A","26 · 26 · 26","0 · 0 · 0 · 90", "CINZA ESCURO","Texto e elementos\nde suporte.", LG),
    ]

    for i, (col, hex_, rgb, cmyk, name, uso, tx) in enumerate(cores):
        x = pad + i*(sw+gap)
        # swatch
        d.rectangle([x, sy, x+sw, sy+sh], fill=col)
        if col == OW:
            d.rectangle([x, sy, x+sw, sy+sh], outline=(200,200,200), width=2)

        # nome e hex no interior do swatch
        d.text((x+44, sy+50), name, font=f_name, fill=tx)
        d.text((x+44, sy+152), hex_, font=f_hex,  fill=tx if col != OW else MG)

        # barra inferior colorida — marcador técnico
        d.rectangle([x, sy+sh-12, x+sw, sy+sh], fill=Y if col != Y else BK)

        # dados abaixo
        by = sy+sh+52
        d.text((x, by),      "RGB",  font=f_sm, fill=LG)
        d.text((x, by+52),   rgb,    font=f_sm, fill=BK)
        d.text((x, by+136),  "CMYK", font=f_sm, fill=LG)
        d.text((x, by+188),  cmyk,   font=f_sm, fill=BK)
        # uso
        for j, line in enumerate(uso.split("\n")):
            d.text((x, by+295+j*52), line, font=f_uso, fill=MG)

    # regra técnica de uso
    rule_y = sy+sh+560
    d.rectangle([pad, rule_y, W-pad, rule_y+2], fill=(210,210,210))
    f_rule = f("DMMono-Regular.ttf", 30)
    note = "Uso exclusivo das cores acima. Qualquer variação deve ser aprovada formalmente."
    d.text((pad, rule_y+20), note, font=f_rule, fill=LG)

    d.text((120, H-70), "PROPAGANDA OCA  —  BRANDBOOK 2025", font=f_foot, fill=LG)
    img.save(os.path.join(OUT, "02_paleta.png"), dpi=(300,300))
    print("02 done")

# ─────────────────────────────────────────────────────────────
# 03 TIPOGRAFIA — fix: cards maiores, preencher espaço vazio
# ─────────────────────────────────────────────────────────────
def make_tipo():
    W, H = 3600, 2400
    img = Image.new("RGB", (W, H), BK)
    d   = ImageDraw.Draw(img)

    f_hd   = f("BigShoulders-Bold.ttf", 100)
    f_sm   = f("DMMono-Regular.ttf", 32)
    f_foot = f("DMMono-Regular.ttf", 28)

    # header
    d.rectangle([0, 0, W, 220], fill=Y)
    d.text((120, 55), "TIPOGRAFIA", font=f_hd, fill=BK)
    d.text((W-380, 90), "03 / TYPE", font=f_sm, fill=BK)

    entries = [
        ("BigShoulders-Bold.ttf",    "TÍTULOS E DISPLAY",
         "BigShoulders", 230,
         "Força, impacto, presença.\nPara quando a marca precisa ocupar espaço.", Y),
        ("InstrumentSans-Regular.ttf","CORPO E SUBTÍTULOS",
         "Instrument Sans", 110,
         "Clareza, fluidez, leitura.\nPara quando o conteúdo precisa respirar.", OW),
        ("DMMono-Regular.ttf",        "DADOS E DESTAQUES",
         "DM  Mono", 88,
         "Precisão, técnica, referência.\nPara números, códigos e labels.", LG),
    ]

    bpad=90; gap=3
    bw=(W-2*bpad-2*gap)//3
    bh=740; by=280

    for i, (fname, role, sample, sz, desc, tx) in enumerate(entries):
        bx = bpad + i*(bw+gap)
        d.rectangle([bx, by, bx+bw, by+bh], fill=D20)
        # role chip
        f_role = f("DMMono-Regular.ttf", 30)
        d.text((bx+44, by+44), role, font=f_role, fill=Y)
        # amostra
        fs = f(fname, sz)
        sw2 = tw(d, sample, fs)
        while sw2 > bw-88 and sz > 40:
            sz -= 8
            fs  = f(fname, sz)
            sw2 = tw(d, sample, fs)
        d.text((bx+44, by+110), sample, font=fs, fill=tx)
        # descrição
        f_desc = f("InstrumentSans-Regular.ttf", 38)
        for j, line in enumerate(desc.split("\n")):
            d.text((bx+44, by+bh-160+j*55), line, font=f_desc, fill=MG)

    # faixa alfabeto
    strip_y = by+bh+60
    d.rectangle([0, strip_y, W, strip_y+220], fill=Y)
    f_alpha = f("BigShoulders-Bold.ttf", 175)
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ax = 50
    for ch in alpha:
        cw2 = tw(d, ch, f_alpha)
        d.text((ax, strip_y+22), ch, font=f_alpha, fill=BK)
        ax += cw2+6
        if ax > W-50: break

    # faixa numérica
    num_y = strip_y+230
    d.rectangle([0, num_y, W, num_y+220], fill=D16)
    f_num = f("DMMono-Regular.ttf", 155)
    nums = "0123456789  .,%;x"
    nx = 60
    for ch in nums:
        cw2 = tw(d, ch, f_num)
        d.text((nx, num_y+30), ch, font=f_num, fill=Y)
        nx += cw2+14
        if nx > W-60: break

    # pairing guide
    pair_y = num_y+240
    d.rectangle([0, pair_y, W, H-60], fill=(14,14,14))
    f_pg = f("DMMono-Regular.ttf", 30)
    d.text((90, pair_y+40), "PAIRING GUIDE", font=f_pg, fill=LG)
    pairs = [
        ("BigShoulders Bold", "Headlines, titulos de secao, identidade principal"),
        ("Instrument Sans Regular", "Corpo de texto, paragrafos, descricoes, legendas"),
        ("DM Mono Regular", "Numeros, metricas, labels tecnicos, URLs, datas"),
    ]
    f_pn = f("InstrumentSans-Bold.ttf", 40)
    f_pd = f("InstrumentSans-Regular.ttf", 40)
    for j, (pname, pdesc) in enumerate(pairs):
        py = pair_y+110+j*90
        pnw = tw(d, pname, f_pn)
        d.text((90, py), pname, font=f_pn, fill=WH)
        # seta como retangulo amarelo
        ax = 90+pnw+20
        d.rectangle([ax, py+14, ax+30, py+20], fill=Y)
        d.text((ax+40, py), pdesc, font=f_pd, fill=MG)

    d.text((120, H-50), "PROPAGANDA OCA  —  BRANDBOOK 2025", font=f_foot, fill=MG)
    img.save(os.path.join(OUT, "03_tipografia.png"), dpi=(300,300))
    print("03 done")

# ─────────────────────────────────────────────────────────────
# 04 MANIFESTO — fix: "PROPAGANDA" vertical não cortado, 1ª linha
# ─────────────────────────────────────────────────────────────
def make_manifesto():
    W, H = 3600, 2400
    img = Image.new("RGB", (W, H), BK)
    d   = ImageDraw.Draw(img)

    # grid de linhas finas
    for x in range(0, W, 200):
        d.line([(x, 0), (x, H)], fill=(22,22,22), width=1)

    # bloco amarelo — metade superior direita
    d.rectangle([W//2+160, 0, W, H//2-60], fill=Y)

    # círculo geométrico no bloco amarelo
    cx2 = W//2+160 + (W - (W//2+160))//2
    cy2 = (H//2-60)//2
    r = 300
    d.ellipse([cx2-r, cy2-r, cx2+r, cy2+r], fill=BK)
    d.ellipse([cx2-r+44, cy2-r+44, cx2+r-44, cy2+r-44], outline=Y, width=4)
    d.ellipse([cx2-10, cy2-10, cx2+10, cy2+10], fill=Y)

    # "PROPAGANDA" vertical — faixa esquerda, tamanho calculado para não cortar
    f_vert = f("BigShoulders-Bold.ttf", 180)
    chars_p = list("PROPAGANDA")
    char_h = th(d, "P", f_vert)
    total_h = len(chars_p) * (char_h + 8)
    start_y = (H - total_h) // 2
    for idx, ch in enumerate(chars_p):
        cy3 = start_y + idx*(char_h+8)
        d.text((28, cy3), ch, font=f_vert, fill=Y)

    # "OCA" — enorme, centro-esquerdo
    f_oca2 = f("BigShoulders-Bold.ttf", 520)
    oca_x = 230
    oca_y = H//2 - 80
    d.text((oca_x, oca_y), "OCA", font=f_oca2, fill=WH)

    # linha amarela acima de OCA
    d.rectangle([oca_x, oca_y-14, W//2+120, oca_y-8], fill=Y)

    # manifesto — TODAS as 3 linhas na metade inferior direita
    f_mani_b = f("InstrumentSans-Bold.ttf", 58)
    f_mani   = f("InstrumentSans-Regular.ttf", 54)
    lines = [
        ("Marketing que funciona de verdade.", f_mani_b, WH),
        ("Feito no interior. Para o interior.", f_mani, LG),
        ("Sem jargão. Sem template. Sem enrolação.", f_mani, LG),
    ]
    mx = W//2+200
    my = H//2+40
    for txt, ft, col in lines:
        d.text((mx, my), txt, font=ft, fill=col)
        my += th(d, txt, ft) + 22

    # bloco métricas — faixa inferior esquerda
    base_y = H-440
    d.rectangle([0, base_y-50, W//2+100, H], fill=D16)
    metrics = [("+120","EMPRESAS"),("3×","MAIS LEADS"),("87%","RETENÇÃO"),("5","ANOS")]
    f_mnum = f("BigShoulders-Bold.ttf", 190)
    f_mlbl = f("DMMono-Regular.ttf", 36)
    mpad   = 230
    slot_w = (W//2+100-mpad) // len(metrics)
    for i, (num, lbl) in enumerate(metrics):
        mx2 = mpad + i*slot_w
        d.text((mx2, base_y), num, font=f_mnum, fill=Y)
        d.text((mx2, base_y+210), lbl, font=f_mlbl, fill=LG)

    # linha inferior amarela
    d.rectangle([0, H-8, W, H], fill=Y)

    # label rodapé
    f_foot = f("DMMono-Regular.ttf", 28)
    d.text((W-680, H-56), "PROPAGANDA OCA  —  2025", font=f_foot, fill=MG)

    img.save(os.path.join(OUT, "04_manifesto.png"), dpi=(300,300))
    print("04 done")

# ─────────────────────────────────────────────────────────────
# 05 SISTEMA — já estava bom, só ajustar proporção dos mockups
# ─────────────────────────────────────────────────────────────
def make_sistema():
    W, H = 3600, 2400
    img = Image.new("RGB", (W, H), OW)
    d   = ImageDraw.Draw(img)

    f_hd   = f("BigShoulders-Bold.ttf", 100)
    f_sm   = f("DMMono-Regular.ttf", 32)
    f_lbl  = f("DMMono-Regular.ttf", 30)
    f_foot = f("DMMono-Regular.ttf", 28)

    # header
    d.rectangle([0, 0, W, 220], fill=BK)
    d.text((120, 55), "SISTEMA DE APLICAÇÃO", font=f_hd, fill=Y)
    d.text((W-460, 90), "05 / GRID", font=f_sm, fill=MG)

    # ── CARTÃO DE VISITA ──
    cw, ch = 1500, 900
    cv_x, cv_y = 100, 300

    # frente
    d.rectangle([cv_x, cv_y, cv_x+cw, cv_y+ch], fill=BK)
    d.rectangle([cv_x, cv_y, cv_x+55, cv_y+ch], fill=Y)
    f_cn = f("CactusClassical-Regular.ttf", 72)
    d.text((cv_x+80, cv_y+80), "PROPAGANDA", font=f_cn, fill=Y)
    f_cn2 = f("OfertaDoDia-Regular.ttf", 115)
    d.text((cv_x+80, cv_y+168), "OCA",    font=f_cn2, fill=Y)
    d.rectangle([cv_x+80, cv_y+ch-310, cv_x+cw-80, cv_y+ch-308], fill=(35,35,35))
    f_nm = f("InstrumentSans-Bold.ttf", 46)
    f_ti = f("InstrumentSans-Regular.ttf", 36)
    d.text((cv_x+80, cv_y+ch-290), "Jéssica Gregório",      font=f_nm, fill=WH)
    d.text((cv_x+80, cv_y+ch-238), "Diretora · Propaganda Oca", font=f_ti, fill=LG)
    d.text((cv_x+80, cv_y+ch-165), "(11) 9 5912-5935",      font=f_ti, fill=LG)
    d.text((cv_x+80, cv_y+ch-108), "oi@propagandaoca.com.br", font=f_ti, fill=LG)
    d.text((cv_x, cv_y+ch+30), "CARTÃO DE VISITA — FRENTE", font=f_lbl, fill=MG)

    # verso
    vx = cv_x+cw+70
    d.rectangle([vx, cv_y, vx+cw, cv_y+ch], fill=Y)
    f_cv_p = f("CactusClassical-Regular.ttf", 100)
    f_cv_o = f("OfertaDoDia-Regular.ttf", 140)
    prop_txt = "PROPAGANDA"
    ptw = tw(d, prop_txt, f_cv_p)
    d.text((vx+(cw-ptw)//2, cv_y+240), prop_txt, font=f_cv_p, fill=BK)
    oca_txt = "OCA"
    otw = tw(d, oca_txt, f_cv_o)
    d.text((vx+(cw-otw)//2, cv_y+360), oca_txt,  font=f_cv_o, fill=BK)
    d.text((vx, cv_y+ch+30), "CARTÃO DE VISITA — VERSO", font=f_lbl, fill=MG)

    # ── INSTAGRAM 1:1 ──
    ig_x, ig_y = 100, cv_y+ch+90
    ig_sz = 980
    d.rectangle([ig_x, ig_y, ig_x+ig_sz, ig_y+ig_sz], fill=BK)
    f_ig = f("BigShoulders-Bold.ttf", 210)
    d.text((ig_x+60, ig_y+80),  "3×",    font=f_ig, fill=Y)
    d.text((ig_x+60, ig_y+330), "MAIS",  font=f_ig, fill=WH)
    d.text((ig_x+60, ig_y+570), "LEADS", font=f_ig, fill=WH)
    d.rectangle([ig_x, ig_y+ig_sz-130, ig_x+ig_sz, ig_y+ig_sz], fill=Y)
    f_ig_s = f("DMMono-Regular.ttf", 36)
    d.text((ig_x+40, ig_y+ig_sz-96), "@propaganda.oca", font=f_ig_s, fill=BK)
    d.text((ig_x, ig_y+ig_sz+30), "POST INSTAGRAM 1:1", font=f_lbl, fill=MG)

    # ── PAPEL TIMBRADO A4 mockup ──
    pt_x = ig_x+ig_sz+80
    pt_w, pt_h = 660, 934
    pt_y = ig_y
    d.rectangle([pt_x, pt_y, pt_x+pt_w, pt_y+pt_h], fill=WH, outline=(200,200,200), width=2)
    d.rectangle([pt_x, pt_y, pt_x+pt_w, pt_y+110], fill=BK)
    d.rectangle([pt_x, pt_y, pt_x+24, pt_y+110], fill=Y)
    f_pt = f("BigShoulders-Bold.ttf", 52)
    d.text((pt_x+36, pt_y+12),  "PROPAGANDA", font=f_pt, fill=Y)
    d.text((pt_x+36, pt_y+62), "OCA",         font=f_pt, fill=Y)
    d.rectangle([pt_x, pt_y+pt_h-66, pt_x+pt_w, pt_y+pt_h], fill=Y)
    f_ptf = f("DMMono-Regular.ttf", 22)
    d.text((pt_x+12, pt_y+pt_h-44), "propagandaoca.com.br  ·  (11) 9 5912-5935", font=f_ptf, fill=BK)
    for k in range(9):
        ly = pt_y+140+k*84
        d.line([(pt_x+22, ly), (pt_x+pt_w-22, ly)], fill=(215,215,215), width=1)
    d.text((pt_x, pt_y+pt_h+30), "PAPEL TIMBRADO A4", font=f_lbl, fill=MG)

    # ── STORY 9:16 ──
    st_x = pt_x+pt_w+80
    st_w, st_h = 546, 970
    st_y = ig_y
    d.rectangle([st_x, st_y, st_x+st_w, st_y+st_h], fill=Y)
    f_st = f("BigShoulders-Bold.ttf", 138)
    for idx, word in enumerate(["MARKET-","ING QUE","FUNCIO-","NA."]):
        d.text((st_x+40, st_y+130+idx*158), word, font=f_st, fill=BK)
    d.rectangle([st_x, st_y+st_h-110, st_x+st_w, st_y+st_h], fill=BK)
    d.text((st_x+24, st_y+st_h-80), "@propaganda.oca", font=f_ig_s, fill=Y)
    d.text((st_x, st_y+st_h+30), "STORY 9:16", font=f_lbl, fill=MG)

    d.text((120, H-70), "PROPAGANDA OCA  —  BRANDBOOK 2025", font=f_foot, fill=LG)
    img.save(os.path.join(OUT, "05_sistema.png"), dpi=(300,300))
    print("05 done")

# ─────────────────────────────────────────────────────────────
# 06 TOM DE VOZ — fix: preencher espaço vazio, pares maiores
# ─────────────────────────────────────────────────────────────
def make_tom():
    W, H = 3600, 2400
    img = Image.new("RGB", (W, H), OW)
    d   = ImageDraw.Draw(img)

    f_hd   = f("BigShoulders-Bold.ttf", 100)
    f_sm   = f("DMMono-Regular.ttf", 32)
    f_attr = f("BigShoulders-Bold.ttf", 100)
    f_body = f("InstrumentSans-Regular.ttf", 48)
    f_lbl  = f("DMMono-Regular.ttf", 36)
    f_sim  = f("InstrumentSans-Regular.ttf", 44)
    f_foot = f("DMMono-Regular.ttf", 28)

    # header
    d.rectangle([0, 0, W, 220], fill=Y)
    d.text((120, 55), "TOM DE VOZ", font=f_hd, fill=BK)
    d.text((W-380, 90), "04 / VOZ", font=f_sm, fill=BK)

    # coluna esquerda — atributos
    attrs = [
        ("DIRETO",    "Vai direto ao ponto. Sem rodeios.\nO empresário não tem tempo a perder."),
        ("REGIONAL",  "Fala como quem conhece a cidade.\nMenciona lugares e contextos locais."),
        ("CONCRETO",  "Sempre com números e resultados\nreais. Nunca promessas vagas."),
        ("PARCEIRO",  "Tom de quem está do lado.\nSem pedantismo, sem jargão."),
    ]
    ay = 280
    col_h = (H-360) // len(attrs)
    for att, desc in attrs:
        # barra lateral amarela
        d.rectangle([80, ay+14, 94, ay+100], fill=Y)
        d.text((130, ay), att, font=f_attr, fill=BK)
        for i, line in enumerate(desc.split("\n")):
            d.text((130, ay+106+i*58), line, font=f_body, fill=MG)
        ay += col_h

    # divisória
    div_x = W//2 - 10
    d.rectangle([div_x, 240, div_x+3, H-80], fill=(200,200,200))

    # coluna direita
    rx = W//2+60
    d.text((rx, 270), "COMO FALAMOS", font=f_hd, fill=BK)
    d.rectangle([rx, 382, rx+240, 388], fill=Y)

    pares = [
        ("A gente entende o seu mercado.", "Potencialize seus KPIs com\nsoluções omnichannel."),
        ("Sem enrolação, sem template.", "Desenvolvemos estratégias\ncustomizadas e escaláveis."),
        ("Resultado em 4 meses.\nNúmero real, cliente real.", "ROI otimizado a longo prazo\ncom metodologias ágeis."),
        ("Feito para Bom Jesus dos Perdões.", "Atendemos empresas de todos\nos portes e segmentos."),
    ]

    rw = W - rx - 80
    col_w2 = (rw - 40) // 2
    px_sim = rx
    px_nao = rx + col_w2 + 40

    py = 420
    # cabeçalhos
    d.rectangle([px_sim, py, px_sim+col_w2, py+72], fill=(234,243,222))
    d.text((px_sim+20, py+14), "SIM", font=f_lbl, fill=(39,80,10))
    d.rectangle([px_nao, py, px_nao+col_w2, py+72], fill=(252,235,235))
    d.text((px_nao+20, py+14), "NÃO", font=f_lbl, fill=(163,45,45))
    py += 84

    for sim, nao in pares:
        sim_lines = sim.split("\n"); nao_lines = nao.split("\n")
        bh2 = max(len(sim_lines), len(nao_lines)) * 62 + 44

        d.rectangle([px_sim, py, px_sim+col_w2, py+bh2], fill=(245,252,240))
        for i, line in enumerate(sim_lines):
            d.text((px_sim+20, py+22+i*62), line, font=f_sim, fill=(39,80,10))

        d.rectangle([px_nao, py, px_nao+col_w2, py+bh2], fill=(255,245,245))
        for i, line in enumerate(nao_lines):
            d.text((px_nao+20, py+22+i*62), line, font=f_sim, fill=(163,45,45))

        py += bh2+12

    # bloco de nota final — preenche todo o espaço restante
    note_y = py + 30
    d.rectangle([rx, note_y, W-80, H-100], fill=BK)
    # label técnico
    f_note_lbl = f("DMMono-Regular.ttf", 30)
    d.text((rx+44, note_y+36), "// REGRA DE OURO", font=f_note_lbl, fill=Y)
    d.rectangle([rx+44, note_y+80, W-120, note_y+83], fill=(40,40,40))
    # quote principal
    f_q = f("InstrumentSans-Regular.ttf", 58)
    f_qb = f("InstrumentSans-Bold.ttf", 58)
    quote_lines = [
        ("Se nao daria para dizer para um cliente", f_q, LG),
        ("olhando nos olhos em Bom Jesus dos Perdoes,", f_q, LG),
        ("nao coloca no conteudo.", f_qb, WH),
    ]
    ny = note_y + 108
    for line, ft, col in quote_lines:
        d.text((rx+44, ny), line, font=ft, fill=col)
        ny += th(d, line, ft) + 20
    # atributos resumo no canto inferior do bloco
    f_mini = f("DMMono-Regular.ttf", 32)
    resume = ["DIRETO", "REGIONAL", "CONCRETO", "PARCEIRO"]
    rx2 = rx+44
    for idx, att in enumerate(resume):
        d.rectangle([rx2, H-190, rx2+tw(d, att, f_mini)+20, H-150], fill=Y)
        d.text((rx2+10, H-188), att, font=f_mini, fill=BK)
        rx2 += tw(d, att, f_mini) + 36

    d.text((120, H-70), "PROPAGANDA OCA  —  BRANDBOOK 2025", font=f_foot, fill=LG)
    img.save(os.path.join(OUT, "06_tom_de_voz.png"), dpi=(300,300))
    print("06 done")

# ─────────────────────────────────────────────────────────────
make_logo()
make_paleta()
make_tipo()
make_manifesto()
make_sistema()
make_tom()
print("\nRefinamento concluído:", OUT)
