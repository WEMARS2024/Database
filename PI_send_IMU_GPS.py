import asyncio
import websockets
import random
import time

async def send_data():
    uri = "ws://<PC_IP>:5678"  # Replace <laptop_ip_address> with the actual IP address of the laptop
    async with websockets.connect(uri) as websocket:
        while True:
            # Generate dummy data for the sake of example
            pitch = random.uniform(-90, 90)
            roll = random.uniform(-90, 90)
            yaw = random.uniform(-180, 180)
            longitude = random.uniform(-180, 180)
            latitude = random.uniform(-90, 90)
            speed = random.uniform(0, 100)
            
            data = f"{pitch},{roll},{yaw},{longitude},{latitude},{speed}"
            await websocket.send(data)
            print(f"Sent data: {data}")
            time.sleep(1)  # Send data every second

asyncio.get_event_loop().run_until_complete(send_data())
