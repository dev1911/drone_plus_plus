import {Component, EventEmitter, OnInit, Output, ViewChild} from '@angular/core';
import * as moment from 'moment';
import {MapService} from '../map/map.service';
import {TrackorderService} from './trackorder.service';
import {MapComponent} from '../map/map.component';

interface Order {
  order_id: number;
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
  @ViewChild(MapComponent, {static : false}) map;
  orders: {};
  showWarehouse = this.trackorderService.getShowWarehouses();
  showDrones = this.trackorderService.getShowDrones();
  showPaths = this.trackorderService.getShowPaths();
  constructor(private mapService: MapService, private trackorderService: TrackorderService) { }

  showWarehouseChange(e) {
    this.trackorderService.setShowWarehouses(e.target.checked);
    if (this.showWarehouse) {
      this.map.showWarehouses();
    } else {
      this.map.hideWarehouses();
    }
  }
  showDronesChange(e) {
    this.trackorderService.setShowDrones(e.target.checked);
  }
  showPathsChange(e) {
    this.trackorderService.setShowPaths(e.target.checked);
  }

  ngOnInit() {
    this.orders = {};
    this.trackorderService.getOrders().subscribe(
      data => {
        console.log({data});
        this.orders = {orders : data};
      }
    );
  }
  track(e) {
    if (e.drone_id === null || e.drone_id === undefined) {
      alert('Drones is not assigned yet.');
      return;
    }
    this.map.showDronePath(e.drone_id, e.latitude, e.longitude);
    this.mapService.trackDrones(e.drone_id);
  }
}
