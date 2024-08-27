import json
import random
import aiofiles



class GetPhrase:     
     
     
     @staticmethod
     async def bored_phrase() -> str:
          async with aiofiles.open('bot/scripts/bored_member/phrase.json', 'r', encoding='utf-8') as file:
               phrase = json.loads(await file.read())
               
          return random.choice(phrase)
                    
                    

