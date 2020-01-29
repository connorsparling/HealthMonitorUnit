import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Chart } from 'chart.js';
import { WebSocketService } from 'src/app/Services/web-socket.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  styleUrls: ['tab2.page.scss']
})
export class Tab2Page implements OnInit {
  @ViewChild('lineCanvas', { static: true }) lineCanvas: ElementRef;

  private lineChart: Chart;
  private maxDataLen = 1000;
  private defaultChartLabels = [];
  private defaultChartValues = [];

  constructor(
    private webSocketService: WebSocketService,
    private router: Router
  ) {}

  ngOnInit() {
    for (let i = 0; i < this.maxDataLen; i++) {
      this.defaultChartLabels.push((i - this.maxDataLen));
      this.defaultChartValues.push(0);
    }
    this.lineChart = new Chart(this.lineCanvas.nativeElement, {
      type: "line",
      data: {
        labels: [...this.defaultChartLabels],
        datasets: [
          {
            label: "ECG Heartbeat",
            fill: false,
            lineTension: 0,
            backgroundColor: "rgba(75, 192, 192, 0.4)",
            borderColor: "rgba(106, 160, 255, 1)",
            borderCapStyle: "butt",
            borderDash: [],
            borderDashOffset: 0.0,
            pointBorderWidth: 0,
            pointRadius: 0,
            pointHitRadius: 10,
            padding: 20,
            data: [...this.defaultChartValues],
            spanGaps: false
          }
        ]
      },
      options: {
        legend: {
          display: false
        },
        scales: {
          yAxes: [{
            ticks: {
              suggestedMin: -20,
              suggestedMax: 20
            }
          }],
          xAxes: [{
            ticks: {
              display: false
            },
            gridLines : {
              display : false
            }
          }]
        },
        tooltips: {
          enabled: false
        },
        hover: {
          mode: null
        },
        animation: {
          duration: 200
        }
      }
    });

    this.webSocketService.addFromEvent(this.router.url, 'clear-messages', data => {
      this.removeData();
    });

    this.webSocketService.addFromEvent(this.router.url, 'ecg-point', data => {
      this.addArrayData(data['data']);
    });
  }

  addArrayData(data) {
    let delay = 0;
    data.forEach(element => {
      setTimeout(() => {
        this.addData(element['sampleNum'], element['value']);
      }, delay);
      delay += 8;
    });
  }

  addData(label, value) {
    this.lineChart.data.labels.push(label);
    this.lineChart.data.datasets[0].data.push(parseInt(value));
    if (this.lineChart.data.datasets[0].data.length > this.maxDataLen) {
      this.lineChart.data.labels.shift();
      this.lineChart.data.datasets[0].data.shift();
    }
    this.lineChart.update();
  }

  removeData() {
    this.lineChart.data.labels = [...this.defaultChartLabels];
    this.lineChart.data.datasets[0].data = [...this.defaultChartValues];
    this.lineChart.update();
  }

  startECG() {
    this.webSocketService.emitMessage('start-ecg');
  }

  pauseECG() {
    this.webSocketService.emitMessage('pause-ecg');
  }

  resetECG() {
    this.removeData();
    this.webSocketService.emitMessage('reset-ecg');
  }

  reconnect() {
    this.webSocketService.disconnect();
    this.webSocketService.connect();
  }

  // ionViewWillLeave() {
  //   this.webSocketService.unsubscribeFromEvents(this.router.url);
  // }
}
