import socketio
import asyncio
import time

sio = socketio.AsyncClient()

# CREATE EVENT HANDLERS
@sio.on('event_name')
async def event_handler_function():
    print("event happened")

# CALL EVENTS
async def call_event_function():
    await sio.emit('event_name', data)

# EXAMPLE
@sio.on('pingmebaby')
async def event_name():
    print("ping!")

async def ping():
    await sio.emit('pingmebaby')

# MAIN PROCESS FUNCTION
async def main_process():
    while True:
        await asyncio.sleep(10)
        await ping()

# DEFAULT EVENTS AND SETUP
@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

async def connect_to_server():
    await sio.connect('http://localhost:8080') # Connect to local server
    # await sio.connect('https://backend.healthmonitor.dev') # Connect to cloud server
    await sio.wait()

async def background_process():
    # Wait until connection is established
    while not sio.sid:
        print("Connecting...")
        await asyncio.sleep(1)

    # Run main process
    await main_process()

async def main():
    await asyncio.gather(
        connect_to_server(),
        background_process(),
    )

asyncio.run(main())