# This Python file uses the following encoding: utf-8
import aiosqlite


class sqlite(object):
    def __init__(self, connect):

        self.file = connect

    async def table_contact(self) -> None:
        async with aiosqlite.connect(self.file) as db:
            await db.execute(f"""
                         CREATE TABLE IF NOT EXISTS CONTACT_TABLE(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         USERNAME CHAR 
                         );
                       """)
            await db.commit()

    async def insert(self, what, table="data_table") -> None:
        async with aiosqlite.connect(self.file) as db:
            await db.execute(f'INSERT INTO {table} {what};')
            await db.commit()

    async def table(self, test=0) -> None:
        if test:
            async with aiosqlite.connect(self.file) as db:
                await db.execute(f'')
                await db.commit()

    async def select(self, what, table="data_table") -> None:
        async with aiosqlite.connect(self.file) as db:
            await db.execute(f'SELECT FROM {table} {what};')
            await db.commit()

    async def insert(self, data: str, colums: str=None, table="data_table") -> None:
         async with aiosqlite.connect(self.file) as db:
            await db.execute(f"""INSERT INTO {table}({colums}) SELECT ? , ({data})""")
            await db.commit()

    async def create_teble(self, create: bool = True) -> None:
        if create:
            async with aiosqlite.connect(self.file) as db:
                await db.execute(f"""
              CREATE TABLE IF NOT EXISTS data_table (
              id INTEGER PRIMARY KEY AUTOINCREMENT
              );
            """)
                await db.commit()

    async def get_lang(self) -> str:
      data = []
      try:
        async with aiosqlite.connect(self.file) as db:
            async with db.execute('SELECT lang  FROM Lang;') as cursor:
                 row = await cursor.fetchall()
                 for i in row:
                     for t in i:
                     
                        data.append(t)
        return data
      except:
          return data
    async def insert_lang(self,lang:str):
        async with aiosqlite.connect(self.file) as db:
            await db.execute(f"""
            INSERT INTO Lang (lang)	VALUES('{lang}');
                     
                   """)
            await db.commit()

    async def create_teble_lang(self) -> None:
        async with aiosqlite.connect(self.file) as db:
            await db.execute(f"""
                                             CREATE TABLE IF NOT EXISTS Lang (
                                           lang TEXT
                                          );
                                           """)


