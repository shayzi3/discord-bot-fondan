import json
import random
import io

import aiofiles
import aiohttp


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
     async def get_wallpaper(id: int) -> str:
          async with aiofiles.open('database/data/command_json/wallpaper.json', 'r') as file:
               read = json.loads(await file.read())
               
          rand = random.choice(read)
          path = f'database/data/images/{id}.jpg'
          
          byte = io.BytesIO()
          async with aiohttp.ClientSession() as session:
               async with session.get(rand) as response:
                    async for chunk in response.content.iter_chunked(1024):
                         byte.write(chunk)
               
               
          async with aiofiles.open(path, 'wb') as file:
               await file.write(byte.getvalue())
          
          return path
