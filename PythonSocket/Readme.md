# Description
The file `pysocket.py` is example code for how to set up a python Socket-IO client. 

# Installation
To install packages run the following command: 
```
pip install -r requirements.txt
```

# Usage
## Event Handlers
Event handlers can be created as follows:
```
@sio.on('event_name')
async def event_handler_function():
    print("event happened")
```

## Call Events
Events can be called as follows:
```
async def call_event_function():
    await sio.emit('event_name', data)
```

## Main Process
Use the `main_process()` function to run concurrent process to collect data etc.