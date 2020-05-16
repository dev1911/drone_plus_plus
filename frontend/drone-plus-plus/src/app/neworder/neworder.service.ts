import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class NewOrderService {
  gatewayUrl = 'http://192.168.99.103:30002';
  constructor(private http: HttpClient) { }

  placeOrder(orderData) {
    return this.http.post(this.gatewayUrl + '/create_order/', {
      orderName: orderData.orderName,
      latitude: orderData.latitude,
      longitude: orderData.longitude,
      address: orderData.address,
      status: orderData.status
    });
  }

}
