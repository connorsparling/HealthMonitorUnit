import { Component, OnInit, Input } from '@angular/core';

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

  constructor() { }

  ngOnInit() {}

}
