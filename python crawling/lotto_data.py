import string
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
from bs4 import BeautifulSoup
# Use a service account
cred = credentials.Certificate('(firebase key).json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def lottoSet():
    lotto = db.collection(u'lotto').document(round_num)
    lotto.set({
        u'round': round_num,
        u'win_num': numbers_list,
        u'win_num1': numbers_list[0],
        u'win_num2': numbers_list[1],
        u'win_num3': numbers_list[2],
        u'win_num4': numbers_list[3],
        u'win_num5': numbers_list[4],
        u'win_num6': numbers_list[5],
        u'bonus': bonus
    })

lowercase = string.ascii_lowercase

st_num = 1          # 시작회차
ed_num = 30         # 종료회차
n = 0
for index in range(st_num, ed_num+1):
    url = f"https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={index}"
    req = requests.get(url)

    if req.status_code != requests.codes.ok:
        print("Connection failure.")
        continue

    soup = BeautifulSoup(req.text, "html.parser")
    win_result = soup.find("div", {"class": "win_result"})
    num_win = soup.find("div", {"class": "num win"})
    num_bonus = soup.find("div", {"class": "num bonus"})

    win_num = num_win.select("span")
    bonus = num_bonus.find("span").text
    if index < 10:
        round_num = win_result.find("h4").text
    elif 10 <= index < 36:
        if ed_num < 100:
            for i in range(ed_num+1):
                round_num = lowercase[n] + win_result.find("h4").text
        elif ed_num >= 100:
            n+=1
    
    numbers_list = [int(number.text) for number in win_num]
    lottoSet()
print("종료")
