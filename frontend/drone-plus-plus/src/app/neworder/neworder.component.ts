import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';

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
  constructor() { }
  ngOnInit() {

  }
  updateLocation(event) {
    this.latVal = event.lat;
    this.longVal = event.long;
  }

  placeOrder() {
    // TODO: create and link order service. handle errors
    console.log('Submit order');
  }
}
