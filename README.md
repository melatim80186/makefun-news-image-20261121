# The World — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/melatim80186/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/melatim80186/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One image that sums up the world's news of Saturday 21 November 2026:
a broadsheet front page for a single day, built for the make.fun
news-image-20261121 competition.

## Running it

```sh
python3 main.py
```

The program copies the bundled `entry.png` to `/output/entry.png`
(or `$MAKEFUN_OUTPUT_DIR/entry.png` when that variable is set),
creating the directory first. It refuses to finish unless the copy
is byte-for-byte identical to the bundled file, so the grader always
sees exactly the image in this repository. Python 3.13, standard
library only — no installs, no network, and the same bytes on every
run.

## What the page carries

Three stories lead: Wall Street sliding into correction as the AI
sell-off deepens, with the Nasdaq down 5.28% and Nvidia about 14%
in the worst week since Covid; Denmark expelling a Russian diplomat
over an alleged plot to kill a Ukrainian rapper; and KL Rahul's
unbeaten century taking India to 255/1 on day three at Wellington,
in reply to New Zealand's 368.

Eight further stories follow — Trump home from his meeting with Xi
and Putin, Estonia closing its border with Russia, fresh Russian
strikes on Kyiv and Kryvyi Rih, COP31 closing divided in Antalya,
Odisha counting the cost of Cyclone Akvan, the guilty verdict in
the Palisades Fire arson trial, new UK–EU deals signed in Brussels,
and the ICC awarding India two cricket World Cups — and nineteen
more fill the "Also Today" strip, from Zverev at the ATP Finals
to Argentina's new disability-rights law. Thirty stories across
seven continents, all dated Saturday 21 November 2026.

Each story was checked against the day's reporting: Reuters, AP,
AFP, the BBC, Al Jazeera, the IMD, The Hindu, the Times of India,
Jagran Josh and COP31.

## About the image

The page is a 1024×1024 PNG of 486,999 bytes, inside the contest's
1 MiB and 1024×1024 limits. Its three lead pictures were drawn
for this front page — a storm-clouded exchange under a plunging
red chart line, Copenhagen's Nyhavn waterfront, and a batsman
at the Basin Reserve — while every headline, caption and listing
was typeset by the build script, making the whole page a single
deterministic file.
