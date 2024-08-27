import disnake

from sqlalchemy import update, select, insert, delete

from database.src.models import DataBase, Member
   



class DataBaseFuncs(DataBase):
    
    @classmethod
    async def balance(
        cls,
        id_guild: int,
        id_member: int,
        cash_member: int,
        mode: str
    ) -> None | bool:
          
        async with cls.session.begin() as conn:
            if mode == 'on':         
                sttm = (
                    update(Member). 
                    where(guild_id=id_guild, member_id=id_member).
                    values(cash=+cash_member)
                         
                )
            elif mode == 'off':
                sttm = (
                    update(Member). 
                    where(guild_id=id_guild, member_id=id_member).
                    values(cash=-cash_member)
                         
                )
            elif mode == 'check':
                sttm = select(Member).filter_by(
                    guild_id=id_guild, 
                    member_id=id_member
                )
                result = await conn.execute(sttm)
                result = result.scalar()
                    
                if result.member_cash >= cash_member:
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
        async with  cls.session.begin() as conn:
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


          
     
    
data_funcs = DataBaseFuncs()