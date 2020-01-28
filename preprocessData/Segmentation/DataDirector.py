import socketio
import asyncio
import Serial_Pi

sio = socketio.AsyncClient()

WEBSOCKET = 'https://backend.healthmonitor.dev'
PACKET_SIZE = 200

pauseEcg = False
Ecg_Data_Buffer = []

@sio.on('connect')
async def on_connect():
    print("CONNECTED")
    pauseEcg = True
    delay = 8 * PACKET_SIZE

@sio.on('start-ecg')
async def event_name():
    print("START")
    pauseEcg = False
    sendNewEcgPoint()
    
@sio.on('pause-ecg')
async def event_name():
    print("PAUSE")
    pauseEcg = True

async def sendNewEcgPoint():
    if pauseEcg == false:
        Serial_Pi.LoadECGData(ECG_Data_Buffer, PACKET_SIZE)
        await sio.emit('new-ecg-point', Ecg_Data_Buffer)     

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
    print('Connecting to ' + WEBSOCKET)
    await sio.connect(WEBSOCKET)
    await sio.wait()

async def main():
    await connect_to_server()
    while True:
        await sendNewEcgPoint()
    
asyncio.run(main()) 