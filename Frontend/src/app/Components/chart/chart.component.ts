import { Component, OnInit, Input, ViewChild, ElementRef } from '@angular/core';
import { Chart } from 'chart.js';
import { BehaviorSubject } from 'rxjs';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.scss'],
})
export class ChartComponent implements OnInit {
  @ViewChild('lineCanvas', { static: true }) lineCanvas: ElementRef;
  private lineChart: Chart;
  private maxDataLen = 100;
  private defaultChartLabels = [];
  private defaultChartValues = [];

  private title: string;

  private _item = new BehaviorSubject<any>([]);

  @Input() set item(item: any) {
    this._item.next(item);
  }

  ngOnInit() {
    for (let i = 0; i < this.maxDataLen; i++) {
      this.defaultChartLabels.push((i - this.maxDataLen));
      this.defaultChartValues.push(1000);
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
              suggestedMin: -1,
              suggestedMax: 1
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
    this.lineChart.update();
    this._item.subscribe(item => {
      this.title = item.title;
      console.log(item);
      this.lineChart.data.labels = item.values.map(d => d.toString());
      this.lineChart.data.datasets[0].data = item.values;
      this.lineChart.update();
    });
  }

  constructor() { }

  createChart() {
    this.lineChart = new Chart(this.lineCanvas.nativeElement, {
      type: 'line',
      data: {
        labels: [],
        datasets: [
          {
            label: 'ECG Heartbeat',
            fill: false,
            lineTension: 0,
            backgroundColor: 'rgba(75, 192, 192, 0.4)',
            borderColor: 'rgba(106, 160, 255, 1)',
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            pointBorderWidth: 0,
            pointRadius: 0,
            pointHitRadius: 10,
            padding: 20,
            data: [],
            spanGaps: true
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
              suggestedMin: -1,
              suggestedMax: 1
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
  }
}
