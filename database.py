import aiomysql
import asyncio

from config import DATABASE_CONNECTION
from stmt import STMT_GET_CLIENTS

async def get_clients() -> dict:
    async with await aiomysql.connect(
        **DATABASE_CONNECTION,
        autocommit=False
    ) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(STMT_GET_CLIENTS) 
            rows = await cursor.fetchall()
            print(rows)

if __name__=="__main__":
    asyncio.run(get_clients())