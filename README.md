# Adaderana News Scraper

Scrapy project for crawling Adaderana news archive with optional filters by category, year, month, and day.

## System requirements

- Linux, macOS, or Windows
- Python 3.10+
- `pip`
- Network access to `www.adaderana.lk`

## Setup

1. Create and activate a virtual environment:
   - Linux/macOS:
     - `python3 -m venv exenv`
     - `source exenv/bin/activate`
   - Windows (PowerShell):
     - `python -m venv exenv`
     - `exenv\Scripts\Activate.ps1`

2. Install requirements:
   - `pip install -r requirements.txt`

3. Move to the Scrapy project directory:
   - `cd newscraper`

## Usage

Run the spider:
- `scrapy crawl derana`

Save output while crawling:
- JSON: `scrapy crawl derana -O complete_scrape.json`
- CSV: `scrapy crawl derana -O adaderana_complete_news_archive.csv`

## Shell arguments (filters)

Spider supports these optional args:
- `-a category=<ids>`
- `-a year=<years>`
- `-a month=<months>`
- `-a day=<days>`

Pass multiple values as comma-separated lists.

Examples:
- One date slice:
  - `scrapy crawl derana -a year=2020 -a month=03 -a day=17 -O out.json`
- Multiple years/months/days:
  - `scrapy crawl derana -a year=2020,2021 -a month=03,04 -a day=1,15 -O out.json`
- Category + year:
  - `scrapy crawl derana -a category=36,37 -a year=2024 -O out.json`

### Category IDs

- `36` Breaking News
- `37` Sports
- `38` Entertainment
- `44` AdaderanaBiz
- `48` Technology
- `49` Covid-19
- `1` Top News Story 1
- `2` Top News Story 2

(From [newscraper/newscraper/options_info.txt](newscraper/newscraper/options_info.txt))

## Pause and resume crawl

Use Scrapy `JOBDIR` to persist crawl state.

Start crawl with state directory:
- `scrapy crawl derana -s JOBDIR=crawls/derana-run-1 -O out.json`

Pause:
- Press `Ctrl+C` once and wait for shutdown to finish.

Resume later:
- Run the exact same command again (same spider args and same `JOBDIR`).

Notes:
- Use a different `JOBDIR` for each separate run.
- `JOBDIR` stores scheduler/request state, not the feed output file.

## Project paths

- Scrapy config: [newscraper/scrapy.cfg](newscraper/scrapy.cfg)
- Spider: [newscraper/newscraper/spiders/derana-spider.py](newscraper/newscraper/spiders/derana-spider.py)

