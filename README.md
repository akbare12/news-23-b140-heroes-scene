[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b140-heroes-scene/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b140-heroes-scene/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# THE WORLD TODAY — Monday 23 November 2026

One image summing up 23 November 2026's world news: the AI rout that hit Asian
markets, the UN chief's call to regulate AI before it's too late, and the US lead
over China at its record low.

## The three big stories

- **AI rout hits Asia** — the Kospi fell 3.3% to 4,708.54, shedding 161 points
  (intraday −5.8%); Samsung −3.1%, SK Hynix −2.5%.
- **Guterres: regulate AI before it's too late** — at the Bridgetown summit in
  Barbados, 150 delegates backed a risk framework (a blueprint, not a treaty).
- **US lead over China at record low** — Asia Power Index 2026: US 78.9, China
  73.6, the 5.3 gap the narrowest since 2018; India third at 40.5.

Plus 10 more stories, 18 also-on-Monday items, a world map with 13 pins, and a
DATE CHECK box that keeps out stories from other days (Dems reach 258, Sparta II
fire, El Chapo Isidro captured, EU–Indonesia pact, Nigeria boat, ICJ Myanmar
ruling) — 31 stories in total, all dated 23 November 2026.

## How it is built

`draw.py` (Pillow) renders `entry.png` (1024×1024). `main.py` (stdlib only)
validates the PNG and copies it to `$MAKEFUN_OUTPUT_DIR/entry.png`:

```sh
python3 draw.py
MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py
```

Scenes are drawn illustrations, not photographs. Figures as reported 23 Nov 2026.
