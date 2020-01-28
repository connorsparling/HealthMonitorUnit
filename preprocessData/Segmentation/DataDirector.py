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
    await sendNewEcgPoint()
    
@sio.on('pause-ecg')
async def event_name():
    print("PAUSE")
    pauseEcg = True

async def sendNewEcgPoint():
    if pauseEcg == False:
        Serial_Pi.LoadECGData(Ecg_Data_Buffer, PACKET_SIZE)
        #print(Ecg_Data_Buffer)
        data = []
        for index in range(len(Ecg_Data_Buffer)):
            data.append({
                'sampleNum': index, 
                'value': int(Ecg_Data_Buffer[index]*1000)
            })
        print(data)
        await sio.emit('new-ecg-point', data)
        print("Ahhhhhhhhh")  

async def background_process():
    while not sio.sid:
        print("Connecting...")
        await asyncio.sleep(1)

    while True:
        print("dfhdhsf")
        await sendNewEcgPoint()

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

# async def main():
#     await connect_to_server()

async def main():
    await asyncio.gather(
        connect_to_server(),
        background_process(),
    )
    
asyncio.run(main()) 