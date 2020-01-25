import { Component, OnInit } from '@angular/core';
import { WebSocketService } from 'src/app/Services/web-socket.service';

@Component({
  selector: 'app-tabs',
  templateUrl: 'tabs.page.html',
  styleUrls: ['tabs.page.scss']
})
export class TabsPage implements OnInit {

  constructor(
    private webSocketService: WebSocketService
  ) {}

  ngOnInit() {
    this.webSocketService.connect();

    window.addEventListener('beforeunload', () => {
      this.webSocketService.disconnect();
    });
  }
}
