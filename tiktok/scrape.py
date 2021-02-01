import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver


def create_browser():
    """Returns a Selenium Chrome WebDriver instance."""
    browser = webdriver.Chrome('../utilities/chromedriver')
    return browser


snapshots = []


def snapshot(browser):
    """Appends the current HTML of the page to the
    snapshots list.
    """
    global snapshots
    snapshots.append(browser.page_source)


def scroll_and_snapshot(browser, max_scroll_secs):
    """Scrolls through the full height of a profile page while
    frequently taking snapshots of the page's HTML.
    """
    SCROLL_PAUSE_TIME = 2
    last_height = browser.execute_script("return document.body.scrollHeight")
    end_time = time.time() + max_scroll_secs

    # Attribution for scrolling mechanism:
    # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python#27760083
    while time.time() < end_time:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        snapshot(browser)

        if new_height <= last_height:
            break
        else:
            last_height = new_height


def collect_links(snapshots):
    """Goes through the HTML snapshots and returns a set of unique
    img elements.
    """
    links = []
    image_pattern = re.compile(r'background-image: url\("(.+)"\)')
    video_pattern = re.compile('src="(.+)"')

    for html in snapshots:
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.find_all('div', class_='image-card')
        # videos = soup.find_all('video')

        for card in cards:
            # Get image link
            match_obj = image_pattern.search(str(card))
            image_link = match_obj[1]
            new_soup = BeautifulSoup(str(card), 'html.parser')
            videos = new_soup.find_all('video')
            match_obj = video_pattern.search(str(videos))
            video_link = match_obj[0]
            # Get video link
            links.append({'image': image_link, 'video': video_link})

    return links


URL = 'https://www.tiktok.com/@mikeservinofficial'

browser = create_browser()
browser.get(URL)

scroll_and_snapshot(browser, 8)


links = collect_links(snapshots)
browser.quit()


def vid_link(obj):
    return {
        'image': obj['image'],
        'video': obj['video'].src
    }


links = map(vid_link, links)
links = list(links)
print(len(links))
print(links[0])
