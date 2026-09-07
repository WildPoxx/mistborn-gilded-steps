# Visual Identity — Mistborn Gilded Steps

## Direction

**Industrial noir at the edge of a gilded city:** iron and soot, cold canal water, worn brass,
copper, lamplight and ledger paper. The look carries the urban drama of Bilming and Yomend
Steps without turning it into epic fantasy.

Deliberately avoided: clean golden epic; decorative steampunk gearwork; fetishised poverty;
glamourised violence; and any reproduction of third-party covers, maps, logos or official art.

## Source of truth

The canonical palette lives in the vault, at
`09_Midia e Assets/Theme - Mistborn Gilded Steps/mistborn-design-tokens.css`.
**That file wins.** `docs/styles/tokens.css` is a **derived adaptation** for the web: same
values, scoped to `:root` instead of the Foundry and MasterQuest selectors.

When the vault palette changes, the file here is updated by hand and the version in the CSS
header is incremented.

## Colour lexicon

| Role | Token | Use |
| --- | --- | --- |
| Iron and soot | `--mgs-iron-*`, `--mgs-slate`, `--mgs-fog` | frames, headers, infrastructure, systemic danger |
| Paper and lime | `--mgs-paper*`, `--mgs-ink*` | long reading, records, forms |
| Brass and bronze | `--mgs-brass*` | primary action, distinction, wealth under tension |
| Copper | `--mgs-copper` | friction, crime, human warmth, moderate alert |
| Verdigris and water | `--mgs-verdigris*` | focus, investigation, the canal, counterweight to gold |
| Ember | `--mgs-ember*` | risk and urgency — never neon |
| States | `--mgs-danger`, `--mgs-success` | system red; the ember is **not** the error red |
| Rust *(table)* | `--mgs-rust-*` | Foundry sheet surface, dark mode — oxidised iron |
| Beige and rule *(table)* | `--mgs-bege-*`, `--mgs-linha-*`, `--mgs-tinta*` | Foundry sheet surface, light mode — red-ruled ledger paper |

The last two families entered the contract on 2026-09-07 and belong to **the table**, not the
portal. The portal stays in the iron family.

## Typography

System stacks only. **No remote fonts, no CDN, no third-party scripts** — the portal must load
offline and create no external dependency.

- Interface: `--mgs-font-ui`
- Reading: `--mgs-font-prose`
- Display: `--mgs-font-display`
- Code: `--mgs-font-mono`

A custom typeface enters only after a redistributable licence and a test of Portuguese
diacritics.

**One derivation on record:** in dark mode, `--text-muted` is not plain `--mgs-slate`, which
sits at roughly 4.3:1 against the background — below the minimum this document sets. It is a
mix of `--mgs-fog` and `--mgs-slate`, computed in CSS from the tokens themselves. No new colour
was invented.

## Form, not only colour

"Gilded Steps" is a topographic metaphor, and the portal uses it as structure:

- **The page is the hillside.** The document descends from the high city (brass, window light)
  to the waterline (iron, verdigris, mist). The `main` gradient and the `.mist` band before the
  footer are what make that descent.
- **The step is the only ornament.** Three brass marks descending (`.step-mark`), used as a
  section mark, as the pivot of dividers, and at the top of cards. Nothing else.
- **The cross-section** in `docs/index.html` is an original inline SVG: water, quay, cranes,
  sawtooth warehouse roofs, the hillside cut into terraces, and the tall houses on the ridge
  with their windows lit. Drawn for this project — it traces no third-party map, plan or art.
  Coloured by the tokens; carries a descriptive `<title>`.
- **The form is the tone.** In the Constabulary Record, what makes a file look like a file is
  the form itself — small-caps labels, typewriter values (`--mgs-font-mono`), ruled fields. An
  empty field is information, and it is stated out loud.

Forbidden **in the portal**, as the vault directive already said: decorative gearwork, rivets,
filigree, torn-parchment edges, shiny metal.

### The reach of that prohibition — Mario's decision, 2026-09-07

The rule above governs **the public portal**. It was written for a reading surface, where
ornament competes with text and where the hillside metaphor is already the structure.

**The character sheet in Foundry is a different surface, with its own lexicon.** There a gear
is not decoration: it is the world. The sheet is the object a player handles at a Scadrial
table in the Second Era — the age of the machine, the port and the factory — and mist
swallowing metal is the signature of *Mistborn*, not a genre quotation.

What separates the two is the qualifier the vault directive always carried and this page had
lost: what is forbidden is the gear **without function**. The portal's would be decorative. The
sheet's carries the setting.

Still binding on both surfaces: no image files, no remote fonts, no fake metal shine faked by a
specular gradient, and contrast measured on the rendered pixel.

The sheet theme lives in `modules/mistborn-gilded-steps-theme/`.

## Portal rules

- Responsive, no horizontal scroll, no essential information behind *hover*.
- Minimum contrast of 4.5:1 for body text and 3:1 for functional graphic elements, validated in
  both light and dark.
- Critical information never depends on colour alone.
- Every meaningful image carries useful alternative text.
- Hierarchy, typography and space before reaching for colour.

## Assets

Every image published in `docs/assets/` needs a line in `docs/assets/ATTRIBUTION.md` with
origin, authorship, process, licence and date. An asset with no recorded provenance does not go
in.
