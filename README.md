# world-news-20261124
[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/sastra-wev/world-news-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/sastra-wev/world-news-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

**The World in One Page** — the whole of Tuesday 24 November 2026's
world news summed up in a single 1024×1024 newspaper front page. The
hero story is President Zelensky's call for four-way peace talks —
Ukraine, Russia, the United States and Europe at one table, Kyiv
ready to meet "literally tomorrow" — drawn as the four flags behind
a negotiating table; alongside it, illustrated panels on the Cikande
factory-fire identification update (26 identified, 28 still missing)
and the US blacklisting chip-smuggling suspect Megaspeed on the
Entity List, briefs on the $3.5tn SpaceX–Tesla merger talks, the
pending Patriot decision, the Russian drone in Polish airspace and
China's death sentence for a spying official, and a "day in numbers"
strip.

The page is drawn programmatically with PIL (`render.py`) from the
day's verified reporting and committed as `entry.png`; `main.py`
copies that asset byte-for-byte to the output path, so the entry is
fully deterministic and needs nothing beyond the Python standard
library.

## Run it

```sh
python3 main.py   # writes /output/entry.png
```

To regenerate the artwork from source (requires Pillow):

```sh
python3 render.py # rewrites entry.png next to the script
```
