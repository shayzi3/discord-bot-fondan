import random
import disnake

from disnake.ext import commands

from database.src.db.base import data_funcs
from database.src.json.base import json_funcs
from database.src.db.schemas import BaseMode
from bot.utils.box import box



class Gift(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        
    @staticmethod
    async def get_random_value(id: int) -> tuple[int]:
        # Изначальная сумма 20 монет
        messages = await json_funcs.get_member_messages(id)
        value = random.randint(1, 100)
        
        # x1, x2, x4
        summa = 20
        if value <= 5:
            summa *= 4
        
        elif value > 5 and value <= 60:
            summa *= 2
        
        elif value > 60 and value <= 100:
            summa *= 1
           
        if messages <= 100:
            summa *= 1
            
        elif messages > 100 and messages <= 1000:
            summa *= 2
            
        elif messages > 1000:
            summa *= 4
        
        return summa, value

        
        
    @commands.cooldown(1, 7200, commands.BucketType.user)
    @commands.slash_command(description='Подарок!')
    async def gift(self, inter: disnake.CmdInter) -> None:
        await inter.response.defer(ephemeral=True)
        
        cash = await self.get_random_value(id=inter.author.id)
        await data_funcs.balance(
            id_guild=inter.guild.id,
            id_member=inter.author.id,
            cash=cash[0],
            mode=BaseMode.ON
        )
        
        
        await inter.send(
            embed=await box(
                title='Подарок! 🎁',
                description=f'**Ты получаешь {cash[0]} монет! С шансом в {cash[1]}%**'
            ),
            ephemeral=True
        )
        
        
        
        
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Gift(bot))