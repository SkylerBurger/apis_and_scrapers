from pprint import pprint

from bs4 import BeautifulSoup
from selenium import webdriver


class AdultSwimShow:
    def __init__(self, show_link):
        self.show_link = show_link

    def get_season(self, number):
        return self.show_guide.get(f'season_{number}')

    def get_episode(self, season, episode):
        season = self.show_guide.get(f'season_{season}')
        return season.get(f'episode_{episode}') if season else None

    @property
    def season_list(self):
        return list(self.show_guide)


class AdultSwimShowBuilder:
    def __init__(self, show_link):
        self.show = AdultSwimShow(show_link)
        self._create_show_guide()

    def _create_browser(self):
        """Returns a Selenium Chrome webdriver."""
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        browser = webdriver.Chrome(
            executable_path='../../utilities/chromedriver', 
            options=options)
        return browser


    def _get_html(self):
        """Returns the HTML content for a given URL."""
        browser = self._create_browser()
        browser.get(self.show.show_link)
        html = browser.page_source
        browser.quit()
        return html


    def _normalize_episodes(self, season):
        """Returns a dict of details for each episode in a given season."""
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

        return episode_guide


    def _normalize_season(self, season):
        """Returns the season number and a dict of episode details for a given season."""
        season_number_tag = season.find(name='meta', attrs={'itemprop':'seasonNumber'})
        season_number = season_number_tag['content']
        episode_guide = self._normalize_episodes(season)

        return season_number, episode_guide


    def _create_show_guide(self):
        """Returns a dict of episode details separated by seasons for a given AdultSwim show link."""
        html = self._get_html()
        soup = BeautifulSoup(html, 'html.parser')
        seasons = soup.find_all(name='div', attrs={'itemprop':'containsSeason'})
        self.show.season_count = len(seasons)
        show_guide = {}

        for index, season in enumerate(seasons):
            season_number, episode_guide = self._normalize_season(season)
            show_guide[f'season_{season_number}'] = episode_guide

        self.show.show_guide = show_guide


class ShowDirector:
    def __init__(self):
        self.builder = None

    def build_adultswim_show(self, show_link):
        # If the Director doesn't give the builder commands,
        # does this mean this is more of an abstract factory?
        self.builder = AdultSwimShowBuilder(show_link)
        return self.builder.show


if __name__ == '__main__':
    adultswim_show_link = adultswim_show_link = 'https://www.adultswim.com/videos/ghost-in-the-shell'
    
    show_director = ShowDirector()

    ghost_in_the_shell = show_director.build_adultswim_show(adultswim_show_link)

    pprint(ghost_in_the_shell.season_count)
    pprint(ghost_in_the_shell.show_link)
    pprint(ghost_in_the_shell.get_season(1))
    pprint(ghost_in_the_shell.season_list)
    pprint(ghost_in_the_shell.get_episode(2, 2))





