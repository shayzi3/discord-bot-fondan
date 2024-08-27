# Подключение модулей
import asyncio
import json

import disnake
import sqlite3 as sql

from disnake.ext import commands
from datetime import datetime as dt
from disnake import CmdInter, Member



# Create cog for contol roles
class RoleCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    # Command for give role
    @commands.slash_command(description='Выдаль роль участнику.')
    async def giverole(self, inter: CmdInter, member: disnake.Member, role: disnake.Role) -> None:
        if inter.author.id != member.id:
            give_role = disnake.utils.get(inter.guild.roles, id=role.id) # Role for issuance
                
            # Check role from the member
            if role in member.roles:
                title = f'{inter.author.mention}, роль {role} уже есть у {member.name}.'
                return await inter.send(title)
                    
            # Give role
            try:
                await member.add_roles(give_role)
            
            except Exception as ex:
                return await inter.send(f'{inter.author.mention}, не получилось дать роль {role}!')
                        
            emb = disnake.Embed(title=f'Роль {role} выдана участнику {member.name} успешно!', timestamp=dt.now())
            emb.set_footer(text=inter.author.name, icon_url=inter.author.avatar)
            await inter.send(embed=emb) 
                
           
        # Если автор сообщения хочет выдать себе роль, сообщаем, что так сделать нельзя     
        else:
            title = f'{inter.author.mention}, нельзя выдавать роль самому себе!'
            await inter.send(title)
            
            
    # Command for take role from the member
    @commands.slash_command(description='Забрать роль у участника')
    async def takerole(self, inter, member: disnake.Member, role: disnake.Role) -> None:
        if inter.author.id != member.id:
            take_role = disnake.utils.get(inter.guild.roles, id=role.id)
                
            # Если роль имеется у участника тогда забираем её If member has a role we take it away
            if role in member.roles:
                try:
                    await member.remove_roles(take_role)
                except Exception as ex:
                    return await inter.send(f'{inter.author.mention}, не получилось забрать роль {role}!')
                    
                emb = disnake.Embed(title=f'Роль {role} больше нет у {member.name}.')
                emb.set_footer(text=inter.author.name, icon_url=inter.author.avatar)
                await inter.send(embed=emb)
                    
            # If member hasnt a role dont take it away
            else:
                title = f'{inter.author.mention}, у {member.name} нет роли {role}!'
                await inter.send(title)
                
    
        else:
            title = f'{inter.author.mention}, нельзя забрать у себя роль!'
            await inter.send(title)
            
            
            
    # Command for check roles at member
    @commands.slash_command(description='Посмотреть все роли у участника сервера')
    async def checkroles(self, inter, member: disnake.Member) -> None:
        # All roles
        result = '\n'.join(rl.name for rl in member.roles)
        
        emb = disnake.Embed(title=f'Все роли участника {member.name} ↓', description=result, timestamp=dt.now())
        emb.set_footer(text=inter.author.name, icon_url=inter.author.avatar)
        await inter.send(embed=emb)
        
        
        
    # Command for create new role on server
    @commands.slash_command(description='Создать новую роль')
    async def createrole(self, inter: CmdInter, role: str) -> None:
        
        # Creating role
        await inter.guild.create_role(name=role, colour=disnake.Colour.blurple())
            
        emb = disnake.Embed(title=f'Роль {role} создана успешно!')
        emb.set_footer(text=inter.author.name, icon_url=inter.author.avatar)
        await inter.send(embed=emb)
        
        
       
    # Command for delete role
    @commands.slash_command(description='Удаление роли с сервера')
    async def delrole(self, inter: CmdInter, role: disnake.Role) -> None:
        try:
            
            role_del = disnake.utils.get(inter.guild.roles, id=role.id)
            await role_del.delete()
            
           
            with sql.connect('projectbot.db') as conn:
                cursor = conn.cursor()
                
                
                # Dict with roles whit cant sold
                rolles = cursor.execute("SELECT roles FROM {}".format(inter.guild.name)).fetchone()[0]
                rolles: dict[str, list[int]] = json.loads(rolles)
                
                
                # If role in shop roles that i delete it
                if role.name in rolles:
                    del rolles[role.name]
                    
                    cursor.execute("UPDATE {} SET roles = ?".format(inter.guild.name), [json.dumps(rolles)])
                    conn.commit()
            cursor.close()
            
            
            emb = disnake.Embed(title=f'Роль {role} удалена успешно!', timestamp=dt.now())
            emb.set_footer(text=inter.author.name, icon_url=inter.author.avatar)
            await inter.send(embed=emb)
            
            
        except Exception as ex:
            title = f'{inter.author.mention}, ❌ Роль {role} удалить не получилось!'
            await inter.send(title)
            
            
            
    @commands.slash_command(description='Удалить все роли у участника сервера')
    async def delallroles(self, inter, member: disnake.Member) -> None:
        member_roles = [roles.name for roles in member.roles]
        del member_roles[0]
        
        for role in member_roles:
            del_role = disnake.utils.get(inter.guild.roles, name=role)
            await member.remove_roles(del_role)
           
        emb = disnake.Embed(title=f'Все роли участника {member.name} удалены!', timestamp=dt.now())
        emb.set_footer(text=inter.author.name, icon_url=inter.author.avatar)
        await inter.send(embed=emb)
        
        
    @commands.slash_command(description='Замутить')
    async def muted(self, inter: CmdInter, member: disnake.Member, time: int = None) -> None:
        
        if inter.author.id != member.id:
            for roles_member in member.roles:
                if roles_member.name == 'mute':
                    title = f'{inter.author.mention}, у {member.name} есть роль мута!'
                    return await inter.send(title)
                
            role = disnake.utils.get(inter.guild.roles, name='mute')
            await member.add_roles(role)
            
                
            if not time:
                emb = disnake.Embed(title=f'{inter.author.name} замутил {member.name}.', timestamp=dt.now())
                await inter.send(embed=emb)
                
            else:
                emb = disnake.Embed(title=f'{inter.author.name} замутил {member.name} на {time} секунд.', timestamp=dt.now())
                emb.set_footer(text=inter.author.name, icon_url=inter.author.avatar)
                await inter.send(embed=emb)
                    
                # Отсчёт времени до размута
                await asyncio.sleep(time)
                await member.remove_roles(role)
                await inter.send(f'Время закончилось! {member.mention} размучен!')
                
        else:
            title = f'{inter.author.mention}, нельзя замутить самого себя!'
            await inter.send(title)
            
            
    @commands.slash_command(description='Размутить участника')
    async def unmuted(self, inter, member: disnake.Member, time: int = None) -> None:
        
        if inter.author.id != member.id:
            
            member_roles = [i.name for i in member.roles]
            if 'mute' in member_roles:
                
                role = disnake.utils.get(inter.guild.roles, name='mute')
                await member.remove_roles(role)
                
                if not time:
                    emb = disnake.Embed(title=f'{inter.author.name} размутил {member.name}', timestamp=dt.now())
                    await inter.send(embed=emb)
                  
                else:
                    emb = disnake.Embed(title=f'{inter.author.name} размутил {member.name} на {time} секунд', timestamp=dt.now())
                    await inter.send(embed=emb)
                    
                    await asyncio.sleep(time)
                    await member.add_roles(role)
                    await inter.send(f'Время кончилось! {member.name} снова замучен!')
            
            else:
                title = f'{inter.author.mention}, у {member.name} нет роли мут!'
                await inter.send(title)
                
        else:
            title = f'{inter.author.mention}, нельзя размутить себя же!'
            await inter.send(title)
        

def setup(bot: commands.Bot) -> None:
    bot.add_cog(RoleCog(bot))
    