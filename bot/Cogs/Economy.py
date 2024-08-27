# Import modules
import json

import disnake
import sqlite3 as sql

from disnake.ext import commands
from disnake import CmdInter
from loguru import logger
from other import onBalance, offBalance, moneyCheck


# Create cog with command: /createbase, pay, balik
class CreateEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    # Creating table for server
    @commands.slash_command(description='Создание базы данных для вашего сервера.')
    async def createbase(self, inter: CmdInter) -> None:
        await inter.response.defer()
        await inter.delete_original_response()        
        
        # Connect to database
        with sql.connect('projectbot.db') as conn:
            cursor = conn.cursor()
            
            # Create table
            cursor.execute("""CREATE TABLE IF NOT EXISTS server{}(
                cash BIGINT,
                id INT,
                name STR,
                inv TEXT,
                mont STR
            )""".format(inter.guild.id))
            conn.commit()
            
            cursor.execute("""CREATE TABLE IF NOT EXISTS rolles{}(
                roles STR,
                notadd STR,
                stopped STR,
                sale INT
            )""".format(inter.guild.id))
            conn.commit()
            
            # Adding members in table
            for member in inter.guild.members:
                answer = cursor.execute("SELECT id FROM server{} WHERE id = ?".format(inter.guild.id), [member.id]).fetchone()
                
                if not answer:
                    cursor.execute("INSERT INTO server{} VALUES(?, ?, ?, ?, ?)".format(inter.guild.id), [100, member.id, member.name, json.dumps({}), 'No'])
                    conn.commit()
                    
            # Adding in table with roles
            answer = cursor.execute("SELECT stopped FROM rolles{}".format(inter.guild.id)).fetchone()
            
            if not answer:
                cursor.execute("INSERT INTO rolles{} VALUES(?, ?, ?, ?)".format(inter.guild.id), [json.dumps({}), json.dumps([]), 'True', 1])
                conn.commit()
                
        cursor.close()
        await inter.author.send(f'{inter.author.mention}, ваша база создана!', delete_after=120.0)  
        
        logger.debug(f'base for {inter.guild.name} created success.')
        
        
        
    # Command for send moneys
    @commands.slash_command(description='Отправь деньги другу.')
    async def pay(self, inter: CmdInter, member: disnake.Member, money: int) -> None:
        # If inter.author not want send money yourself
        if inter.author.id != member.id:
                
            # Check moneys inter.author. If money > money author
                
            if await moneyCheck(inter.guild.id, inter.author.id, money):
                return await inter.send(f'{inter.author.mention}, у вас на балансе нет {money}!', ephemeral=True, delete_after=120.0)   # Send 'U not have on balance {money} coins!'
                
                
            # If author want send money less or equals 0
            elif money < 0 or money == 0:
                return await inter.send(f'{inter.author.mention}, меньше 0 или 0 отправить нельзя!', ephemeral=True, delete_after=120.0)   
                    
                    
            # If okay that send money author to member
            else:
                await onBalance(inter.guild.id, member.id, money)
                await offBalance(inter.guild.id, inter.author.id, money)
                
            await inter.send(f'Деньги успешно отправлены участнику {member.mention}.', ephemeral=True, delete_after=120.0)   # Send 'Succes! Mony send {member.mention}.'
        
                
        # If inter.author send moneys yourself
        else:
            await inter.send(f'{inter.author.mention}, нельзя отправить деньги самому себе!', ephemeral=True, delete_after=120.0)
            
            
    # Command for check balance
    @commands.slash_command(description='Ваш баланс')
    async def balik(self, inter: CmdInter, member: disnake.Member = None) -> None:
        
        # Connect to databse
        with sql.connect('projectbot.db') as conn:
            cursor = conn.cursor()
            
            # If memder is True
            if member:
                money = cursor.execute("SELECT cash FROM server{} WHERE id = ?".format(inter.guild.id), [member.id]).fetchone()[0]
                await inter.send(f'{inter.author.mention}, у {member.mention} на балансе {money}.', ephemeral=True, delete_after=120.0)
                
                
            # If not member
            else:
                money = cursor.execute("SELECT cash FROM server{} WHERE id = ?".format(inter.guild.id), [inter.author.id]).fetchone()[0]
                await inter.send(f'{inter.author.mention}, у вас на балансе {money}.', ephemeral=True, delete_after=120.0)
        cursor.close()
            
# Adding cog in bot
def setup(bot) -> None:
    bot.add_cog(CreateEconomy(bot))
    
        