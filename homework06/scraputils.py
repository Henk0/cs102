import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = [{
        'author': None,
        'comments': 0,
        'points': 0,
        'title': None,
        'url': None
    } for _ in range(30)]

    news = parser.table.find("table", attrs={"class": "itemlist"})

    rows = news.findAll("tr", attrs={"class": "athing"})
    for index, row in enumerate(rows):
        title = row.find("a", attrs={"class": "storylink"}).text
        link = row.find("a", attrs={"class": "storylink"})['href']
        news_list[index]['title'] = title
        news_list[index]['url'] = link

    subs = news.findAll("td", attrs={"class": "subtext"})
    for index, sub in enumerate(subs):
        try:
            points = ''.join([ch for ch in sub.find('span', attrs={"class": "score"}).text if ch.isdigit()])
        except:
            points = None
        try:
            author = sub.find('a', attrs={"class": "hnuser"}).text
        except:
            author = None
        iscom = sub.text.find('comments')
        if iscom != -1:
            begining = sub.text.rfind('|')
            comments = sub.text[begining + 2:iscom - 1]
        else:
            comments = 0
        news_list[index]['comments'] = comments
        news_list[index]['author'] = author
        news_list[index]['points'] = points
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    link = parser.find("a", attrs={"class": "morelink"})['href']
    return link


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
