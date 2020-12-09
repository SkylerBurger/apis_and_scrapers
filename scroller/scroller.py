import time

from selenium import webdriver


class Browser:
    def __init__(self):
        """Instantiates a Browser object.
        """
        self.driver = webdriver.Chrome('./chromedriver')

    def get(self, url):
        """Navigates the browser to the given URL.

        Args:
            url (str): The URL to navigate to.
        """
        self.driver.get(url)


class Scroller(Browser):
    def __init__(self, base_url, next_class=None):
        """Instantiates a Scroller object.

        Args:
            base_url (str): The URL for the site to be crawled.
            next_class (str, optional): The class given to the next page button. Defaults to None.
        """
        super().__init__(self)
        self.base_url = base_url
        self.next_class = next_class
        self.snapshots = []


    def click_next(self):
        """Attempts to locate a button to advance the page and then click it.
        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            button = self.driver.find_element_by_class_name(self.next_class)
            button.click()
        except:
            return

    def take_snapshot(self):
        """Captures the soure code for the current page and adds it to the snapshots list.
        """
        self.snapshots.append(self.driver.page_source)

    def collect_pages(self, num):
        """Advances through the given number of pages while collecting the source code for each in snapshots.

        Args:
            num (int): The number of pages to advance through.
        """
        self.get(f'{self.base_url}1')
        for _ in range(num):
            time.sleep(1)
            self.take_snapshot()
            time.sleep(0.5)
            self.click_next()
