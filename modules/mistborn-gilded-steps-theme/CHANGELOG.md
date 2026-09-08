# Changelog

The format follows semantic versioning. While the version is 0.x, nothing has been validated at
runtime.

## 0.9.1 — 2026-09-08

- **Fix: the number inside the resource bars could be unreadable.** Mario caught it on the light
  themes; measuring showed the dark ones had the mirror image of the same fault.
- The system writes that number inside the bar and paints it a fixed white, with the separator in
  `--cosmere-color-accent`. On a light theme the bar is dark and the separator went dark on dark;
  on a dark theme the bar is light and the white vanished. The fixed white only ever worked by
  accident.
- Two halves to the fix, both needed. The **empty** part of a bar now sits on the same side of the
  luminance divide as the filled part — they were on opposite sides, so a half-full bar had no
  single number colour that served both. And the number itself now comes from `--mgs-barra-tinta`,
  light where the bar is dark and dark where it is light.
- The override wins on **specificity**, nine classes against the system's seven, not on file
  order, which is what survives a system update.
- Measured on rendered pixels, with the prototype reproducing the system's own white rule so the
  cascade is actually exercised: 66 pairs — eleven themes, three bars, filled and empty — and the
  worst is 4.80:1.

## 0.9.0 — 2026-09-08

- **Bendalloy and Cromo**, the tenth and eleventh themes, built like Platina and Cádmio and named
  for what actually produces those colours. Bendalloy is a bismuth alloy, and a bismuth crystal
  takes exactly that lilac iridescence from its own oxide film; Cromo is chrome-oxide green, the
  industrial pigment — a green from a metal compound rather than from corrosion, which is what
  keeps it clear of Verdete.
- Bendalloy is the one colour in the set that is not a metal in open air. That was argued against
  and kept deliberately: it is the only theme that can mark what is invested rather than
  industrial.
- Worst measured pair, on rendered pixels: 5.50:1.
- **Every theme renamed after a metal**, at Mario's request: a player picks the sheet that looks
  like their character's metal. Ferrugem became **Ferro**, Negativo **Latão**, Registro
  **Electro**, Mínio **Cobre**, Verdete **Bronze** and Platina **Aço**; Peltre, Zinco, Cádmio,
  Bendalloy and Cromo were already metals. Eleven of the sixteen allomantic metals are covered.
- Only the **labels** changed. The ids did not, and that is deliberate: an id is what gets
  stored — in each player's theme preference and, for the sheets, on the actor — so renaming one
  would send every choice already made to something that no longer exists, and each sheet would
  fall back to the default in silence. `mgs-ferrugem` is still `mgs-ferrugem`; it just reads
  "Ferro".
- Eleven themes bring the stylesheet to about 1.6 MB, ~300 KB gzipped. Each further theme costs
  roughly 150 KB raw.

## 0.8.0 — 2026-09-08

- **Platina and Cádmio**, two light themes built the same way and the eighth and ninth of the set.
  Platina and the negative of Peltre: polished steel, a near-white plate,
  frames and hairlines in mid grey. It is the first theme whose **default metal is silver, not
  gold** — the grey frame is what Mario asked for, so gold would have defeated it. The other
  three metals are there, in versions dark enough to read on a pale ground.
- Its mist and gears are darker than the ground, like Registro's; on a white plate a pale metal
  simply disappears.
- **Cádmio** is Platina at another temperature: an ice-blue plate with steel-blue frames, named
  for the temporal metal. Same construction, same silver default.
- Worst measured pair, on rendered pixels: 5.16:1 for Platina, 5.24:1 for Cádmio.
- Nine themes bring the stylesheet to about 1.3 MB, ~250 KB gzipped.

## 0.7.0 — 2026-09-08

- **Four more themes**, taking the range from three to seven, at Mario's suggestion: a spread of
  metal finishes rather than variations on rust.
  - **Mínio** — red-oxide primer on structural steel.
  - **Verdete** — verdigris on bronze and copper in harbour air.
  - **Peltre** — matte pewter, the most neutral of the set.
  - **Zinco** — blued steel and galvanised zinc, kept deliberately away from the system's navy.
- All four are dark, since the two light themes already existed, and each brings its own four
  metals and its own mist and gear tints. Contrast was measured on rendered pixels against the
  hardest panel of each: the worst pair in the four is 4.95:1.
- Seven themes means seven sets of tiles: the stylesheet is now about 1 MB, ~200 KB over the wire
  once the server gzips it. The graphics are `data:` URIs of SVG text, which compresses to a fifth
  of its size.

## 0.6.1 — 2026-09-08

- **Fix: the per-actor sheets never reached the list.** They were registered on the `setup` hook,
  and in Foundry 13.351 that is too early to *find* the system's sheet class and too early to
  *register* one. `DocumentSheetConfig.registerSheet` writes straight to
  `CONFIG.<Document>.sheetClasses` only once `game.ready` is true; before that it queues, and
  `Game#setupGame` drains that queue in `initializeSheets()` — which first wipes `sheetClasses`
  entirely. The real order is `init` → `setup` → `initializeSheets()` → `ready`, so during both
  `init` and `setup` the registry is empty: the lookup for the base class found nothing, warned in
  the console, and gave up. Registration moved to `ready`, where the queue has been drained (the
  base class exists) and `game.ready` is true (the registration lands immediately).

## 0.6.0 — 2026-09-08

- **An appearance per actor.** Three sheets are registered under **This Sheet** in an actor's
  configuration — Ferrugem, Negativo, Registro — for both `character` and `adversary`. The choice
  is stored on the actor, so a table can have one NPC in rust and another in beige, and everyone
  sees them that way. It overrides the player's own theme for that window only.
- Each theme block now carries two selectors, `body.cosmere-theme-<id>` and
  `.application.cosmere-rpg.mgs-tema-<name>`, in one declaration list rather than two blocks: the
  graphics live in those variables as `data:` URIs, and duplicating them would have doubled the
  stylesheet for nothing.
- The per-actor metal rule gained a `:not([class*="mgs-tema-"])` guard. Without it the body-scoped
  rule — one element longer, therefore more specific — reached a sheet that had its own
  appearance and gave it the metal of the wrong palette.
- The sheet render hook is confirmed as `renderCharacterSheet`, read from a live console in
  13.351. The Status section no longer claims it is unknown.

## 0.5.0 — 2026-09-08

- **Three themes on the system's own list**, registered through
  `cosmereRPG.api.registerTheme()` instead of overriding the Default: *Ferrugem*, *Negativo* and
  *Registro*. The specificity trick the previous versions depended on — a leading `:root` to win
  by one element — is gone, because there is no longer anything to win against.
- **Negativo**, a new theme: the rust plate at forge heat, with a hot orange ground and gears and
  smoke in near black.
- **Mist redrawn.** It was blurred fractal noise; it is now ribbons whose spine comes from
  integrating a curvature function — a funnel opening at the top, a lit and a shaded side, a roll
  at the end, hooked tendrils shed from the edge. Built on reference drawings supplied by the
  project owner; no traced geometry.
- **Mist in two planes**, one behind the gears and one in front, so it wraps the mechanism
  instead of sitting flat behind it. Transparency is per-path `fill-opacity`, never group
  `opacity`, so overlapping ribbons accumulate.
- **Side bands.** Left and right edges now carry their own tile. This needs per-layer
  `background-position`, `-repeat` and `-size`; without those three the tile floods the sheet,
  which is what happened on the first attempt.
- **Veil.** Measured on rendered pixels, the character's name over the dense mist fell to 3.33:1
  in Ferrugem and 1.45:1 in Negativo. A gradient of the sheet's own colour, absent at the edge
  and full where text lands, restores it. The worst pair in the theme now measures 4.62:1.
- `--mgs-fumaca-fraca` darkened from `#4d2d0d` to `#43270b`: it measured 4.23:1 under the header
  mist.
- Metals are now explicitly orthogonal to the theme: silver, gold, copper and tin work in all
  three, with their own values in each.
- Geometry is instanced with `<use>` rather than repeated. A tile went from 368 KB to 33 KB.
- New generator `tools/bruma.py`; `tools/contraste.py` added for token-level contrast checks.
- The API method names and metal keys stay Portuguese. Renaming was considered and deferred: the
  keys are stored as actor flags, so a rename drops every character's metal without a migration.

## 0.4.0 — 2026-09-07

- Dark mode in orange rust. A darker, browner variant was evaluated and rejected.
- Light mode in beige with red hairlines and near-black brown ink.
- Bands of gears submerged in mist at the head and foot, procedural, with a version of their own
  for each mode.
- Four metals per character — silver, gold, copper, tin — applicable to the document body or to
  each sheet.
- Life green adjusted from `#5f9c83` to `#6cab90`: against the orange rust, the previous tone
  measured 4.08:1 on the lighter panel.

## 0.3.0

- Per-character metal, with the mark stored on the actor.
- A denser band, more covered by mist.

## 0.2.0

- Gear and mist graphics, procedural, with no image files.

## 0.1.0

- First sheet: palette, surfaces and resource bars.
