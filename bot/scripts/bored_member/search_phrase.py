import json
import requests

from bs4 import BeautifulSoup



def lifehacker(url: str) -> list[str]:
     response = requests.get(url)

     soup = BeautifulSoup(response.text, 'lxml')
     block = soup.find_all('article')
     
     data = []
     for i in range(1, 80 + 1):
          for j in block:
               txt = j.text.split(f'{i}.')[1].split(f'{i + 1}.')[0].strip()
               data.append(txt)
     
     return data[:-1]



def thevoicemag(url: str, data: list[str]) -> list[str]:
     response = requests.get(url)
     
     soup = BeautifulSoup(response.text, 'lxml')
     block = soup.findAll('article', class_='article-detail_tag_p')[1:]
     
     count = 1
     for info in block[:-1]:
          txt = info.text.split(f'{count}.')[1].strip()
          count += 1
          
          data.append(txt)
     
     return data



def intrigue_dating(url, data: list[str]) -> None:
     response = requests.get(url)
     
     soup = BeautifulSoup(response.text, 'lxml')
     block = soup.find_all('ul')
     
     actions = []
     for i in range(len(block)):
          if block[i].text == '1 Почему иногда нам скучно2 200 идей, чтобы не заскучать':
               for j in range(3, 7 + 1):
                    actions.append(block[i + j].text)
     
     new = []
     for info in actions:
          new.append(info.split('.'))
          
          
     for list_ in new:
          for str_ in list_:
               if str_:
                    data.append(str_.strip() + '.')
                    
     with open('bot/scripts/bored_member/phrase.json', 'w', encoding='utf-8') as file:
          file.write(json.dumps(data, indent=2, ensure_ascii=False))     