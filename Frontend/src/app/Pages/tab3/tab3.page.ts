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
      console.log(data);
      const items = data.data.map(item => item.value);
      console.log(items);
      //this.addData({type: 'data', message: JSON.stringify(items)});
      this.addData({type: 'normal', message: 'New ECG data'});
    });

    this.webSocketService.addFromEvent(this.router.url, 'alert', data => {
      this.addData({type: 'alert', message: 'Alert: ' + data});
    });

    this.webSocketService.addFromEvent(this.router.url, 'segment-ok', data => {
      this.addData({type: 'ok', message: 'Segment OK'});
    });

    this.webSocketService.addFromEvent(this.router.url, 'new-ecg-segments', data => {
      this.addData({type: 'normal', message: 'New ECG segments'});
    });
  }

  addData(message) {
    this.logMessages.push(message);
    if (this.logMessages.length > 1000) {
      this.logMessages.shift();
    }
  }
}
