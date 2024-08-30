import json
import random

import aiofiles


class Get:
     
     @staticmethod
     async def get_citata() -> str:
          async with aiofiles.open('database/data/command_json/statham.json', 'r') as file:
               read = json.loads(await file.read())
          
          return random.choice(read)
     
     
     
     @staticmethod
     async def get_bored_phrase() -> str:
          async with aiofiles.open('database/data/command_json/bored_phrase.json', 'r', encoding='utf-8') as file:
               read = json.loads(await file.read())
               
          return random.choice(read)
     
     
     
     @staticmethod
     async def get_wallpaper() -> str:
          async with aiofiles.open('database/data/command_json/wallpaper.json', 'r') as file:
               read = json.loads(await file.read())
               
          return random.choice(read)