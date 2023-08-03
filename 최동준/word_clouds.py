import requests
from bs4 import BeautifulSoup
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter

resultList = ""

url = "https://search.naver.com/search.naver?"

pages = 3
for page in range(pages):
    start = page+1
    if start != 1:
        start = (start-1)*10 + 1
    params = {
        "where": 'news',
        # 네이버 기사 검색 값
        "query": '전동 킥보드',

        # 페이지네이션 값q
        "start": start,
        "ds" : "2020.01.01",
        "de" : "2020.12.31",
        # "nso": 'so:r,p:1y,a:all'
    }
    raw = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, params=params)
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select("ul.list_news > li")
    
    for article in articles :
        title = article.select_one("a.news_tit").text
        resultList += title
print(resultList)   
okt = Okt()
nouns = okt.nouns(resultList) # 명사만 추출

words = [n for n in nouns if len(n) > 1] # 단어의 길이가 1개인 것은 제외

c = Counter(words) # 위에서 얻은 words를 처리하여 단어별 빈도수 형태의 딕셔너리 데이터를 구함
print(c)
wc = WordCloud(font_path="", width=800, height=800, scale=2.0, max_font_size=250)
gen = wc.generate_from_frequencies(c)
plt.figure()
plt.imshow(gen)
wc.to_file("2020.png")
    