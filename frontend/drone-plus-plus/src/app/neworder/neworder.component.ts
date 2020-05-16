import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {NewOrderService} from './neworder.service';
import {Router} from '@angular/router';

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
  error = '';
  constructor(private newOrderService: NewOrderService, private router: Router) { }
  ngOnInit() {

  }
  updateLocation(event) {
    this.latVal = event.lat;
    this.longVal = event.long;
  }

  placeOrder() {
    if (this.orderName === undefined || this.latVal === undefined || this.longVal === undefined) {
      this.error = 'Order name and location both are required.';
      return;
    }
    this.error = '';
    const orderData = {
      orderName: this.orderName,
      latitude: this.latVal,
      longitude: this.longVal,
      address: 'some random address',
      status: ''
    };
    this.newOrderService.placeOrder(orderData).subscribe((data) => {
      alert('Order placed successfully.');
      this.router.navigate(['/']);
    }, error => {
      console.error(error)
      this.error = error.error.error;
    })
    ;
  }
}
