import socketio
import asyncio
import time
import numpy as np
import os
import csv

sio = socketio.AsyncClient()

WEBSOCKET_CLOUD = 'https://backend.healthmonitor.dev'
WEBSOCKET_LOCAL = 'http://localhost:8080'

segment_type_dict = {}
ECGSegments = []

# GET ECG SEGMENTS
@sio.on('get-ecg-segments')
async def event_name():
    segments_to_send = get_ECG_segments()
    await sio.emit('new-ecg-segments', segments_to_send)

def load_ECG_segments():
    print('Loading ECG Segments...')
    filename = '../Datasets/SectionData.csv'
    if os.path.exists(filename):
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            headers = next(csv_reader)
            for row in csv_reader:
                col = segment_type_dict.get(row[-1])
                if col is None:
                    col = len(ECGSegments)
                    segment_type_dict[row[-1]] = col
                    ECGSegments.append([])
                dataRow = []
                for i in range(len(row)-2):
                    dataRow.append(float(row[i]))
                ECGSegments[col].append(dataRow)
        csv_file.close()
    print('Finished Loading Segments')

def get_ECG_segments():
    segments = []
    for item in segment_type_dict:
        count = len(ECGSegments[segment_type_dict[item]])
        randomIndex = int(np.random.random() * count)
        segments.append({
            "type": item,
            "item": randomIndex,
            "count": count,
            "values": ECGSegments[segment_type_dict[item]][randomIndex]
        })
    return segments

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
    await sio.connect(WEBSOCKET)
    await sio.wait()

async def main():
    load_ECG_segments()
    await connect_to_server()

asyncio.run(main())