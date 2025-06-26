import aiomysql
import asyncio

from config import DATABASE_CONNECTION
from stmt import STMT_GET_CLIENTS, STMT_GET_LPU_ID

async def getClients() -> dict:
    async with await aiomysql.connect(
        **DATABASE_CONNECTION,
        autocommit=False
    ) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(STMT_GET_CLIENTS) 
            rows = await cursor.fetchall()
            print(cleanClient(rows[0]))
            # return list(map(cleanClient, rows))

async def getLpuId() -> str:
    async with await aiomysql.connect(
        **DATABASE_CONNECTION,
        autocommit=False
    ) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(STMT_GET_LPU_ID) 
            rows = await cursor.fetchone()
            print(rows)

def cleanClient(clientInfo: tuple) -> dict:
    return {
        "patientSurname": clientInfo[0],
        "patientName": clientInfo[1],
        "patientPatronymic": clientInfo[2],
        "birthDate": str(clientInfo[3]),
        "docType": clientInfo[4],
        "docNumber": ''.join(clientInfo[5].split())
    }

if __name__=="__main__":
    asyncio.run(getClients())
    asyncio.run(getLpuId())