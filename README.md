**English** · [简体中文](README.zh-CN.md)

<p align="center">
  <img src="assets/logo.svg" width="112" height="112" alt="myygo logo">
</p>

<h1 align="center">myygo</h1>
<p align="center"><strong>Yu-Gi-Oh! card effects as data</strong></p>
<p align="center">A compact, lambda-driven DSL that turns card prose into a uniform ten-field effect tuple — auditable like text, structured like code.</p>

> **Archived design sketch.** Not runnable, not maintained, and no host engine is included. The artifact is the DSL design and the card data. See [archive notes](docs/project-status.md).

[Quick start](#quick-start) · [What it can do](#what-it-can-do-now) · [Architecture](#architecture) · [Develop](#how-to-develop) · [Roadmap](#roadmap)

## Why it is interesting

Yu-Gi-Oh! effects are written as prose. Implementing them usually means scattering conditions, costs, targets and resolutions across ad-hoc functions. myygo keeps the Chinese card text directly above its effect data and forces every effect through the same shape:

```text
[ type, loc, cond, costCheck, cost, opCheck, opTarget, op, countLimit, flag ]
```

Each hook is either `None` or a plain lambda over inferred context (`c` current card, `tp` current player, `tg` targets, `re` reason effect, …). Card and zone operations are chainable (`Get`, `L.*`, `Cards.is*`, `Cards.spsum`, …), so a complete effect reads as a few lines next to the text it implements.

The repository is a sketch, not an engine: it shows the authoring layer and a set of real card entries.

## Quick start

No install, no dependencies, no entrypoint. Start with the contract, then read one card.

```bash
git clone https://github.com/ZisIsNotZis/myygo.git
cd myygo
sed -n '1,72p' script.py     # the DSL contract
sed -n '73,94p' script.py    # first card: Chinese text + effect data
```

Then continue through `script.py`; each card is a block of Chinese text followed by its effect list. `script2.py` repeats the same cards against a terser syntax that was never finished.

## What it can do now

- **One shape for different effect classes** — activation (`IGNITE`), trigger (`SUMED`, `DESTROYED`, …), "do" triggers (`ATKING`, …), continuous effects and summon procedures all use the same tuple.
- **Chain predicates and actions** — `L` builds partial lambdas, `Cards` treats zero, one or many cards as one collection, and `Get` / `Choose` handle zones and choices.
- **Encode limits and flags** — per-turn counters, shared counter IDs, `CONTINUOUS`, `NODISABLE`, `TOEQUIPER`, and related flags.
- **Keep text and logic together** — 11 card entries in each script, with the Chinese card text directly above the effect data.
- **Stay dependency-free** — two plain Python files with no imports; the engine that supplies the globals is deliberately absent.

## Architecture

```text
.
├── assets/logo.svg          project mark
├── docs/project-status.md   provenance and archive status
├── script.py                DSL reference + the more complete card set
├── script2.py               alternate revision: renamed constants, unfinished micro-syntax
├── README.md                this file
├── README.zh-CN.md          Simplified Chinese README
├── LICENSE                  AGPL-3.0-only
└── .gitignore
```

Three layers are visible in the source:

1. **Contract** — the module docstring in `script.py` (lines 1–72) defines the ten fields, hook arguments, zones, flags and helper vocabulary. `script2.py` repeats it with small drift.
2. **Helpers** — `L`, `Cards`, `Get`, `Choose`, `Register`, `Draw`, zone constants and flags. They are referenced, never defined here.
3. **Card data** — one list of effect tuples per card, preceded by its Chinese text. Both scripts carry the same 11 cards; `script.py` is the more complete version.

The host engine, card database and any executable entrypoint are not in this repository. Neither script imports anything or parses as written.

## How to develop

This is an archive, so there is no build, test suite or supported workflow. If you want to resume the sketch:

1. Read the module docstring in `script.py` first; it is the closest thing to a specification.
2. Keep the ten-field shape and the inferred hook arguments stable, or update the contract and every card together.
3. Treat `script.py` as the reference. `script2.py` is an experiment, not a successor.
4. Fix the parse errors before adding effects: `script.py` is missing a comma between the `Choose(...)` call and the `[1, 1]` limit (lines 91–92); `script2.py` switches at line 308 to undeclared lowercase micro-syntax (`ignite`, `hand|mzone`, `equip(...)`) and leaves its final card entry unterminated.
5. Keep each card's Chinese text directly above its effect list.

## How to contribute

The project is archived and not maintained, so pull requests may not be reviewed. If you want to build on the DSL, fork it. If you find a factual error in the documentation, an issue with the exact file and line is welcome.

## Roadmap

### Implemented

- [x] Ten-field effect contract documented in the module docstring.
- [x] Helper vocabulary sketched: `L`, `Cards`, `Get`, `Choose`, `Register`, `Draw`, zones and flags.
- [x] 11 card entries with Chinese text in each script.
- [x] Provenance and archive status recorded in `docs/project-status.md`.
- [x] AGPL-3.0-only license.

### Planned — only if the sketch is resumed

- [ ] Make both scripts parse as Python.
- [ ] Collapse the duplicate card data into one source of truth.
- [ ] Extract the DSL contract into a standalone specification.
- [ ] Add a minimal host-engine adapter and executable examples.
- [ ] Decide whether `script2.py`'s terser micro-syntax is worth defining — or delete it.

No dates are promised; the repository is an archive.

## Future vision

If resumed, myygo would be the authoring layer of a small, readable Yu-Gi-Oh! rules engine: card text and executable effect data side by side, with an engine small enough to audit. The interesting question is not card coverage, but whether messy, interacting card effects can stay declarative without turning into a second programming language.

## License and third-party data

The repository's code is licensed under [AGPL-3.0-only](LICENSE). Copyright © 2026 ZisIsNotZis.

The Chinese card-effect texts, passcodes and set/attribute constants are Konami card data, quoted as data rather than code to implement the rules. They are nominative references; no Konami code or artwork is included. Yu-Gi-Oh! is a trademark of Konami Digital Entertainment. This is an unofficial project, not affiliated with or endorsed by Konami.
