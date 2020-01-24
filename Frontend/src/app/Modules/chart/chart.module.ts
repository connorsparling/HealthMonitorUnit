import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartComponent } from 'src/app/Components/chart/chart.component';
import { ChartGridComponent } from 'src/app/Components/chart-grid/chart-grid.component';
import { IonicModule } from '@ionic/angular';


@NgModule({
  imports: [
    IonicModule,
    CommonModule
  ],
  declarations: [ChartComponent, ChartGridComponent],
  exports: [ChartComponent, ChartGridComponent]
})
export class ChartModule { }
