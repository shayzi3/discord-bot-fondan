
import aiohttp

from googletrans import Translator



class Responses:
     translate = Translator()
     
     url_api_bored = 'https://bored-api.appbrewery.com/random'     
     
     
     @classmethod
     async def api_bored(cls) -> str:
          async with aiohttp.ClientSession() as session:
               async with session.get(cls.url_api_bored) as response:
                    if response.status != 200:
                         return None
                    
                    data = await response.json()
                    soup = cls.translate.translate(
                         text=data['activity'], 
                         dest='ru', 
                         src='en').text
                    return soup
                    
                    

