import asyncio
import websockets
import sqlite3

# Establish connection to the database
conn = sqlite3.connect('rover_data.db')
cursor = conn.cursor()

# Define a function to create the table if it doesn't exist
def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SensorData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            pitch REAL,
            roll REAL,
            yaw REAL,
            longitude REAL,
            latitude REAL,
            speed REAL
        )
    """)
    conn.commit()

create_table()

async def insert_data(pitch, roll, yaw, longitude, latitude, speed):
    cursor.execute("""
        INSERT INTO SensorData (pitch, roll, yaw, longitude, latitude, speed)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (pitch, roll, yaw, longitude, latitude, speed))
    conn.commit()

async def handler(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        # Assuming the data format is: pitch,roll,yaw,longitude,latitude,speed
        if message:
            try:
                data = message.split(',')
                pitch = float(data[0])
                roll = float(data[1])
                yaw = float(data[2])
                longitude = float(data[3])
                latitude = float(data[4])
                speed = float(data[5])
                
                # Insert data into the database
                await insert_data(pitch, roll, yaw, longitude, latitude, speed)
            except Exception as e:
                print(f"Error processing message: {e}")

start_server = websockets.serve(handler, "0.0.0.0", 5678)
print("Websocket server started")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
