# Changelog

The format follows semantic versioning. While the version is 0.x, nothing has been validated at
runtime.

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
