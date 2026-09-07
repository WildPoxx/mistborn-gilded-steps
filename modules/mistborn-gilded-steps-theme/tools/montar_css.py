# -*- coding: utf-8 -*-
"""Monta o CSS do tema embutindo os grafismos gerados por grafismo.py.
Rodar este script é o jeito de regerar a folha; não edite os data: URI à mão."""
import io

topo    = open('topo.uri',          encoding='utf-8').read()
rodape  = open('rodape.uri',        encoding='utf-8').read()
topo_c  = open('topo-claro.uri',    encoding='utf-8').read()
rodape_c= open('rodape-claro.uri',  encoding='utf-8').read()
fuligem = open('fuligem.uri',       encoding='utf-8').read()

CAB = '''/*
 * Mistborn Gilded Steps — tema para Cosmere RPG em Foundry VTT 13.351
 * Versão 0.2.0 — proposta, não homologada.
 *
 * REGENERAÇÃO
 * Os desenhos deste arquivo NÃO foram escritos à mão. Saem de
 * `09_Midia e Assets/Theme - Mistborn Gilded Steps/gerador/grafismo.py`, que
 * calcula os dentes das engrenagens e monta a névoa, e de `montar_css.py`, que
 * costura tudo aqui. Para mudar o desenho, mexa no gerador e rode de novo —
 * editar um `data:` URI à mão é como editar um JPEG no bloco de notas.
 *
 * O QUE ESTE ARQUIVO FAZ
 * Só redefine valores. Nenhuma regra toca em `display`, `position`, `flex`,
 * `grid`, `width` ou `height`: o HTML da ficha é do sistema Cosmere e muda a
 * cada versão dele. (Regra da caixa, SPEC-01 §3.1 do projeto Skin Forge.)
 *
 * COMO ELE SE PRENDE
 * O sistema define suas cores em `:root { .cosmere-theme-default { &.theme-dark
 * {...} } }`, o que compila com especificidade (0,3,0). Um seletor
 * `body.cosmere-theme-default.theme-dark` daria (0,2,1) e PERDERIA. Por isso o
 * `:root` na frente: `:root body.cosmere-theme-default.theme-dark` dá (0,3,1) e
 * vence por um elemento. Quem "limpar" esse `:root` achando que é redundante
 * desliga o tema inteiro, em silêncio.
 *
 * OS GRAFISMOS
 * Engrenagens submersas em névoa, no topo e no rodapé — as duas únicas faixas
 * ancoradas que o sistema expõe (`.banners .top` e `.bot`, 200px cada, largura
 * inteira, sem `background-size` nem `background-repeat` declarados). Por isso o
 * desenho é um ladrilho de 400×200 que emenda sozinho na horizontal: a
 * engrenagem cortada na borda direita é completada pela cópia seguinte, e o
 * ruído da névoa usa `stitchTiles` para não deixar costura.
 *
 * NAS LATERAIS não há faixa ancorada. Uma camada de imagem no fundo da ficha
 * ladrilharia a ficha inteira em vez de ficar na borda — foi testado, e vira
 * neblina em cima do texto. As laterais recebem névoa em gradiente, que se
 * ancora sozinho na caixa. Engrenagem nas bordas exigiria o módulo inserir
 * elemento próprio na ficha, e aí deixa de ser pele.
 *
 * Tudo é procedural: gradientes e SVG em `data:` URI. Nenhum arquivo de imagem,
 * nenhuma fonte, nenhuma chamada remota, nenhuma licença de terceiro.
 *
 * AS VARIAÇÕES DE METAL
 * `--mgs-metal` é o único valor que uma variação troca. Prata, ouro, cobre e
 * estanho mudam a cor de destaque e o banho de luz sobre as engrenagens; o ferro
 * das peças continua ferro nas quatro. Os quatro valores foram medidos: nenhum
 * fica abaixo de 4,5:1 sobre a folha nem sobre o painel mais escuro, nos dois
 * modos.
 */

'''

def bloco(modo, tokens, mapa, metal_padrao, tinta_metal, vinheta, mist_lateral, faixa_topo, faixa_rodape):
    L=[]
    L.append(f":root body.cosmere-theme-default.theme-{modo} {{")
    L.append(tokens)
    L.append(f"\n  /* Metal da ficha. É o único valor que as variações trocam. */")
    L.append(f"  --mgs-metal: {metal_padrao};")
    L.append(mapa)
    L.append(f"""
  /* --- Grafismos. Engrenagens na névoa, topo e rodapé; névoa nas laterais. --- */
  --cosmere-banner-actor-top:
    linear-gradient(180deg, color-mix(in srgb, var(--mgs-metal) {tinta_metal}, transparent) 0%, transparent 56%),
    {faixa_topo};
  --cosmere-banner-actor-bot:
    linear-gradient(0deg, color-mix(in srgb, var(--mgs-metal) {tinta_metal}, transparent) 0%, transparent 56%),
    {faixa_rodape};
  --cosmere-banner-item-top:
    linear-gradient(180deg, color-mix(in srgb, var(--mgs-metal) {tinta_metal}, transparent) 0%, transparent 56%),
    {faixa_topo};
  --cosmere-sheet-texture:
    linear-gradient(to right, {mist_lateral} 0, transparent 15%, transparent 85%, {mist_lateral} 100%),
    radial-gradient(130% 108% at 50% 46%, transparent 48%, {vinheta} 100%),
    {fuligem};""")
    L.append("}\n")
    return "\n".join(L)

TOK_ESC = """  /* --- Ferrugem: a superfície da ficha é ferro oxidado, não ferro limpo.
         Marrom-avermelhado puxado para o alaranjado, escurecendo até quase
         preto. Decisão de Mario, 2026-09-07 — escolhida entre duas
         temperaturas; a variante mais escura e amarronzada foi recusada. --- */
  --mgs-rust-990: #1a0e08;
  --mgs-rust-950: #231409;
  --mgs-rust-900: #301c0f;
  --mgs-rust-850: #3b2312;
  --mgs-rust-800: #472a15;
  --mgs-rust-700: #5f3a1d;
  --mgs-rust-line: #94684a;

  /* Névoa e bruma, agora quentes: cinza frio sobre ferrugem briga. */
  --mgs-fog: #d6c8b8;
  --mgs-mist: #bda893;
  --mgs-paper: #e8e2d5;

  --mgs-brass: #b88940;
  --mgs-brass-bright: #dfba69;
  --mgs-verdigris: #4e8d85;
  --mgs-verdigris-bright: #6fb3a9;
  --mgs-danger: #a43d36;
  --mgs-danger-bright: #e08a80;"""

MAPA_ESC = """
  /* --- Superfícies --- */
  --cosmere-color-sheet: var(--mgs-rust-950);
  --cosmere-color-base-1: var(--mgs-rust-800);
  --cosmere-color-base-2: var(--mgs-rust-990);
  --cosmere-color-base-3: var(--mgs-rust-900);
  --cosmere-color-base-4: var(--mgs-rust-850);
  --cosmere-color-base-5: var(--mgs-rust-line);
  --cosmere-color-base-6: var(--mgs-rust-700);
  --cosmere-color-neutral: var(--mgs-rust-950);

  /* --- Tinta --- */
  --cosmere-color-text-main: var(--mgs-paper);
  --cosmere-color-text-sub: var(--mgs-fog);
  --cosmere-color-faded: var(--mgs-mist);
  --cosmere-color-text-accent: var(--mgs-metal);
  --cosmere-color-accent: var(--mgs-metal);
  --cosmere-color-highlight: var(--mgs-verdigris-bright);

  /* --- Barras. Claras de propósito: o sistema usa estas três também como TINTA
         de texto nos cartões de chat, sobre a folha escura. --- */
  /* O verde subiu de #5f9c83 para cá: sobre a ferrugem alaranjada, o tom
     anterior media 4,08:1 no painel mais claro. Este mede 4,89:1. */
  --cosmere-color-health-front: #6cab90;
  --cosmere-color-health-back: #5a2415;
  --cosmere-color-focus-front: #8b9c9e;
  --cosmere-color-focus-back: #362a1f;
  --cosmere-color-invest-front: var(--mgs-brass);
  --cosmere-color-invest-back: #4a3213;

  /* --- Dado de trama --- */
  --cosmere-color-complication: var(--mgs-danger);
  --cosmere-color-complication-text: var(--mgs-danger-bright);
  --cosmere-color-complication-background-dark: #35120a;
  --cosmere-color-opportunity: #26403c;
  --cosmere-color-opportunity-text: var(--mgs-verdigris-bright);
  --cosmere-color-opportunity-background-dark: #16201c;

  --cosmere-color-turn-fast: var(--mgs-brass);
  --cosmere-color-turn-slow: var(--mgs-rust-700);
  --cosmere-color-parchment: var(--mgs-paper);"""

TOK_CLA = """  /* --- Bege, linha vermelha, tinta marrom. O par claro do ferrugem:
         papel de registro portuário pautado a lápis vermelho.
         Decisão de Mario, 2026-09-07. --- */
  --mgs-bege-claro: #f6efe1;
  --mgs-bege: #ece2cf;
  --mgs-bege-painel: #e6dac4;
  --mgs-bege-sombra: #ddceb4;
  --mgs-bege-fundo: #d2c0a2;

  /* A linha é vermelha: é ela que desenha molduras, filetes e divisórias. */
  --mgs-linha-vermelha: #a33a2a;
  --mgs-linha-forte: #7a2b1f;

  /* Tinta: marrom muito escuro, quase preto. */
  --mgs-tinta: #2a1a12;
  --mgs-tinta-sub: #4a3223;
  --mgs-tinta-fraca: #61402c;

  --mgs-danger: #8b271d;"""

MAPA_CLA = """
  --cosmere-color-sheet: var(--mgs-bege);
  --cosmere-color-base-1: var(--mgs-bege-fundo);
  --cosmere-color-base-2: var(--mgs-bege-claro);
  --cosmere-color-base-3: var(--mgs-bege-painel);
  --cosmere-color-base-4: var(--mgs-bege-sombra);
  /* base-5 e base-6 são as duas famílias de filete do sistema: aqui, vermelhas. */
  --cosmere-color-base-5: var(--mgs-linha-vermelha);
  --cosmere-color-base-6: var(--mgs-linha-forte);
  --cosmere-color-neutral: var(--mgs-bege-sombra);

  --cosmere-color-text-main: var(--mgs-tinta);
  --cosmere-color-text-sub: var(--mgs-tinta-sub);
  --cosmere-color-faded: var(--mgs-tinta-fraca);
  --cosmere-color-text-accent: var(--mgs-metal);
  --cosmere-color-accent: var(--mgs-metal);
  --cosmere-color-highlight: var(--mgs-linha-vermelha);

  /* Medidas sobre o painel mais escuro do bege (#d2c0a2), que é o pior caso. */
  --cosmere-color-health-front: #284d3f;   /* 5,31 */
  --cosmere-color-health-back: #b09a7c;
  --cosmere-color-focus-front: #44525a;    /* 4,54 */
  --cosmere-color-focus-back: #c3bfb4;
  --cosmere-color-invest-front: var(--mgs-metal);
  --cosmere-color-invest-back: #c9b795;

  --cosmere-color-complication: var(--mgs-danger);
  --cosmere-color-complication-text: var(--mgs-danger);
  --cosmere-color-complication-background: #f0d8ce;
  --cosmere-color-opportunity: #1b4f4e;
  --cosmere-color-opportunity-text: #1b4f4e;
  --cosmere-color-opportunity-background: #d5e0dc;

  --cosmere-color-turn-fast: var(--mgs-metal);
  --cosmere-color-turn-slow: var(--mgs-linha-forte);
  --cosmere-color-parchment: var(--mgs-bege-claro);"""

VARIACOES = """
/* =======================================================================
   VARIAÇÕES DE METAL
   Uma variação troca UM valor. Se a classe nunca chegar — porque o módulo
   perdeu o gancho, por exemplo — nada quebra: fica o ouro, que é o padrão.

   Dois lugares aceitam a classe:
   - no <body>, e vale para todas as fichas do mundo;
   - na PRÓPRIA FICHA (`.application.cosmere-rpg`), e vale só para aquele
     personagem. É assim que cada ficha ganha o metal do seu portador.
   A regra da ficha vence a do body porque redefine `--mgs-metal` num elemento
   mais fundo: o valor é substituído onde é usado, dentro da ficha.
   Contraste medido de cada metal, como tinta, sobre a folha e sobre o painel
   mais escuro de cada modo. Nenhum abaixo de 4,5:1.
   ======================================================================= */

:root body.cosmere-theme-default.theme-dark.mgs-metal-prata   { --mgs-metal: #c2ced0; } /* 11,24 e 10,28 */
:root body.cosmere-theme-default.theme-dark.mgs-metal-ouro    { --mgs-metal: #dfba69; } /*  9,80 e  8,97 */
:root body.cosmere-theme-default.theme-dark.mgs-metal-cobre   { --mgs-metal: #d68258; } /*  6,20 e  5,68 */
:root body.cosmere-theme-default.theme-dark.mgs-metal-estanho { --mgs-metal: #6fb3a9; } /*  7,50 e  6,86 */

:root body.cosmere-theme-default.theme-light.mgs-metal-prata   { --mgs-metal: #3a4749; } /* 7,51 e 5,42 */
:root body.cosmere-theme-default.theme-light.mgs-metal-ouro    { --mgs-metal: #6b3f16; } /* 6,96 e 5,03 */
:root body.cosmere-theme-default.theme-light.mgs-metal-cobre   { --mgs-metal: #8c2f10; } /* 6,46 e 4,67 */
:root body.cosmere-theme-default.theme-light.mgs-metal-estanho { --mgs-metal: #1b4f4e; } /* 7,19 e 5,19 */

/* Por personagem: a classe vai na janela da ficha, não no corpo do documento. */

body.theme-dark  .application.cosmere-rpg.mgs-metal-prata   { --mgs-metal: #c2ced0; }
body.theme-dark  .application.cosmere-rpg.mgs-metal-ouro    { --mgs-metal: #dfba69; }
body.theme-dark  .application.cosmere-rpg.mgs-metal-cobre   { --mgs-metal: #d68258; }
body.theme-dark  .application.cosmere-rpg.mgs-metal-estanho { --mgs-metal: #6fb3a9; }

body.theme-light .application.cosmere-rpg.mgs-metal-prata   { --mgs-metal: #3a4749; }
body.theme-light .application.cosmere-rpg.mgs-metal-ouro    { --mgs-metal: #6b3f16; }
body.theme-light .application.cosmere-rpg.mgs-metal-cobre   { --mgs-metal: #8c2f10; }
body.theme-light .application.cosmere-rpg.mgs-metal-estanho { --mgs-metal: #1b4f4e; }
"""

css = (CAB
  + "/* =======================================================================\n"
    "   MODO ESCURO — o padrão da ficha Cosmere\n"
    "   ======================================================================= */\n\n"
  + bloco("dark", TOK_ESC, MAPA_ESC, "#dfba69", "11%", "rgb(12 5 3 / 34%)", "rgb(214 192 176 / 13%)", topo, rodape)
  + "\n/* =======================================================================\n"
    "   MODO CLARO — papel de registro portuário\n"
    "   ======================================================================= */\n\n"
  + bloco("light", TOK_CLA, MAPA_CLA, "#6b3f16", "9%", "rgb(90 40 24 / 15%)", "rgb(163 58 42 / 9%)", topo_c, rodape_c)
  + VARIACOES)

open('/home/claude/mgs-theme/styles/mistborn-gilded-steps-theme.css','w',encoding='utf-8',newline='\n').write(css)
print("CSS montado:", len(css), "caracteres")
