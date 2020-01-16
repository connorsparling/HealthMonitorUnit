let csv = require('csv');
const io = require('socket.io-client');

const socket = io('http://localhost:8080');

// this.socket.subscribe('ecg-point', message => {
//     console.log('I GOT IT BACK');
// });

// socket.emit('new-ecg-point', {sampleNum: 234234234, value: 5673245, time: 3657432});
// function ECGDatatype(Fone, Ftwo) {
//     this.sample_num = Fone;
//     this.value = Ftwo;
// }; 

var time = new Date().valueOf();
var index = 0;

ecgData = [];

socket.emit('clear-stream-data');

socket.on('ecg-point', function(data) {
    while(true) {
        newTime = new Date().valueOf();
        if (newTime - time > 8) {
            time += 8;
            i = index;
            index++;
            socket.emit('new-ecg-point', {sampleNum: parseInt(ecgData[i][0]), value: parseInt(ecgData[i][1]), time: new Date().valueOf()});
            break;
        }
    }
});

const obj = csv();
obj.from.path('ecg_data/mitbih-database/100.csv').to.array(function (data) {
    ecgData = data;
    i = index;
    index++;
    socket.emit('new-ecg-point', {sampleNum: parseInt(ecgData[i][0]), value: parseInt(ecgData[i][1]), time: new Date().valueOf()});
});