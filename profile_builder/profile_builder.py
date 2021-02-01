from random import randint
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver


class ChromedriverMixin:
    """A Mixin Class for adding the ability to generate a Selenium Chrome 
    Webdriver instance.
    """
    def _get_browser(self):
        """Creates and returns a Selenium Chrome WebDriver instance."""
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        browser = webdriver.Chrome(
            '../utilities/chromedriver', 
            options=options,
        )

        return browser


class TikTokProfile:
    def __init__(self, profile_name):
        self.profile_name = profile_name
        self.profile_url = f'https://www.tiktok.com/{profile_name}'
        self.image_urls = []

    @property
    def image_count(self):
        return len(self.image_urls)


class InstaProfile:
    """Models an Instagram profile."""
    def __init__(self, profile_name):
        """Instantiates an InstaProfile object."""
        self.profile_name = profile_name
        self.profile_url = f'https://www.instagram.com/{profile_name}'
        self.image_urls = []

    def download_images(self, max=None):
        """Downloads images to the current working directory.

        Arguments:
            max (int): The maximum number of images to download. If no number 
                is specified all images will be downloaded.
        """
        browser = self._get_browser()

        image_subset = self.image_urls[:max] if max else self.image_urls

        for index, image in enumerate(image_subset):
            browser.get(image['src'])
            images = browser.find_elements_by_tag_name('img')
            images[0].screenshot(f'./screenshot_{index}.png')
            wait_time = randint(1, 2)
            time.sleep(wait_time)

        browser.quit()

    @property
    def image_count(self):
        """Returns the count of image links captured in the InstaProfile 
        instance.

        Returns:
            (int): The quantity of image links in the InstaProfile instance.
        """
        return len(self.image_urls)


class TikTokBuilder(ChromedriverMixin):
    def __init__(self, profile_name, max_scroll_secs):
        self.tiktok_profile = TikTokProfile(profile_name)
        self.snapshots = []
        self.max_scroll_secs = max_scroll_secs

    def gather_html(self):
        """Captures snapshots of the entire HTML content of the profile page 
        being modelled and sets it to the InstaBuilder instance.
        """
        browser = self._get_browser()
        browser.get(self.tiktok_profile.profile_url)

        SCROLL_PAUSE_TIME = 2
        last_height = browser.execute_script("return document.body.scrollHeight")
        end_time = time.time() + self.max_scroll_secs
        
        while time.time() < end_time:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height <= last_height:
                self.snapshots.append(browser.page_source)
                break
            self.snapshots.append(browser.page_source)
            last_height = new_height

        browser.quit()

    def gather_image_tags(self):
        """Reduces a collection HTML content snapshots into a list of unique 
        image URLs.
        """
        image_tags = []
        image_pattern = re.compile(r'background-image: url\("(.+)"\)')

        
        for html in self.snapshots:
            soup = BeautifulSoup(html, 'html.parser')
            cards = soup.find_all('div', class_='image-card')

            for card in cards:
                match_obj = image_pattern.search(str(card))
                image_tags.append(match_obj[1])
            
        self.tiktok_profile.image_urls = list(set(image_tags))


class InstaBuilder(ChromedriverMixin):
    """A Builder class for creating instances of InstaProfile."""
    def __init__(self, profile_name, max_scroll_secs):
        """Instantiates an InstaBuilder object."""
        self.insta_profile = InstaProfile(profile_name)
        self.snapshots = []
        self.max_scroll_secs = max_scroll_secs

    def _click_show_more_button(self, browser):
        """Simulates a click on the 'show more' button, if present.

        Args:
            browser (WebDriver): The current WebDriver being utilized.
        """
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            button = browser.find_element_by_class_name('z4xUb')
            button.click()
        except:
            return

    def gather_html(self):
        """Captures snapshots of the entire HTML content of the profile page 
        being modelled and sets it to the InstaBuilder instance.
        """
        browser = self._get_browser()
        browser.get(self.insta_profile.profile_url)
        self._click_show_more_button(browser)

        SCROLL_PAUSE_TIME = 2
        last_height = browser.execute_script("return document.body.scrollHeight")
        end_time = time.time() + self.max_scroll_secs
        
        while time.time() < end_time:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height <= last_height:
                self.snapshots.append(browser.page_source)
                break
            self.snapshots.append(browser.page_source)
            last_height = new_height

        browser.quit()

    def gather_image_tags(self):
        """Reduces a collection HTML content snapshots into a list of unique 
        image URLs.
        """
        image_tags = []
        
        for html in self.snapshots:
            soup = BeautifulSoup(html, 'html.parser')
            image_tags += soup.find_all('img', class_='FFVAD')
            
        self.insta_profile.image_urls = list(set(image_tags))


class ProfileDirector:
    """A Director class for generating representations of social profiles."""
    def __init__(self):
        """Instantiates a ProfileDirector object."""
        self.builder = None

    def build_insta_profile(self, profile_name, max_scroll_secs=300):
        """Utilizes a Builder class to build and return an InstaProfile object.

        Arguments:
            profile_name (str): Represents the name of an Instagram profile.
            max_scroll_seconds (int): Limits the number of seconds Selenium is 
                allowed to scroll through a profile page before stopping. If no 
                number is provided it will scroll until it reaches the end of 
                the page.

        Returns:
            (InstaProfile): An InstaProfile instance.
        """
        self.builder = InstaBuilder(profile_name, max_scroll_secs)
        self.builder.gather_html()
        self.builder.gather_image_tags()

        return self.builder.insta_profile

    def build_tiktok_profile(self, profile_name, max_scroll_secs=300):
        self.builder = TikTokBuilder(profile_name, max_scroll_secs)
        self.builder.gather_html()
        self.builder.gather_image_tags()

        return self.builder.tiktok_profile


if __name__ == "__main__":
    director = ProfileDirector()
    tiktok_profile = director.build_tiktok_profile('@mikeservinofficial')
    print(tiktok_profile.image_urls)