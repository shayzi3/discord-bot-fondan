import disnake

from disnake.ext import commands

from bot.utils.casino.gaming import Gaming
from bot.utils.casino.buttons import SetColur
from database.src.db.base import data_funcs
from database.src.db.schemas import BaseMode
        
        
     

class Casino(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        
    @commands.slash_command(description='Поставь свою ставку.')
    async def casino(self, inter: disnake.CmdInter, money: int) -> None:
        await inter.response.defer()
        
        if money <= 0:
            return await inter.delete_original_response()
        
        member_balance = await data_funcs.balance(
            id_guild=inter.guild.id,
            id_member=inter.author.id,
            cash=money,
            mode=BaseMode.CHECK
        )
        if not member_balance:
            return await inter.send(f'{inter.author.mention}, у тебя на балансе нет {money} монет!', ephemeral=True)
            
        view = SetColur()
        title = f'{inter.author.mention}, выбери ставку! Ты поставил {money} монет.'
        
        await inter.send(title, view=view, ephemeral=True)
        await view.wait()
        
        if not view.choice:
            return await self.ctx.send('Ты проигнорировал выбор.', ephemeral=True)
        
        game = Gaming(inter, view.choice, money)
        await game.flags()
        
        

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Casino(bot))