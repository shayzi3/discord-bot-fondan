import disnake

from disnake.ext import commands


class PurgeMessage(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.slash_command(description='Удаление сообщений')
    async def purge(self, inter: disnake.CmdInter, amount: int) -> None:
        await inter.channel.purge(limit=amount)
        
        emb = disnake.Embed(
            title=f'✅ Удалено {amount} сообщений.', 
            colour=disnake.Colour.blue()
        )
        emb.set_author(name=inter.author.name, icon_url=inter.author.avatar)
        await inter.send(embed=emb, delete_after=300)



def setup(bot: commands.Bot) -> None:
    bot.add_cog(PurgeMessage(bot))