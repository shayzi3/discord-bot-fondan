
import disnake

from disnake.ext import commands
from aiohttp import ClientSession
from disnake import CmdInter
from googletrans import Translator
from random import choice



class AioCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        
    @commands.slash_command(description='Чем заняться скучно')
    async def bored(self, inter: CmdInter):
        await inter.response.defer()
        
        translate = Translator()
        url = 'https://www.boredapi.com/api/activity/'
        
        async with ClientSession() as sesion:
            async with sesion.get(url) as response:
                data = await response.json()   # Получаем словарь с активностью
                
                if response.status != 200:
                    return await inter.send('Не получилось выполнить запрос.', ephemeral=True)
                
        soup = translate.translate(text=data['activity'], dest='ru', src='en').text   # Ответ от bored api на русском языке
        emb = disnake.Embed(title=soup)
        
        await inter.send(embed=emb, ephemeral=True)
        
        
        
    @commands.slash_command(description='Да или нет')
    async def who(self, inter: CmdInter, *, text: str):
        await inter.response.defer()
        
        url = 'https://yesno.wtf/api'
        member = choice([i.id for i in inter.guild.members])   # Выбираем рандомный id из списка участников сервера
        user = await inter.guild.fetch_member(member)   # Получаем класс Member для того чтобы отметить человека
        
        async with ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                
                if response.status != 200:
                    return await inter.send('Не получилось выполнить запрос.', ephemeral=True)
        
        emb = disnake.Embed(title=text, colour=disnake.Colour.dark_magenta())
        emb.add_field(name=f'Делал ли {user.global_name} это?', value=f' **{data["answer"].capitalize()}** ')
        emb.set_image(url=data['image'])
        
        await inter.send(embed=emb)
        
        
def setup(bot: commands.Bot):
    bot.add_cog(AioCog(bot))