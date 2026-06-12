from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_DIR = "/Users/jessicagregorio/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/4de4bdeb-9118-47dd-a7f9-0c3df3ef70fc/41e6c620-7e74-4cf6-9af2-fcd17229ba4c/skills/canvas-design/canvas-fonts"
pdfmetrics.registerFont(TTFont('CactusClassical', f'{FONT_DIR}/CactusClassical-Regular.ttf'))
pdfmetrics.registerFont(TTFont('OfertaDoDia',    f'{FONT_DIR}/OfertaDoDia-Regular.ttf'))

W, H = A4
YELLOW   = HexColor('#FFDE21')
BLACK    = HexColor('#0A0A0A')
OFFWHITE = HexColor('#F5F5F0')
DARKGRAY = HexColor('#1A1A1A')
MID      = HexColor('#444444')
LIGHT    = HexColor('#CCCCCC')

OUTPUT = "/Users/jessicagregorio/Oca Propaganda/Brandbook_Propaganda_Oca.pdf"

def spaced_text(c, text, x, y, font, size, space, color=None):
    if color:
        c.setFillColor(color)
    t = c.beginText(x, y)
    t.setFont(font, size)
    t.setCharSpace(space)
    t.textLine(text)
    c.drawText(t)

def wrap_para(c, text, x, y, width, size=9, color=MID, leading_mult=1.55):
    st = ParagraphStyle('p', fontName='Helvetica', fontSize=size,
                        leading=size*leading_mult, textColor=color)
    p = Paragraph(text, st)
    pw, ph = p.wrap(width, 9999)
    p.drawOn(c, x, y - ph)
    return y - ph

def section_label(c, num):
    c.setFillColor(MID)
    c.setFont("Helvetica", 8)
    c.drawString(20*mm, 12*mm, "PROPAGANDA OCA  —  BRANDBOOK 2025")
    c.drawRightString(W - 20*mm, 12*mm, f"SECAO {num}")

def yellow_rule(c, x, y, w=35*mm, h=1.2*mm):
    c.setFillColor(YELLOW)
    c.rect(x, y, w, h, stroke=0, fill=1)

def sub_heading(c, text, x, y):
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(x, y, text.upper())
    yellow_rule(c, x, y - 3*mm)
    return y - 13*mm

# ==============================
# CAPA
# ==============================
def draw_cover(c):
    c.setFillColor(BLACK)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(YELLOW)
    c.rect(0, 0, 12*mm, H, stroke=0, fill=1)
    c.setFillColor(YELLOW)
    c.setFont("CactusClassical", 72)
    c.drawString(28*mm, H - 78*mm, "PROPAGANDA")
    spaced_text(c, "OCA", 28*mm, H - 108*mm, "OfertaDoDia", 80, 8, YELLOW)
    c.setFillColor(YELLOW)
    c.rect(28*mm, H - 116*mm, 155*mm, 1.5*mm, stroke=0, fill=1)
    c.setFillColor(HexColor('#AAAAAA'))
    c.setFont("Helvetica", 14)
    c.drawString(28*mm, H - 130*mm, "Marketing que funciona de verdade.")
    c.setFillColor(YELLOW)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(28*mm, H - 146*mm, "BRANDBOOK  /  IDENTIDADE VISUAL  /  TOM DE VOZ")
    c.setFillColor(HexColor('#555555'))
    c.setFont("Helvetica", 9)
    c.drawString(28*mm, 20*mm, "propagandaoca.com.br  .  Bom Jesus dos Perdoes, SP  .  2025")
    c.setFillColor(HexColor('#333333'))
    c.drawRightString(W - 20*mm, 20*mm, "v1.0")

# ==============================
# SUMARIO
# ==============================
def draw_sumario(c):
    c.setFillColor(OFFWHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(BLACK)
    c.rect(0, H - 36*mm, W, 36*mm, stroke=0, fill=1)
    c.setFillColor(YELLOW)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(20*mm, H - 26*mm, "SUMARIO")
    items = [
        ("01", "Sobre a Empresa",    "Missao, visao, valores e posicionamento"),
        ("02", "Identidade Visual",  "Cores, tipografia, grid e espacamento"),
        ("03", "Logotipo",           "Versoes, usos corretos e incorretos"),
        ("04", "Tom de Voz",         "Linguagem, exemplos e diretrizes"),
        ("05", "Aplicacoes",         "Instagram, cartao de visita, papel timbrado"),
        ("06", "Fotografia e Imagem","Padroes e diretrizes visuais"),
    ]
    y = H - 58*mm
    for num, title, sub in items:
        c.setFillColor(YELLOW)
        c.rect(20*mm, y - 1.5*mm, 8*mm, 8*mm, stroke=0, fill=1)
        c.setFillColor(BLACK)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(24*mm, y + 1*mm, num)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(32*mm, y + 1.5*mm, title)
        c.setFillColor(MID)
        c.setFont("Helvetica", 9)
        c.drawString(32*mm, y - 5*mm, sub)
        c.setStrokeColor(LIGHT); c.setLineWidth(0.3)
        c.line(20*mm, y - 9*mm, W - 20*mm, y - 9*mm)
        y -= 22*mm
    c.setFillColor(MID)
    c.setFont("Helvetica", 8)
    c.drawString(20*mm, 12*mm, "PROPAGANDA OCA  —  BRANDBOOK 2025")

# ==============================
# SECTION OPENER
# ==============================
def draw_opener(c, num, title, subtitle=""):
    c.setFillColor(YELLOW)
    c.rect(0, H - 42*mm, W, 42*mm, stroke=0, fill=1)
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(20*mm, H - 14*mm, f"SECAO {num}")
    c.setFont("Helvetica-Bold", 32)
    c.drawString(20*mm, H - 30*mm, title.upper())
    if subtitle:
        c.setFont("Helvetica", 11)
        c.drawString(20*mm, H - 38*mm, subtitle)
    section_label(c, num)
    c.setStrokeColor(LIGHT); c.setLineWidth(0.3)
    c.line(20*mm, 18*mm, W - 20*mm, 18*mm)

# ==============================
# CONTRACAPA
# ==============================
def draw_back(c):
    c.setFillColor(YELLOW)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(BLACK)
    c.setFont("CactusClassical", 52)
    c.drawCentredString(W/2, H/2 + 30*mm, "PROPAGANDA")
    spaced_text(c, "OCA", W/2 - 38*mm, H/2 + 2*mm, "OfertaDoDia", 58, 4, BLACK)
    c.setFont("Helvetica", 13)
    c.drawCentredString(W/2, H/2 - 15*mm, "propagandaoca.com.br")
    c.setFont("Helvetica", 11)
    c.drawCentredString(W/2, H/2 - 25*mm, "oi@propagandaoca.com.br  .  (11) 9 5912-5935")
    c.setFillColor(HexColor('#333333'))
    c.setFont("Helvetica", 9)
    c.drawCentredString(W/2, 20*mm, "Bom Jesus dos Perdoes, SP  .  2025  .  Todos os direitos reservados.")

# ==============================
# PAGINA: SOBRE
# ==============================
def draw_sobre(c):
    mx = 20*mm
    c.setFillColor(OFFWHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - 30*mm
    y = sub_heading(c, "Missao", mx, y)
    y = wrap_para(c, "Ajudar pequenas empresas do interior de SP a crescerem com marketing que faz sentido para o seu contexto. Sem jargao, sem template, sem agencia grande que nao conhece sua rua.", mx, y, W - 2*mx, size=10) - 8*mm
    y = sub_heading(c, "Visao", mx, y)
    y = wrap_para(c, "Ser a agencia de referencia em Inbound Marketing e geracao de demanda para pequenas empresas de Bom Jesus dos Perdoes, Atibaia e Braganca Paulista, reconhecida por resultados concretos e parceria real.", mx, y, W - 2*mx, size=10) - 8*mm
    y = sub_heading(c, "Valores", mx, y)
    valores = [
        ("Estrategia local",    "Planos feitos para o seu mercado especifico. Nunca templates de agencia de Sao Paulo."),
        ("Transparencia total", "Relatorios mensais em linguagem humana. Sem jargao, sem enrolacao."),
        ("Parceria real",       "Sem contratos longos ou multas abusivas. A gente fica porque entrega resultado."),
        ("Agilidade",           "Equipe enxuta e focada. Voce fala com quem faz, nao com assistente de assistente."),
    ]
    for v, desc in valores:
        c.setFillColor(YELLOW)
        c.roundRect(mx, y - 2*mm, 3*mm, 3*mm, 0.5*mm, stroke=0, fill=1)
        c.setFillColor(BLACK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(mx + 5*mm, y, v)
        y = wrap_para(c, desc, mx + 5*mm, y - 3*mm, W - 2*mx - 5*mm, size=9) - 5*mm
    y -= 4*mm
    y = sub_heading(c, "Posicionamento", mx, y)
    wrap_para(c, "A Propaganda Oca e a unica agencia de Inbound Marketing especializada nas pequenas cidades do interior paulista. Enquanto agencias grandes vendem pacotes genericos, a gente constroi estrategias a partir do mercado, do publico e da cultura de cada cidade.", mx, y, W - 2*mx, size=10)
    section_label(c, "01")

# ==============================
# PAGINA: NUMEROS
# ==============================
def draw_numeros(c):
    mx = 20*mm
    c.setFillColor(OFFWHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(mx, H - 30*mm, "NUMEROS QUE FALAM POR NOS")
    yellow_rule(c, mx, H - 33*mm, 60*mm)
    nums = [("+120","empresas atendidas"),("3x","mais leads em media"),("87%","taxa de retencao"),("5 anos","no mercado regional")]
    bw = (W - 2*mx - 10*mm) / 2
    bh = 38*mm
    for i, (n, l) in enumerate(nums):
        col = i % 2; row = i // 2
        x = mx + col * (bw + 10*mm)
        y = H - 55*mm - row * (bh + 8*mm)
        c.setFillColor(BLACK)
        c.roundRect(x, y, bw, bh, 3*mm, stroke=0, fill=1)
        c.setFillColor(YELLOW)
        c.setFont("Helvetica-Bold", 34)
        c.drawString(x + 8*mm, y + bh - 20*mm, n)
        c.setFillColor(HexColor('#888888'))
        c.setFont("Helvetica", 9)
        c.drawString(x + 8*mm, y + 8*mm, l.upper())
    section_label(c, "01")

# ==============================
# PAGINA: PALETA
# ==============================
def draw_paleta(c):
    mx = 20*mm
    c.setFillColor(OFFWHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - 30*mm
    y = sub_heading(c, "Paleta de Cores", mx, y) + 2*mm
    cores = [
        (YELLOW,   "#FFDE21", "255 / 222 / 33",   "0 / 13 / 87 / 0",  "Amarelo Primario",
         "Cor de identidade. Destaques, CTAs, titulos sobre fundo escuro."),
        (BLACK,    "#0A0A0A", "10 / 10 / 10",     "0 / 0 / 0 / 96",   "Preto",
         "Fundos principais, texto sobre fundo claro."),
        (OFFWHITE, "#F5F5F0", "245 / 245 / 240",  "0 / 0 / 2 / 4",    "Off-white",
         "Fundos secundarios, backgrounds de secoes claras."),
        (DARKGRAY, "#1A1A1A", "26 / 26 / 26",     "0 / 0 / 0 / 90",   "Cinza Escuro",
         "Texto secundario, fundos alternativos."),
    ]
    for bg, hex_, rgb, cmyk, name, uso in cores:
        sw = 28*mm; bh = 22*mm
        c.setFillColor(bg)
        c.roundRect(mx, y - bh, sw, bh, 2*mm, stroke=0, fill=1)
        if bg == OFFWHITE:
            c.setStrokeColor(LIGHT); c.setLineWidth(0.4)
            c.roundRect(mx, y - bh, sw, bh, 2*mm, stroke=1, fill=0)
        c.setFillColor(BLACK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(mx + sw + 5*mm, y - 2*mm, name)
        c.setFillColor(MID)
        c.setFont("Helvetica", 8)
        c.drawString(mx + sw + 5*mm, y - 7*mm, f"HEX {hex_}   RGB {rgb}")
        c.drawString(mx + sw + 5*mm, y - 12*mm, f"CMYK {cmyk}")
        wrap_para(c, uso, mx + sw + 5*mm, y - 12*mm, W - mx - sw - 25*mm, size=8, color=HexColor('#888888'))
        y -= 30*mm
    section_label(c, "02")

# ==============================
# PAGINA: TIPOGRAFIA
# ==============================
def draw_tipografia(c):
    mx = 20*mm
    c.setFillColor(OFFWHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - 30*mm
    y = sub_heading(c, "Tipografia", mx, y) + 2*mm
    fontes = [
        ("Bebas Neue",    "TITULOS E DISPLAY",            "Aa Bb Cc Dd 0123", 38,
         "Usada em headings principais, nome da marca, secoes de destaque e chamadas de alto impacto. Nunca usar em corpo de texto."),
        ("Space Grotesk", "CORPO E SUBTITULOS",           "Aa Bb Cc Dd 0123", 20,
         "Fonte principal de leitura. Usada em paragrafos, subtitulos, legendas, formularios e qualquer bloco de texto corrido."),
        ("DM Mono",       "DADOS E DESTAQUES TECNICOS",   "Aa 01 #FFDE21 ->", 16,
         "Usada para numeros de destaque, metricas, codigos, labels tecnicos e elementos de interface como tags e badges."),
    ]
    for fname, role, sample, ssize, desc in fontes:
        bh = 38*mm
        c.setFillColor(BLACK)
        c.roundRect(mx, y - bh, W - 2*mx, bh, 2*mm, stroke=0, fill=1)
        c.setFillColor(YELLOW)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(mx + 4*mm, y - 4*mm, role)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(mx + 4*mm, y - 10*mm, fname)
        c.setFont("Helvetica", ssize)
        c.drawString(mx + 4*mm, y - 22*mm, sample)
        c.setFillColor(HexColor('#888888'))
        wrap_para(c, desc, mx + 4*mm, y - bh + 8*mm, W - 2*mx - 8*mm, size=7.5, color=HexColor('#888888'))
        y -= bh + 8*mm
    section_label(c, "02")

# ==============================
# PAGINA: LOGOTIPO
# ==============================
def draw_logotipo(c):
    mx = 20*mm
    c.setFillColor(OFFWHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - 30*mm
    y = sub_heading(c, "Versoes do Logotipo", mx, y) + 2*mm

    versoes = [
        (BLACK,    YELLOW,  None,  "Versao Principal",  "Fundos escuros, posts, apresentacoes."),
        (YELLOW,   BLACK,   None,  "Versao Amarela",     "Impressos, papelaria, eventos."),
        (OFFWHITE, BLACK,   LIGHT, "Versao Clara",       "Fundos brancos ou off-white."),
    ]
    bw = (W - 2*mx - 10*mm) / 3
    bh = 32*mm
    for i, (bg, fg, stroke_c, title, desc) in enumerate(versoes):
        x = mx + i * (bw + 5*mm)
        c.setFillColor(bg)
        c.roundRect(x, y - bh, bw, bh, 2*mm, stroke=0, fill=1)
        if stroke_c:
            c.setStrokeColor(stroke_c); c.setLineWidth(0.4)
            c.roundRect(x, y - bh, bw, bh, 2*mm, stroke=1, fill=0)
        c.setFillColor(fg)
        c.setFont("CactusClassical", 10)
        c.drawCentredString(x + bw/2, y - 13*mm, "PROPAGANDA")
        spaced_text(c, "OCA", x + bw/2 - 18*mm, y - 22*mm, "OfertaDoDia", 14, 2, fg)
        c.setFillColor(BLACK)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawCentredString(x + bw/2, y - bh - 5*mm, title)
        wrap_para(c, desc, x, y - bh - 5*mm - 7*mm, bw, size=7, color=MID)

    y -= bh + 22*mm
    y = sub_heading(c, "Area de Protecao", mx, y)
    wrap_para(c, "Manter uma area livre equivalente a altura da letra 'O' do logotipo em todos os lados. Tamanho minimo: 30mm de largura em impresso / 120px em digital.", mx, y, W - 2*mx, size=9)
    y -= 22*mm

    y = sub_heading(c, "Usos Incorretos", mx, y)
    erros = [
        "Nao distorcer proporcoes do logotipo",
        "Nao alterar as cores fora deste manual",
        "Nao usar sobre fundos que prejudiquem a legibilidade",
        "Nao adicionar sombras, contornos ou efeitos",
        "Nao rotacionar o logotipo",
        "Nao recriar com outras fontes",
    ]
    half = len(erros) // 2
    for i, e in enumerate(erros):
        col = i // half; row = i % half
        ex = mx + col * (W/2 - mx)
        ey = y - row * 10*mm
        c.setFillColor(HexColor('#CC0000'))
        c.circle(ex + 2*mm, ey + 2*mm, 1.5*mm, stroke=0, fill=1)
        c.setFillColor(BLACK)
        c.setFont("Helvetica", 8.5)
        c.drawString(ex + 5*mm, ey, e)
    section_label(c, "03")

# ==============================
# PAGINA: TOM DE VOZ
# ==============================
def draw_tom(c):
    mx = 20*mm
    c.setFillColor(OFFWHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - 30*mm
    y = sub_heading(c, "Diretrizes de Linguagem", mx, y) + 2*mm

    atributos = [
        ("Direto",    "Vai direto ao ponto. Sem rodeios, sem enrolacao. O empresario do interior nao tem tempo a perder."),
        ("Regional",  "Fala como quem conhece a cidade. Menciona lugares, contextos e desafios locais. Nunca generico."),
        ("Concreto",  "Sempre com numeros, resultados e exemplos reais. Nunca promessas vagas."),
        ("Parceiro",  "Tom de quem esta do lado, nao de quem vende. Sem pedantismo ou superioridade tecnica."),
    ]
    for att, desc in atributos:
        c.setFillColor(YELLOW)
        c.roundRect(mx, y - 2*mm, 22*mm, 7*mm, 1*mm, stroke=0, fill=1)
        c.setFillColor(BLACK)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(mx + 11*mm, y + 1.5*mm, att.upper())
        ynew = wrap_para(c, desc, mx + 27*mm, y + 4*mm, W - mx - 27*mm - mx, size=9)
        y = min(ynew, y - 12*mm) - 4*mm

    y -= 5*mm
    y = sub_heading(c, "Exemplos de Linguagem", mx, y) + 2*mm
    pares = [
        ("A gente entende o seu mercado.", "Potencialize seus KPIs com solucoes omnichannel."),
        ("Sem enrolacao, sem template.", "Desenvolvemos estrategias customizadas e escalaveis."),
        ("Resultado em 4 meses. Numero real, cliente real.", "ROI otimizado a longo prazo com metodologias ageis."),
        ("Feito para Bom Jesus dos Perdoes. Feito para voce.", "Atendemos empresas de todos os portes e segmentos."),
    ]
    col_w = (W - 2*mx - 8*mm) / 2
    for sim, nao in pares:
        bh = 13*mm
        c.setFillColor(HexColor('#EAF3DE'))
        c.roundRect(mx, y - bh, col_w, bh, 2*mm, stroke=0, fill=1)
        c.setFillColor(HexColor('#27500A'))
        c.setFont("Helvetica-Bold", 7)
        c.drawString(mx + 3*mm, y - 3*mm, "SIM")
        wrap_para(c, sim, mx + 3*mm, y - 5*mm, col_w - 6*mm, size=8, color=HexColor('#27500A'))

        nx = mx + col_w + 8*mm
        c.setFillColor(HexColor('#FCEBEB'))
        c.roundRect(nx, y - bh, col_w, bh, 2*mm, stroke=0, fill=1)
        c.setFillColor(HexColor('#A32D2D'))
        c.setFont("Helvetica-Bold", 7)
        c.drawString(nx + 3*mm, y - 3*mm, "NAO")
        wrap_para(c, nao, nx + 3*mm, y - 5*mm, col_w - 6*mm, size=8, color=HexColor('#A32D2D'))
        y -= 17*mm
    section_label(c, "04")

# ==============================
# PAGINA: APLICACOES
# ==============================
def draw_aplicacoes(c):
    mx = 20*mm
    c.setFillColor(OFFWHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - 30*mm
    y = sub_heading(c, "Cartao de Visita", mx, y) + 2*mm

    cw, ch = 85*mm, 54*mm
    # Frente
    c.setFillColor(BLACK)
    c.roundRect(mx, y - ch, cw, ch, 2*mm, stroke=0, fill=1)
    c.setFillColor(YELLOW)
    c.rect(mx, y - ch, 5*mm, ch, stroke=0, fill=1)
    c.setFillColor(YELLOW); c.setFont("CactusClassical", 9)
    c.drawString(mx + 8*mm, y - ch + ch - 13*mm, "PROPAGANDA")
    spaced_text(c, "OCA", mx + 8*mm, y - ch + ch - 23*mm, "OfertaDoDia", 13, 2, YELLOW)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 9)
    c.drawString(mx + 8*mm, y - ch + 20*mm, "Jessica Gregorio")
    c.setFillColor(HexColor('#AAAAAA')); c.setFont("Helvetica", 7)
    c.drawString(mx + 8*mm, y - ch + 13*mm, "Diretora de Marketing")
    c.setFillColor(HexColor('#666666')); c.setFont("Helvetica", 6.5)
    c.drawString(mx + 8*mm, y - ch + 6*mm, "(11) 9 5912-5935  .  oi@propagandaoca.com.br")
    c.setFillColor(MID); c.setFont("Helvetica", 7)
    c.drawString(mx, y - ch - 5*mm, "Frente")

    # Verso
    vx = mx + cw + 8*mm
    c.setFillColor(YELLOW)
    c.roundRect(vx, y - ch, cw, ch, 2*mm, stroke=0, fill=1)
    c.setFillColor(BLACK); c.setFont("CactusClassical", 13)
    c.drawCentredString(vx + cw/2, y - ch/2 + 6*mm, "PROPAGANDA")
    spaced_text(c, "OCA", vx + cw/2 - 22*mm, y - ch/2 - 6*mm, "OfertaDoDia", 18, 2, BLACK)
    c.setFillColor(MID); c.setFont("Helvetica", 7)
    c.drawString(vx, y - ch - 5*mm, "Verso")

    y -= ch + 18*mm

    # Papel timbrado mockup
    y = sub_heading(c, "Papel Timbrado", mx, y)
    pw2, ph2 = 90*mm, 110*mm
    c.setFillColor(white); c.setStrokeColor(LIGHT); c.setLineWidth(0.5)
    c.rect(mx, y - ph2, pw2, ph2, stroke=1, fill=1)
    c.setFillColor(BLACK)
    c.rect(mx, y - 18*mm, pw2, 18*mm, stroke=0, fill=1)
    c.setFillColor(YELLOW); c.setFont("CactusClassical", 8)
    c.drawString(mx + 4*mm, y - 11*mm, "PROPAGANDA")
    spaced_text(c, "OCA", mx + 4*mm, y - 18*mm, "OfertaDoDia", 11, 1, YELLOW)
    c.setFillColor(YELLOW)
    c.rect(mx, y - ph2, pw2, 9*mm, stroke=0, fill=1)
    c.setFillColor(BLACK); c.setFont("Helvetica", 5.5)
    c.drawCentredString(mx + pw2/2, y - ph2 + 3*mm, "propagandaoca.com.br  .  (11) 9 5912-5935  .  Bom Jesus dos Perdoes, SP")
    c.setFillColor(LIGHT)
    for i in range(6):
        ly = y - 25*mm - i * 7*mm
        c.rect(mx + 4*mm, ly, pw2 - 8*mm, 2*mm, stroke=0, fill=1)

    # Instagram mockup
    ix = mx + pw2 + 10*mm
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 11)
    c.drawString(ix, y + 10*mm, "INSTAGRAM")
    yellow_rule(c, ix, y + 7*mm, 28*mm)
    pw3 = 60*mm; ph3 = 60*mm
    c.setFillColor(BLACK)
    c.roundRect(ix, y - ph3, pw3, ph3, 2*mm, stroke=0, fill=1)
    c.setFillColor(YELLOW)
    c.rect(ix, y - ph3, pw3, 8*mm, stroke=0, fill=1)
    c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 5.5)
    c.drawCentredString(ix + pw3/2, y - ph3 + 3*mm, "@propaganda.oca  .  propagandaoca.com.br")
    c.setFillColor(YELLOW); c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(ix + pw3/2, y - 22*mm, "3x MAIS")
    c.drawCentredString(ix + pw3/2, y - 31*mm, "LEADS")
    c.setFillColor(white); c.setFont("Helvetica", 7)
    c.drawCentredString(ix + pw3/2, y - 39*mm, "em 4 meses de estrategia")
    c.setFillColor(HexColor('#555555')); c.setFont("Helvetica", 6)
    c.drawCentredString(ix + pw3/2, y - 47*mm, "Arquitetura LF . Bom Jesus dos Perdoes")
    section_label(c, "05")

# ==============================
# PAGINA: FOTOGRAFIA
# ==============================
def draw_foto(c):
    mx = 20*mm
    c.setFillColor(OFFWHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - 30*mm
    y = sub_heading(c, "Padroes de Imagem", mx, y) + 2*mm

    diretrizes = [
        ("Fotografia documental",
         "Imagens reais de estabelecimentos e empresarios da regiao. Nada de banco de imagens generico com pessoas sorridentes em escritorios."),
        ("Tratamento de cor",
         "Contraste alto, tons ligeiramente desaturados. Sobreposicao amarela semitransparente (#FFDE21 a 20-30% de opacidade) como recurso de identidade."),
        ("Enquadramento",
         "Composicao geometrica, uso de linhas arquitetonicas. Espaco negativo para texto. Preferencia por formato quadrado (1:1) ou retrato (4:5) para redes sociais."),
        ("Pessoas",
         "Fotos dos clientes e donos de negocio reais, em contexto de trabalho. Evitar poses ensaiadas. Expressoes naturais e ambientes autenticos."),
        ("Icones e ilustracoes",
         "Uso exclusivo de icones outline minimalistas. Sem ilustracoes complexas ou clipart. Icones sempre na paleta da marca."),
    ]
    for titulo, desc in diretrizes:
        c.setFillColor(BLACK); c.setFont("Helvetica-Bold", 9.5)
        c.drawString(mx, y, titulo)
        y = wrap_para(c, desc, mx, y - 3*mm, W - 2*mx, size=9) - 10*mm

    y -= 5*mm
    y = sub_heading(c, "Referencia de Tratamento Visual", mx, y) + 2*mm
    labels = ["Foto original", "Contraste +20", "Overlay amarelo", "Versao final com texto"]
    bw2 = (W - 2*mx - 9*mm) / 4
    bh2 = 26*mm
    for i, label in enumerate(labels):
        bx = mx + i * (bw2 + 3*mm)
        gray = HexColor('#%02x%02x%02x' % (180 - i*20, 180 - i*20, 180 - i*20))
        c.setFillColor(gray)
        c.roundRect(bx, y - bh2, bw2, bh2, 2*mm, stroke=0, fill=1)
        if i == 3:
            c.setFillColor(BLACK)
            c.roundRect(bx, y - bh2, bw2, bh2, 2*mm, stroke=0, fill=1)
            c.setFillColor(YELLOW); c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(bx + bw2/2, y - bh2/2, "TITULO")
        c.setFillColor(MID); c.setFont("Helvetica", 7)
        c.drawCentredString(bx + bw2/2, y - bh2 - 6*mm, label)
    section_label(c, "06")

# ==============================
# GERAR PDF
# ==============================
c = canvas.Canvas(OUTPUT, pagesize=A4)
c.setTitle("Brandbook Propaganda Oca")
c.setAuthor("Propaganda Oca")
c.setSubject("Identidade Visual e Tom de Voz — 2025")

draw_cover(c);        c.showPage()
draw_sumario(c);      c.showPage()
draw_opener(c, "01", "Sobre a Empresa", "Quem somos, onde estamos e o que defendemos"); c.showPage()
draw_sobre(c);        c.showPage()
draw_numeros(c);      c.showPage()
draw_opener(c, "02", "Identidade Visual", "Cores, tipografia, grid e espacamento"); c.showPage()
draw_paleta(c);       c.showPage()
draw_tipografia(c);   c.showPage()
draw_opener(c, "03", "Logotipo", "Versoes, usos corretos e area de protecao"); c.showPage()
draw_logotipo(c);     c.showPage()
draw_opener(c, "04", "Tom de Voz", "Como a Propaganda Oca fala com o mundo"); c.showPage()
draw_tom(c);          c.showPage()
draw_opener(c, "05", "Aplicacoes", "Instagram, cartao de visita, papel timbrado"); c.showPage()
draw_aplicacoes(c);   c.showPage()
draw_opener(c, "06", "Fotografia e Imagem", "Padroes visuais e diretrizes de uso de imagem"); c.showPage()
draw_foto(c);         c.showPage()
draw_back(c);         c.showPage()

c.save()
print("PDF gerado:", OUTPUT)
