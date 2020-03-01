import requests
import csv

import pandas as pd
from bs4 import BeautifulSoup



def get_recipe_url():
    page = 0
    url_collection = []
    while True:
        req = requests.get("https://foodly-store.myshopify.com/blogs/recipes?page=" + str(page))
        page = page + 1
        html = req.text
        soup = BeautifulSoup(html, 'lxml')
        recipe_url = soup.select('div.content-wrapper > main > div > section > div > div > div > div.blog-container > article > h3')
        if not recipe_url:
            break
        for url in recipe_url:
            url = url.select_one('a').get('href')
            url_collection.append(url)
    return (url_collection)


def get_recipe_details(url_collection):
#    for_cnt = 0
    recipe_details = []

    for i in url_collection:
        req = requests.get(f"https://foodly-store.myshopify.com{i}")
        html = req.text
        soup = BeautifulSoup(html, 'lxml')

        title = soup.select('div.content-wrapper > main > div > section > div.wrapper > div > div > article > div > h1')

        posting_date = soup.select('div.content-wrapper > main > div > section > div.wrapper > div > div > article > div > p > time')

        author = soup.select('div.content-wrapper > main > div > section > div.wrapper > div > div > article > div > div > span:nth-child(1)')

        company = soup.select('div.content-wrapper > main > div > section > div.wrapper > div > div > article > div > div > span:nth-child(2)')

        description = soup.select('div.rte.article__content')

        ingredient_list = soup.select('div.recipe__ingredients.clearfix')

        directions = soup.select('div.recipe__directions')

 #       for_cnt += 1

        thumbnail_url = soup.select('div.img-holder.img-holder--cover > img')[0]['src']
#        print(thumbnail_url)
#        print("thumb=",end=""), print(dir(thumbnail_url))
#        print("thumb title=",end=""), print(thumbnail_url.title)

        for item in zip(title, posting_date, author, company, description, ingredient_list, directions, thumbnail_url):
            recipe_details.append(
                {
                    'title'        : item[0].text,
                    'posting_date' : item[1].text,
                    'author'       : item[2].text,
                    'company'      : item[3].text,
                    'description'  : item[4].text.replace("\n",""),
                    'ingredients'  : item[5].text.replace("\n",""),
                    'directions'   : item[6].text.replace("\n",""),
                    'thumbnail_url': "http:" + thumbnail_url,
                }
            )
    return recipe_details

a = get_recipe_url()
results = get_recipe_details(a)
#print(get_recipe_details(a))

data = pd.DataFrame(results)

data.columns = ['title', 'posting_date', 'author', 'company', 'description', 'ingredient_list', 'directions', 'thumbnail_url']
data.head()
data.to_csv('recipe_scraping_results.csv')
