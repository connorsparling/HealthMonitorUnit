let csv = require('csv');
const io = require('socket.io-client');

console.log("STARTING TEST CLIENT");
var WEBSOCKET = 'https://backend.healthmonitor.dev';
//var WEBSOCKET = process.env.WEBSOCKET || 'http://localhost:8080';
console.log("CONNECTING TO: " + WEBSOCKET);
const socket = io(WEBSOCKET);

socket.on('connect', function(){
    console.log("CONNECTED");

    var time = new Date().valueOf();
    var index = 1;
    var pauseEcg = true;
    var packetSize = 200;
    var delay = 8 * packetSize;

    function sendNewEcgPoint() {
        if (!pauseEcg) {
            while(true) {
                newTime = new Date().valueOf();
                if (newTime - time > delay) {
                    time += delay;
                    console.log("SENDING NEW POINT AT " + newTime);
                    var data = [];
                    for (var i = index; i < index + packetSize; i++) {
                        if (index < ecgData.length) {
                            data.push({
                                sampleNum: parseInt(ecgData[i][0]), 
                                value: parseInt(ecgData[i][1]), 
                            })
                        }
                    }
                    socket.emit(
                        'new-ecg-point', 
                        { data }, 
                        () => {
                            console.log("RESPONSE AT " + new Date().valueOf());
                            sendNewEcgPoint();
                        }
                    );
                    index += packetSize;
                    if (index >= ecgData.length) {
                        index = 1;
                    }
                    break;
                }
            }
        }
    }

    // function sendEcgPoints() {
    //     if (!pauseEcg) {
    //         while(true) {
    //             newTime = new Date().valueOf();
    //             if (newTime - time > 8) {
    //                 time += 8;
    //                 sendNewEcgPoint();
    //                 break;
    //             }
    //         }
    //     }
    // }

    ecgData = [];

    socket.on('start-ecg', function() {
        console.log('START');
        pauseEcg = false;
        time = new Date().valueOf();
        sendNewEcgPoint();
    });

    socket.on('pause-ecg', function() {
        console.log('PAUSE');
        pauseEcg = true;
    });

    socket.on('reset-ecg', function() {
        console.log('RESET');
        index = 0;
    });

    const obj = csv();
    obj.from.path('ecg_data/mitbih-database/104.csv').to.array(function (data) {
        ecgData = data;
        sendNewEcgPoint();
    });
});