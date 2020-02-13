import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { WebSocketService } from 'src/app/Services/web-socket.service';

@Component({
  selector: 'app-chart-grid',
  templateUrl: './chart-grid.component.html',
  styleUrls: ['./chart-grid.component.scss'],
})
export class ChartGridComponent implements OnInit {
  @Input() items: {
    title: string,
    values: number[]
  }[];

  constructor(
    private webSocketService: WebSocketService
  ) { }

  ngOnInit() {}

  testData(data) {
    console.log("CLICK");
    console.log(data);
    this.webSocketService.emitMessage('test-segment', data);
  }
}
