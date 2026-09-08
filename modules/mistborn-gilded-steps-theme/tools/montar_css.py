# -*- coding: utf-8 -*-
"""Monta o CSS do tema embutindo os grafismos gerados por grafismo.py.
Rodar este script é o jeito de regerar a folha; não edite os data: URI à mão.

v0.5.0 (2026-09-08): o tema deixou de sobrescrever o Default do Cosmere e passou
a REGISTRAR temas próprios pela API do sistema. São três entradas na lista, e
cada uma tem seu bloco aqui.
"""
import pathlib

G = pathlib.Path(__file__).parent
def u(n): return G.joinpath(n).read_text(encoding='utf-8')

CAB = '''/*
 * Mistborn Gilded Steps — temas para Cosmere RPG em Foundry VTT 13.351
 * Versão 0.5.0 — proposta, não homologada em runtime.
 *
 * REGENERAÇÃO
 * Os desenhos deste arquivo NÃO foram escritos à mão. Saem de `grafismo.py`,
 * que calcula os dentes das engrenagens e traça as volutas de bruma, e de
 * `montar_css.py`, que costura tudo aqui. Para mudar o desenho, mexa no gerador
 * e rode de novo — editar um `data:` URI à mão é como editar um JPEG no bloco
 * de notas.
 *
 * O QUE ESTE ARQUIVO FAZ
 * Só redefine valores. Nenhuma regra toca em `display`, `position`, `flex`,
 * `grid`, `width` ou `height`: o HTML da ficha é do sistema Cosmere e muda a
 * cada versão dele. As únicas propriedades não-variável aqui são de PINTURA
 * (`background-position`, `-repeat`, `-size`), necessárias porque uma camada de
 * imagem sem posição declarada ladrilha a ficha inteira.
 *
 * COMO ELE SE PRENDE — mudou na v0.5.0
 * Antes, o tema sobrescrevia `.cosmere-theme-default` e precisava vencer uma
 * disputa de especificidade com o próprio sistema. Agora não disputa nada: o
 * Cosmere expõe `cosmereRPG.api.registerTheme()`, e o menu de temas é montado
 * em `registerDeferredSettings()`, no hook `setup` — depois que os módulos
 * carregam. `scripts/metal.mjs` registra três temas no `init`, e o sistema põe
 * a classe `cosmere-theme-<id>` no <body> quando o Mestre escolhe.
 *
 * A consequência importante: o sistema define suas variáveis SÓ dentro de
 * `.cosmere-theme-default`. Um tema nosso não herda nada dele — por isso cada
 * bloco abaixo define o conjunto INTEIRO, e não só as diferenças.
 *
 * DOIS NÍVEIS DE ESCOLHA (v0.6.0)
 * Cada bloco tem dois seletores. `body.cosmere-theme-<id>` é a preferência de
 * quem joga, na configuração do sistema. `.application.cosmere-rpg.mgs-tema-<nome>`
 * é a ficha de aparência própria, escolhida em "This Sheet" na configuração
 * daquele ator e gravada nele — de modo que um NPC pode ter cor diferente de
 * outro, e todo mundo o vê assim. Quando os dois valem, a ficha ganha, porque o
 * seletor é mais específico e está mais fundo na árvore.
 *
 * OS GRAFISMOS
 * Engrenagens submersas em volutas de bruma. Topo e rodapé usam as duas faixas
 * ancoradas que o sistema expõe (`.banners .top` e `.bot`, 200px, largura
 * inteira): ladrilho de 400×200 que emenda sozinho na horizontal. As LATERAIS
 * são ladrilho de 120×400 aplicado ao fundo da própria ficha, com posição,
 * repetição e tamanho declarados por camada — foi a falta dessas três
 * declarações que, na primeira tentativa, encheu a ficha de neblina.
 *
 * A BRUMA (v3, sobre as referências Mists-001/002/003 de Mario): funil aberto
 * em cima, fita com volume descendo, rolo no fim, gavinhas presas à borda. O
 * eixo sai de integração de curvatura — desenha-se por como a linha vira, não
 * por onde passa. A transparência vai em `fill-opacity`, path a path, nunca em
 * `opacity` de grupo: grupo achata, e é a SOMA das camadas que faz a bruma
 * adensar onde se cruza. A bruma vem em dois planos, um ATRÁS das engrenagens e
 * outro À FRENTE — é isso que a faz envolver o mecanismo em vez de ficar colada
 * num plano só. Cada peça é instanciada por `<use>`: a geometria entra uma vez
 * e cada aparição custa uma linha, o que derrubou o ladrilho de 368 KB para 33.
 *
 * Tudo procedural: gradientes e SVG em `data:` URI. Nenhum arquivo de imagem,
 * nenhuma fonte, nenhuma chamada remota, nenhuma licença de terceiro.
 *
 * OS METAIS
 * `--mgs-metal` é o único valor que uma variação de metal troca, e ela é
 * ORTOGONAL ao tema: prata, ouro, cobre e estanho valem nos três. Cada tema tem
 * seus quatro valores, porque metal claro sobre papel some. Todos medidos: nada
 * abaixo de 4,5:1 sobre a folha nem sobre o painel mais difícil do tema.
 */

'''

# ----------------------------------------------------------------- ferrugem

TOK_FERRUGEM = """  /* --- Ferrugem: a superfície da ficha é ferro oxidado, não ferro limpo.
         Marrom-avermelhado puxado para o alaranjado, escurecendo até quase
         preto. Decisão de Mario, 2026-09-07. --- */
  --mgs-rust-990: #1a0e08;
  --mgs-rust-950: #231409;
  --mgs-rust-900: #301c0f;
  --mgs-rust-850: #3b2312;
  --mgs-rust-800: #472a15;
  --mgs-rust-700: #5f3a1d;
  --mgs-rust-line: #94684a;

  --mgs-fog: #d6c8b8;
  --mgs-mist: #bda893;
  --mgs-paper: #e8e2d5;

  --mgs-brass: #b88940;
  --mgs-brass-bright: #dfba69;
  --mgs-verdigris: #4e8d85;
  --mgs-verdigris-bright: #6fb3a9;
  --mgs-danger: #a43d36;
  --mgs-danger-bright: #e08a80;"""

MAPA_FERRUGEM = """
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

# ----------------------------------------------------------------- negativo

TOK_NEGATIVO = """  /* --- Negativo: a mesma chapa, em brasa. A ferrugem invertida na luminância,
         não na cor — laranja quente por baixo, ferro e fumaça quase pretos por
         cima. Escolha de Mario, 2026-09-08, entre três leituras de "invertida".
         O piso de contraste é medido contra #d98d3e, o painel mais escuro. --- */
  --mgs-brasa-clara: #ffdcae;
  --mgs-brasa: #f2b063;
  --mgs-brasa-painel: #eca85c;
  --mgs-brasa-sombra: #e59d4e;
  --mgs-brasa-fundo: #d98d3e;

  /* Fumaça: o que no ferrugem era névoa clara, aqui é fuligem escura. */
  --mgs-fumaca: #241207;
  --mgs-fumaca-sub: #3d2410;
  --mgs-fumaca-fraca: #43270b;   /* 5,11 no pior painel; 4,68 sob a bruma do cabeçalho,
                                    onde o valor anterior (#4d2d0d) media 4,23 */

  --mgs-linha-brasa: #611d10;    /* 4,63 — serve como tinta, não só como filete */
  --mgs-linha-brasa-forte: #4a1409;
  --mgs-danger: #611d10;"""

MAPA_NEGATIVO = """
  --cosmere-color-sheet: var(--mgs-brasa);
  --cosmere-color-base-1: var(--mgs-brasa-fundo);
  --cosmere-color-base-2: var(--mgs-brasa-clara);
  --cosmere-color-base-3: var(--mgs-brasa-painel);
  --cosmere-color-base-4: var(--mgs-brasa-sombra);
  --cosmere-color-base-5: var(--mgs-linha-brasa);
  --cosmere-color-base-6: var(--mgs-linha-brasa-forte);
  --cosmere-color-neutral: var(--mgs-brasa-sombra);

  --cosmere-color-text-main: var(--mgs-fumaca);
  --cosmere-color-text-sub: var(--mgs-fumaca-sub);
  --cosmere-color-faded: var(--mgs-fumaca-fraca);
  --cosmere-color-text-accent: var(--mgs-metal);
  --cosmere-color-accent: var(--mgs-metal);
  --cosmere-color-highlight: var(--mgs-linha-brasa);

  /* Medidas sobre #d98d3e, o pior fundo do tema. */
  --cosmere-color-health-front: #183a2d;   /* 4,66 */
  --cosmere-color-health-back: #c98a4e;
  --cosmere-color-focus-front: #26383f;    /* 4,55 */
  --cosmere-color-focus-back: #cf9a63;
  --cosmere-color-invest-front: var(--mgs-metal);
  --cosmere-color-invest-back: #d29a5c;

  --cosmere-color-complication: var(--mgs-danger);
  --cosmere-color-complication-text: var(--mgs-danger);
  --cosmere-color-complication-background: #f7cfa8;
  --cosmere-color-opportunity: #183a2d;
  --cosmere-color-opportunity-text: #183a2d;
  --cosmere-color-opportunity-background: #dcd0ae;

  --cosmere-color-turn-fast: var(--mgs-metal);
  --cosmere-color-turn-slow: var(--mgs-linha-brasa-forte);
  --cosmere-color-parchment: var(--mgs-brasa-clara);"""

# ----------------------------------------------------------------- registro

TOK_REGISTRO = """  /* --- Bege, linha vermelha, tinta marrom. Papel de registro portuário
         pautado a lápis vermelho. Decisão de Mario, 2026-09-07. --- */
  --mgs-bege-claro: #f6efe1;
  --mgs-bege: #ece2cf;
  --mgs-bege-painel: #e6dac4;
  --mgs-bege-sombra: #ddceb4;
  --mgs-bege-fundo: #d2c0a2;

  --mgs-linha-vermelha: #a33a2a;
  --mgs-linha-forte: #7a2b1f;

  --mgs-tinta: #2a1a12;
  --mgs-tinta-sub: #4a3223;
  --mgs-tinta-fraca: #61402c;

  --mgs-danger: #8b271d;"""

MAPA_REGISTRO = """
  --cosmere-color-sheet: var(--mgs-bege);
  --cosmere-color-base-1: var(--mgs-bege-fundo);
  --cosmere-color-base-2: var(--mgs-bege-claro);
  --cosmere-color-base-3: var(--mgs-bege-painel);
  --cosmere-color-base-4: var(--mgs-bege-sombra);
  --cosmere-color-base-5: var(--mgs-linha-vermelha);
  --cosmere-color-base-6: var(--mgs-linha-forte);
  --cosmere-color-neutral: var(--mgs-bege-sombra);

  --cosmere-color-text-main: var(--mgs-tinta);
  --cosmere-color-text-sub: var(--mgs-tinta-sub);
  --cosmere-color-faded: var(--mgs-tinta-fraca);
  --cosmere-color-text-accent: var(--mgs-metal);
  --cosmere-color-accent: var(--mgs-metal);
  --cosmere-color-highlight: var(--mgs-linha-vermelha);

  /* Medidas sobre #d2c0a2, o pior fundo do tema. */
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

# ----------------------------------------------------------------- minio

TOK_MINIO = """  /* --- Mínio — avermelhado. Zarcão de mínio, a tinta de fundo que se passa em estrutura de aço antes da pintura. Vermelho de óxido, opaco, industrial.
         Sugestão de Mario, 2026-09-08: ampliar a gama para emular metais.
         Piso de contraste medido contra #4a211a, o painel mais claro. --- */
  --mgs-minio-990: #180705;
  --mgs-minio-950: #23100c;
  --mgs-minio-900: #301511;
  --mgs-minio-850: #3c1a15;
  --mgs-minio-800: #4a211a;
  --mgs-minio-700: #63302a;
  --mgs-minio-line: #a36a5e;

  --mgs-fog: #dfcac3;
  --mgs-mist: #c4a79e;
  --mgs-paper: #f2e4df;

  --mgs-danger: #e08a80;"""

MAPA_MINIO = """
  --cosmere-color-sheet: var(--mgs-minio-950);
  --cosmere-color-base-1: var(--mgs-minio-800);
  --cosmere-color-base-2: var(--mgs-minio-990);
  --cosmere-color-base-3: var(--mgs-minio-900);
  --cosmere-color-base-4: var(--mgs-minio-850);
  --cosmere-color-base-5: var(--mgs-minio-line);
  --cosmere-color-base-6: var(--mgs-minio-700);
  --cosmere-color-neutral: var(--mgs-minio-950);

  --cosmere-color-text-main: var(--mgs-paper);
  --cosmere-color-text-sub: var(--mgs-fog);
  --cosmere-color-faded: var(--mgs-mist);
  --cosmere-color-text-accent: var(--mgs-metal);
  --cosmere-color-accent: var(--mgs-metal);
  --cosmere-color-highlight: #6fb3a9;

  --cosmere-color-health-front: #6cab90;
  --cosmere-color-health-back: var(--mgs-minio-850);
  --cosmere-color-focus-front: #8b9c9e;
  --cosmere-color-focus-back: var(--mgs-minio-900);
  --cosmere-color-invest-front: var(--mgs-metal);
  --cosmere-color-invest-back: var(--mgs-minio-850);

  --cosmere-color-complication: var(--mgs-danger);
  --cosmere-color-complication-text: #e08a80;
  --cosmere-color-complication-background-dark: var(--mgs-minio-990);
  --cosmere-color-opportunity: #6fb3a9;
  --cosmere-color-opportunity-text: #6fb3a9;
  --cosmere-color-opportunity-background-dark: var(--mgs-minio-990);

  --cosmere-color-turn-fast: var(--mgs-metal);
  --cosmere-color-turn-slow: var(--mgs-minio-700);
  --cosmere-color-parchment: var(--mgs-paper);"""

# ----------------------------------------------------------------- verdete

TOK_VERDETE = """  /* --- Verdete — esverdeado. A pátina do bronze e do cobre exposto ao ar do porto. Verde acinzentado, frio, de metal que envelheceu ao relento.
         Sugestão de Mario, 2026-09-08: ampliar a gama para emular metais.
         Piso de contraste medido contra #1e4032, o painel mais claro. --- */
  --mgs-verdete-990: #07160f;
  --mgs-verdete-950: #0d2018;
  --mgs-verdete-900: #132a20;
  --mgs-verdete-850: #183328;
  --mgs-verdete-800: #1e4032;
  --mgs-verdete-700: #2b5646;
  --mgs-verdete-line: #6fa392;

  --mgs-fog: #cfe0d7;
  --mgs-mist: #aec5b9;
  --mgs-paper: #e6f0ea;

  --mgs-danger: #e18f85;"""

MAPA_VERDETE = """
  --cosmere-color-sheet: var(--mgs-verdete-950);
  --cosmere-color-base-1: var(--mgs-verdete-800);
  --cosmere-color-base-2: var(--mgs-verdete-990);
  --cosmere-color-base-3: var(--mgs-verdete-900);
  --cosmere-color-base-4: var(--mgs-verdete-850);
  --cosmere-color-base-5: var(--mgs-verdete-line);
  --cosmere-color-base-6: var(--mgs-verdete-700);
  --cosmere-color-neutral: var(--mgs-verdete-950);

  --cosmere-color-text-main: var(--mgs-paper);
  --cosmere-color-text-sub: var(--mgs-fog);
  --cosmere-color-faded: var(--mgs-mist);
  --cosmere-color-text-accent: var(--mgs-metal);
  --cosmere-color-accent: var(--mgs-metal);
  --cosmere-color-highlight: #6fb3a9;

  --cosmere-color-health-front: #76b198;
  --cosmere-color-health-back: var(--mgs-verdete-850);
  --cosmere-color-focus-front: #99a8aa;
  --cosmere-color-focus-back: var(--mgs-verdete-900);
  --cosmere-color-invest-front: var(--mgs-metal);
  --cosmere-color-invest-back: var(--mgs-verdete-850);

  --cosmere-color-complication: var(--mgs-danger);
  --cosmere-color-complication-text: #e18f85;
  --cosmere-color-complication-background-dark: var(--mgs-verdete-990);
  --cosmere-color-opportunity: #6fb3a9;
  --cosmere-color-opportunity-text: #6fb3a9;
  --cosmere-color-opportunity-background-dark: var(--mgs-verdete-990);

  --cosmere-color-turn-fast: var(--mgs-metal);
  --cosmere-color-turn-slow: var(--mgs-verdete-700);
  --cosmere-color-parchment: var(--mgs-paper);"""

# ----------------------------------------------------------------- peltre

TOK_PELTRE = """  /* --- Peltre — prateado. Peltre polido e fosco: cinza de estanho com chumbo, sem calor nenhum. É o tema mais neutro dos sete.
         Sugestão de Mario, 2026-09-08: ampliar a gama para emular metais.
         Piso de contraste medido contra #33373e, o painel mais claro. --- */
  --mgs-peltre-990: #101114;
  --mgs-peltre-950: #1a1c20;
  --mgs-peltre-900: #232529;
  --mgs-peltre-850: #2a2d33;
  --mgs-peltre-800: #33373e;
  --mgs-peltre-700: #474c56;
  --mgs-peltre-line: #939aa6;

  --mgs-fog: #d7dbe1;
  --mgs-mist: #b6bcc6;
  --mgs-paper: #eef0f3;

  --mgs-danger: #e08a80;"""

MAPA_PELTRE = """
  --cosmere-color-sheet: var(--mgs-peltre-950);
  --cosmere-color-base-1: var(--mgs-peltre-800);
  --cosmere-color-base-2: var(--mgs-peltre-990);
  --cosmere-color-base-3: var(--mgs-peltre-900);
  --cosmere-color-base-4: var(--mgs-peltre-850);
  --cosmere-color-base-5: var(--mgs-peltre-line);
  --cosmere-color-base-6: var(--mgs-peltre-700);
  --cosmere-color-neutral: var(--mgs-peltre-950);

  --cosmere-color-text-main: var(--mgs-paper);
  --cosmere-color-text-sub: var(--mgs-fog);
  --cosmere-color-faded: var(--mgs-mist);
  --cosmere-color-text-accent: var(--mgs-metal);
  --cosmere-color-accent: var(--mgs-metal);
  --cosmere-color-highlight: #6fb3a9;

  --cosmere-color-health-front: #70ae93;
  --cosmere-color-health-back: var(--mgs-peltre-850);
  --cosmere-color-focus-front: #94a4a6;
  --cosmere-color-focus-back: var(--mgs-peltre-900);
  --cosmere-color-invest-front: var(--mgs-metal);
  --cosmere-color-invest-back: var(--mgs-peltre-850);

  --cosmere-color-complication: var(--mgs-danger);
  --cosmere-color-complication-text: #e08a80;
  --cosmere-color-complication-background-dark: var(--mgs-peltre-990);
  --cosmere-color-opportunity: #6fb3a9;
  --cosmere-color-opportunity-text: #6fb3a9;
  --cosmere-color-opportunity-background-dark: var(--mgs-peltre-990);

  --cosmere-color-turn-fast: var(--mgs-metal);
  --cosmere-color-turn-slow: var(--mgs-peltre-700);
  --cosmere-color-parchment: var(--mgs-paper);"""

# ----------------------------------------------------------------- zinco

TOK_ZINCO = """  /* --- Zinco — azulado. Aço azulado e zinco galvanizado. Azul de chapa temperada, frio, longe do azul-marinho de Roshar que o sistema traz de fábrica.
         Sugestão de Mario, 2026-09-08: ampliar a gama para emular metais.
         Piso de contraste medido contra #1c3546, o painel mais claro. --- */
  --mgs-zinco-990: #071219;
  --mgs-zinco-950: #0d1a24;
  --mgs-zinco-900: #12232f;
  --mgs-zinco-850: #172c3a;
  --mgs-zinco-800: #1c3546;
  --mgs-zinco-700: #2a4c64;
  --mgs-zinco-line: #6f9bb8;

  --mgs-fog: #c9dbe6;
  --mgs-mist: #a5bfcf;
  --mgs-paper: #e4eef5;

  --mgs-danger: #e08a80;"""

MAPA_ZINCO = """
  --cosmere-color-sheet: var(--mgs-zinco-950);
  --cosmere-color-base-1: var(--mgs-zinco-800);
  --cosmere-color-base-2: var(--mgs-zinco-990);
  --cosmere-color-base-3: var(--mgs-zinco-900);
  --cosmere-color-base-4: var(--mgs-zinco-850);
  --cosmere-color-base-5: var(--mgs-zinco-line);
  --cosmere-color-base-6: var(--mgs-zinco-700);
  --cosmere-color-neutral: var(--mgs-zinco-950);

  --cosmere-color-text-main: var(--mgs-paper);
  --cosmere-color-text-sub: var(--mgs-fog);
  --cosmere-color-faded: var(--mgs-mist);
  --cosmere-color-text-accent: var(--mgs-metal);
  --cosmere-color-accent: var(--mgs-metal);
  --cosmere-color-highlight: #6fb3a9;

  --cosmere-color-health-front: #6cab90;
  --cosmere-color-health-back: var(--mgs-zinco-850);
  --cosmere-color-focus-front: #8e9fa1;
  --cosmere-color-focus-back: var(--mgs-zinco-900);
  --cosmere-color-invest-front: var(--mgs-metal);
  --cosmere-color-invest-back: var(--mgs-zinco-850);

  --cosmere-color-complication: var(--mgs-danger);
  --cosmere-color-complication-text: #e08a80;
  --cosmere-color-complication-background-dark: var(--mgs-zinco-990);
  --cosmere-color-opportunity: #6fb3a9;
  --cosmere-color-opportunity-text: #6fb3a9;
  --cosmere-color-opportunity-background-dark: var(--mgs-zinco-990);

  --cosmere-color-turn-fast: var(--mgs-metal);
  --cosmere-color-turn-slow: var(--mgs-zinco-700);
  --cosmere-color-parchment: var(--mgs-paper);"""

# ------------------------------------------------------------------- temas

TEMAS = [
  dict(id='mgs-ferrugem', nome='Ferrugem',
       tokens=TOK_FERRUGEM, mapa=MAPA_FERRUGEM, var='ferrugem',
       metal='#dfba69', tinta_metal='11%',
       vinheta='rgb(12 5 3 / 34%)', fuligem='fuligem.uri',
       metais={'prata':('#c2ced0','11,24 e 10,28'), 'ouro':('#dfba69','9,80 e 8,97'),
               'cobre':('#d68258','6,20 e 5,68'), 'estanho':('#6fb3a9','7,50 e 6,86')}),
  dict(id='mgs-negativo', nome='Negativo',
       tokens=TOK_NEGATIVO, mapa=MAPA_NEGATIVO, var='negativo',
       metal='#4b2e0d', tinta_metal='13%',
       vinheta='rgb(120 58 20 / 20%)', fuligem='fuligem.uri',
       metais={'prata':('#2b3636','4,65 no pior painel'), 'ouro':('#4b2e0d','4,62'),
               'cobre':('#5e200a','4,64'), 'estanho':('#103a38','4,65')}),
  dict(id='mgs-registro', nome='Registro',
       tokens=TOK_REGISTRO, mapa=MAPA_REGISTRO, var='registro',
       metal='#6b3f16', tinta_metal='9%',
       vinheta='rgb(90 40 24 / 15%)', fuligem='fuligem-claro.uri',
       metais={'prata':('#3a4749','7,51 e 5,42'), 'ouro':('#6b3f16','6,96 e 5,03'),
               'cobre':('#8c2f10','6,46 e 4,67'), 'estanho':('#1b4f4e','7,19 e 5,19')}),
  dict(id='mgs-minio', nome='Mínio',
       tokens=TOK_MINIO, mapa=MAPA_MINIO, var='minio',
       metal='#dfba69', tinta_metal='11%',
       vinheta='rgb(0 0 0 / 30%)', fuligem='fuligem.uri',
       metais={'prata':('#c2ced0','medido contra #4a211a'), 'ouro':('#dfba69','medido contra #4a211a'), 'cobre':('#d68258','medido contra #4a211a'), 'estanho':('#6fb3a9','medido contra #4a211a')}),
  dict(id='mgs-verdete', nome='Verdete',
       tokens=TOK_VERDETE, mapa=MAPA_VERDETE, var='verdete',
       metal='#dfba69', tinta_metal='11%',
       vinheta='rgb(0 0 0 / 30%)', fuligem='fuligem.uri',
       metais={'prata':('#c2ced0','medido contra #1e4032'), 'ouro':('#dfba69','medido contra #1e4032'), 'cobre':('#dc936f','medido contra #1e4032'), 'estanho':('#6fb3a9','medido contra #1e4032')}),
  dict(id='mgs-peltre', nome='Peltre',
       tokens=TOK_PELTRE, mapa=MAPA_PELTRE, var='peltre',
       metal='#dfba69', tinta_metal='11%',
       vinheta='rgb(0 0 0 / 30%)', fuligem='fuligem.uri',
       metais={'prata':('#c2ced0','medido contra #33373e'), 'ouro':('#dfba69','medido contra #33373e'), 'cobre':('#db906a','medido contra #33373e'), 'estanho':('#6fb3a9','medido contra #33373e')}),
  dict(id='mgs-zinco', nome='Zinco',
       tokens=TOK_ZINCO, mapa=MAPA_ZINCO, var='zinco',
       metal='#dfba69', tinta_metal='11%',
       vinheta='rgb(0 0 0 / 30%)', fuligem='fuligem.uri',
       metais={'prata':('#c2ced0','medido contra #1c3546'), 'ouro':('#dfba69','medido contra #1c3546'), 'cobre':('#d88860','medido contra #1c3546'), 'estanho':('#6fb3a9','medido contra #1c3546')}),
]


def bloco(t):
    v = t['var']
    # a classe da ficha usa o nome curto: mgs-tema-ferrugem, não mgs-tema-mgs-ferrugem
    c = t['var']
    return f"""/* =======================================================================
   TEMA "{t['nome']}" — id `{t['id']}`
   ======================================================================= */

/* Dois seletores, um bloco só. O primeiro é o tema escolhido por quem joga, no
   <body>; o segundo é a ficha que carrega a classe da sua própria aparência,
   escolhida em "This Sheet" na configuração daquele ator.

   Lista de seletores, e não dois blocos iguais, porque as variáveis de grafismo
   carregam os desenhos inteiros em `data:` URI. Duplicar o bloco dobraria o
   arquivo — de 450 KB para 900 — sem acrescentar um pixel.

   Quando os dois valem ao mesmo tempo, a ficha ganha: `.application` é mais
   específico e está mais fundo. É o que faz a escolha do ator sobrepor a
   preferência do jogador, e só naquela janela. */
body.cosmere-theme-{t['id']},
.application.cosmere-rpg.mgs-tema-{c} {{
{t['tokens']}

  /* Metal da ficha. É o único valor que as variações trocam. */
  --mgs-metal: {t['metal']};
{t['mapa']}

  /* --- Grafismos --- */
  /* Três camadas, de cima para baixo: o banho de metal na borda; o VÉU, que é
     a folha voltando por cima da bruma; e o desenho.

     O véu não é enfeite. Medido em pixel renderizado, o nome do personagem
     sobre a bruma densa caía a 3,33:1 na ferrugem e a 1,45:1 no negativo —
     abaixo do piso de 4,5:1. O véu devolve a leitura sem tirar a bruma da
     borda, que é onde ela conta. Mexer nas paradas dele é a maneira certa de
     regular "mais bruma" ou "mais legível". */
  --cosmere-banner-actor-top:
    linear-gradient(180deg, color-mix(in srgb, var(--mgs-metal) {t['tinta_metal']}, transparent) 0%, transparent 56%),
    linear-gradient(180deg, transparent 0%, color-mix(in srgb, var(--cosmere-color-sheet) 62%, transparent) 26%, var(--cosmere-color-sheet) 62%, var(--cosmere-color-sheet) 100%),
    {u(f'topo-{v}.uri')};
  --cosmere-banner-actor-bot:
    linear-gradient(0deg, color-mix(in srgb, var(--mgs-metal) {t['tinta_metal']}, transparent) 0%, transparent 56%),
    linear-gradient(0deg, transparent 0%, color-mix(in srgb, var(--cosmere-color-sheet) 62%, transparent) 26%, var(--cosmere-color-sheet) 62%, var(--cosmere-color-sheet) 100%),
    {u(f'rodape-{v}.uri')};
  --cosmere-banner-item-top:
    linear-gradient(180deg, color-mix(in srgb, var(--mgs-metal) {t['tinta_metal']}, transparent) 0%, transparent 56%),
    linear-gradient(180deg, transparent 0%, color-mix(in srgb, var(--cosmere-color-sheet) 62%, transparent) 26%, var(--cosmere-color-sheet) 62%, var(--cosmere-color-sheet) 100%),
    {u(f'topo-{v}.uri')};

  /* Textura da folha: só o grão. Este valor vai parar em `#tooltip` e em
     `.application.dialog`, que não declaram posição nem repetição — uma camada
     ancorada aqui viraria neblina em cima do texto. As faixas laterais têm
     regra própria, logo abaixo, com as três declarações de pintura. */
  --cosmere-sheet-texture:
    radial-gradient(130% 108% at 50% 46%, transparent 48%, {t['vinheta']} 100%),
    {u(t['fuligem'])};

  --mgs-lado-esq: {u(f'lado-esq-{v}.uri')};
  --mgs-lado-dir: {u(f'lado-dir-{v}.uri')};
}}

/* As duas faixas laterais. Precisam de `position`, `repeat` e `size` POR CAMADA:
   sem isso, o ladrilho de 150×460 se repete pela ficha inteira. Nenhuma dessas
   três propriedades é de caixa — são de pintura, e não mexem no layout. */
body.cosmere-theme-{t['id']} .application.cosmere-rpg,
.application.cosmere-rpg.mgs-tema-{c} {{
  background-image:
    linear-gradient(90deg, transparent 0, color-mix(in srgb, var(--cosmere-color-sheet) 55%, transparent) 6%, var(--cosmere-color-sheet) 13%, var(--cosmere-color-sheet) 87%, color-mix(in srgb, var(--cosmere-color-sheet) 55%, transparent) 94%, transparent 100%),
    var(--mgs-lado-esq),
    var(--mgs-lado-dir),
    var(--cosmere-sheet-texture);
  background-position: 0 0, left top, right top, 0 0;
  background-repeat: no-repeat, repeat-y, repeat-y, repeat;
  background-size: 100% 100%, 150px 460px, 150px 460px, auto;
}}

"""


def metais(t):
    c = t['var']
    L = [f"/* Metais do tema \"{t['nome']}\". No <body> vale para o mundo inteiro;",
         "   na própria ficha vale só para aquele personagem, e vence porque",
         "   redefine a variável num elemento mais fundo. */"]
    for m, (cor, nota) in t['metais'].items():
        L.append(f"body.cosmere-theme-{t['id']}.mgs-metal-{m:<8} {{ --mgs-metal: {cor}; }} /* {nota} */")
    L.append("")
    L.append("/* Por ator, em dois casos que NÃO podem se misturar:")
    L.append("   1. a ficha herda o tema do <body> — e aí o metal tem de vir da paleta")
    L.append("      desse tema. O `:not` é o que impede esta regra de alcançar uma ficha")
    L.append("      que tem aparência própria: sem ele, `body.cosmere-theme-x .application")
    L.append("      .cosmere-rpg.mgs-metal-y` (um elemento a mais na conta) vence a regra")
    L.append("      da ficha e o ator sai com o metal do tema errado;")
    L.append("   2. a ficha tem aparência própria — e aí o metal vem da paleta DELA. */")
    for m, (cor, _) in t['metais'].items():
        L.append(f'body.cosmere-theme-{t["id"]} .application.cosmere-rpg.mgs-metal-{m}:not([class*="mgs-tema-"]),')
        L.append(f".application.cosmere-rpg.mgs-tema-{c}.mgs-metal-{m:<8} {{ --mgs-metal: {cor}; }}")
    return "\n".join(L) + "\n\n"


if __name__ == "__main__":
    css = CAB + "".join(bloco(t) for t in TEMAS)
    css += ("/* =======================================================================\n"
            "   VARIAÇÕES DE METAL — ortogonais ao tema\n"
            "   Se a classe nunca chegar (o módulo perdeu o gancho, por exemplo),\n"
            "   nada quebra: fica o metal padrão do tema.\n"
            "   ======================================================================= */\n\n")
    css += "".join(metais(t) for t in TEMAS)
    destino = pathlib.Path('/home/claude/mgs-theme/styles/mistborn-gilded-steps-theme.css')
    destino.write_text(css, encoding='utf-8', newline='\n')
    print("CSS montado:", len(css), "caracteres em", destino)
