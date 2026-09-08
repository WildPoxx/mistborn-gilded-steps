# -*- coding: utf-8 -*-
"""Razão de contraste WCAG entre valores de token. Não substitui a medição em
pixel renderizado; serve para escolher candidatos antes de renderizar."""
def lum(h):
    h = h.lstrip('#')
    c = [int(h[i:i+2],16)/255 for i in (0,2,4)]
    c = [v/12.92 if v <= 0.04045 else ((v+0.055)/1.055)**2.4 for v in c]
    return 0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2]
def cr(a,b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la+0.05)/(lb+0.05)
if __name__ == '__main__':
    fundos = {'folha':'#e2913f','claro':'#f2b063','painel':'#d8823a','sombra':'#c4702e','fundo':'#ad5f24'}
    tintas = {'tinta':'#241207','sub':'#3d2410','fraca':'#5a3616','linha':'#7a2b1f','linha-forte':'#5c1d14',
              'prata':'#33403f','ouro':'#5e3a10','cobre':'#7a2a0d','estanho':'#12403e',
              'verde':'#1d4536','azul':'#26383f'}
    print(f"{'':14}" + "".join(f"{k:>9}" for k in fundos))
    for tn, tv in tintas.items():
        piores = [cr(tv, fv) for fv in fundos.values()]
        print(f"{tn:14}" + "".join(f"{v:9.2f}" for v in piores) + f"   pior={min(piores):.2f}")
