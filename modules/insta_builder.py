from random import randint
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


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
            max (int) - The maximum number of images to download. If no number 
                is specified all images will be downloaded.
        """
        # Create Selenium WebDriver instance
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(
            '../utilities/chromedriver', 
            options=chrome_options,
        )

        image_subset = self.image_urls[:max] if max else self.image_urls

        for index, image in enumerate(image_subset):
            browser.get(image['src'])
            images = browser.find_elements_by_tag_name('img')
            # Edit file name f-string below  as needed
            images[0].screenshot(f'./screenshot_{index}.png')
            wait_time = randint(1, 2)
            time.sleep(wait_time)

        browser.quit()

    def report_images(self):
        """Prints the number of image URLs collected."""
        print(f'Image URLs Captured: {len(self.image_urls)}')


class InstaBuilder:
    """A Builder class for creating instances of InstaProfile."""
    def __init__(self, profile_name, max_scroll_secs):
        """Instantiates an InstaBuilder object."""
        self.insta_profile = InstaProfile(profile_name)
        self.snapshots = []
        self.max_scroll_secs = max_scroll_secs

    def _get_chrome_webdriver(self):
        """Creates and returns a Selenium Chrome WebDriver instance."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        return webdriver.Chrome(
            '../utilities/chromedriver', 
            options=chrome_options,
        )

    def gather_html(self):
        """Scrolls and records the HTML content of a profile page."""
        SCROLL_PAUSE_TIME = 1

        browser = self._get_chrome_webdriver()

        browser.get(self.insta_profile.profile_url)

        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")
        
        end_time = time.time() + self.max_scroll_secs
        
        while time.time() < end_time:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height <= last_height:
                self.snapshots.append(browser.page_source)
                break
            # Create HTML snapshot
            self.snapshots.append(browser.page_source)
            last_height = new_height

        browser.quit()

    def gather_image_tags(self):
        """Reduces a collection HTML content into unique image URLs."""
        
        image_tags = []
        
        for html in self.snapshots:

            soup = BeautifulSoup(html, 'html.parser')
            # 'FFVAD' is currently the common class for all profile images
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
            profile_name (str) - Represents the name of an Instagram profile.
            max_scroll_seconds (int) - Limits the number of seconds Selenium is 
                allowed to scroll through a profile page before stopping. If no 
                number is provided it will scroll until it reaches the end of 
                the page.

        Returns:
            (InstaProfile) - An InstaProfile instance.
        """
        self.builder = InstaBuilder(profile_name, max_scroll_secs)
        self.builder.gather_html()
        self.builder.gather_image_tags()

        return self.builder.insta_profile


if __name__ == "__main__":
    # Add an Instagram profile name below
    # profile_name = ''

    # Change value below to int, or leave as None to download all
    # max_images_to_download = None

    director = ProfileDirector()

    instagram_profile = director.build_insta_profile(profile_name)

    instagram_profile.report_images()

    instagram_profile.download_images(max_images_to_download)