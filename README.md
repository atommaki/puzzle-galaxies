# Galaxy puzzle

Inspired by https://www.puzzle-galaxies.com/
Quote from the site:
"The rules are simple. You have to divide the grid into regions (galaxies) in such a way that:
 * Each region has exactly 1 white circle in it.
 * The circle is the center of its rotational symmetry. In other words: If you rotate the region around the circle at 180° you should get the same shape, position and orientation.
 * A region cannot be a neighbour to itself "

For example, this is a puzzle with marked galaxy centers (ID=381831 on puzzle-galaxies.com):
```
┌───┬───┬───┬───┬───┬───┬───┐
│   │   │   │   │   │   │   │
├───┼───o ──┼───┼───o ──┼─o ┤
│   │   │   │   │   │   │   │
├───┼───┼───┼───┼───┼───┼───┤
│   │ o │   │   │   │   │   │
├───┼───┼───┼─o ┼───┼───┼───┤
│ o │   │   │   │   │ o │   │
├───┼─o ┼───┼───┼───┼───┼───┤
│   │   │   │   │ o │   │   │
├───┼───┼───┼───┼───┼───┼───┤
│   o   │   │ o │   │ o │   │
├───┼───┼───┼───┼───┼───┼───┤
│ o │   │   │   │   │   o   │
└───┴───┴───┴───┴───┴───┴───┘
```

And this is the (only possible) solution:
```
┌───────────────┬───────┬───┐
│               │       │   │
│       o       │   o   │ o │
│               │       │   │
├───────────┬───┼───────┴───┤
│     o     │   │           │
├───┬───┬───┤ o │   ┌───┐   │
│ o │   │   │   │   │ o │   │
├───┤ o │   └───┘   └───┘   │
│   │   │         o         │
│   └───┤   ┌───┐   ┌───┐   │
│   o   │   │ o │   │ o │   │
├───┐   │   └───┘   ├───┴───┤
│ o │   │           │   o   │
└───┴───┴───────────┴───────┘
```


# Galaxy puzzle solver

This python script solves these kind of puzzles. As far as I can tell it can solve any puzzles from the puzzle-galaxies.com site, but I can't be 100% sure. Becuase of the puzzles you can find on the site my scipt always assumes the puzzle has one and only one solution (it raises an exception if it detects multiple possible soulutions)


