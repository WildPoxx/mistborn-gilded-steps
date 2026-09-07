# Instructions for assistants — mistborn-gilded-steps

This is the **public repository** of the Mistborn — Era 2 project. It is not the vault.

## Read first

In this order:

1. `CONTENT_POLICY.md`
2. `SPOILER_POLICY.md`
3. `VISUAL_IDENTITY.md`

In the vault (`C:\Users\amari\source\Mistborn`), the sources of truth remain `AGENTS.md`,
`00_index/00 - Diretrizes do Projeto Mistborn.md` and
`00_index/02 - Registro de Decisões do Projeto.md`.

## Language

**This repository is written in English**, so the Foundry community can read and use it. The
vault stays in Portuguese. Material crossing from the vault to this repository is rewritten,
not translated line by line.

## Direction of flow

Vault → repository, always. Content is **rewritten** for the public, never copied from a GM
note. Nothing returns from the repository to the vault without a recorded decision.

## Constabulary Record

`docs/constabulary-record.html` follows a fixed schema. Before opening, editing or filling a
file, read `02_Personagens e NPCs/Modelo - Ficha Constabulária.md` in the vault: it defines the
field order, the three states (`NO RECORD`, `PRESUMED`, `SEALED`), what never goes in, and how
to open a new file.

Two rules that do not bend: the character's canonical note in the vault comes **before** the
public file, and nothing goes in without passing that character's visibility matrix. Mechanical
sheet data — attributes, skills, talents, money — is not public material.

## Character assets

Portraits and tokens of player characters are produced by the players and granted to the
project. The tool is their choice; the authorisation is Mario's. What this repository requires
is the provenance line in `docs/assets/ATTRIBUTION.md` — origin, authorship, process,
authorisation and date.

Art **commissioned by the project** is a different category and follows the visual identity
directive in the vault, with a brief and a recorded prompt.

## Modules

`modules/` holds Foundry VTT modules built for this campaign and released to the community.
Each module carries its own `README.md`, `CHANGELOG.md` and `module.json`, and is versioned on
its own. A module folder name must match the `id` in its manifest, or Foundry refuses it.

Nothing in `modules/` may alter rules, rolls, templates, permissions or data structures of a
system it themes.

## Never without Mario's explicit authorisation

- Creating, changing or removing a remote, workflow, GitHub Pages deployment, release or tag.
- `git push --force`, `git filter-repo`, any history rewrite.
- Publishing a module as installable by manifest URL.
- Touching the server, ports, Caddy, PM2, a Foundry world or its data.
- Creating `data/` or `tools/` at the repository root by anticipation. They arrive when there
  is a real need, not before.

## When you finish

Report: files changed; decisions and sources used; what you verified; risks left open; and the
next decision that depends on Mario.
