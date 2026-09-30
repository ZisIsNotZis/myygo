# myygo

**A small DSL for describing *Yu-Gi-Oh!* card effects as data**, plus two
working scripts of card-effect definitions (Galaxy/Photon and Horus
archetypes) written against that DSL.

### What it is

The DSL models an effect as a fixed 9-slot tuple
`[type, loc, condFn, costChkFn, costFn, opChkFn, opTargetFn, opFn, countLimit, flag]`
where every hook is a plain lambda over inferred arguments (`c` current card,
`tp` current player, `tg` targets returned by the previous hook, `re` reason
effect, …). Cards are always a `Cards` collection object with chainable
predicates/actions (`Get(...)`, `L.fn(...)`, `Cards.isSet/isCode/canSpsum/spsum/...`).
The authoritative description is the module docstring at
`/home/z/my/myygo/script.py:1-72` (`script2.py:1-72` repeats it with slight
drift).

### Why it exists

It is the card-authoring layer of a personal *Yu-Gi-Oh!* rules engine: the
engine provides the globals (`IGNITE`, `Get`, `L`, `Cards`, `Choose`, `Draw`,
…) and these files supply the card behaviour. Each effect is preceded by the
official card text as a Chinese docstring, so the file doubles as a
card-implementation checklist.

### How to run

None — **not runnable as-is.** Neither file imports anything and neither
defines the engine symbols it uses (`IGNITE`, `Get`, `L`, `Cards`, `Choose`,
`Draw`, `MZONE`, …). They are effect-data modules that must be loaded by the
engine, which is **not present in this directory**. No setup file, no
entrypoint, no tests. Cross-check: the nearest sibling, `/home/z/my/ygopy/model.py`,
is a *different* engine port (ygopro-core-style `Effect_` / `Card_` /
`GetOriginalCode` / `SUMMON_TYPE_SPECIAL`) and defines none of the DSL globals
used here (`IGNITE`, `Cards`, `L`, `Get(filter, selfZone, …)`), so it is not the
host for these scripts; the actual engine was not located.

### Status

**deprecated (2025 era) – kept as an archive.** Not because the libraries are
old (there are none), but because this is an orphaned fragment: the engine that
consumes the DSL is absent, and `script2.py` is an unfinished intermediate
revision. `script.py` (2025-04-16) is the coherent version; `script2.py`
(2025-04-17) copies the card data, renames some constants (`BATTLED`→`BATD`,
`isLevel`→`isLv`, `isMon`…), and then breaks down at
`/home/z/my/myygo/script2.py:308-316`: it switches to an undeclared lowercase
micro-syntax (`ignite`, `hand|mzone`, `equip(...)`) that the documented API does
not define, the `'''` docstring at line 310 is unterminated, and the final two
entries are never closed. Read as a design sketch of a terser DSL, not as code.

### License

No `LICENSE` file and no copyright header anywhere in the directory: the
implementation is the owner's own, all rights reserved by default. Two
third-party elements are embedded as **data, not code**: (a) the Chinese
card-effect texts used as docstrings throughout, and (b) card passcodes
(e.g. `93717133`, `16528181`, `98555327`, `863795`) and set/attribute constants
— both are Konami *Yu-Gi-Oh!* official card data. They are quoted for the
purpose of implementing the rules and should be treated as nominative
references if this is ever published; no Konami code or assets are copied.
