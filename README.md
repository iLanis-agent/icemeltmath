# Ice melt math

Sidewalk de-icing arithmetic: the walk names the grams, the grams name the bag, and the forecast names the chemistry.

Live at https://ilanis-agent.github.io/icemeltmath/

## The three tools

- **Melt plan** - grams = walk area x a labeled rate by ice thickness (40 g/m2 frost film, 80 thin glaze, 140 stubborn sheet), with film, glaze, sheet and shovel-first bands.
- **Bag plan** - bags = ceil(grams / 1000 / labeled 10 kg bag), with the leftover kilograms and one-bag, shelf-stack and pallet bands.
- **Chemistry plan** - the coldest night picks the chemistry: rock salt to -9 C, magnesium chloride to -15 C, calcium chloride to -29 C, sand for grip below that.

## Formulas and limits

- Kilogram leftovers are rounded to one decimal (round half up), mirroring the oracle float-for-float.
- Every number the app borrows is labeled in the interface: spread rates, bag size, chemistry temperature floors.
- Illustrative planning arithmetic only. Melt is for the film the shovel leaves behind - clear the snow first. Chlorides burn paws and young concrete, and sweep up what the melt leaves. Real footing comes from boots and sand, not from chemistry. Product labels govern real spread rates.

## Development

- `engine.js` - calculation and render engine (browser global `IceMeltMath`, CommonJS for tests).
- `oracle.py` - Python mirror of the engine; regenerates `expected.json`.
- `test.js` - runs every case through the engine and compares fields and render strings: `node test.js`.
