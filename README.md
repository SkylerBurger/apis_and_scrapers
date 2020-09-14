# APIs and Scrapers

This repo is a collection of Jupyter Notebooks in which I try to collect data using APIs and web scraping. These examples are for educational purposes only.

### JavaScript Dependencies

- [`cookie-parser`](https://www.npmjs.com/package/cookie-parser) - Library for setting, accessing, and clearing cookies on request and response objects.
- [`dotenv`](https://www.npmjs.com/package/dotenv) - Library for populating environment variables from a `.env` file.
- [`express`](https://www.npmjs.com/package/express) - Lightweight web framework.
- [`superagent`](https://www.npmjs.com/package/superagent) - Library for making HTTP requests.

### Python Dependencies

- [`beautifulsoup`](https://pypi.org/project/beautifulsoup4/) - Library for web scraping that makes parsing HTML content a breeze.
- [`environs`](https://pypi.org/project/environs/) - Library for reading in environment varbiales.
- [`google-api-python-client`](https://pypi.org/project/google-api-python-client/) - Library for interacting with various Google APIs with Python.
- [`jupyterlab`](https://pypi.org/project/jupyterlab/) - Library for running a Jupyter Lab server and Jupyter Notebooks.
- [`requests`](https://pypi.org/project/requests/) - Library for making HTTP requests.
- [`selenium`](https://pypi.org/project/selenium/) - Library for controlling web browsers.

## AdultSwim

This scraper gathers details for available seasons and episodes featured on a specific show's page on [AdultSwim.com](https://www.adultswim.com/videos/).

## Craigslist

This scraper goes through the housing page of Seattle's Craigslist and collects the titles of all of the listings on the first page of listings.

## Instagram

This scraper takes in an Instagram profile name. If the user's profile is public, the scraper will download every photo available on their profile.

## Medium

This scraper takes in the URL to a Medium article and scrapes the text content of the article. The text content is then written to a Markdown file.

## The Movie Database (TMDB)

This lightweight server goes through the auth process for generating account-approved access tokens as described in TMDB API version 4's documentation. Once the access token has been generated it makes a quick request to retrieve info about every list the user has created (even private lists).

## Wikipedia

This scraper attempts to locate areas where citations are needed within a specific article on Wikipedia.

## YouTube

This is an example of using a library to access API data from YouTube without having to make the API calls directly with a tool like `requests`.
