"""Gera os grafismos do tema: engrenagens e névoa espiralada, em SVG procedural.
Nada de arquivo de imagem — a saída é um data: URI que vive dentro do CSS.

v2 (2026-09-08): a névoa deixou de ser ruído borrado e virou VOLUTA — espiral
logarítmica desenhada como fita que afina para dentro, do jeito que a bruma de
Mistborn se enrola. O ruído continua, mas agora só como deslocamento: ele torce
a espiral para ela não parecer matemática. E há faixa lateral, além de topo e
rodapé.
"""
import math, urllib.parse

# ---------------------------------------------------------------- engrenagens

def engrenagem(cx, cy, r_ext, r_int, dentes, r_furo, giro=0.0):
    """Caminho SVG de uma engrenagem: coroa dentada + furo central."""
    p = []
    passo = 2*math.pi/dentes
    base, topo = passo*0.30, passo*0.19
    for i in range(dentes):
        a = giro + i*passo
        for ang, r in ((a-base, r_int), (a-topo, r_ext), (a+topo, r_ext), (a+base, r_int)):
            x, y = cx + r*math.cos(ang), cy + r*math.sin(ang)
            p.append(f"{'M' if (i==0 and ang==a-base) else 'L'}{x:.1f} {y:.1f}")
        a2 = a + passo - base
        p.append(f"A{r_int:.1f} {r_int:.1f} 0 0 1 {cx + r_int*math.cos(a2):.1f} {cy + r_int*math.sin(a2):.1f}")
    p.append("Z")
    p.append(f"M{cx+r_furo:.1f} {cy:.1f}")
    p.append(f"A{r_furo:.1f} {r_furo:.1f} 0 1 0 {cx-r_furo:.1f} {cy:.1f}")
    p.append(f"A{r_furo:.1f} {r_furo:.1f} 0 1 0 {cx+r_furo:.1f} {cy:.1f}Z")
    return "".join(p)


def raios(cx, cy, r1, r2, n, esp, giro=0.0):
    """Braços internos da engrenagem, para ela não parecer um anel liso."""
    out = []
    for i in range(n):
        a = giro + i*2*math.pi/n
        dx, dy = math.cos(a), math.sin(a)
        nx, ny = -dy*esp/2, dx*esp/2
        x1, y1 = cx+dx*r1, cy+dy*r1
        x2, y2 = cx+dx*r2, cy+dy*r2
        out.append(f"M{x1+nx:.1f} {y1+ny:.1f}L{x2+nx:.1f} {y2+ny:.1f}"
                   f"L{x2-nx:.1f} {y2-ny:.1f}L{x1-nx:.1f} {y1-ny:.1f}Z")
    return "".join(out)


# --------------------------------------------------------------------- névoa

def voluta(cx, cy, r_ext, voltas, w0, w1, fase=0.0, sentido=1, mingua=0.09):
    """Fita em espiral logarítmica que entra larga e se enrola até sumir.

    Parametrizada pelo que se vê, não pela fórmula: `r_ext` é o raio de onde a
    voluta começa (o braço que varre a faixa) e `voltas` é quanto ela dá até o
    miolo. O decaimento `b` sai daí — no fim do percurso o raio vale `mingua`
    do inicial.

    Desenhada como área fechada, não como traço, porque a fita precisa AFINAR:
    grossa na ponta que entra na cena, fio de nada no centro do rolo. Um
    `stroke` tem espessura única.

    sentido=-1 espelha o enrolamento (bruma que gira para o outro lado).
    """
    span = voltas*2*math.pi
    b = -math.log(mingua)/span
    passos = max(26, int(span*4.6))
    pts_ext, pts_int = [], []
    for i in range(passos+1):
        s = i/passos
        t = span*s
        r = r_ext*math.exp(-b*t)
        ang = sentido*(t + fase)
        x, y = cx + r*math.cos(ang), cy + r*math.sin(ang)
        # tangente da espiral logarítmica (sinal do decaimento invertido)
        dx = (-b*math.cos(ang) - sentido*math.sin(ang))
        dy = (-b*math.sin(ang) + sentido*math.cos(ang))
        n = math.hypot(dx, dy) or 1.0
        ux, uy = -dy/n, dx/n
        # a fita afina rápido no começo e devagar no fim: s² dá esse perfil
        w = (w1 + (w0-w1)*(1-s)**1.7) / 2.0
        pts_ext.append((x+ux*w, y+uy*w))
        pts_int.append((x-ux*w, y-uy*w))
    d = ["M{:.0f} {:.0f}".format(*pts_ext[0])]
    d += ["L{:.0f} {:.0f}".format(*p) for p in pts_ext[1:]]
    d += ["L{:.0f} {:.0f}".format(*p) for p in reversed(pts_int)]
    d.append("Z")
    return "".join(d)


def _envolve(cx, cy, periodo, eixo, alcance=0):
    """A peça na sua posição, mais as vizinhas — quando alcançam o ladrilho.

    O ladrilho tem de emendar consigo mesmo. Uma voluta cortada pela borda
    esquerda precisa reaparecer inteira entrando pela direita — senão a emenda
    fica visível como um risco vertical, que foi o defeito da primeira tentativa.
    Só se desenha a cópia que de fato entra na área visível: replicar as três
    sempre dobrava o tamanho do CSS sem acrescentar um pixel.
    """
    c = cx if eixo == 'x' else cy
    for k in (-1, 0, 1):
        if k and not (c + k*periodo - alcance < periodo and c + k*periodo + alcance > 0):
            continue
        yield (cx + k*periodo, cy) if eixo == 'x' else (cx, cy + k*periodo)


def bruma(pecas, periodo, eixo='x'):
    """Conjunto de volutas com opacidades próprias, replicado para emendar."""
    out = []
    for cx, cy, r, v, w0, w1, fase, sent, op in pecas:
        for x, y in _envolve(cx, cy, periodo, eixo, r + w0):
            out.append(f"<path opacity='{op}' d='{voluta(x,y,r,v,w0,w1,fase,sent)}'/>")
    return "".join(out)


def rodas(pecas, periodo, eixo='x'):
    """Engrenagens, também replicadas nas duas bordas do ladrilho."""
    out = []
    for cx, cy, re_, ri, d, f, g, op in pecas:
        for x, y in _envolve(cx, cy, periodo, eixo, re_):
            out.append(
                f"<g opacity='{op}'>"
                f"<path fill-rule='evenodd' d='{engrenagem(x,y,re_,ri,d,f,g)}'/>"
                f"<path d='{raios(x,y,f+2,ri-3,5,max(3,re_*0.10),g)}'/>"
                f"</g>")
    return "".join(out)


# ------------------------------------------------------------------ ladrilhos

L, A = 400, 200          # faixa horizontal: emenda na horizontal
LL, LA = 120, 400        # faixa lateral: emenda na vertical

_ENGRENAGENS_TOPO = [
    # (cx, cy, r_ext, r_int, dentes, furo, giro, opacidade)
    (  0,  10, 84, 68, 16, 22, 0.10, .40),
    (118, -14, 62, 49, 13, 16, 0.34, .36),
    (196,  30, 40, 31, 10, 11, 0.62, .30),
    (272, -20, 70, 56, 14, 18, 0.21, .34),
    ( 58,  46, 27, 20,  9,  7, 0.50, .24),
    (162,  52, 20, 15,  8,  5, 0.15, .22),
    (238, -46, 34, 26,  9,  9, 0.44, .26),
    (330,  40, 33, 25,  9,  9, 0.08, .22),
    ( 96,  18, 15, 11,  7,  4, 0.55, .20),
    (368,  -4, 22, 16,  8,  6, 0.30, .20),
    (  8,  70, 17, 12,  7,  4, 0.70, .18),
]

# Volutas da faixa horizontal. Braços largos que varrem a faixa e se enrolam.
# As duas âncoras em x=0 e x=400 são a mesma voluta partida pela emenda.
_VOLUTAS_TOPO = [
    # (cx, cy, r_ext, voltas, w0, w1, fase, sentido, opacidade)
    (  70,  44, 96, 1.45, 34, 2, 2.10,  1, .52),
    ( 214,  30, 82, 1.35, 30, 2, 5.20, -1, .46),
    ( 330,  50, 90, 1.40, 32, 2, 0.90,  1, .48),
    (   0,  16, 66, 1.25, 24, 2, 3.60, -1, .38),
    ( 146,  74, 54, 1.20, 19, 2, 1.40,  1, .32),
    ( 282,  84, 46, 1.15, 16, 2, 4.40, -1, .28),
    (  36,  96, 38, 1.10, 13, 1, 0.30,  1, .24),
    ( 366,  92, 40, 1.10, 14, 1, 2.70,  1, .24),
]

# Volutas da faixa lateral: mesmo gesto, girado para descer pela borda.
_VOLUTAS_LADO = [
    (  40,  74, 74, 1.35, 27, 2, 1.60,  1, .46),
    (  24, 206, 62, 1.25, 22, 2, 4.10, -1, .40),
    (  52, 330, 70, 1.30, 25, 2, 0.50,  1, .42),
    (   8,   0, 52, 1.20, 18, 2, 2.90,  1, .32),
    (  74, 142, 42, 1.15, 15, 1, 5.00, -1, .26),
    (  70, 272, 38, 1.10, 13, 1, 1.20,  1, .24),
]

_ENGRENAGENS_LADO = [
    (  2,   0, 58, 46, 12, 15, 0.20, .34),
    ( 14, 196, 44, 35, 11, 12, 0.44, .30),
    ( -8, 300, 30, 23,  9,  8, 0.10, .24),
    ( 40,  96, 20, 15,  8,  5, 0.62, .20),
    ( 34, 348, 15, 11,  7,  4, 0.35, .18),
]


def _defs(seed, escala_desloc, dissolve_stops, id_grad='d'):
    """Filtro de torção + máscara de dissolução.

    O ruído aqui NÃO borra: ele desloca. `feDisplacementMap` empurra cada pixel
    da voluta segundo o ruído, de modo que a espiral continua legível como
    espiral, mas com a borda esgarçada de bruma. Borrão apagava o desenho; era
    esse o defeito da v1.
    """
    paradas = "".join(
        f"<stop offset='{o}' stop-color='white' stop-opacity='{op}'/>"
        for o, op in dissolve_stops)
    return (
      "<defs>"
        f"<filter id='t' x='-25%' y='-25%' width='150%' height='150%'>"
          f"<feTurbulence type='fractalNoise' baseFrequency='0.012 0.026' numOctaves='4'"
          f" seed='{seed}' stitchTiles='stitch' result='r'/>"
          f"<feDisplacementMap in='SourceGraphic' in2='r' scale='{escala_desloc}'"
          f" xChannelSelector='R' yChannelSelector='G'/>"
          "<feGaussianBlur stdDeviation='0.9'/>"
        "</filter>"
        f"<linearGradient id='{id_grad}' x1='0' y1='0' x2='0' y2='1'>{paradas}</linearGradient>"
        f"<mask id='m'><rect width='100%' height='100%' fill='url(%23{id_grad})'/></mask>"
      "</defs>")


def _defs_lado(seed, escala_desloc, dissolve_stops):
    paradas = "".join(
        f"<stop offset='{o}' stop-color='white' stop-opacity='{op}'/>"
        for o, op in dissolve_stops)
    return (
      "<defs>"
        f"<filter id='t' x='-25%' y='-25%' width='150%' height='150%'>"
          f"<feTurbulence type='fractalNoise' baseFrequency='0.020 0.011' numOctaves='4'"
          f" seed='{seed}' stitchTiles='stitch' result='r'/>"
          f"<feDisplacementMap in='SourceGraphic' in2='r' scale='{escala_desloc}'"
          f" xChannelSelector='R' yChannelSelector='G'/>"
          "<feGaussianBlur stdDeviation='0.9'/>"
        "</filter>"
        # dissolução horizontal: dentro da ficha a bruma acaba
        f"<linearGradient id='d' x1='0' y1='0' x2='1' y2='0'>{paradas}</linearGradient>"
        f"<mask id='m'><rect width='100%' height='100%' fill='url(%23d)'/></mask>"
      "</defs>")


def banda(topo=True, ferro='%23b3a196', nevoa='%23e8ddd0', op_nevoa=0.55, seed=7):
    """Faixa horizontal: engrenagens submersas em volutas de bruma."""
    corpos = rodas(_ENGRENAGENS_TOPO, L, 'x')
    defs = _defs(seed, 7, [(0, .95), (0.30, .52), (0.62, .16), (1, 0)])
    svg = (
      f"<svg xmlns='http://www.w3.org/2000/svg' width='{L}' height='{A}' viewBox='0 0 {L} {A}'>"
      f"{defs}"
      f"<g mask='url(%23m)' fill='{ferro}'>{corpos}</g>"
      f"<g mask='url(%23m)' fill='{nevoa}' opacity='{op_nevoa}' filter='url(%23t)'>"
      f"{bruma(_VOLUTAS_TOPO, L, 'x')}</g>"
      "</svg>")
    if not topo:
        svg = svg.replace(f"viewBox='0 0 {L} {A}'>",
                          f"viewBox='0 0 {L} {A}'><g transform='translate(0,{A}) scale(1,-1)'>")
        svg = svg.replace("</svg>", "</g></svg>")
    return svg


def lateral(direita=False, ferro='%23b3a196', nevoa='%23e8ddd0', op_nevoa=0.5, seed=11):
    """Faixa vertical: a bruma desce pela borda e dissolve para o miolo."""
    corpos = rodas(_ENGRENAGENS_LADO, LA, 'y')
    defs = _defs_lado(seed, 6, [(0, .92), (0.34, .46), (0.68, .12), (1, 0)])
    svg = (
      f"<svg xmlns='http://www.w3.org/2000/svg' width='{LL}' height='{LA}' viewBox='0 0 {LL} {LA}'>"
      f"{defs}"
      f"<g mask='url(%23m)' fill='{ferro}'>{corpos}</g>"
      f"<g mask='url(%23m)' fill='{nevoa}' opacity='{op_nevoa}' filter='url(%23t)'>"
      f"{bruma(_VOLUTAS_LADO, LA, 'y')}</g>"
      "</svg>")
    if direita:
        svg = svg.replace(f"viewBox='0 0 {LL} {LA}'>",
                          f"viewBox='0 0 {LL} {LA}'><g transform='translate({LL},0) scale(-1,1)'>")
        svg = svg.replace("</svg>", "</g></svg>")
    return svg


def fuligem(op=0.05):
    """Grão fino para o fundo da ficha. Ladrilha e some: é textura, não desenho."""
    return ("<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'>"
      "<filter id='f' x='0' y='0' width='100%' height='100%'>"
        "<feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/>"
        "<feColorMatrix type='saturate' values='0'/></filter>"
      f"<rect width='180' height='180' filter='url(%23f)' opacity='{op}'/></svg>")


def uri(svg):
    return 'url("data:image/svg+xml,' + urllib.parse.quote(svg, safe="=:/?&;,'%<>()#.- ") + '")'


# ------------------------------------------------------------------ variantes
# Cada tema tem sua tinta. O desenho é o mesmo; muda a cor do ferro, a cor da
# bruma e a força dela.
VARIANTES = {
    # ferrugem escura: ferro claro, bruma clara
    'ferrugem':  dict(ferro='%23b3a196', nevoa='%23efe6da', op_nevoa=0.52, seed=7),
    # negativo: chapa em brasa, ferro e fumaça quase pretos
    'negativo':  dict(ferro='%233a2110', nevoa='%23241207', op_nevoa=0.46, seed=13),
    # registro portuário: papel bege, metal escuro, bruma cinza-quente
    'registro':  dict(ferro='%238a5a44', nevoa='%237a6353', op_nevoa=0.34, seed=19),
}


# ============================================================================
# v3 — bruma no vocabulário das referências de Mario (Mists-001/002/003)
# ============================================================================
import bruma as _B

L3, A3 = 800, 200        # faixa horizontal: ladrilho mais largo, menos repetição
LL3, LA3 = 150, 460      # faixa lateral

def _defs_motivos(corpo, luz, crista):
    """A geometria do motivo entra no arquivo UMA vez, e cada aparição é um
    `<use>` com transform.

    Sem isso o ladrilho pesava 368 KB: sete motivos, cada um com cinco fitas de
    três camadas, repetidos nas bordas. Como todas as aparições são o mesmo
    desenho em outra escala, posição ou espelho, guardar a geometria uma vez e
    instanciá-la custa uma linha por aparição.

    A opacidade fica no `<use>`, e as camadas internas guardam só a RAZÃO entre
    si. Assim a densidade muda por instância sem perder o volume da fita, e
    duas instâncias sobrepostas continuam somando.
    """
    def corpo_svg(**kw):
        return "".join(_B.fita(p, w, corpo, luz, crista, op=1.0)
                       for p, w in _B.motivo(**kw))
    return ("<g id='mv'>"  + corpo_svg() + "</g>"
            "<g id='mvs'>" + corpo_svg(com_funil=False) + "</g>")


def _usos(motivos, periodo, eixo_):
    """Uma linha `<use>` por aparição, replicada nas bordas do ladrilho."""
    out = []
    for m in motivos:
        cfg = dict(m)
        op = cfg['op']; esc = cfg.get('escala', 1.0)
        alvo = '%23mvs' if cfg.get('com_funil') is False else '%23mv'
        esp = -1 if cfg.get('espelha') else 1
        base_x, base_y = cfg.get('dx', 0), cfg.get('dy', 0)
        alcance = 340*esc
        for k in (-1, 0, 1):
            c = (base_x if eixo_ == 'x' else base_y) + k*periodo
            if k and not (c - alcance < periodo and c + alcance > 0):
                continue
            x = base_x + (k*periodo if eixo_ == 'x' else 0)
            y = base_y + (k*periodo if eixo_ == 'y' else 0)
            out.append(f"<use href='{alvo}' opacity='{op}' transform="
                       f"'translate({x:.0f} {y:.0f}) scale({esc*esp:.2f} {esc:.2f})'/>")
    return "".join(out)


# Motivos da faixa horizontal. Dois planos: os de trás são maiores e mais
# ralos; os da frente, menores e mais densos. É a diferença de escala e de
# densidade que dá profundidade, não o desfoque sozinho.
# Poucos e GRANDES. Muitos motivos pequenos liam-se como rabisco espalhado; a
# referência tem duas ou três massas que varrem o quadro inteiro. O corte da
# máscara é aliado: o motivo nasce fora da folha e só entra pela borda.
_FUNDO_TOPO = [
    dict(escala=1.25, dx=110, dy=-118, op=0.26, semente=0),
    dict(escala=1.05, dx=520, dy=-96,  op=0.24, espelha=True, semente=1),
]
_FRENTE_TOPO = [
    dict(escala=0.86, dx=320, dy=-64, op=0.30, espelha=True, semente=1),
    dict(escala=0.74, dx=700, dy=-52, op=0.28, semente=2),
    dict(escala=0.58, dx= 20, dy=-30, op=0.26, espelha=True, semente=0,
         com_funil=False),
]

_FUNDO_LADO = [
    dict(escala=0.92, dx=-30, dy= 20, op=0.26, semente=0),
    dict(escala=0.78, dx= 24, dy=250, op=0.24, espelha=True, semente=2),
]
_FRENTE_LADO = [
    dict(escala=0.62, dx= 10, dy=130, op=0.30, espelha=True, semente=1),
    dict(escala=0.50, dx=-24, dy=340, op=0.28, semente=0, com_funil=False),
]

# As engrenagens da faixa larga: as mesmas rodas, espalhadas em 800.
_RODAS_TOPO_800 = [
    (  0,  10, 84, 68, 16, 22, 0.10, .40),
    (118, -14, 62, 49, 13, 16, 0.34, .36),
    (196,  30, 40, 31, 10, 11, 0.62, .30),
    (272, -20, 70, 56, 14, 18, 0.21, .34),
    ( 58,  46, 27, 20,  9,  7, 0.50, .24),
    (162,  52, 20, 15,  8,  5, 0.15, .22),
    (238, -46, 34, 26,  9,  9, 0.44, .26),
    (330,  40, 33, 25,  9,  9, 0.08, .22),
    (368,  -4, 22, 16,  8,  6, 0.30, .20),
    (446,  16, 74, 59, 15, 19, 0.27, .36),
    (540, -26, 52, 41, 12, 14, 0.51, .30),
    (612,  34, 38, 29, 10, 10, 0.12, .26),
    (700, -12, 66, 53, 14, 17, 0.40, .34),
    (766,  44, 25, 19,  9,  6, 0.66, .22),
    (504,  58, 18, 13,  8,  5, 0.20, .20),
    (664,  62, 16, 12,  7,  4, 0.72, .18),
]


def _defs3(seed, largura, altura, horizontal=True, motivos=''):
    """Só a máscara de dissolução. A v2 torcia a bruma com deslocamento de
    ruído; aqui a forma é o desenho, e ruído por cima só a suja."""
    x1, y1, x2, y2 = ("0", "0", "0", "1") if horizontal else ("0", "0", "1", "0")
    return (
      "<defs>"
        f"<linearGradient id='d' x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}'>"
          "<stop offset='0' stop-color='white' stop-opacity='1'/>"
          "<stop offset='0.42' stop-color='white' stop-opacity='0.72'/>"
          "<stop offset='0.74' stop-color='white' stop-opacity='0.26'/>"
          "<stop offset='1' stop-color='white' stop-opacity='0'/>"
        "</linearGradient>"
        "<mask id='m'><rect width='100%' height='100%' fill='url(%23d)'/></mask>"
        "<filter id='b' x='-15%' y='-15%' width='130%' height='130%'>"
          "<feGaussianBlur stdDeviation='2.2'/></filter>"
        + motivos +
      "</defs>")


def banda3(topo=True, ferro='%23b3a196', corpo='%23a2947f', luz='%23cdc0af',
           crista='%23f0e7db', seed=7):
    """Faixa horizontal em três planos: bruma atrás, engrenagens, bruma à frente.

    A ordem é o ponto todo. A bruma que passa POR TRÁS das rodas some sob elas;
    a que passa PELA FRENTE cobre o dente. Ver as duas coisas ao mesmo tempo é o
    que faz a névoa parecer envolver o mecanismo em vez de estar colada num
    plano só atrás dele.
    """
    fundo  = _usos(_FUNDO_TOPO,  L3, 'x')
    frente = _usos(_FRENTE_TOPO, L3, 'x')
    rodas_ = rodas(_RODAS_TOPO_800, L3, 'x')
    svg = (
      f"<svg xmlns='http://www.w3.org/2000/svg' width='{L3}' height='{A3}' viewBox='0 0 {L3} {A3}'>"
      f"{_defs3(seed, L3, A3, True, _defs_motivos(corpo, luz, crista))}"
      f"<g mask='url(%23m)'>"
        f"<g filter='url(%23b)'>{fundo}</g>"
        f"<g fill='{ferro}'>{rodas_}</g>"
        f"{frente}"
      "</g></svg>")
    if not topo:
        svg = svg.replace(f"viewBox='0 0 {L3} {A3}'>",
                          f"viewBox='0 0 {L3} {A3}'><g transform='translate(0,{A3}) scale(1,-1)'>")
        svg = svg.replace("</svg>", "</g></svg>")
    return svg


_RODAS_LADO_460 = [
    (  2,   0, 58, 46, 12, 15, 0.20, .34),
    ( 14, 216, 44, 35, 11, 12, 0.44, .30),
    ( -8, 330, 30, 23,  9,  8, 0.10, .24),
    ( 46, 106, 20, 15,  8,  5, 0.62, .20),
    ( 38, 386, 15, 11,  7,  4, 0.35, .18),
    ( 20, 148, 34, 27,  9,  9, 0.55, .22),
]


def lateral3(direita=False, ferro='%23b3a196', corpo='%23a2947f', luz='%23cdc0af',
             crista='%23f0e7db', seed=11):
    """Faixa vertical: mesmo empilhamento, dissolvendo da borda para o miolo."""
    fundo  = _usos(_FUNDO_LADO,  LA3, 'y')
    frente = _usos(_FRENTE_LADO, LA3, 'y')
    rodas_ = rodas(_RODAS_LADO_460, LA3, 'y')
    svg = (
      f"<svg xmlns='http://www.w3.org/2000/svg' width='{LL3}' height='{LA3}' viewBox='0 0 {LL3} {LA3}'>"
      f"{_defs3(seed, LL3, LA3, False, _defs_motivos(corpo, luz, crista))}"
      f"<g mask='url(%23m)'>"
        f"<g filter='url(%23b)'>{fundo}</g>"
        f"<g fill='{ferro}'>{rodas_}</g>"
        f"{frente}"
      "</g></svg>")
    if direita:
        svg = svg.replace(f"viewBox='0 0 {LL3} {LA3}'>",
                          f"viewBox='0 0 {LL3} {LA3}'><g transform='translate({LL3},0) scale(-1,1)'>")
        svg = svg.replace("</svg>", "</g></svg>")
    return svg


# Cada tema tem sua tinta de bruma: corpo, lado claro e crista.
VARIANTES3 = {
    'ferrugem': dict(ferro='%23b3a196', corpo='%23a2947f', luz='%23cdc0af',
                     crista='%23f0e7db', seed=7),
    'negativo': dict(ferro='%233a2110', corpo='%234a2c14', luz='%23331c0c',
                     crista='%23241207', seed=13),
    'registro': dict(ferro='%238a5a44', corpo='%23a08876', luz='%238a7160',
                     crista='%236b5445', seed=19),
}


if __name__ == "__main__":
    import pathlib
    saida = pathlib.Path(__file__).parent
    for nome, cfg in VARIANTES3.items():
        (saida / f"topo-{nome}.uri").write_text(uri(banda3(True, **cfg)), encoding="utf-8")
        (saida / f"rodape-{nome}.uri").write_text(uri(banda3(False, **cfg)), encoding="utf-8")
        (saida / f"lado-esq-{nome}.uri").write_text(uri(lateral3(False, **cfg)), encoding="utf-8")
        (saida / f"lado-dir-{nome}.uri").write_text(uri(lateral3(True, **cfg)), encoding="utf-8")
    (saida / "fuligem.uri").write_text(uri(fuligem()), encoding="utf-8")
    (saida / "fuligem-claro.uri").write_text(uri(fuligem(0.045)), encoding="utf-8")
    print("grafismos gerados:", len(VARIANTES), "variantes")
