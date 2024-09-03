import json
import aiofiles
import disnake



class JsonDataFuncs:
     
     @staticmethod
     async def __get_dict_from_file() -> dict:
          async with aiofiles.open('database/data/discord.json', 'r') as f:
               read = await f.read()
               
               if not read:
                    return {}
          return json.loads(read)
     
     
     @staticmethod
     async def __save_dict_in_file(data: dict) -> None:
          async with aiofiles.open('database/data/discord.json', 'w') as f:
               await f.write(json.dumps(data, indent=2))
     
     
     
     @classmethod
     async def update_member(cls, member: disnake.Member) -> None:
          file = await cls.__get_dict_from_file()
          

          if not member.bot:
               if str(member.id) not in file.keys():
                    file[member.id] = {
                         'member_id': member.id,
                         'member_name': member.name,
                         'guild_id': member.guild.id,
                         'guild_name': member.guild.name,
                         'member_messages': 1
                    }
               
               else:
                    file[str(member.id)]['member_messages'] += 1
                    
               await cls.__save_dict_in_file(file)
          
          
     @classmethod
     async def get_member_messages(cls, member_id: int) -> int:
          file = await cls.__get_dict_from_file()
          
          if str(member_id) in file.keys():
               return file[str(member_id)]['member_messages']
          return 0
     
          
     @classmethod
     async def delete_member(cls, member_id: int) -> None:
          file = await cls.__get_dict_from_file()
          
          if str(member_id) in file.keys():
               del file[str(member_id)]
               await cls.__save_dict_in_file(file)
          
          
     @classmethod
     async def delete_guild(cls, guild_id: int):
          file = await cls.__get_dict_from_file()
          
          new = {}
          for key, value in file.items():
               if value['guild_id'] != guild_id:
                    new[key] = value
                    
          await cls.__save_dict_in_file(new)


json_funcs = JsonDataFuncs()