# main.py -- put your code here!
import asyncio
from uart import Uart


async def main():
    connection = Uart()
    while True:
        await asyncio.sleep(0)
        message =  await connection.get_position()
        print(message)
        print(message[3].yaw)
        
asyncio.run(main())