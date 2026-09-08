/**
 * Mistborn Gilded Steps — fichas de aparência por ator.
 *
 * POR QUE ISTO EXISTE
 * O tema escolhido na configuração do sistema vale para TODAS as fichas daquele
 * jogador. Para dar cor diferente a NPCs diferentes é preciso o outro caminho, o
 * mesmo que os módulos do SWADE usam: registrar FICHAS próprias. Elas aparecem em
 * "This Sheet" na configuração de cada ator, a escolha fica gravada no ator, e
 * por isso todo mundo vê aquele NPC da mesma cor.
 *
 * Os dois níveis convivem: o tema do sistema é o padrão de cada jogador; a ficha
 * escolhida no ator sobrepõe, e só naquela janela. Quem decide é o CSS — o
 * seletor da ficha é mais específico e está mais fundo que o do <body>.
 *
 * O QUE ESTA CLASSE FAZ
 * Nada além de acrescentar uma classe CSS à janela. Não altera dado, template,
 * permissão, comportamento nem estrutura: herda a ficha do sistema inteira e só
 * marca o elemento raiz.
 *
 * O ACOPLAMENTO QUE ISTO INTRODUZ
 * Aqui, e só aqui, o módulo deixa de ser pele e passa a depender da CLASSE de
 * ficha do Cosmere. Se uma atualização do sistema renomear ou reorganizar essas
 * classes, `base()` não acha nada e as entradas simplesmente não aparecem na
 * lista; o ator volta à ficha padrão do sistema. A falha é visível e sem perda:
 * a escolha continua gravada e volta a valer quando as entradas voltarem.
 */

const ID = 'mistborn-gilded-steps-theme';

/** Os mesmos três temas do CSS. O nome curto é o que vira classe. */
const TEMAS = [
    { curto: 'ferrugem', label: 'Gilded Steps — Ferrugem' },
    { curto: 'negativo', label: 'Gilded Steps — Negativo' },
    { curto: 'registro', label: 'Gilded Steps — Registro' },
];

/** Os dois tipos de ator do Cosmere. */
const TIPOS = ['character', 'adversary'];

/**
 * A classe de ficha que o sistema registrou como padrão para um tipo de ator.
 *
 * Procura pelo dono do registro, não pelo nome da classe: o `id` de uma ficha
 * registrada é `<pacote>.<Classe>`, e o que nos interessa é a do `cosmere-rpg`.
 * Assim uma renomeação da classe não quebra a busca — só uma troca de pacote.
 */
function base(tipo) {
    const registradas = CONFIG.Actor?.sheetClasses?.[tipo];
    if (!registradas) return null;
    const entradas = Object.values(registradas);
    // Vazio aqui significa quase sempre tempo errado, não sistema ausente:
    // ver a nota sobre `ready` mais abaixo.
    const doSistema =
        entradas.find((e) => e.id?.startsWith('cosmere-rpg.') && e.default) ??
        entradas.find((e) => e.id?.startsWith('cosmere-rpg.'));
    return doSistema?.cls ?? null;
}

/** Uma subclasse que só carimba a classe do tema na janela. */
function fabricar(Base, curto, nome) {
    const Ficha = class extends Base {
        async _onRender(context, options) {
            await super._onRender(context, options);
            // `this.element` é a janela inteira da ficha; é nela que o CSS pousa.
            this.element?.classList.add(`mgs-tema-${curto}`);
        }
    };
    // O nome da classe importa: o Foundry monta o gancho `render<Nome>` a partir
    // dele, e a lista de fichas usa o nome como chave do registro. Anônima, a
    // classe entraria como "" e colidiria com as outras.
    Object.defineProperty(Ficha, 'name', { value: nome });
    return Ficha;
}

/**
 * Registrar no `ready`, e a razão está no código do Foundry 13.351.
 *
 * `DocumentSheetConfig.registerSheet` tem dois caminhos: se `game.ready` já é
 * verdadeiro, grava direto em `CONFIG.<Documento>.sheetClasses`; se ainda não,
 * empilha numa fila privada. `Game#setupGame` só esvazia essa fila mais tarde,
 * em `initializeSheets()`, que ANTES apaga `sheetClasses` inteiro e só então
 * repõe o que estava na fila.
 *
 * A ordem real é: hook `init` → hook `setup` → `initializeSheets()` → `ready`.
 * Como o sistema registra as fichas dele no `init`, elas ficam na fila e
 * `CONFIG.Actor.sheetClasses` continua VAZIO durante o `init` e durante o
 * `setup`. Foi isso que derrubou a v0.6.0: no `setup` a busca pela classe-base
 * não achava nada, avisava no console e desistia.
 *
 * No `ready` as duas condições finalmente valem ao mesmo tempo — a fila já foi
 * esvaziada, então a classe-base existe; e `game.ready` já é verdadeiro, então
 * o registro entra na hora em vez de cair numa fila que ninguém mais esvazia.
 * A janela de configuração lê a lista quando abre, e sempre abre depois disso.
 */
Hooks.once('ready', () => {
    const Actors = foundry.documents?.collections?.Actors ?? globalThis.Actors;
    if (!Actors?.registerSheet) {
        console.warn(
            `${ID} | Não achei o registro de fichas do Foundry. As aparências ` +
            `por ator não entram na lista; o tema do sistema continua valendo.`,
        );
        return;
    }

    for (const tipo of TIPOS) {
        const Base = base(tipo);
        if (!Base) {
            console.warn(
                `${ID} | Não achei a ficha do Cosmere para "${tipo}". As ` +
                `aparências por ator não entram na lista desse tipo.`,
            );
            continue;
        }
        for (const { curto, label } of TEMAS) {
            const nome = `MgsTema${curto[0].toUpperCase()}${curto.slice(1)}${
                tipo[0].toUpperCase()
            }${tipo.slice(1)}Sheet`;
            try {
                Actors.registerSheet(ID, fabricar(Base, curto, nome), {
                    types: [tipo],
                    label,
                    makeDefault: false,
                });
            } catch (erro) {
                console.error(
                    `${ID} | Falhou ao registrar a ficha ${label} (${tipo}):`,
                    erro,
                );
            }
        }
    }
});
