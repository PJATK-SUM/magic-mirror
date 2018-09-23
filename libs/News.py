# -*- coding: utf-8 -*-
import urllib2
import json
from peewee import *
import datetime
import Database


class NewsModel(Database.BaseModel):
    id = IntegerField(null=False)
    title = FixedCharField(null=False)
    date = CharField(null=False)
    content = FixedCharField(null=False)


class News:
    RSS_URL = "https://pja-rss.herokuapp.com/?format=json"

    def __init__(self):
        NewsModel.create_table(fail_silently=True)

    @staticmethod
    def substringUntil(article, n, delim=['.', '?', '!']):
        end = len(article) - 1
        for ch in delim:
            idx = article.find(ch, n) + len(ch)
            if idx > 0:
                end = min(end, idx)
        return article[:end]

    def requestNews(self, count=5):
        response = None
        try:
            response = urllib2.urlopen(News.RSS_URL).read()
        except:
            return

        newsObj = json.loads(response)
        subNews = newsObj[:-count]
        for item in subNews:
            nid = int(item['id'])
            try:
                news = NewsModel.get(NewsModel.id == nid)
            except NewsModel.DoesNotExist:
                try:
                    NewsModel.create(id=nid, date=item['published_at'], title=item['title'], content=item['content'])
                except IntegrityError:
                    continue
                except OperationalError:
                    pass
            except OperationalError:
                pass

    def get(self, count):
        ret = []
        try:
            for x in NewsModel.select().order_by(-NewsModel.id).limit(count):
                ret.append({
                    'title': x.title,
                    'content': News.substringUntil(x.content, 500),
                    'date': x.date
                })
        except NewsModel.DoesNotExist:
            pass
        except OperationalError:
            pass

        return ret
