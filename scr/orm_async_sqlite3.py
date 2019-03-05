import aiosqlite


class sqlite(object):
    def __init__(self, connect):
        self.file = connect

    async def insert(self, what,table="data_table"):
        async with aiosqlite.connect(self.file) as db:
            await db.execute(f'INSERT INTO {table} {what}')
            await db.commit()


    async def table(self,test=0):
        if test:
            async with aiosqlite.connect(self.file) as db:
                await db.execute(f'')
                await db.commit()



    async def select(self, what, table="data_table"):
        async with aiosqlite.connect(self.file) as db:
            await db.execute(f'SELECT FROM {table} {what}')
            await db.commit()


    async def insert(self, data, table="data_table"):
        async with aiosqlite.connect(self.file) as db:
            await db.execute(f'INSERT INTO {table} {data}')
            await db.commit()


    async def create_teblae(self, create: bool = True):
       if create:
          async with aiosqlite.connect(self.file) as db:

            await db.execute(f"""
              CREATE TABLE IF NOT EXISTS data_table (
              id INTEGER PRIMARY KEY AUTOINCREMENT
              );
            """)
            await db.commit()
            self.table = "data_table"





class State(sqlite, object):
    def __init__(self, table,db):
        self.table = table
        self.file = db.file



    async def crt(self, tr=1):
        if tr:
            async with aiosqlite.connect(self.file) as db:
                await db.execute(f"""
                              CREATE TABLE IF NOT EXISTS state (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              state STRING
                              );
                            """)
                await db.commit()

                self.table = "state"

    async def set(self, id, state):
        async with aiosqlite.connect(self.file) as db:
            await db.execute(f'INSERT INTO {self.table} {id} {state}')
            await db.commit()


    async def deleted(self):
        async with aiosqlite.connect(self.file) as db:
            await db.execute(f'INSERT INTO {self.table} ')
            await db.commit()



