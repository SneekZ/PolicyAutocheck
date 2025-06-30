import aiomysql
import asyncio

from config import DATABASE_CONNECTION
from stmt import STMT_GET_CLIENTS, STMT_GET_LPU_ID, STMT_INSERT_POLICY_CHECK, STMT_CLEAN_CHECK_POLICY

async def getClients() -> dict:
    async with await aiomysql.connect(
        **DATABASE_CONNECTION,
        autocommit=False
    ) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(STMT_GET_CLIENTS) 
            rows = await cursor.fetchall()
            return list(map(cleanClient, rows))

async def getLpuId() -> str:
    async with await aiomysql.connect(
        **DATABASE_CONNECTION,
        autocommit=False
    ) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(STMT_GET_LPU_ID) 
            row = await cursor.fetchone()
            return row[0]

async def writeCheckPolicy(messageId, clientId, error) -> str:
    async with await aiomysql.connect(
        **DATABASE_CONNECTION,
        autocommit=True
    ) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(STMT_INSERT_POLICY_CHECK, (messageId, clientId, error))

async def cleanCheckPolicy() -> None:
    async with await aiomysql.connect(
        **DATABASE_CONNECTION,
        autocommit=True
    ) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(STMT_CLEAN_CHECK_POLICY)

def cleanClient(clientInfo: tuple) -> tuple[int, dict]:
    return clientInfo[0], {
        "patientSurname": clientInfo[1],
        "patientName": clientInfo[2],
        "patientPatronymic": clientInfo[3],
        "birthDate": str(clientInfo[4]),
        "docType": "urn:oid:1.2.643.2.69.1.1.1.6." + clientInfo[5],
        "docNumber": ''.join(clientInfo[6].split())
    }

if __name__=="__main__":
    asyncio.run(getClients())
    asyncio.run(getLpuId())