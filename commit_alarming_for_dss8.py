
# coding: utf-8

# # DSS 8기 1일 1 commit
# 
#     - 매일 11시 pm, 아직 커밋 안 한 사람 report 공지 through Slack 공지 창 
#     

# In[1]:


import requests
from bs4 import BeautifulSoup 
import re
import datetime
import json
import pickle 


# In[2]:


####### "https://github.com/minus31" : "김 현규 매니져",
github_table = {
    "https://github.com/ViniKim" : '김 휘수B',
    "https://github.com/tmdgms" : "백 승흔B",
    "https://github.com/MaengHyoyeol" : "맹 효열B", 
    "https://github.com/brightscannon" : "김 민우B",
    "https://github.com/Junhojuno" : "김 준호B", 
    "https://github.com/hyelansgithub" : "정 혜란B",
    "https://github.com/annakimm" : "김 혜진B" ,
    "https://github.com/seokyeongheo" : '허 석영B',
    "https://github.com/jtrhee" : "이 정택B",
    "https://github.com/ChanminJun" : "전 찬민B",
    "https://github.com/Jeonhyunil" : "전 현일B",
    "https://github.com/jaykim-asset" : "김 종재B",
    "https://github.com/hhj235" : "황 한진A",
    "https://github.com/woncheolSon" : "손 원철A",
    "https://github.com/SHDeseo" : "배 소현A",
    "https://github.com/jahn0406" : "안 태언A",
    "https://github.com/benestump" : "윤 현근A",
    "http://github.com/twosb" : "이 상범A",
    "https://github.com/Boston123456" : "표 준희A"
}

github_url = [url for url in github_table.keys()]


# In[3]:


# today_count
today_counts = {}
today_date = datetime.datetime.now().strftime('%Y-%m-%d')
for i in range(len(github_url)):
    # getting html file
    res = requests.get(github_url[i])
    soup = BeautifulSoup(res.content, "html.parser")
    # today_date's data
    today = soup.select_one("rect[data-date={}]".format(today_date))
    # count! (target)
    today_count = int(today["data-count"])
    # github url(key)와 연결되어있는 이름 호출하고 이에 그날의 커밋 수를 할당
    today_counts[github_table[github_url[i]]] = today_count


# In[4]:


today_counts


# In[13]:


def today_commit_max(today_counts):
    
    """
    today_counts : 오늘의 커밋 현황 
    ---------------------------
    return : 중복인 사람 모두 출력 
    """
    
    result = []
    max_commit = max(today_counts.items(), key = lambda x: x[1])[1]
    
    for name in today_counts.keys():
        if today_counts[name] == max_commit:
            result.append([name, str(today_counts[name])])
    
    return result

today_commit_king = today_commit_max(today_counts)


# In[14]:


# finding no commit people 

no_commit_people = [] # no commit people list 
for name in today_counts.keys():
    if today_counts[name] == 0:
        no_commit_people.append(name)


# In[15]:


# for security of webhook url 

# Webhook_URL = ""
# with open("webhookurl.p", "wb") as f:
#     pickle.dump(Webhook_URL, f) # (obj, file)


# In[16]:


# # load webhook url 

with open("webhookurl.p", "rb") as f:
    webhook_url = pickle.load(f)


# In[17]:


def send_slack(msg, emoji):
    

    # 슬랙 웹훅 URL
    webhook_URL = webhook_url

    # 데이터
    #1day1commit
    data = {
        "channel": "#1day1commit", # 채널이름이 다르면 다른 채널의 이름을 작성
        "emoji": emoji,
        "msg": msg,
        "username": "김 현규 매니져B",
    }

    # 페이로드 생성
    payload = {
        "channel": data["channel"],
        "username": data["username"],
        "icon_emoji": data["emoji"], 
        "text": data["msg"],
    }

    # 전송
    response = requests.post(
        webhook_URL, 
        data = json.dumps(payload),
    )

    # 결과    
    print(response)
    
# creating msg and emoji 
msg = """
     *오늘 커밋 안한 사람! :shipit: * \n\n> *`{}!`* \n\n *오늘의 커밋왕* :gorilla: \n\n> *`{}`* \n 열심히 하셨군요 ! 
    """.format(("! ").join(no_commit_people), ("`*, \n*`").join([" : ".join(r) for r in today_commit_king]))
emoji = ":angry:"
if len(no_commit_people) == 0:
    msg = """
    *한 사람도 빠짐 없이 커밋 하다니!* :woman-wrestling: \n 여러분들이 자랑스럽습니다. 앞으로도 쭉! 화이팅 입니다! \n 
    *오늘의 커밋왕* :gorilla: \n\n> *`{}`* \n\n 모두들 하룻동안 수고하셨습니다. 
    """.format(("`*, \n*`").join([" : ".join(r) for r in today_commit_king]))
    emoji = ":peach:"
    

send_slack(msg, emoji)


# In[18]:


print(today_counts, sep="\n", end='\n')

