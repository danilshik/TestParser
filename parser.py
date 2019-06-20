from bs4 import BeautifulSoup
import requests
import string
import random
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time



headers = {'User-agent': 'Mozilla/5.0'}

urls = ["https://cakeboost.com/"]


visited_urls = []

tags = []

count_thread = 8



def get_request(url):
    r = requests.get(url, headers=headers)
    visited_urls.append(url)
    print(visited_urls)
    if r.status_code == 200:
        print("Запрос:", url)
        return r.text
    return False

def check_visited_url(url):
    if url in visited_urls:

        return True
    return False


def get_html(text):
    return BeautifulSoup(text, 'lxml')

def check_correctly_url(href):
    """

    :param href:
    :return: true - правильно
    """
    if(href is not None):
        if (href.find("http") != -1):
            if(href.find("mailto") == -1):
                if (href.find("tel:") == -1):
                    if (href.find("http://#") == -1):
                        return True
    return False

        # if el[:4] == "http" and el not in page_arr and (
        #         "mailto" or "tel:" or "http://#" or "# " or "https://") not in el:



def parse(url):
    r = get_request(url)
    html = get_html(r)

    a_list = html.find_all('a')
    for a in a_list:
        href = a.get("href")

        # print(href)
        if(check_correctly_url(href)):
            if(check_visited_url(href) == False):

                # urls.append(href)
                print(href)







    ####

    temp = []

    # цикл выводищяй теги без разметки html
    titles = ""
    for title in html.find_all('title'):
        print('Title:', title.text)
        titles += title.text + ";"

    # Отбрасываем ; у последнего пункта
    titles = titles[:-1]
    temp.append(['Title', titles])

    descriptions = ""
    for description in html.find_all('meta', {'name': 'description'}, {'content': ' '}):
        descriptions += description.get('content') + ";"
        print('description', description.get('content'))  # получение содержимого одиночного тега

    descriptions = descriptions.strip()

    temp.append(['Description', descriptions])

    h1s = ""
    for h1 in html.find_all('h1'):
        if (h1.text.strip() != ""):
            h1s += h1.text + ";"
            print("h1", h1.text)

    temp.append(['H1', h1s])
    # заполняем цикл данными

    temp.append(['links', urls])
    tags.append(dict(temp))

    time.sleep(1)  # ТАЙМАУТ В СЕКУНДУ



def start_threading():
    while len(urls) > 0:
        temp = urls.copy()
        urls.clear()
        with ThreadPoolExecutor(count_thread) as executor:
            # Создается пул потоков,
            for _ in executor.map(parse, temp):
                pass

        print(len(urls))
        print(len(temp))





if __name__ == '__main__':

    start_threading()
    #
    #
    # visited_urls.append("https://cakeboost.com/")
    #
    # print(check_visited_url("https://cakeboost.com/"))
    # print(check_correctly_url("https://cakeboost.com/games-news/"))


