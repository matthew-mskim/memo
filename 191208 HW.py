import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number

rank = 1
for tr in trs:
    a_tag = tr.select_one('td.info > a.title.ellipsis')
    if a_tag is not None:
        title = a_tag.text.strip()
        singer = tr.select_one('td.info > a.artist.ellipsis').text
        doc = {
            'rank' : rank,
            'title' : title,
            'singer' : singer
        }
        print(rank, title, singer)
        db.music.insert_one(doc)
        rank += 1


#body-content > div.newest-list > div > table > tbody > tr:nth-child(49) > td.number

#body-content > div.newest-list > div > table > tbody > tr:nth-child(49) > td.number