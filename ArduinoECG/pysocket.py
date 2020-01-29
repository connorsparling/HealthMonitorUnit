import socketio
from log import print_log

sio = socketio.Client()

# CREATE EVENT HANDLERS
@sio.on('test-ecg')
def test_ecg(data):
    print_log("test-ecg")
    print_log(data)

@sio.on('pingmebaby')
def ping_me_baby():
    print_log("ping!")

# CALL EVENTS
def send_live_segment(data):
    print_log('SEND NEW ECG SEGMENT')
    sio.emit('new-ecg-segment', data)

def send_alert(data):
    print_log('IMPLEMENT SEND ALERT')
    sio.emit('alert', data)

def send_os_data(data):
    print_log('IMPLEMENT SEND OS DATA')
    sio.emit('alert', data)

def ping():
    call_ping = False
    sio.emit('pingmebaby')

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