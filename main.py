import aiohttp
import asyncio

import database as db
from config import BASE_URL, GUID

async def sendIdentityPatient(lpuId, client: dict) -> dict:
    client["lpuId"] = lpuId

    async with aiohttp.ClientSession() as session:
        async with session.post(
            BASE_URL,
            json={
                "resourceType": "Parameters",
                "parameter": toFhir(client),
                },
            headers={
                "Authorization": "N3 " + GUID,
                "Content-Type": "application/json",
            }
            ) as response:

            status = response.status
            if status == 200:
                text = await response.text()  
                await db.writeCheckPolicy(text["parameter"][0]["valueString"])
            else:
                print(f"🌐 Статус: {status}")

def toFhir(client: dict) -> list[dict]:
    result = []
    
    for k, v in client.items():
        result.append({
            "name": k,
            "valueString": v
        })

    return result

async def main():
    clients = await db.getClients()
    lpuId = await db.getLpuId()

    print(f"sending client {clients[0][0]}")
    await sendIdentityPatient(lpuId, clients[0][1])

if __name__=="__main__":
    asyncio.run(main())
