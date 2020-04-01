import { Component, OnInit } from '@angular/core';
import * as moment from 'moment';
import {MapService} from '../map/map.service';

@Component({
  selector: 'app-trackorder',
  templateUrl: './trackorder.component.html',
  styleUrls: ['./trackorder.component.css']
})
export class TrackorderComponent implements OnInit {
  orders: object;

  constructor(private mapService: MapService) { }

  ngOnInit() {
    // TODO: fetch orders of current customer and update this.orders
    this.orders = {
      orders: [
        {id: 1, name: 'First Order', type: 'Simple Order', eta: moment('25/03/2020, 14:20', 'DD/MM/YYYY, h:mm').fromNow()},
        {id: 2, name: 'Second Order', type: 'Critical Order', eta: moment('24/03/2020, 15:20', 'DD/MM/YYYY, h:mm').fromNow()},
      ]
    };
  }
  track(e) {
    this.mapService.trackDrones(e);
  }
}
