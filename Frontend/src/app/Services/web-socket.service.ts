import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { SERVER_URL } from 'src/environments/environment';
import { WebSocketCallback } from '../Models/WebSocket.model';

@Injectable({
  providedIn: 'root'
})
export class WebSocketService{
  private callbacks: WebSocketCallback[] = [];

  constructor(
    private socket: Socket
  ) {}

  connect() {
    console.log('Connecting to ' + SERVER_URL + ' ...');
    this.socket.connect();
    const name = `user-${new Date().getTime()}`;

    this.socket.emit('set-name', name);
  }

  addFromEvent(page: string, eventName: string, callback: (data: any) => void) {
    this.callbacks.push({
      page,
      eventName,
      callback,
      subscription: this.socket.fromEvent(eventName).subscribe(callback)
    });
  }

  emitMessage(eventName: string, data?: any) {
    this.socket.emit(eventName, data);
  }

  unsubscribeFromEvents(page: string) {
    this.callbacks.forEach((c, i, arr) => {
      if (c.page === page) {
        c.subscription.unsubscribe();
      }
      arr.splice(i, 1);
    });
  }

  disconnect() {
    this.emitMessage('pause-ecg');
    this.socket.disconnect();
  }
}
