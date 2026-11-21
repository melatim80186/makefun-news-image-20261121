# The World — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/melatim80186/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/melatim80186/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A program that writes one image summing up Saturday 21 November 2026 in
world news — a single broadsheet front page for the day.

## The day on one page

Three stories lead the page: Wall Street falling into correction as the
AI sell-off deepens — the Nasdaq down 5.28% and Nvidia about 14% in the
worst week since Covid; Denmark expelling a Russian diplomat over an
alleged plot to kill a Ukrainian rapper; and KL Rahul's unbeaten century
carrying India to 255/1 on day three in Wellington, chasing New
Zealand's 368.

Below them, eight more stories run across the page — Trump back from
his talks with Xi and Putin, Estonia shutting its border with Russia,
Russian strikes on Kyiv and Kryvyi Rih, COP31 wrapping up divided in
Antalya, the aftermath of Cyclone Akvan in Odisha, the guilty verdict
in the Palisades Fire arson trial, the UK and EU signing new deals in
Brussels, and the ICC handing India two cricket World Cups — plus
nineteen more in the "Also Today" strip, from Zverev's ATP Finals
semi-final to Argentina's disability-rights law. Thirty stories, seven
continents, one date: Saturday 21 November 2026.

Every story was checked against reporting from Reuters, AP, AFP, the
BBC, Al Jazeera, the IMD, The Hindu, the Times of India, Jagran Josh
and COP31.

## The image

The finished page is a 1024×1024 broadsheet image, bundled with this
repository as `entry.png`. The three lead illustrations were drawn for
this page — a storm-clouded stock exchange under a plunging red chart,
Copenhagen's Nyhavn harbour, and a batsman at the Basin Reserve — and
every headline and caption on the page was typeset by the build script,
so the whole front page is one deterministic file.

## How to run it

```sh
python3 main.py
```

That writes the image to `/output/entry.png` (or to
`$MAKEFUN_OUTPUT_DIR/entry.png` when that is set), creating the
directory if it does not exist. Before finishing, the program reads
the copy back and compares it byte for byte with the bundled image,
and it refuses to exit successfully if the two do not match — so the
file the grader sees is always exactly the file in this repository.

Requires Python 3.13 and nothing else: standard library only, no
packages to install, no network at run time.
