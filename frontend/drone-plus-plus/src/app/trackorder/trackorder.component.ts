import { Component, OnInit } from '@angular/core';
import * as moment from 'moment';
import {MapService} from '../map/map.service';
import {TrackorderService} from './trackorder.service';

interface Order {
  id: number;
  name: string;
  type: string;
  eta: string;
}

interface OrderArray {
  orders: Order[];
}

@Component({
  selector: 'app-trackorder',
  templateUrl: './trackorder.component.html',
  styleUrls: ['./trackorder.component.css']
})
export class TrackorderComponent implements OnInit {
  orders: OrderArray;
  showWarehouse = this.trackorderService.getShowWarehouses();
  showDrones = this.trackorderService.getShowDrones();
  showPaths = this.trackorderService.getShowPaths();
  constructor(private mapService: MapService, private trackorderService: TrackorderService) { }

  showWarehouseChange(e) {
    this.trackorderService.setShowWarehouses(e.target.checked);
  }
  showDronesChange(e) {
    this.trackorderService.setShowDrones(e.target.checked);
  }
  showPathsChange(e) {
    this.trackorderService.setShowPaths(e.target.checked);
  }

  ngOnInit() {
    // TODO: fetch orders of current customer and update this.orders
    this.orders = {
      orders: [
        {id: 1, name: 'First Order', type: 'Simple Order', eta: moment('25/03/2020, 14:20', 'DD/MM/YYYY, h:mm').fromNow()},
        {id: 2, name: 'Second Order', type: 'Critical Order', eta: moment('24/03/2020, 15:20', 'DD/MM/YYYY, h:mm').fromNow()},
      ]
    };

    // this.trackorderService.getOrders().subscribe(
    //   data => {
    //     this.orders = data;
    //   }
    // );
  }
  track(e) {
    this.mapService.trackDrones(e);
  }
}
