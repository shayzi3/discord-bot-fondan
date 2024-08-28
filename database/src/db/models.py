import asyncio

from sqlalchemy.ext.asyncio import (
     AsyncAttrs,
     create_async_engine,
     async_sessionmaker
)
from sqlalchemy.orm import (
     Mapped,
     mapped_column,
     DeclarativeBase
)


class Base(AsyncAttrs, DeclarativeBase):
     pass



class Member(Base):
     __tablename__ = 'members'
     
     member_id:  Mapped[int] = mapped_column(nullable=False, unique=True, primary_key=True)
     member_name: Mapped[str] = mapped_column(nullable=False)
     member_cash: Mapped[int] = mapped_column(nullable=False)
     created_at:  Mapped[str] = mapped_column(nullable=False)
     joinet_at: Mapped[str] = mapped_column(nullable=False)
     avatar: Mapped[str] = mapped_column(nullable=False)
     guild_id: Mapped[int] = mapped_column(nullable=False)
     guild_name: Mapped[str] = mapped_column(nullable=False)
    
     

     
class DataBase:
     eng = create_async_engine('sqlite+aiosqlite:///database/data/discord.db', echo=True)
     session = async_sessionmaker(eng)
     
     
     @classmethod
     async def create(cls) -> None:
          async with cls.eng.begin() as conn:
               await conn.run_sync(Base.metadata.create_all)
               
               
     @classmethod
     async def drop(cls) -> None:
          async with cls.eng.begin() as conn:
               await conn.run_sync(Base.metadata.drop_all)
               
               
               
if __name__ == '__main__':
     data_base = DataBase()
     
     # asyncio.run(data_base.drop())
     asyncio.run(data_base.create())
     

     
     