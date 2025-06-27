import aiohttp
import asyncio

import database as db
from config import BASE_URL, GUID

async def sendIdentityPatient(lpuId, client: dict) -> tuple[str, str]:
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
            text = await response.json()  

            if status == 200:
                return text["parameter"][0]["valueString"], ""
            else:
                return "", text["issue"][0]["details"]["coding"][0]["display"]

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

    result = await sendIdentityPatient(lpuId, clients[0][1])
    await db.writeCheckPolicy(result[0], clients[0][0], result[1])

if __name__=="__main__":
    asyncio.run(main())
