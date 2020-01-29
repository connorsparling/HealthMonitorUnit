#== GLOBAL ==========================================================================================================================
import threading
import time
import queue
from log import print_log
import serialRecieve
import socketio

LOCAL = 'http://localhost:8080'
CLOUD = 'https://backend.healthmonitor.dev'

def add_to_queue(queue, item):
    if queue is not None:
        try:
            queue.put(item, timeout=1)
        except:
            return False
        return True
    return False

#== SERIAL ==========================================================================================================================
# def send_serial_ping():
#     while True:
#         result = add_to_queue(emit_queue, {'function': 'pingmebaby', 'data': None})
#         if result:
#             break
#         print_log("EMIT QUEUE ADD = FALSE")

def serial(threadname, emit_queue, segment_queue):
    print_log("SERIAL THREAD WORKING")
    emit_buffer = []
    #segment_buffer = []
    index = 0
    for value in serialRecieve.LoadECGData():
        # add to 100 buffer
        emit_buffer.append({'sampleNum': index, 'value': value})
        # add to 1000 buffer
        #segment_buffer.append(value)
        # if 100 buffer is 100 then add to emit queue and clear
        if len(emit_buffer) >= 100:
            while True:
                result = add_to_queue(emit_queue, {'function': 'new-ecg-point', 'data': {'data': emit_buffer}})
                if result:
                    break
                print_log("EMIT QUEUE ADD = FALSE")
            emit_buffer = []
        # if 1000 buffer is 1000 then add to segment queue and clear
        # if len(segment_buffer) >= 1000:
        #     while True:
        #         result = add_to_queue(segment_queue, segment_buffer)
        #         if result:
        #             break
        #         print_log("SEGMENT QUEUE ADD = FALSE")
        #     segment_buffer = []

#== SOCKET IO CLIENT ================================================================================================================
global sio
sio = socketio.Client()

# CREATE EVENT HANDLERS
@sio.on('test-ecg')
def test_ecg(data):
    print_log("test-ecg")
    print_log(data)

@sio.on('pingmebaby')
def ping_me_baby():
    print_log("ping!")

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

def connect_to_server(server):
    sio.connect(server)
    sio.wait()

def socketIOClient():
    print_log("SOCKETIO THREAD WORKING")
    connect_to_server(LOCAL)

#== SOCKET IO EMIT QUEUE ============================================================================================================
# def send_live_segment(data):
#     print_log('SEND NEW ECG SEGMENT')
#     sio.emit('new-ecg-segment', data)

# def send_alert(data):
#     print_log('IMPLEMENT SEND ALERT')
#     sio.emit('alert', data)

# def send_os_data(data):
#     print_log('IMPLEMENT SEND OS DATA')
#     sio.emit('new-os-data', data)

# def ping(data):
#     sio.emit('pingmebaby')

def socketIOEmitQueue(threadname, emit_queue):
    print_log("SOCKETIO SENDING THREAD WORKING")
    while not sio.sid:
        pass
        #print_log("Connecting...")
    while True:
        try:
            item = emit_queue.get()
            if item is not None:
                if item['function'] is not None:
                    if item['data'] is not None:
                        sio.emit(item['function'], item['data'])
                    else:
                        sio.emit(item['function'])
                else:
                    print_log("ITEM FUNCTION IS NONE")
                emit_queue.task_done()
            else:
                print_log("QUEUE ITEM IS NONE")
        except:
            pass

#== NEURAL NET ======================================================================================================================
def neuralNet(threadname, neural_net_queue, emit_queue):
    print_log("NEURAL NET THREAD WORKING")
    while True:
        time.sleep(3)

#== SEGMENTATION ====================================================================================================================
def segmentation(threadname, segment_queue, neural_net_queue):
    print_log("SEGMENTATION THREAD WORKING")
    while True:
        time.sleep(4)

#== MAIN ============================================================================================================================
def main():
    emit_queue = queue.Queue(100)
    segment_queue = queue.Queue(100)
    neural_net_queue = queue.Queue(100)

    serial_t = threading.Thread(name="Serial", target=serial, args=("Serial", emit_queue, segment_queue))
    socketIOClient_t = threading.Thread(name="SocketIOClient", target=socketIOClient)
    socketIOEmitQueue_t = threading.Thread(name="SocketIOQueue", target=socketIOEmitQueue, args=("SocketIOQueue", emit_queue))
    neuralNet_t = threading.Thread(name="NeuralNet", target=neuralNet, args=("NeuralNet", neural_net_queue, emit_queue))
    segmentation_t = threading.Thread(name="Segmentation", target=segmentation, args=("Segmentation", segment_queue, neural_net_queue))

    try:
        serial_t.start()
        socketIOClient_t.start()
        socketIOEmitQueue_t.start()
        neuralNet_t.start()
        segmentation_t.start()
    except:
        serial_t.join()
        socketIOClient_t.join()
        socketIOEmitQueue_t.join()
        neuralNet_t.join()
        segmentation_t.join()

if __name__ == "__main__":
    main()