# APIs and Scrapers

This repo is a collection of Jupyter Notebooks in which I try to collect data using APIs and web scraping. These examples are for educational purposes only.

### Dependencies

- [`beautifulsoup`](https://pypi.org/project/beautifulsoup4/) - Library for web scraping that makes parsing HTML content a breeze.
- [`environs`](https://pypi.org/project/environs/) - Library for reading in environment varbiales.
- [`google-api-python-client`](https://pypi.org/project/google-api-python-client/) - Library for interacting with various Google APIs with Python.
- [`jupyterlab`](https://pypi.org/project/jupyterlab/) - Library for running a Jupyter Lab server and Jupyter Notebooks.
- [`requests`](https://pypi.org/project/requests/) - Library for making HTTP requests.
- [`selenium`](https://pypi.org/project/selenium/) - Library for controlling web browsers.

## Craigslist

This scraper goes through the housing page of Seattle's Craigslist and collects the titles of all of the listings on the first page of listings.

### To Do

- [ ] Grab links for posts as well. Possibly hot-link the extracted title.

## Instagram

This scraper takes in an Instagram profile name. If the user's profile is public, the scraper will download every photo available on their profile.

### To Do

- [ ] Add a way to check if a post is a multi-image post. If so, find out how to collect the URLs for all of the images in the post.
- [ ] Find out whether or not a post is a video and see if there is a way to extract it.

## Medium

This scraper takes in the URL to a Medium article and scrapes the text content of the article. The text content is then written to a Markdown file.

### To Do

- [ ] Find a way to identify section headings, code blocks, and images to add them to the final Markdown output file.

## YouTube

This is an example of using a library to access API data from YouTube without having to make the API calls directly with a tool like `requests`.

### To Do

Develop further examples/use-cases.