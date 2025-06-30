import aiohttp
import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler
import os

import database as db
from config import BASE_URL, GUID

log_dir = './logs/'
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, 'policy.log')

logger = logging.getLogger('PolicyAutocheck')
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(
    log_file,
    when='midnight',
    interval=1,    
    backupCount=14,
    encoding='utf-8',
    utc=False   
)

formatter = logging.Formatter(
    fmt='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)

logger.addHandler(handler)

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
    await db.cleanCheckPolicy()

    clients = await db.getClients()
    lpuId = await db.getLpuId()

    for client in clients:
        try:
            result = await sendIdentityPatient(lpuId, client[1])
            await db.writeCheckPolicy(result[0], client[0], result[1])
            logger.info(f"Клиент {client[0]} успешно отправлен")

        except Exception as e:
            logger.error(f"Клиента {client[0]} не удалось отправить: {str(e)}")


if __name__=="__main__":
    asyncio.run(main())
