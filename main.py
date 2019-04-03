from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import time

#시간표 입력
t_mon = ['자율','영어3(송)','확률과통계','영어1(귀)','물리','미적분','진로']
t_tue = ['국어2(혜)','지구과학', '기하와벡터','세계지리','영어2(손)','정보','국어3']
t_wed = ['스포츠','국어1(미)','물리','한국사','동아리(봉사)','동아리(봉사)','자습']
t_thu = ['한국사','지구과학','국어2(혜)','미적분','기하와벡터','영어3(송)','영어1(귀)']
t_fri = ['국어3(연)','물리','정보','영어2(손)','확률과통계','지구과학','세계지리']

#텔레그램 봇 키, 채팅 ID
APIKey = '000000000:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
chatID = '-0000000000000'

def getcarte():
    html = urlopen("http://www.kyeongbuk.hs.kr/user/carte/list.do").read()

    soup = BeautifulSoup(html, "html.parser")
    link = soup.find("ul", { "class" : "meals_today_list"})
    msg = ''

    for m in link:
        if ('.' in str(m)):
            msg +=  '\n-----\n' + m.text.strip() 

    return msg

def printtime():
    print('현시각 시:', datetime.now().hour, end='')
    print(' :', datetime.now().minute, end='')
    print(' :', datetime.now().second)

def sendTelegramMsg(APIKey, chatID, text):
  r = requests.get("https://api.telegram.org/bot" + APIKey 
  + "/sendMessage?chat_id=" + chatID + "&text=" + text + "&parse_mode=Markdown")
  return r


prevmin = -1 #datetime.now().minute
print("===== 시간표&급식 알리미 1.0v =====")

while(1):
    time.sleep(5)

    try:
        if (prevmin != datetime.now().minute):
            #초 시간 전환 이벤트
            printtime()
            tmsg = ''


            weekday = datetime.now().weekday()

            #월
            if(weekday==0):
                ttable = t_mon
            
            elif(weekday==1):
                ttable = t_tue
            
            elif(weekday==2):
                ttable = t_wed
            
            elif(weekday==3):
                ttable = t_thu

            elif(weekday==4):
                ttable = t_fri

            else:
                ttable = ''

            nowclass = ''
            targettime = -1

            #중식일때
            if ((datetime.now().hour == 12 or datetime.now().hour == 16) 
            and datetime.now().minute == 25):
                tmsg = '*급식 식단표' + getcarte()
            else:
                #1~7교시일때
                if (8 <= datetime.now().hour <= 12):
                    nowclassnum = datetime.now().hour - 7
                    nowclass = ttable[nowclassnum - 1]
                    targettime = 20

                #5~7교시일때
                elif (13 <= datetime.now().hour <= 15):
                    nowclassnum = datetime.now().hour - 8
                    nowclass = ttable[nowclassnum - 1]
                    targettime = 10

                if (datetime.now().minute == targettime):
                    tmsg = '*시간표 알림*\n' + str(nowclassnum) + '교시 과목: ' + ttable
                    

            if not (tmsg == ''):
                sendTelegramMsg(APIKey, chatID, tmsg)
                print('===== 메시지 보냄 =====\n' + tmsg)
                print('===== 메시지 끝 =====')
            else:
                print('===== 이벤트 없음 =====')

            prevmin = datetime.now().minute  

    except:
        print('오류 발생 - 5초 뒤 다시 시도합니다...')
