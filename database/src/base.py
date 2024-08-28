import disnake

from sqlalchemy import update, select, insert, delete

from database.src.models import DataBase, Member
from database.src.schemas import BaseMode
   



class DataBaseFuncs(DataBase):
    
    @classmethod
    async def balance(
        cls,
        id_guild: int,
        id_member: int,
        cash: int,
        mode: BaseMode
    ) -> None | bool:
        
        user_cash = await cls.get_balance(id_guild, id_member)
        
        async with cls.session.begin() as conn:
            if mode == BaseMode.ON: 
                sttm = (
                    update(Member).
                    filter_by(guild_id=id_guild, member_id=id_member).
                    values(member_cash=user_cash + cash)
                )
                
            elif mode == BaseMode.OFF:
                if user_cash < cash:
                    return False
                    
                sttm = (
                    update(Member).
                    filter_by(guild_id=id_guild, member_id=id_member).
                    values(member_cash=user_cash - cash)  
                )
                 
            elif mode == BaseMode.CHECK:
                if user_cash >= cash:
                    return True
                return None
            
            
            await conn.execute(sttm)

        
    @classmethod
    async def insert_new_user(
        cls,
        user: disnake.Member
    ) -> None:
        async with cls.session.begin() as conn:
            sttm = (
                insert(Member).
                values(
                    guild_id=user.guild.id,
                    guild_name=user.guild.name,
                    member_id=user.id,
                    member_name=user.name,
                    member_cash=100,
                    created_at=user.created_at.strftime("%d-%m-%Y %H:%M:%S"),
                    joinet_at=user.joined_at.strftime("%d-%m-%Y %H:%M:%S"),
                    avatar=user.avatar.url
                )
            )
            await conn.execute(sttm)
            
            
        
    @classmethod
    async def delete_user(
        cls,
        id_guild: int,
        id_member: int
    ) -> None:
        async with cls.session.begin() as conn:
            sttm = (
                delete(Member).filter_by(
                    guild_id=id_guild,
                    member_id=id_member
                )
            )
            await conn.execute(sttm)


          
          
    @classmethod
    async def get_member(
        cls,
        id_guild: int,
        id_member: int
    ) -> Member:
        async with cls.session() as conn:
            sttm = select(Member).filter_by(
                guild_id=id_guild,
                member_id=id_member
            )
            result = await conn.execute(sttm)
            
        return result.scalar()
    
    
    
    @classmethod
    async def get_balance(
        cls,
        id_guild: int,
        id_member: int
    ) -> int:
        async with cls.session() as conn:
            sttm = select(Member.member_cash).filter_by(
                guild_id=id_guild,
                member_id=id_member
            )
            result = await conn.execute(sttm)
            
        return result.scalar()
    
    
    @classmethod
    async def delete_guild(
        cls,
        id_guild: int
    ) -> None:
        async with cls.session.begin() as conn:
            sttm = (
                delete(Member).filter_by(
                    guild_id=id_guild
                )
            )
            await conn.execute(sttm)
            
            
    @classmethod
    async def insert_guild(
        cls,
        data: list[dict]
    ) -> None:
        async with cls.session.begin() as conn:
            sttm = (
                insert(Member).
                values(data)
            )
            await conn.execute(sttm)
            
            
    @classmethod
    async def payment(
        cls,
        id_guild: int,
        id_author: int,
        id_member: int,
        moneys: int
    ) -> None:
        # id_author - send moneys
        # id_member - receive moneys

        await cls.balance(
            id_guild=id_guild,
            id_member=id_author,
            cash=moneys,
            mode=BaseMode.OFF,
        )
        await cls.balance(
            id_guild=id_guild,
            id_member=id_member,
            cash=moneys,
            mode=BaseMode.ON,
        )


          
     
    
data_funcs = DataBaseFuncs()