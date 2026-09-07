# Content Policy

This repository is **public**. Everything committed here is visible to anyone, and Git history
preserves what was published even after it is deleted. The rule of thumb is simple: **when in
doubt, don't commit.**

## Allowed

- Original writing introducing the campaign, the setting and the tone.
- Character creation guidance written for this table.
- House rules already promoted to project canon, written in our own words.
- Lore already revealed to the table, or safe by nature.
- Handouts made for players to see.
- Session chronicles, reviewed, with no backstage and no unresolved plot solutions.
- Original project artwork, with provenance, authorship and licence recorded in
  `docs/assets/ATTRIBUTION.md`.
- Original code: the portal's CSS and HTML, and the Foundry modules under `modules/`.

## Not allowed

- PDFs, EPUBs or scans of the *Mistborn Handbook*, the *Mistborn World Guide*, the *Cosmere
  RPG* or any commercial work — nor long excerpts from them.
- Official tables, stat blocks, talent lists and whole rules copied out. Citing a page of the
  source is fine; reproducing it is not.
- Art, covers, logos and maps belonging to Dragonsteel, Brotherwise or any third party.
- GM notes, campaign secrets, clocks, fronts, future scenes, faction agendas and the true
  identity of antagonists.
- Internal mechanics, prototypes and studies not yet approved.
- Anything past the current spoiler line (see `SPOILER_POLICY.md`).
- Heavy working files: PSD, AI, INDD, video, raw exports, temporary files.
- Google Drive shortcuts (`.gdoc`, `.gsheet`, `.gslides`) and `.lnk`, which preserve no content
  in Git.
- Any personal data of players: legal name, email, phone number, address.

## The practical test

If the text answers a player's question without spoiling a discovery still ahead, and without
reproducing someone else's work, it belongs in the wiki. If it reveals backstage, the solution
to a mystery, a complete antagonist stat block or licensed material, it stays in the vault.

## Before publishing

1. Is the source note in the vault marked player-visible?
2. Was the text **rewritten** for the public, rather than copied from a GM note?
3. Does any sentence reproduce a commercial source?
4. Does anything cross the current spoiler line?
5. Do images have authorship, process and licence on record?

Only then: `git add`.

## If something wrong gets published

Deleting the file **is not enough** — the history remains. The procedure is: remove the
content, tell Mario, and decide explicitly between rewriting history (`git filter-repo`) and
recreating the repository. Do not improvise.
