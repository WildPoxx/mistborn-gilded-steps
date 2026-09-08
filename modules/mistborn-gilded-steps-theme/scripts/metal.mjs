/**
 * Mistborn Gilded Steps — registro de temas e marca de metal por personagem.
 *
 * DUAS COISAS, EM DOIS TEMPOS
 *
 * 1. No `init`, registra três temas na lista do Cosmere pela API oficial
 *    (`cosmereRPG.api.registerTheme`). O sistema monta o menu de temas em
 *    `registerDeferredSettings()`, que roda no hook `setup` — depois que os
 *    módulos carregam. É essa ordem que torna o registro possível; se o menu
 *    fosse montado no `init` do próprio sistema, nenhum módulo chegaria a tempo.
 *
 * 2. Ao abrir uma ficha, põe nela a classe do metal do personagem. O tema faz o
 *    resto: o CSS troca `--mgs-metal` e com ele moldura, números e o brilho
 *    sobre as engrenagens.
 *
 * O QUE ACONTECE SE ALGO FALHAR
 * Tudo aqui é defensivo de propósito. Sem a API, os temas não aparecem na lista
 * e o mundo segue no tema do sistema. Sem o gancho certo, toda ficha abre no
 * metal padrão do tema. Em nenhum dos casos alguma coisa quebra — o sintoma é
 * silencioso, e está documentado no README para não ser confundido com defeito.
 */

const ID = 'mistborn-gilded-steps-theme';

/** Os temas que este módulo acrescenta à lista do Cosmere. */
const TEMAS = [
    { id: 'mgs-ferrugem', label: 'Gilded Steps — Ferrugem' },
    { id: 'mgs-negativo', label: 'Gilded Steps — Negativo' },
    { id: 'mgs-registro', label: 'Gilded Steps — Registro' },
    { id: 'mgs-minio',    label: 'Gilded Steps — Mínio' },
    { id: 'mgs-verdete',  label: 'Gilded Steps — Verdete' },
    { id: 'mgs-peltre',   label: 'Gilded Steps — Peltre' },
    { id: 'mgs-zinco',    label: 'Gilded Steps — Zinco' },
];

/** Os metais são ortogonais ao tema: valem nos três. */
const METAIS = ['prata', 'ouro', 'cobre', 'estanho'];
const FLAG = 'metal';

/* ------------------------------------------------------------------ temas */

Hooks.once('init', () => {
    const api = globalThis.cosmereRPG?.api ?? game?.system?.api;
    if (typeof api?.registerTheme !== 'function') {
        console.warn(
            `${ID} | O sistema Cosmere não expôs registerTheme(). Os temas do ` +
            `Gilded Steps não entrarão na lista; o CSS continua inerte e nada quebra.`,
        );
        return;
    }
    for (const tema of TEMAS) {
        try {
            api.registerTheme({ ...tema, source: ID, priority: 0 });
        } catch (erro) {
            console.error(`${ID} | Falhou ao registrar o tema ${tema.id}:`, erro);
        }
    }
});

/* ------------------------------------------------------------------ metal */

function normaliza(valor) {
    return METAIS.includes(valor) ? valor : null;
}

/** Põe (ou tira) a classe do metal na janela da ficha, sem deixar resto. */
function aplicar(app, elemento) {
    const raiz = elemento?.[0] ?? elemento;
    if (!(raiz instanceof HTMLElement)) return;
    const ator = app?.document ?? app?.actor;
    if (!ator?.getFlag) return;

    const metal = normaliza(ator.getFlag(ID, FLAG));
    for (const m of METAIS) raiz.classList.remove(`mgs-metal-${m}`);
    if (metal) raiz.classList.add(`mgs-metal-${metal}`);
}

/**
 * Quatro nomes possíveis de gancho. ApplicationV2 dispara `render<Classe>`, e
 * a classe da ficha do Cosmere pode variar entre versões do sistema e do
 * Foundry. Escutar os quatro é barato; errar todos custa apenas o metal padrão.
 */
for (const gancho of [
    'renderCharacterSheet',
    'renderAdversarySheet',
    'renderActorSheet',
    'renderActorSheetV2',
]) {
    Hooks.on(gancho, aplicar);
}

/* --------------------------------------------------------------- interface */

Hooks.once('ready', () => {
    game.mgsTheme = {
        metais: [...METAIS],
        temas: TEMAS.map((t) => t.id),

        /** Grava o metal de um ator e redesenha a ficha aberta, se houver. */
        async definir(ator, metal) {
            if (!ator?.setFlag) throw new Error('Ator inválido.');
            const valor = normaliza(metal);
            if (valor) await ator.setFlag(ID, FLAG, valor);
            else await ator.unsetFlag(ID, FLAG);
            ator.sheet?.render(false);
            return valor;
        },

        /** Caixa de escolha para o token selecionado. */
        async escolher(ator = canvas?.tokens?.controlled?.[0]?.actor) {
            if (!ator) {
                ui.notifications?.warn('Selecione um token primeiro.');
                return null;
            }
            const atual = normaliza(ator.getFlag(ID, FLAG));
            const opcoes = [
                `<option value=""${atual ? '' : ' selected'}>padrão</option>`,
                ...METAIS.map(
                    (m) =>
                        `<option value="${m}"${m === atual ? ' selected' : ''}>${m}</option>`,
                ),
            ].join('');

            let respondeu = false;
            const escolha = await foundry.applications.api.DialogV2.prompt({
                window: { title: `Metal de ${ator.name}` },
                content: `<p>Metal da ficha:</p><select name="metal">${opcoes}</select>`,
                ok: {
                    label: 'Aplicar',
                    callback: (_ev, botao) => {
                        respondeu = true;
                        return botao.form.elements.metal.value || null;
                    },
                },
                rejectClose: false,
            }).catch(() => null);

            // `null` é ambíguo: pode ser "padrão" ou "a caixa não abriu".
            // O sinalizador desfaz a ambiguidade — sem ele, fechar a janela
            // apagaria o metal do personagem em silêncio.
            if (!respondeu) return null;
            return this.definir(ator, escolha);
        },
    };
});
