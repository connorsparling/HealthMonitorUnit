import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Chart } from 'chart.js';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  styleUrls: ['tab2.page.scss']
})
export class Tab2Page  implements OnInit {
  @ViewChild('lineCanvas', { static: true }) lineCanvas: ElementRef;

  private lineChart: Chart;

  constructor(
    private socket: Socket
  ) {}

  ngOnInit() {
    this.lineChart = new Chart(this.lineCanvas.nativeElement, {
      type: "line",
      data: {
        labels: [],
        datasets: [
          {
            label: "My First dataset",
            fill: false,
            lineTension: 0,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)",
            borderCapStyle: "butt",
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: "miter",
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data: [],
            spanGaps: false
          }
        ]
      },
      options: {
          scales: {
              yAxes: [{
                  ticks: {
                      suggestedMin: 900,
                      suggestedMax: 1250
                  }
              }]
          }
      }
    });

    this.socket.fromEvent('clear-messages').subscribe(data => {
      this.removeData();
    });

    this.socket.fromEvent('ecg-point').subscribe(data => {
      this.addData(data['sampleNum'], data['value']);
    });
  }

  addData(label, data) {
    this.lineChart.data.labels.push(label);
    this.lineChart.data.datasets[0].data.push(parseInt(data));
    if (this.lineChart.data.datasets[0].data.length > 400) {
      this.lineChart.data.labels.shift();
      this.lineChart.data.datasets[0].data.shift();
    }
    this.lineChart.update();
  }

  removeData() {
    this.lineChart.data.labels = [];
    this.lineChart.data.datasets[0].data = [];
    this.lineChart.update();
  }
}
