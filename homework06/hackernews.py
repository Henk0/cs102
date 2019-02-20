from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    label = request.query.label
    n_id = request.query.id
    news = s.query(News).filter(News.id == n_id).one()
    news.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    new = get_news('https://news.ycombinator.com/', 5)
    old = s.query(News).all()
    old_ta = [(news.title, news.author) for news in old]
    for news in new:
        if (news['title'], news['author']) not in old_ta:
            add = News(
                title = news['title'],
                author = news['author'],
                url = news['url'],
                comments = news['comments'],
                points = news['points'],
                label = None)
            s.add(add)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    return None


if __name__ == "__main__":
    run(host="localhost", port=8080)

