# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from collections import defaultdict
from tx.storage import Storage
from tx.tfidf import TFIDF


class Search(object):
    @classmethod
    def search(cls, v, count=5):
        """
        vに関連するwikipediaページを検索する
        """
        # vを形態素解析して特徴ベクトルを抽出
        tfidf = TFIDF.gen(v)
        print tfidf
        s = Storage()
        result = defaultdict(float)
        for search_word, search_score in tfidf:
            # 逆索引に問い合わせ実施
            title_score_map = s.get_r_index(search_word)

            for _title, _score in title_score_map:
                # 類似度を計算して集計
                result[_title] += search_score * _score

        # 類似度scoreで降順ソート
        search_result = [(k, result[k]) for k in result]
        search_result = sorted(search_result, key=lambda x: x[1], reverse=True)

        if len(search_result) >= count:
            return search_result[:count]
        return search_result


def printer(l, keyword):
    print "++++++++++++++++++++++"
    print "検索結果:{}".format(keyword)
    print "++++++++++++++++++++++"
    count = 1
    for title, score in l:
        print "- {}位:類似度:{}".format(str(count).encode("utf-8"), score)
        print "-", title, Storage.get_wikipedia_url(title)

        count += 1


def main():
    v = "体の抗酸化力や解毒力"
    printer(Search.search(v), v)
    #
    # v = "地域型JPドメイン名"
    # printer(Search.search(v), v)

    v = "ニュートリノを除く質量のある粒子の中で最も軽い素粒子"
    printer(Search.search(v), v)

main()
