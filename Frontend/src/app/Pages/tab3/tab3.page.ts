import { Component, OnInit } from '@angular/core';
import { WebSocketService } from 'src/app/Services/web-socket.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-tab3',
  templateUrl: 'tab3.page.html',
  styleUrls: ['tab3.page.scss']
})
export class Tab3Page implements OnInit {
  logMessages = [];

  constructor(
    private webSocketService: WebSocketService,
    private router: Router
  ) { }

  ngOnInit() {
    this.webSocketService.addFromEvent(this.router.url, 'new-ecg-point', data => {
      this.addData('Received new ECG data: ' + data.toString());
    });

    this.webSocketService.addFromEvent(this.router.url, 'alert', data => {
      this.addData('Received Alert: ' + data);
    });

    this.webSocketService.addFromEvent(this.router.url, 'segment-ok', data => {
      this.addData('Received segment OK');
    });
  }

  addData(message) {
    this.logMessages.push(message);
    if (this.logMessages.length > 1000) {
      this.logMessages.shift();
    }
  }
}
