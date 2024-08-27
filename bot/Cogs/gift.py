import disnake
import sqlite3 as sql

from disnake.ext import commands
from disnake import CmdInter, Colour
from other import onBalance


class GiftCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        
    # Команда для получения подарка
    @commands.cooldown(1, 7199, commands.BucketType.user)
    @commands.slash_command(description='Подарок!')
    async def getgift(self, inter: CmdInter) -> None:
        await onBalance(inter.guild.id, inter.author.id, 25)   # пополняем баланс участника на 25 монет
        
        emb = disnake.Embed(title='Подарок! 🎁', colour=Colour.dark_blue(), description=' **Ты получаешь 25 монет!** ')
        emb.set_footer(text=inter.author.name, icon_url=inter.author.avatar)
        await inter.send(embed=emb, ephemeral=True, delete_after=30.0)
        
        
    # Обрабатываем ошибку на повторное использование команды
    @getgift.error
    async def gift_error(self, inter: CmdInter, error) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            await inter.send(f'{inter.author.mention}, подарка ещё нет, потерпи! Обновление каждые 2 часа.', delete_after=30.0, ephemeral=True)
        
        
def setup(bot: commands.Bot) -> None:
    bot.add_cog(GiftCog(bot))