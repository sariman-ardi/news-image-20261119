[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/sariman-ardi/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/sariman-ardi/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

# World News in One Image — 19 November 2026

One image that sums up Thursday 19 November 2026's world news, built for
the [make.fun bounty](https://make.fun/bounty/news-image-20261119)
"news-image-20261119" (total prize $250, 1st place $50).

## The six stories

1. **GTA VI launches worldwide** — after 13 years, the game opens at
   midnight from New Zealand; ~17m pre-orders, $1.65bn+, Metacritic 99.
2. **Trump, Xi & Putin meet in Shenzhen** — first-ever trilateral summit
   on the APEC sidelines; nuclear weapons, Ukraine and Iran on the agenda.
3. **World court rules on Rohingya** — the ICJ delivers its verdict today
   at 10:00 CET in Gambia v. Myanmar; a possible first genocide ruling.
4. **Crimea Bridge hit a third time** — a strike just after midnight halts
   traffic; part of the roadway collapsed earlier in the week.
5. **Cyclone Akvan nears India** — the storm is set to make landfall
   between Machilipatnam and Puri on India's east coast.
6. **Anthropic debuts on Nasdaq** — shares trade today as ANT; an $81bn
   IPO at $83 a share, valuing the firm near $1.5tn, the biggest ever.

Sources: Reuters, Yonhap, BBC, The Hindu, IMD, ICJ.

## The image

`entry.png` (1024×1024, PNG) is a clean infographic drawn with Python's
Pillow library: a dated masthead, one panel per story with a short headline,
a one-sentence summary and a small drawn icon. No photographs and no
downloaded artwork — every pixel is drawn by the build script.

## How to run

```sh
python3 build_image.py        # rebuild entry.png from the news data
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` uses only the Python standard library, needs no network, and
copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`, verifying the copy
byte for byte with SHA-256. Running it twice writes byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
