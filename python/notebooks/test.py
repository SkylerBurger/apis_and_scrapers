# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
from selenium import webdriver
from bs4 import BeautifulSoup



as_show_link = 'https://www.adultswim.com/videos/ghost-in-the-shell'



options = webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome(executable_path='../../utilities/chromedriver', chrome_options=options)
browser.get(as_show_link)
html = browser.page_source
browser.quit()
soup = BeautifulSoup(html, 'html.parser')
episodes = soup.find_all('div', class_='_29ThWwPi')

for episode in episodes:
    print(episode)







# %%
