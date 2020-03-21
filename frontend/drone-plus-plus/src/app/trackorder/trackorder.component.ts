import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-trackorder',
  templateUrl: './trackorder.component.html',
  styleUrls: ['./trackorder.component.css']
})
export class TrackorderComponent implements OnInit {
  orders: object;

  constructor() { }

  ngOnInit() {
    // TODO: fetch orders of current customer and update this.orders
    this.orders = {
      orders: [
        {id: 1, name: 'First Order', type: 'Simple Order', date: '11/11/11'},
        {id: 2, name: 'Second Order', type: 'Critical Order', date: '12/12/12'},
        {id: 1, name: 'First Order', type: 'Simple Order', date: '11/11/11'},
        {id: 2, name: 'Second Order', type: 'Critical Order', date: '12/12/12'},
        {id: 1, name: 'First Order', type: 'Simple Order', date: '11/11/11'},
        {id: 2, name: 'Second Order', type: 'Critical Order', date: '12/12/12'},
        {id: 1, name: 'First Order', type: 'Simple Order', date: '11/11/11'},
        {id: 2, name: 'Second Order', type: 'Critical Order', date: '12/12/12'},
        {id: 1, name: 'First Order', type: 'Simple Order', date: '11/11/11'},
        {id: 2, name: 'Second Order', type: 'Critical Order', date: '12/12/12'},
      ]
    };
  }
}
