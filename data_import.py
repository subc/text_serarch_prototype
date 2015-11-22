# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import ssl
import time
from tx.storage import Storage
import requests
from tx.tfidf import TFIDF

# wikipedia 全タイトルリスト
DATA_PATH = './data/jawiki-latest-all-titles-in-ns0'


def create_index(title):
    """
    WikipediaのページにHTTPアクセスして
    文章の特徴ベクトルを抽出して、検索用の索引を生成する
    """
    url = Storage.get_wikipedia_url(str(title))
    print title, url

    # WikipediaのページにHTTPアクセスして文章の特徴ベクトルを抽出
    tfidf = TFIDF.gen_web(url)

    # 検索用の索引を生成する
    s.save_tfidf(title, tfidf)
    return


print 'start'

# wikipedia全タイトルリストファイルからURLを生成
s = Storage()
f = open(DATA_PATH, 'r')
ct = 0
for title in f:
    ct += 1
    if ct < 531000:
        continue
    try:
        create_index(title)
    except UnicodeDecodeError:
        print "ERROR", title
    except requests.exceptions.ConnectionError:
        time.sleep(2)
    except requests.exceptions.Timeout:
        time.sleep(2)
    except ssl.SSLError:
        time.sleep(2)
