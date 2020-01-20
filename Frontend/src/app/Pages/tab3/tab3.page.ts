import { Component, OnInit } from '@angular/core';
import { ToastController } from '@ionic/angular';
import { WebSocketService } from 'src/app/Services/web-socket.service';
import { Router } from '@angular/router';

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
    private toastCtrl: ToastController,
    private webSocketService: WebSocketService,
    private router: Router
  ) { }

  ngOnInit() {
    // const name = `user-${new Date().getTime()}`;
    // this.currentUser = name;

    // this.webSocketService.emitMessage('set-name', name);

    this.webSocketService.addFromEvent(this.router.url, 'users-changed', data => {
      const user = data['user'];
      if (data['event'] === 'left') {
        this.showToast('User left: ' + user);
      } else {
        this.showToast('User joined: ' + user);
      }
    });

    this.webSocketService.addFromEvent(this.router.url, 'ecg-point', data => {
      this.addData(data['sampleNum'], data['value']);
    });
  }

  addData(label, value) {
    this.ecgData.push({sampleNum: label, value: parseInt(value)});
    if (this.ecgData.length > 1000) {
      this.ecgData.shift();
    }
  }

  sendMessage() {
    this.webSocketService.emitMessage('send-message', { text: this.message });
    this.message = '';
  }

  async showToast(msg) {
    const toast = await this.toastCtrl.create({
      message: msg,
      position: 'top',
      duration: 2000
    });
    toast.present();
  }

  // ionViewWillLeave() {
  //   this.webSocketService.unsubscribeFromEvents(this.router.url);
  // }
}
