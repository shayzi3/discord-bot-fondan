import disnake

from disnake.ext import commands

from database.src.base import data_funcs



class GuildAction(commands.Cog):
     def __init__(self, bot: commands.Bot) -> None:
          self.bot = bot
          
     
     @commands.Cog.listener()
     async def on_guild_join(self, guild: disnake.Guild) -> None:
          all_members = []
          
          for member in guild.members:
               if not member.bot:
                    all_members.append(
                         {
                              'guild_id': guild.id,
                              'guild_name': guild.name,
                              'member_id': member.id,
                              'member_name': member.name,
                              'member_cash': 100,
                              'created_at':  member.created_at.strftime("%d-%m-%Y %H:%M:%S"),
                              'joinet_at': member.joined_at.strftime("%d-%m-%Y %H:%M:%S"),
                              'avatar': member.avatar.url
                         }
                    )
          await data_funcs.insert_guild(data=all_members)

          
          
     @commands.Cog.listener()
     async def on_guild_remove(self, guild: disnake.Guild) -> None:
          await data_funcs.delete_guild(id_guild=guild.id)
          
          


def setup(bot: commands.Bot):
     bot.add_cog(GuildAction(bot))