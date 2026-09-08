# -*- coding: utf-8 -*-
"""Volutas de bruma no vocabulário das referências Mists-001/002/003.

v3 (2026-09-08). As espirais da v2 eram fitas de opacidade única: liam-se como
espiral, mas chapadas. As referências que Mario indicou têm quatro traços que a
v2 não tinha, e são eles que fazem a bruma parecer bruma:

  1. o eixo NÃO é uma espiral pura — é um S que só no fim se enrola;
  2. a fita tem VOLUME: um lado claro, um lado escuro, e um fio de luz na crista;
  3. o topo abre em FUNIL, um rolo visto de cima, não um caracol chapado;
  4. saem GAVINHAS ganchudas da silhueta, finas e curtas.

Nada aqui é traçado de arquivo nenhum: o eixo sai da integração de uma função de
curvatura, que é como se desenha uma curva por como ela vira, não por onde ela
passa. É o que permite pedir "vira devagar para a esquerda, depois cada vez mais
rápido para a direita" e receber a linha correspondente.
"""
import math


# --------------------------------------------------------------------- eixo

def eixo(x0, y0, ang0, tramos, passo=3.0):
    """Integra uma curvatura por comprimento de arco e devolve os pontos.

    `tramos` é uma lista de (comprimento, curvatura_inicial, curvatura_final).
    Curvatura positiva vira para um lado, negativa para o outro; zero é reta.
    Um S é um tramo com curvatura de sinal trocado; um rolo é curvatura que
    cresce sem trocar de sinal.
    """
    pts = [(x0, y0)]
    ang = ang0
    x, y = x0, y0
    for comp, k0, k1 in tramos:
        n = max(2, int(comp/passo))
        for i in range(n):
            s = i/(n-1) if n > 1 else 0.0
            k = k0 + (k1-k0)*s
            ang += k*passo
            x += passo*math.cos(ang)
            y += passo*math.sin(ang)
            pts.append((x, y))
    return pts


def _normais(pts):
    """Normal unitária em cada ponto, pela direção média dos vizinhos."""
    out = []
    n = len(pts)
    for i in range(n):
        a = pts[max(0, i-1)]
        b = pts[min(n-1, i+1)]
        dx, dy = b[0]-a[0], b[1]-a[1]
        h = math.hypot(dx, dy) or 1.0
        out.append((-dy/h, dx/h))
    return out


def perfil(n, w_ini, w_meio, w_fim, expoente=1.6):
    """Largura ao longo da fita: abre, engrossa e afina até nada.

    Não é interpolação linear: a bruma engrossa depressa e afina devagar, e é
    esse desequilíbrio que dá a ponta longa e fina do desenho de referência.
    """
    out = []
    for i in range(n):
        s = i/(n-1) if n > 1 else 0.0
        if s < 0.35:
            t = s/0.35
            out.append(w_ini + (w_meio-w_ini)*(t**0.8))
        else:
            t = (s-0.35)/0.65
            out.append(w_fim + (w_meio-w_fim)*((1-t)**expoente))
    return out


def _lado(pts, nor, larg, fator_ext, fator_int):
    """Contorno fechado entre duas frações da largura (permite fatiar a fita)."""
    ext = [(p[0]+n[0]*w*fator_ext, p[1]+n[1]*w*fator_ext)
           for p, n, w in zip(pts, nor, larg)]
    itn = [(p[0]+n[0]*w*fator_int, p[1]+n[1]*w*fator_int)
           for p, n, w in zip(pts, nor, larg)]
    d = ["M{:.0f} {:.0f}".format(*ext[0])]
    d += ["L{:.0f} {:.0f}".format(*p) for p in ext[1:]]
    d += ["L{:.0f} {:.0f}".format(*p) for p in reversed(itn)]
    d.append("Z")
    return "".join(d)


def fita(pts, larg, cor_corpo, cor_luz, cor_crista, op=1.0, dx=0.0, dy=0.0,
         escala=1.0, giro=0.0):
    """A fita em três camadas: corpo, lado claro e fio de luz na crista.

    É o mínimo para a fita ler como volume e não como recorte de papel. Três
    camadas chapadas custam menos que um gradiente por peça e sobrevivem à
    troca de tema, porque as cores vêm de fora.
    """
    if escala != 1.0 or giro or dx or dy:
        c, s = math.cos(giro), math.sin(giro)
        pts = [((x*c - y*s)*escala + dx, (x*s + y*c)*escala + dy) for x, y in pts]
        larg = [w*escala for w in larg]
    nor = _normais(pts)
    # A transparência vai em `fill-opacity`, path a path — NÃO em `opacity` de
    # grupo. Grupo transparente achata: duas volutas sobrepostas ficam iguais a
    # uma. Path a path, elas SOMAM, e é essa soma que faz bruma parecer bruma —
    # mais densa onde se cruza, rala onde é fiapo solto.
    g = [f"<path fill='{cor_corpo}' fill-opacity='{op:.2f}' "
         f"d='{_lado(pts,nor,larg,-0.5,0.5)}'/>"]
    if cor_luz:
        g.append(f"<path fill='{cor_luz}' fill-opacity='{op*0.85:.2f}' "
                 f"d='{_lado(pts,nor,larg,-0.5,-0.02)}'/>")
    if cor_crista:
        g.append(f"<path fill='{cor_crista}' fill-opacity='{op*0.75:.2f}' "
                 f"d='{_lado(pts,nor,larg,-0.5,-0.36)}'/>")
    return "".join(g)


# ------------------------------------------------------------------ motivos

def voluta_s(comp=680, larg=(3, 52, 1.5), ang0=-1.35, espelha=False):
    """O gesto principal: haste, S, volta longa e rolo.

    As curvaturas estão em 1/px, e é assim que devem ser lidas: 0,008 é uma
    curva de raio 125, quase um arco de horizonte; 0,075 é raio 13, o miolo do
    rolo. Foi a leitura errada dessa escala que fez a primeira tentativa sair
    enrolada como caracol em vez de varrida como bruma.
    """
    f = -1 if espelha else 1
    pts = eixo(0, 0, ang0*f, [
        (comp*0.21, f*0.004, f*0.011),
        (comp*0.26, f*0.011, -f*0.013),
        (comp*0.29, -f*0.013, -f*0.021),
        (comp*0.24, -f*0.021, -f*0.078),
    ])
    return pts, perfil(len(pts), *larg)


def funil(raio=92, achatamento=0.42, voltas=2.1, larg=(26, 22, 2)):
    """O rolo visto de cima: espiral achatada em elipse, que lê como cone.

    O achatamento é o que transforma caracol em funil — sem ele o topo do
    desenho de referência não se distingue de uma espiral qualquer.
    """
    pts = []
    n = 150
    span = voltas*2*math.pi
    for i in range(n):
        t = span*i/(n-1)
        r = raio*math.exp(-1.15*t/span)
        pts.append((r*math.cos(t), r*math.sin(t)*achatamento - t*4.2))
    return pts, perfil(n, *larg)


def gavinha(comp=96, larg=(1.2, 13, 0.8), ang0=0.0, espelha=False):
    """A gavinha ganchuda que sai da silhueta. Curta, fina, e vira muito."""
    f = -1 if espelha else 1
    pts = eixo(0, 0, ang0, [
        (comp*0.5, f*0.012, f*0.030),
        (comp*0.5, f*0.030, f*0.115),
    ])
    return pts, perfil(len(pts), *larg, expoente=2.2)


# ------------------------------------------------------------------ composição

def _ponto_borda(pts, larg, frac, lado=1):
    """Um ponto sobre a BORDA da fita, e a direção normal ali.

    É por aqui que as gavinhas se prendem: na primeira tentativa elas flutuavam
    soltas ao lado da fita, e a referência mostra o contrário — elas se
    destacam da borda, como fiapo que o vento arranca do corpo da bruma.
    """
    i = max(1, min(len(pts)-2, int(frac*(len(pts)-1))))
    a, b = pts[i-1], pts[i+1]
    dx, dy = b[0]-a[0], b[1]-a[1]
    h = math.hypot(dx, dy) or 1.0
    nx, ny = -dy/h, dx/h
    x = pts[i][0] + nx*larg[i]*0.5*lado
    y = pts[i][1] + ny*larg[i]*0.5*lado
    return x, y, math.atan2(dy, dx)


def motivo(escala=1.0, dx=0.0, dy=0.0, espelha=False, com_funil=True,
           gavinhas=((0.30, 1), (0.52, -1), (0.74, 1)), semente=0):
    """O gesto inteiro: funil em cima, fita descendo, rolo no fim, gavinhas
    presas à borda. Devolve uma lista de (pontos, larguras) já posicionada.

    O pescoço abaixo do funil começa grosso de propósito. Fino, o desenho lia
    como cogumelo — haste e chapéu — em vez de uma coluna de bruma que se abre.
    """
    fora = []
    f = -1 if espelha else 1

    pts, larg = voluta_s(comp=560, larg=(16, 46, 1.5), ang0=-1.75)
    pts = [(x, -y) for x, y in pts]          # gira 180°: o rolo vai para baixo
    larg = list(larg)
    if espelha:
        pts = [(-x, y) for x, y in pts]

    def põe(p, w):
        return ([(x*escala + dx, y*escala + dy) for x, y in p],
                [v*escala for v in w])

    for frac, lado in gavinhas:
        gx, gy, ang = _ponto_borda(pts, larg, frac, lado*f)
        gp, gw = gavinha(comp=52 + 26*((semente + int(frac*10)) % 3),
                         espelha=(lado*f < 0))
        c, s = math.cos(ang + 0.9*lado*f), math.sin(ang + 0.9*lado*f)
        gp = [(x*c - y*s + gx, x*s + y*c + gy) for x, y in gp]
        fora.append(põe(*reamostra(gp, gw, 20)))

    fora.append(põe(*reamostra(pts, larg, 52)))

    if com_funil:
        fp, fw = funil(raio=86, achatamento=0.40, voltas=2.1, larg=(24, 20, 2))
        x0, y0 = pts[0]
        if espelha:
            fp = [(-x, y) for x, y in fp]
        fp = [(x + x0, y + y0 + 18) for x, y in fp]
        fora.append(põe(*reamostra(fp, fw, 44)))

    return fora


def reamostra(pts, larg, n):
    """Reduz a poligonal a n pontos, por comprimento de arco.

    O eixo é integrado com passo fino porque a integração precisa disso; o
    DESENHO não. Guardar 280 vértices numa fita de 150px triplicava o tamanho
    do CSS sem mudar um pixel na tela.
    """
    if len(pts) <= n:
        return pts, larg
    acum = [0.0]
    for a, b in zip(pts, pts[1:]):
        acum.append(acum[-1] + math.hypot(b[0]-a[0], b[1]-a[1]))
    total = acum[-1] or 1.0
    saida_p, saida_w, j = [], [], 0
    for i in range(n):
        alvo = total*i/(n-1)
        while j < len(acum)-2 and acum[j+1] < alvo:
            j += 1
        t = (alvo-acum[j])/((acum[j+1]-acum[j]) or 1.0)
        saida_p.append((pts[j][0] + (pts[j+1][0]-pts[j][0])*t,
                        pts[j][1] + (pts[j+1][1]-pts[j][1])*t))
        saida_w.append(larg[j] + (larg[j+1]-larg[j])*t)
    return saida_p, saida_w
