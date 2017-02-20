import re

from bs4 import BeautifulSoup
import requests

__author__ = 'Tobias'


class Root(object):
    def __init__(self, url='http://trinesmatblogg.no'):
        self.url = url

        recipe_link_pages = self.get_all_recipe_link_pages(self.url)

        all_recipes = []
        for recipe_list_page in recipe_link_pages:
            all_recipes += self.get_all_recipes(recipe_list_page)

        # Remove duplicates:
        all_recipes = {r['title']: r for r in all_recipes}

        for k, v in all_recipes.items():
            page_parse = self.parse_recipe_page(v['url'])
            pass



    def parse_recipe_page(self, url):
        """Method that parses relevant information from a recipe page."""
        soup = BeautifulSoup(requests.get(url).content, "html.parser")

        # Get ingredients:
        ingredient_lists = []
        ing_match = soup.find_all(re.compile(r'div|ul'))
        # TODO: fix matching of ingredients. I can find the title of the ingredient list using the below logic, and I
        # then need to grab the following unordered list (ul).
        for i in ing_match:
            if i.has_attr('class'):
                if 'shortcode-unorderedlist' in i['class']:
                    ingredient_lists += [{'title': i.contents}]



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
        recipes = []
        soup = BeautifulSoup(requests.get(recipe_list_page).content, "html.parser")
        stuff = soup.find_all('div')

        for s in stuff:
            if s.has_attr('class'):
                if 'post' in s['class'] and \
                        not 'tag-reise' in s['class'] and \
                        not 'tag-favoritt' in s['class'] and \
                        not 'category-diverse-2' in s['class']:
                    classes = s['class']
                    link = s.find_all('a')[0]
                    url = link['href']
                    title = link['title']
                    date = s.find_all('p')[0].contents[0]
                    recipes += [dict(classes=classes, url=url, title=title, date=date)]

        return recipes


if __name__ == '__main__':
    test = Root()

    tet = Root()
    print('a')