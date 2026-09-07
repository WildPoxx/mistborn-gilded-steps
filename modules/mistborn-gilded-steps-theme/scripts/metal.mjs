/*
 * Mistborn Gilded Steps — metal por personagem.
 *
 * O QUE FAZ
 * Cada ator pode guardar um metal — prata, ouro, cobre ou estanho. Quando a
 * ficha abre, este arquivo põe a classe correspondente na janela dela, e o CSS
 * do tema faz o resto. Nada mais: não altera regra, dado, template, permissão
 * nem estrutura da ficha. Uma classe, e só.
 *
 * SE FALHAR, NÃO QUEBRA
 * Todo o trabalho está dentro de try/catch e a falha é registrada no console
 * como aviso, não como erro. Se o gancho não existir nesta versão do Foundry, ou
 * se o Cosmere renomear suas classes, a classe simplesmente não é colocada e a
 * ficha abre no ouro, que é o padrão do tema. Nenhum caminho aqui pode impedir
 * a ficha de abrir.
 *
 * NÃO TESTADO EM RUNTIME
 * Escrito lendo o código do Cosmere RPG 3.1.0 e a documentação do Foundry, sem
 * nenhum mundo para rodar. É a única parte do módulo que não foi verificada.
 * O CSS foi; isto não.
 */

const ID = 'mistborn-gilded-steps-theme';
const METAIS = ['prata', 'ouro', 'cobre', 'estanho'];
const CLASSES = METAIS.map((m) => `mgs-metal-${m}`);

/** Descobre o elemento raiz da janela, seja ApplicationV2 ou a API antiga. */
function raiz(app, alvo) {
  if (alvo instanceof HTMLElement) return alvo.closest('.application') ?? alvo;
  if (alvo?.[0] instanceof HTMLElement) return alvo[0].closest('.application') ?? alvo[0];
  if (app?.element instanceof HTMLElement) return app.element;
  if (app?.element?.[0] instanceof HTMLElement) return app.element[0];
  return null;
}

function aplicar(app, alvo) {
  try {
    const el = raiz(app, alvo);
    const ator = app?.document ?? app?.actor ?? app?.object;
    if (!el || !ator?.getFlag) return;

    const metal = ator.getFlag(ID, 'metal');
    el.classList.remove(...CLASSES);
    if (METAIS.includes(metal)) el.classList.add(`mgs-metal-${metal}`);
  } catch (e) {
    console.warn(`${ID} | não consegui aplicar o metal na ficha:`, e);
  }
}

/* Os nomes de gancho mudaram entre as gerações de aplicação do Foundry, e o
 * Cosmere usa ApplicationV2, cujo gancho leva o nome da classe da ficha. Em vez
 * de apostar num nome, registramos todos os plausíveis: os que não existirem
 * nunca disparam, e isso não custa nada. */
for (const gancho of [
  'renderCharacterSheet',
  'renderAdversarySheet',
  'renderActorSheet',
  'renderActorSheetV2',
]) {
  Hooks.on(gancho, aplicar);
}

/* Utilitário para o mestre. Chamado por macro — ver o LEIA do módulo.
 * Fica em game.mgsTheme para não poluir o escopo global. */
Hooks.once('ready', () => {
  try {
    game.mgsTheme = {
      metais: METAIS,

      /** Grava o metal de um ator e reabre a ficha para o efeito aparecer. */
      async definir(ator, metal) {
        if (!ator) return ui.notifications?.warn('Nenhum ator selecionado.');
        if (metal && !METAIS.includes(metal)) {
          return ui.notifications?.warn(`Metal desconhecido: ${metal}. Use ${METAIS.join(', ')}.`);
        }
        if (metal) await ator.setFlag(ID, 'metal', metal);
        else await ator.unsetFlag(ID, 'metal');
        if (ator.sheet?.rendered) ator.sheet.render(false);
        ui.notifications?.info(`Metal de ${ator.name}: ${metal ?? 'padrão'}.`);
      },

      /** Pergunta o metal. Tenta a caixa de diálogo do Foundry e, se a API não
       *  for a esperada nesta versão, cai num prompt simples do navegador. */
      async escolher(ator = canvas?.tokens?.controlled?.[0]?.actor ?? game.user?.character) {
        if (!ator) return ui.notifications?.warn('Selecione um token ou defina seu personagem.');
        let escolha;
        let respondeu = false;   // sem isto, "padrão" (null) seria confundido
                                 // com "o diálogo não funcionou"
        try {
          const D = foundry?.applications?.api?.DialogV2;
          if (D?.wait) {
            escolha = await D.wait({
              window: { title: `Metal de ${ator.name}` },
              content: `<p>Com que metal ${ator.name} se conecta?</p>`,
              buttons: [
                ...METAIS.map((m) => ({ action: m, label: m, callback: () => m })),
                { action: 'padrao', label: 'padrão', callback: () => null },
              ],
              rejectClose: false,
            });
            respondeu = true;
          }
        } catch (e) {
          console.warn(`${ID} | diálogo indisponível, usando prompt:`, e);
        }
        if (respondeu) {
          if (escolha === undefined) return;          // fechou sem escolher
        } else {
          const digitado = window.prompt(
            `Metal de ${ator.name} — ${METAIS.join(', ')} (vazio = padrão)`, '');
          if (digitado === null) return;              // cancelou
          escolha = digitado.trim() || null;
        }
        return this.definir(ator, escolha);
      },
    };
  } catch (e) {
    console.warn(`${ID} | não consegui publicar os utilitários:`, e);
  }
});
