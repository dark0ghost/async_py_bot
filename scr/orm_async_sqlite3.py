import aiosqlite
import asyncio


class sqlite():
    def __init__(self,connect):
        self.file = connect

    async def insert(self,what,table):
        async with aiosqlite.connect(self.file) as db:
            await db.execute(f'INSERT INTO {table} {what}')
            await db.commit()
            await db.close()

    async def table(self,test=0):
        if test:
            async with aiosqlite.connect(self.file) as db:
                await db.execute(f'')
                await db.commit()
                await db.close()


    async def select(self,what,table):
        async with aiosqlite.connect(self.file) as db:
            await db.execute(f'SELECT FROM {table} {what}')
            await db.commit()
            await db.close()

    async def insert_state(self,id,table):
        async with aiosqlite.connect(self.file) as db:
            await db.execute(f'INSERT INTO {table} {id}')
            await db.commit()
            await db.close()

    async def create_teblae(self,create = True):
      if create:
        async with aiosqlite.connect(self.file) as db:

            await db.execute(f'')
            await db.commit()
            await db.close()



class State(sqlite):
    def __init__(self,table):
        self.table = table
    async def crt(self,tr=1):
        if tr:
            async with aiosqlite.connect(self.file) as db:
                await db.execute(f'')
                await db.commit()
                await db.close()

    async def set(self,id,state):
        async with aiosqlite.connect(self.file) as db:
            await db.execute(f'INSERT INTO {self.table} {id} {state}')
            await db.commit()
            await db.close()

    async def deleted(self):
        async with aiosqlite.connect(self.file) as db:
            await db.execute(f'INSERT INTO {self.table} ')
            await db.commit()
            await db.close()
