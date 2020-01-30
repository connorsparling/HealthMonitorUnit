import { Component, OnInit } from '@angular/core';
import { WebSocketService } from 'src/app/Services/web-socket.service';
import { ToastController } from '@ionic/angular';

@Component({
  selector: 'app-tabs',
  templateUrl: 'tabs.page.html',
  styleUrls: ['tabs.page.scss']
})
export class TabsPage implements OnInit {

  constructor(
    private webSocketService: WebSocketService,
    public toastController: ToastController
  ) {}

  ngOnInit() {
    this.webSocketService.connect();

    window.addEventListener('beforeunload', () => {
      this.webSocketService.disconnect();
    });

    this.webSocketService.addFromEvent('tabs', 'alert', this.presentAlertToast);
    this.webSocketService.addFromEvent('tabs', 'segment-ok', this.presentOkToast);
  }

  async presentOkToast(data) {
    const toast = await this.toastController.create({
      position: 'middle',
      message: 'Segment classified as normal',
      duration: 2000,
      cssClass: 'success-toast'
    });
    toast.present();
  }

  async presentAlertToast(data) {
    const toast = await this.toastController.create({
      position: 'middle',
      message: 'ALERT!  ' + data,
      duration: 3000,
      cssClass: 'alert-toast'
    });
    toast.present();
  }
}
