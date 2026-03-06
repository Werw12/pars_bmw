# BMW Used Cars Scraper

A Scrapy-based web scraper that extracts used car listings from the official BMW Used Cars website and stores them in an SQLite database.

## Features
- Bypasses CSRF protection.
- Scrapes the first 5 pages of car listings.
- Identifies electric vehicles (EVs), properly storing `NULL` in the `engine` column.
- Accurately captures EV `range` values.
- Retrieves `Exterior` and `Upholstery` fields using deep search if standard values are missing.

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Werw12/pars_bmw.git
   cd pars_bmw
   ```

2. **Create a virtual environment & install requirements**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the Spider**:
   ```bash
   scrapy crawl bmw
   ```
   Data will be automatically inserted into the provided `bmw_cars.db` file.