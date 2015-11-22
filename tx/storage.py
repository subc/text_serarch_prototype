# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import redis
import urllib

PREFIX = 'tx'
KEY_TITLE = '%s:TITLE:{}' % PREFIX
KEY_INDEX_TITLE = '%s:INDEX:{}' % PREFIX
KEY_R_INDEX_WORD = '%s:R_INDEX:{}' % PREFIX


class KeyMixin(object):
    @classmethod
    def get_key_title(cls, title):
        title = urllib.quote_plus(title)
        return KEY_TITLE.format(title)

    @classmethod
    def get_key_index(cls, title):
        title = urllib.quote_plus(title)
        return KEY_INDEX_TITLE.format(title)

    @classmethod
    def get_key_r_index(cls, word):
        return KEY_R_INDEX_WORD.format(word)


class Storage(KeyMixin):
    """
    タイトル毎のindexと特徴語毎のindexをredisに保存する

    title ... Wikipediaのタイトル
    word ... 特徴語
    """

    _cli = None
    timeout = 60 * 60 * 24 * 30

    @classmethod
    def get_wikipedia_url(cls, title):
        """
        titleからwikipediaのURLを生成
        """
        _base_url = "https://ja.wikipedia.org/wiki/{}"
        url = _base_url.format(urllib.quote_plus(title))
        return url[:-3]

    @property
    def client(self):
        """
        :rtype : Redis
        """
        if Storage._cli is None:
            Storage._cli = redis.Redis(host='localhost', port=6379, db=2)
        return Storage._cli

    def save_tfidf(self, title, tfidf):
        self.set_index(title, tfidf)
        self.set_r_index(title, tfidf)

    def set_index(self, title, tfidf):
        """
        title毎のtfidf
        titleをkeyとするZSETにtfidf値を上書き
        """
        key = Storage.get_key_index(title)
        self.client.delete(key)
        for word, score in tfidf:
            self.client.zadd(key, word, score)

    def set_r_index(self, title, tfidf):
        """
        文字毎の逆索引
        特徴文字列(word)からtitleを逆引きできる。
        """
        for word, score in tfidf:
            key = Storage.get_key_r_index(word)
            self.client.zadd(key, title, score)

    def get_r_index(self, word):
        """
        特徴語から記事を逆引きする。
        """
        key = Storage.get_key_r_index(word)
        return self.client.zrevrange(key, 0, 1000, withscores=True)
