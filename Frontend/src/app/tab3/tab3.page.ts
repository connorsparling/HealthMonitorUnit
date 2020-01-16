import { Component, OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { ToastController } from '@ionic/angular';
import { SERVER_URL } from 'src/environments/environment';

@Component({
  selector: 'app-tab3',
  templateUrl: 'tab3.page.html',
  styleUrls: ['tab3.page.scss']
})
export class Tab3Page implements OnInit {
  message = '';
  messages = [];
  ecgData = [];
  currentUser = '';

  constructor(
    private socket: Socket,
    private toastCtrl: ToastController
  ) { }

  ngOnInit() {
    console.log('Connecting to ' + SERVER_URL + ' ...');
    this.socket.connect();

    const name = `user-${new Date().getTime()}`;
    this.currentUser = name;

    this.socket.emit('set-name', name);

    this.socket.fromEvent('users-changed').subscribe(data => {
      const user = data['user'];
      if (data['event'] === 'left') {
        this.showToast('User left: ' + user);
      } else {
        this.showToast('User joined: ' + user);
      }
    });

    this.socket.fromEvent('message').subscribe(message => {
      this.messages.push(message);
    });

    this.socket.fromEvent('clear-messages').subscribe(data => {
      this.ecgData = [];
    });

    this.socket.fromEvent('ecg-point').subscribe(data => {
      this.ecgData.push({sampleNum: data['sampleNum'], value: data['value']});
    });
  }

  sendMessage() {
    this.socket.emit('send-message', { text: this.message });
    this.message = '';
  }

  ionViewWillLeave() {
    this.socket.disconnect();
  }

  async showToast(msg) {
    const toast = await this.toastCtrl.create({
      message: msg,
      position: 'top',
      duration: 2000
    });
    toast.present();
  }
}
