let app = require('express')();
let server = require('http').createServer(app);
let io = require('socket.io')(server);
 
io.on('connection', (socket) => {
  socket.on('disconnect', function(){
    io.emit('users-changed', {user: socket.username, event: 'left'});   
  });
 
  socket.on('set-name', (name) => {
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
    console.log(message);
    io.emit('ecg-point', {sampleNum: message.sampleNum, value: message.value, createdAt: new Date().valueOf()}); 
  });
});

var port = process.env.PORT || 8080;

server.listen(port, function(){
  console.log('listening in http://localhost:' + port);
});