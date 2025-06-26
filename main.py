import aiohttp
import asyncio

import database as db
from config import BASE_URL, GUID

async def sendIdentityPatient(lpuId, client: dict) -> dict:
    client["lpuId"] = lpuId

    async with aiohttp.ClientSession() as session:
        async with session.post(
            BASE_URL,
            json=client,
            headers={
                "Authorization": "N3 " + GUID,
            }
            ) as response:

            status = response.status
            headers = response.headers
            text = await response.text()  

            print(f"🌐 Статус: {status}")
            print("📦 Заголовки:", headers)
            print("📄 Ответ:")
            print(text)

            return text

async def main():
    clients = await db.getClients()
    lpuId = await db.getLpuId()

    print(f"sending client {clients[0][0]}")
    await sendIdentityPatient(lpuId, clients[0][1])

if __name__=="__main__":
    asyncio.run(main())
