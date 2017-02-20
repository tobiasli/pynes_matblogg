
from bs4 import BeautifulSoup
import requests

__author__ = 'Tobias'


class Root(object):
    def __init__(self, pages=RECIPE_PAGES):
        url = 'http://trinesmatblogg.no'

        recipe_link_pages = self.get_all_recipe_link_pages(url)
        self.recipe_urls = []
        for recipe_list_page in recipe_link_pages:
            self.recipe_urls += self.get_all_recipes(recipe_list_page)

    @staticmethod
    def get_all_recipe_link_pages(url):
        link_pages = []
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        links = soup.find_all('li')
        for link in links:
            if link.has_attr('class') and 'menu-item' in link['class'] and 'menu-item-object-category' in link['class']:
                link_pages += [link.find('a')['href']]

        return link_pages

    @staticmethod
    def get_all_recipes(recipe_list_page):
        recipes = {}
        soup = BeautifulSoup(requests.get(recipe_list_page).content, "html.parser")
        stuff = soup.find_all('div')

        for s in stuff:
            if s.has_attr('class'):
                if 'post' in s['class'] and not 'tag-reise' in s['class']:
                    classes = s['class']
                    link = s.find_all('a')[0]
                    url = link['href']
                    title = link['title']
                    date = s.find_all('p')[0].contents[0]
                    recipes[title] = dict(classes=classes, url=url, title=title, date=date)

        return recipes


if __name__ == '__main__':
    test = Root()

    tet = Root()
    print('a')