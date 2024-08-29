import json
import requests


from bs4 import BeautifulSoup


class Stathtam:

     @staticmethod
     def parse(url: str) -> None:
          response = requests.get(url).text
          
          soup = BeautifulSoup(response, 'lxml')
          
          block = soup.find('div', class_='images')
          figure = block.find_all('figure')
          
          with open('bot/scripts/statham/statham.json', 'r') as file:
               data: list[str] = json.loads(file.read())
          
          for item in figure:
               data.append(item.find('img').get('src'))
          
          
          with open('bot/scripts/statham/statham.json', 'w') as file:
               file.write(json.dumps(data, indent=2))
               
     
     @staticmethod
     async def get_citata() -> list[str]:
          with open('bot/scripts/statham/statham.json', 'r') as file:
               return json.loads(file.read())
     
     
statham = Stathtam()