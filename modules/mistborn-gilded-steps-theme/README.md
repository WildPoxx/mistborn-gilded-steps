# Gilded Steps Theme for Cosmere RPG on Foundry VTT

An appearance module for this campaign's table. It adds three themes to the Cosmere RPG system's
own theme list, dressing the sheet in the project's visual language instead of the Roshar look
the system ships with.

This is **original code**: CSS, one short script and the Python generators that draw the
graphics. It contains, reproduces and redistributes no text, art, rules or code belonging to the
Cosmere RPG, Brotherwise, Dragonsteel or Brandon Sanderson. What it uses are the **CSS variable
names the system itself publishes** — the interface any stylesheet has — and supplies its own
values.

## What it does

It redefines colour and ornament. **No rule, roll, template, permission or sheet structure is
altered,** and there is not one box property — `display`, `position`, `flex`, `grid`, `width`,
`height` — in the whole stylesheet. The only non-variable declarations are paint
(`background-position`, `-repeat`, `-size`), and they are required: an image layer with no
declared position tiles across the entire sheet.

Disabling the module restores the original appearance. That is the undo button, and there is no
other state to revert.

### Eleven themes, on the system's own list

Since 0.5.0 the module no longer overrides the system's Default theme. It registers its own
entries through the published API, `cosmereRPG.api.registerTheme()`, and they appear in
**Settings → Theme** alongside the system's:

- **Gilded Steps — Ferro.** Oxidised iron: a red-brown pulled towards orange, darkening to
  near black at the edges.
- **Gilded Steps — Latão.** The same plate, at forge heat: a hot orange ground with gears and
  smoke in near black.
- **Gilded Steps — Electro.** Harbour ledger paper: a beige ground, hairlines and frames in
  brick red, numbers and text in a near-black brown.
- **Gilded Steps — Cobre.** Red-oxide primer, the paint that goes on structural steel before the
  finish coat. Opaque, industrial.
- **Gilded Steps — Bronze.** The verdigris of bronze and copper left in harbour air: a cool,
  greyed green.
- **Gilded Steps — Peltre.** Pewter, matte: tin-and-lead grey with no warmth in it. The most
  neutral of the seven.
- **Gilded Steps — Zinco.** Blued steel and galvanised zinc — a cold plate blue, deliberately
  away from the navy the system ships with.
- **Gilded Steps — Aço.** Peltre's negative: polished steel, a near-white plate with mid-grey
  frames instead of gold. The only theme whose default metal is silver rather than gold, because
  the grey frame *is* the point of it.
- **Gilded Steps — Cádmio.** Platina's cousin at another temperature: an ice-blue plate with
  steel-blue frames. Its default metal is silver too.
- **Gilded Steps — Bendalloy.** Bismuth alloy: the lilac iridescence a bismuth crystal takes from
  its own oxide film. The one colour in the set that is not a metal in open air, and so the one
  that can mark what is *invested* rather than industrial.
- **Gilded Steps — Cromo.** Chrome-oxide green, the industrial pigment. A green from a metal
  compound, not from corrosion — which is what keeps it clear of Verdete.

The names are metals, so a player can pick the sheet that looks like their character's. The
labels changed in 0.9.0; the ids behind them did not, because an id is what gets stored — in each
player's theme preference and, for the sheets, on the actor itself. Renaming one would silently
send every choice already made to something that no longer exists.

This works because the system builds that menu in `registerDeferredSettings()`, on the `setup`
hook — after modules have initialised. The module registers on `init` and arrives in time.

One consequence matters for anyone editing the CSS: the system defines its colour variables
**only inside `.cosmere-theme-default`**. A theme of ours inherits nothing from it, so each block
here declares the complete set, not just the differences.

### An appearance per actor

The theme above is each player's own preference and applies to every sheet they
open. For a different look on a *specific* actor — one NPC in rust, another in
beige — the module also registers eleven **sheets** of its own, the same mechanism
the SWADE companion modules use. They appear under **This Sheet** in an actor's
sheet configuration:

```
Default Sheet
Gilded Steps — Ferro
Gilded Steps — Latão
Gilded Steps — Electro
Gilded Steps — Cobre
Gilded Steps — Bronze
Gilded Steps — Peltre
Gilded Steps — Zinco
Gilded Steps — Aço
Gilded Steps — Cádmio
Gilded Steps — Bendalloy
Gilded Steps — Cromo
```

The choice is stored on the actor, so everyone sees that NPC the same way, and it
overrides the player's own theme for that window only. Available for both actor
types, `character` and `adversary`.

These sheets subclass the system's own and add nothing but a CSS class — no data,
template, permission or behaviour is touched. **This is the one place where the
module stops being a pure skin** and depends on the Cosmere sheet classes. If a
system update reorganises them, the entries simply stop appearing and the actor
falls back to the default sheet; the stored choice survives and takes effect again
when they return.

### Four metals

Each character can have their own: silver, gold, copper or tin. The metal is **orthogonal to the
theme** — all four work in all three, with their own values in each, because a pale metal
disappears on paper. The metal changes the frame, the numerals and the sheen; the iron of the
fittings stays iron. With no mark set, the sheet opens in the theme's default metal.

```js
game.mgsTheme.escolher();                // picker for the selected token
game.mgsTheme.definir(actor, 'cobre');   // set directly
game.mgsTheme.definir(actor, null);      // back to the default
```

> The API method names and metal keys are still Portuguese, matching the CSS selectors. Renaming
> them was considered for this release and **deliberately deferred**: the metal keys are stored
> as actor flags, so a rename silently drops every character's metal. It needs a migration, not
> a search and replace.

## Procedural graphics

The drawings are **not image files**. Three generators produce them and embed them in the CSS as
`data:` URIs:

- `tools/bruma.py` — the mist. Each curl is a ribbon whose spine comes from integrating a
  curvature function: the curve is described by *how it turns*, not by where it passes. The
  ribbon opens into a funnel, descends with a lit side and a shaded side, rolls up at the end,
  and sheds hooked tendrils from its edge.
- `tools/grafismo.py` — the gears, and the composition of the tiles.
- `tools/montar_css.py` — the stylesheet.

Three details are load-bearing. Transparency goes in `fill-opacity`, path by path, never in group
`opacity`: a transparent group flattens, and it is the **sum** of overlapping ribbons that makes
mist thicken where it crosses. The mist comes in two planes, one **behind** the gears and one **in
front**, which is what makes it wrap the mechanism instead of sitting flat behind it. And each
appearance is a `<use>` of geometry defined once — without that, a single tile weighed 368 KB
instead of 33.

No external assets, no remote fonts, no network calls — the same principle the portal follows.

To change the composition, edit the generators and run:

```
python tools/grafismo.py && python tools/montar_css.py
```

Editing a `data:` URI by hand is like editing a JPEG in Notepad.

## Accessibility

Every colour pair carrying text was measured on rendered pixels, not estimated: a minimum of
4.5:1 for text and 3:1 for functional graphic elements, in all three themes and across all four
metals, against the sheet and against the hardest panel of each theme.

The mist forced one addition. Measured against the header band, the character's name fell to
3.33:1 in Ferrugem and 1.45:1 in Negativo. A **veil** — the sheet's own colour returning over the
mist, absent at the edge and full where text lands — restores it without removing the mist from
where it counts. Its gradient stops are the right place to trade legibility against atmosphere.
The worst pair in the theme now measures 4.62:1.

`tools/contraste.py` computes these ratios from token values; the figures quoted in the CSS
comments come from measuring the rendered image.

## Installation

**From Foundry.** In *Add-on Modules → Install Module*, paste this manifest URL:

```
https://github.com/WildPoxx/mistborn-gilded-steps/releases/latest/download/module.json
```

**By hand.** Copy this folder into `Data/modules/` of the instance's data root, under the name
`mistborn-gilded-steps-theme` — identical to the `id` in the manifest, or Foundry will refuse
it.

Either way, enable the module under **Settings → Manage Modules**, then pick a theme under
**Settings → Theme**.

## Status

**Nothing here has been validated at runtime.** The selectors and the theme API were read in the
published source of Cosmere RPG 3.1.0; the contrast was measured on rendered images of a
scaffold that reconstructs the sheet's markup. But a selector that exists is no guarantee of a
visible effect on screen.

Confirmed on 2026-09-08 in Foundry 13.351 with Cosmere RPG 3.1.0: the module loads and is
active, `cosmereRPG.api.registerTheme` is a function, the themes reach the list, and the sheet
render hook is **`renderCharacterSheet`** — the first of the four names the script listens for.
What has *not* been verified is the per-actor sheet registration introduced in 0.6.0.

One failure mode is known and quiet. If `registerTheme` is absent from a future build, the
themes never reach the list and the world stays on the system's own; the console says so.

| | |
|---|---|
| Foundry VTT | 13 (verified on 13.351, maximum 13) |
| Cosmere RPG | 3.1.0 (declares `maximum: "13"` — do not assume V14) |

## Two divergences, resolved on 2026-09-07

1. **Gears.** `VISUAL_IDENTITY.md` forbade decorative gearwork. Mario's decision: the
   prohibition governs **the portal**; the Foundry sheet is a table surface with its own lexicon,
   where a gear carries the setting instead of decorating the reading. The document was amended,
   with a date, and recovered the qualifier the vault directive always had — what is forbidden is
   the gear **without function**.

2. **Palette.** The rust and beige families were promoted into the contract in
   `mistborn-design-tokens.css` (v0.5), with their contrast figures measured. This theme is once
   again a **derivation** of the contract, not an adaptation. The portal stays in the iron
   family, which has not changed.

## Licence

This module is released under the **MIT License** — see [`LICENSE`](LICENSE). The CSS, the
script and the graphics generators are original work and you are free to use, adapt and
redistribute them.

**The MIT licence covers this folder only.** The rest of the repository is campaign material
that draws on third-party settings and is not licensed for reuse; see the repository README.

## Rights

Fan material, non-commercial. *Mistborn*, the Cosmere and Scadrial belong to Brandon Sanderson
and Dragonsteel Entertainment. The *Cosmere RPG* belongs to Brotherwise Games and its rights
holders. This module is not affiliated with, endorsed by, or produced by any of them, and it
redistributes none of their text, art, rules or code.
