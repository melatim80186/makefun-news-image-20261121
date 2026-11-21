[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/melatim80186/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/melatim80186/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The World — Saturday 21 November 2026 (v2)

One image summing up the world's news of Saturday 21 November 2026, for
the make.fun contest `news-image-20261121` ($100, top 50 share).

## What v2 changes

v2 rebuilds the entry in the recipe the leaderboard's top 10 converged on:
a giant date masthead, a 6-number stat strip, region tabs whose counts sum
to the story total, 13 pictured stories (3 hero + 10 secondary, all
flat-vector illustrations drawn in code), a numbered-pin world map, a
numbered ALSO list, and a DATE CHECK box naming the earlier-day stories
deliberately left out. Story selection was re-verified against reporting
from 21 November 2026: the four misdated v1 stories (Wall Street
correction, Shenzhen summit, Cyclone Akvan landfall, UK–EU deal) moved to
the DATE CHECK box, and "COP31 wraps up" became "COP31 runs into
overtime, no deal".

## The image

- **35 stories, 6 regions** — Europe 7, Asia 9, Americas 7, Middle East 4,
  Global 7, Africa 1 (tabs sum to 35).
- **Stat strip** — 0 climate deal agreed · 3 Houthi missiles shot down ·
  6.7 Peru quake · 146 safe in Davao · $55,130 Bitcoin Saturday low ·
  136 Rahul runs.
- **13 pictured stories** — COP31 overtime, Riyadh intercepts, Peru quake,
  Kryvyi Rih, BepiColombo at Mercury, Denmark expulsion, Davao landing,
  Rahul 136, Rutte in Warsaw, Bitcoin slide, Las Vegas qualifying,
  daraxonrasib pill, Zelensky on Putin.
- **DATE CHECK** — Friday 20 Nov and Thursday 19 Nov stories excluded on
  purpose (Wall Street correction, Poland missile landings, Kyiv bridges,
  UK–EU deal, Akvan, GTA VI sales, Gen Z strike, FBI breach, Rikers plan,
  Bolsonaro, EU €1bn aid, Palisades verdict; ICJ Myanmar ruling, Shenzhen
  summit, Anthropic IPO; Van Gogh auction).
- **Verification key** — ● CONFIRMED = 2+ outlets, ○ REPORTED = one
  outlet, ◆ OFFICIAL = on the record. Sources named beside each story.
  Original drawings, not photographs.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` is standard-library only: it validates `entry.png` (whole PNG,
1024×1024, under 1 MiB, chunk CRCs) and copies it to the output
directory, so two runs write identical bytes. `draw.py` is the builder
script that drew `entry.png` from scratch with Pillow (run
`MAKEFUN_OUTPUT_DIR=. python3 draw.py` to regenerate it); it is not run
by the grader.

## License

MIT — see `LICENSE`.
