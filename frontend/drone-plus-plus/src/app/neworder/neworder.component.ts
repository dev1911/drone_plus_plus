import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {NewOrderService} from './neworder.service';

@Component({
  selector: 'app-neworder',
  templateUrl: './neworder.component.html',
  styleUrls: ['./neworder.component.css']
})
export class NeworderComponent implements OnInit {
  @ViewChild('lat', {static: true}) lat: ElementRef;
  @ViewChild('long', {static: true}) long: ElementRef;
  orderName: string;
  latVal: number;
  longVal: number;
  constructor(private newOrderService: NewOrderService) { }
  ngOnInit() {

  }
  updateLocation(event) {
    this.latVal = event.lat;
    this.longVal = event.long;
  }

  placeOrder() {
    this.newOrderService.placeOrder({
      orderName: this.orderName,
      latitude: this.latVal,
      longitude: this.longVal,
      address: 'some random address',
      status: ''
    }).subscribe((data) => {
      console.log(data);
    })
    ;
  }
}
