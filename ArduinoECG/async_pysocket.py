import socketio
import asyncio
from log import print_log

sio = socketio.AsyncClient()

LOCAL = 'http://localhost:8080'
CLOUD = 'https://backend.healthmonitor.dev'

# EXTERNAL FUNCTIONS
call_ping_request = False
def call_ping():
    call_ping_request = True

# CREATE EVENT HANDLERS
@sio.on('test-ecg')
async def test_ecg(data):
    print_log("test-ecg")
    print_log(data)

@sio.on('pingmebaby')
async def ping_me_baby():
    print_log("ping!")

# CALL EVENTS
async def send_live_segment(data):
    print_log('SEND NEW ECG SEGMENT')
    await sio.emit('new-ecg-segment', data)

async def send_alert(data):
    print_log('IMPLEMENT SEND ALERT')
    await sio.emit('alert', data)

async def send_os_data(data):
    print_log('IMPLEMENT SEND OS DATA')
    await sio.emit('alert', data)

async def ping():
    call_ping = False
    await sio.emit('pingmebaby')

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
    await sio.connect(LOCAL)
    await sio.wait()

async def background_process(callback):
    # Wait until connection is established
    while not sio.sid:
        print("Connecting...")
        await asyncio.sleep(1)

    while True:
        await asyncio.sleep(1)
        result = callback()
        print_log("DOATHING")
        if result:
            ping()

async def main(callback):
    await asyncio.gather(
        connect_to_server(),
        background_process(callback),
    )

def start_socketio(callback):
    asyncio.run(main(callback))