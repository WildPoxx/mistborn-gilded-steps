"""Gera os grafismos do tema: engrenagens e névoa, em SVG procedural.
Nada de arquivo de imagem — a saída é um data: URI que vive dentro do CSS."""
import math, urllib.parse

def engrenagem(cx, cy, r_ext, r_int, dentes, r_furo, giro=0.0):
    """Caminho SVG de uma engrenagem: coroa dentada + furo central.
    Os dentes são trapézios entre o raio interno e o externo."""
    p = []
    passo = 2*math.pi/dentes
    # largura angular do dente na base e no topo (topo mais estreito = trapézio)
    base, topo = passo*0.30, passo*0.19
    for i in range(dentes):
        a = giro + i*passo
        for ang, r in ((a-base, r_int), (a-topo, r_ext), (a+topo, r_ext), (a+base, r_int)):
            x, y = cx + r*math.cos(ang), cy + r*math.sin(ang)
            p.append(f"{'M' if (i==0 and ang==a-base) else 'L'}{x:.1f} {y:.1f}")
        # arco do vale até o próximo dente
        a2 = a + passo - base
        p.append(f"A{r_int:.1f} {r_int:.1f} 0 0 1 {cx + r_int*math.cos(a2):.1f} {cy + r_int*math.sin(a2):.1f}")
    p.append("Z")
    # furo central, sentido inverso para vazar (fill-rule evenodd)
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
        x1,y1 = cx+dx*r1, cy+dy*r1
        x2,y2 = cx+dx*r2, cy+dy*r2
        out.append(f"M{x1+nx:.1f} {y1+ny:.1f}L{x2+nx:.1f} {y2+ny:.1f}"
                   f"L{x2-nx:.1f} {y2-ny:.1f}L{x1-nx:.1f} {y1-ny:.1f}Z")
    return "".join(out)

L, A = 400, 200          # ladrilho: emenda na horizontal, altura exata da faixa

def banda(topo=True, claro=False):
    """Uma faixa de engrenagens submersas em névoa.
    topo=True: densa em cima, dissolve para baixo. topo=False: espelhada.
    claro=True: metal escuro sobre bege, para o modo claro. O mesmo desenho com
    a tinta invertida — sobre papel, aço claro simplesmente some."""
    # y=0 é a borda externa da ficha nos dois casos; espelhamos no fim.
    pecas = [
        # (cx, cy, r_ext, r_int, dentes, furo, giro, opacidade)
        # As duas primeiras são a mesma engrenagem cortada pela emenda: a cópia
        # do ladrilho vizinho completa a metade que falta.
        (  0,  10, 84, 68, 16, 22, 0.10, .34),
        (400,  10, 84, 68, 16, 22, 0.10, .34),
        (118, -14, 62, 49, 13, 16, 0.34, .30),
        (196,  30, 40, 31, 10, 11, 0.62, .26),
        (272, -20, 70, 56, 14, 18, 0.21, .28),
        ( 58,  46, 27, 20,  9,  7, 0.50, .22),
        (162,  52, 20, 15,  8,  5, 0.15, .20),
        (238, -46, 34, 26,  9,  9, 0.44, .22),
        (330,  40, 33, 25,  9,  9, 0.08, .20),
        ( 96,  18, 15, 11,  7,  4, 0.55, .18),
        (368,  -4, 22, 16,  8,  6, 0.30, .18),
        (  8,  70, 17, 12,  7,  4, 0.70, .16),
    ]
    corpos = []
    for cx, cy, re_, ri, d, f, g, op in pecas:
        corpos.append(
            f"<g opacity='{op}'>"
            f"<path fill-rule='evenodd' d='{engrenagem(cx,cy,re_,ri,d,f,g)}'/>"
            f"<path d='{raios(cx,cy,f+2,ri-3,5,max(3,re_*0.10),g)}'/>"
            f"</g>")
    svg = (
      f"<svg xmlns='http://www.w3.org/2000/svg' width='{L}' height='{A}' viewBox='0 0 {L} {A}'>"
      "<defs>"
        # névoa: ruído fractal borrado, o mesmo recurso que faz fumaça em SVG
        "<filter id='n' x='-10%' y='-10%' width='120%' height='120%'>"
          "<feTurbulence type='fractalNoise' baseFrequency='0.005 0.035' numOctaves='5' seed='7' stitchTiles='stitch'/>"
          "<feGaussianBlur stdDeviation='3.5'/>"
          "<feColorMatrix type='saturate' values='0'/>"
          "<feComponentTransfer><feFuncA type='gamma' exponent='1.8' amplitude='1.5'/></feComponentTransfer>"
        "</filter>"
        # o metal só aparece onde a névoa não cobre: gradiente de dissolução
        "<linearGradient id='d' x1='0' y1='0' x2='0' y2='1'>"
          "<stop offset='0' stop-color='white' stop-opacity='0.88'/>"
          "<stop offset='0.24' stop-color='white' stop-opacity='0.38'/>"
          "<stop offset='0.52' stop-color='white' stop-opacity='0.09'/>"
          "<stop offset='1' stop-color='white' stop-opacity='0'/>"
        "</linearGradient>"
        "<mask id='m'><rect width='100%' height='100%' fill='url(%23d)'/></mask>"
      "</defs>"
      # camada 1: engrenagens em ferro, dissolvendo para dentro da ficha
      f"<g mask='url(%23m)' fill='{'%238a5a44' if claro else '%23b3a196'}'>{''.join(corpos)}</g>"
      # camada 2: a névoa passa POR CIMA do metal e o come por partes
      f"<g mask='url(%23m)'><rect width='{L}' height='{A}' filter='url(%23n)' opacity='{0.34 if claro else 0.72}'/></g>"
      "</svg>")
    if not topo:
        # espelha na vertical: a faixa de baixo tem a névoa subindo
        svg = svg.replace(f"viewBox='0 0 {L} {A}'>",
                          f"viewBox='0 0 {L} {A}'><g transform='translate(0,{A}) scale(1,-1)'>")
        svg = svg.replace("</svg>", "</g></svg>")
    return svg

def uri(svg):
    return 'url("data:image/svg+xml,' + urllib.parse.quote(svg, safe="=:/?&;,'%<>()#.- ") + '")'

def fuligem():
    """Grão fino de fuligem para o fundo da ficha. Ladrilha e some: é textura,
    não desenho. As LATERAIS não usam SVG — uma camada de imagem sem controle de
    posição ladrilha a ficha inteira em vez de ficar na borda, e a névoa vira
    neblina em cima do texto. Nas bordas usamos gradiente, que se ancora sozinho."""
    return ("<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'>"
      "<filter id='f' x='0' y='0' width='100%' height='100%'>"
        "<feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/>"
        "<feColorMatrix type='saturate' values='0'/></filter>"
      "<rect width='180' height='180' filter='url(%23f)' opacity='0.05'/></svg>")

if __name__ == "__main__":
    saidas = (("topo", True, False), ("rodape", False, False),
              ("topo-claro", True, True), ("rodape-claro", False, True),
              ("fuligem", None, None))
    for nome, t, cl in saidas:
        u = uri(fuligem() if t is None else banda(t, cl))
        open(f"/home/claude/mgs-theme/gerador/{nome}.uri","w").write(u)
        print(nome, len(u), "caracteres")
