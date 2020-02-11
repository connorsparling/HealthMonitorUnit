let app = require('express')();
let server = require('http').createServer(app);
let io = require('socket.io')(server);

console.log("STARTING SERVER");
io.on('connection', (socket) => {
  console.log('CONNECTION ESTABLISHED');
  socket.on('disconnect', function(){
    io.emit('users-changed', {user: socket.username, event: 'left'});   
  });

  socket.on('set-name', (name) => {
    console.log('SET NAME: ' + name);
    socket.username = name;
    io.emit('users-changed', {user: name, event: 'joined'});  
  });
  
  socket.on('send-message', (message) => {
    io.emit('message', {msg: message.text, user: socket.username, createdAt: new Date()});
  });

  socket.on('clear-stream-data', () => {
    io.emit('clear-messages'); 
  });

  socket.on('new-ecg-point', (message) => {
    socket.broadcast.emit('new-ecg-point', {data: message.data, createdAt: new Date().valueOf()}); 
  });

  socket.on('alert', function(data) {
    console.log('ALERT! ' + data);
    socket.broadcast.emit('alert', data);
  });

  socket.on('segment-ok', function() {
    socket.broadcast.emit('segment-ok');
  });

  socket.on('test-segment', function(data) {
    console.log('test segment received');
    io.emit('test-segment', data);
  });

  socket.on('start-ecg', function() {
    console.log('START ECG');
    io.emit('start-ecg');
  });

  socket.on('pause-ecg', function() {
    console.log('PAUSE ECG');
    io.emit('pause-ecg');
  });

  socket.on('reset-ecg', function() {
    console.log('RESET ECG');
    io.emit('reset-ecg');
  });

  socket.on('get-ecg-segments', function() {
    console.log('GET ECG SEGMENTS');
    io.emit('get-ecg-segments');
  });

  socket.on('new-ecg-segments', function(data) {
    console.log('NEW ECG SEGMENTS');
    io.emit('new-ecg-segments', data);
  });

  socket.on('pingmebaby', function() {
    console.log('pingmebaby');
    io.emit('pingmebaby');
  });
});

var port = process.env.PORT || 8080;

function updateMe() {
  setTimeout(function() {
    console.log('still working at ' + new Date().getTime());
    updateMe();
  }, 10000);
}

server.listen(port, function(){
  console.log('listening in http://localhost:' + port);
  updateMe();
});