from bs4 import BeautifulSoup
from selenium import webdriver


class AdultSwimShow:
    """Models an AdultSwim show."""
    def __init__(self, show_link):
        """Instantiates an AdultSwimShow object.
        
        Arguments:
            show_link (str): A link to a show's page on AdultSwim.com.
        """
        self.show_link = show_link
        self.episode_count = 0

    def get_season(self, number):
        """Returns a specific season of the show, if available.

        Args:
            number (int): Represents the number of the requested season.

        Returns:
            (dict) or (None): A dict of episode details if the season is 
                available, otherwise None.
        """
        return self.show_guide.get(f'season_{number}')

    def get_episode(self, season, episode):
        """Returns the details of a specific episode, if available.

        Args:
            season (int): Represents the number of the requested season.
            episode (int): Represents the number of the requested episode.

        Returns:
            (dict) or (None): A dict of details for the requested episode if
                the epsiode if available, otherwise None.
        """
        season = self.show_guide.get(f'season_{season}')
        return season.get(f'episode_{episode}') if season else None

    @property
    def season_list(self):
        """Returns a list of available seasons.

        Returns:
            (list): Contains the names of available seasons.
        """
        return list(self.show_guide)


class AdultSwimShowBuilder:
    """A Builder class for creating instances of AdultSwimShow."""
    def __init__(self, chromedriver_location, args):
        """Instantiates an AdultSwimShowBuilder object.

        Args:
            show_link (str): A link to a show's page on AdultSwim.
        """
        show_link = args[0]
        self.chromedriver_location = chromedriver_location
        self.product = AdultSwimShow(show_link)
        self._create_show_guide()

    def _create_browser(self):
        """Returns a Selenium Chrome WebDriver.

        Returns:
            (WebDriver): A Selenium Chrome WebDriver that runs headless.
        """
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        browser = webdriver.Chrome(
            executable_path=self.chromedriver_location, 
            options=options)
        return browser

    def _get_html(self):
        """Retrieves the HTML content of the modelled AdultSwim show.
        
        Returns:
            html (str): The HTML content of the modelled AdultSwim show's page.
        """ 
        browser = self._create_browser()
        browser.get(self.product.show_link)
        html = browser.page_source
        browser.quit()
        return html

    def _normalize_episodes(self, season):
        """Returns a dict of details for each episode in a given season.
        
        Args:
            season (Tag): A BeautifulSoup Tag element containing the HTML
                contents for a single season from the modelled AdultSwim show 
                page.

        Returns:
            episode_guide (dict): Contains details for each available episode 
                in this season.
        """
        episodes = season.find_all('div', class_='_29ThWwPi')
        episode_guide = {}

        for index, episode in enumerate(episodes):
            episode_data = {}
            episode_number = 0
            meta_tags = episode.find_all('meta')

            for meta_data in meta_tags:
                prop, content = meta_data.get('itemprop'), meta_data.get('content')
                if prop == 'episodeNumber': 
                    episode_number = content
                elif prop and content: 
                    episode_data[prop] = content

            episode_guide[f'episode_{episode_number}'] = episode_data
            self.product.episode_count += 1

        return episode_guide

    def _normalize_season(self, season):
        """Returns the season number and a dict of episode details for a given season.
        
        Args:
            season (Tag): A BeautifulSoup Tag element containing the HTML
                contents for a single season from the modelled AdultSwim show 
                page.

        Returns:
            season_number (str): Represents the chronological number for this 
                season
            episode_guide (dict): Contains details for each available episode
                in this season.
        """
        season_number_tag = season.find(name='meta', attrs={'itemprop':'seasonNumber'})
        season_number = season_number_tag['content']
        episode_guide = self._normalize_episodes(season)

        return season_number, episode_guide

    def _create_show_guide(self):
        """Generates a dict of details for all available episodes and assigns 
        it to the AdultSwimShow instance.
        """
        html = self._get_html()
        soup = BeautifulSoup(html, 'html.parser')
        seasons = soup.find_all(name='div', attrs={'itemprop':'containsSeason'})
        self.product.season_count = len(seasons)
        show_guide = {}

        for index, season in enumerate(seasons):
            season_number, episode_guide = self._normalize_season(season)
            show_guide[f'season_{season_number}'] = episode_guide

        self.product.show_guide = show_guide


class AdultSwimCollectionBuilder:
    pass


# Question: Is this Director more of an Abstract Factory?
# Doesn't seem to interact much with the Builder class.
class AdultSwimDirector:
    """A Director class for generating representations of shows."""
    builders = {
        'show': AdultSwimShowBuilder,
        'collection': AdultSwimCollectionBuilder,
    }

    def __init__(self, chromedriver_location):
        """Instantiates a ShowDirector object."""
        self.builder = None
        self.chromedriver_location = chromedriver_location

    def build_adultswim_show(self, show_link):
        """Utilizes an AdultSwimShowBuilder instance to build up an 
            AdultSwimShow instance modelled after the requested show.

        Args:
            show_link (str): A link to an AdultSwim show page.

        Returns:
            (AdultSwimShow): An AdultSwimShow instance modelled after the 
                requested show.
        """
        self.builder = AdultSwimShowBuilder(self.chromedriver_location, show_link)
        return self.builder.show

    def build(self, build_type, *args):
        self.builder = AdultSwimDirector.builders.get(build_type)
        
        if self.builder == None:
            raise TypeError(f'The AdultSwimDirector does not support build type \'{build_type}\'.')

        self.builder = self.builder(self.chromedriver_location, args)

        return self.builder.product
