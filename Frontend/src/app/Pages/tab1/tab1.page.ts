import { Component, OnInit } from '@angular/core';
import { WebSocketService } from 'src/app/Services/web-socket.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss']
})
export class Tab1Page implements OnInit {
  ecgSegments;
  private ecgData = null;

  constructor(
    private router: Router,
    private webSocketService: WebSocketService
  ) {}

  ngOnInit() {
    this.webSocketService.addFromEvent(this.router.url, 'new-ecg-segments', (data) => {
      this.ecgData = data;
      this.replaceECGSegments();
    });
  }

  getNewECGSegments() {
    this.webSocketService.emitMessage('get-ecg-segments');
  }

  replaceECGSegments() {
    console.log(this.ecgData);
    this.ecgSegments = this.ecgData.map(d => ({
      title: `ECG Type: '${d.type}' (${d.item} of ${d.count})`,
      values: d.values
    }));
  }
}
