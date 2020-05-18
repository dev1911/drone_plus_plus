import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class NewOrderService {
  gatewayUrl = 'http://127.0.0.1:8000/';
  constructor(private http: HttpClient) { }

  placeOrder(orderData) {
    return this.http.post(this.gatewayUrl + 'create_order/', {
      orderName: orderData.orderName,
      latitude: orderData.latitude,
      longitude: orderData.longitude,
      address: orderData.address,
      status: orderData.status
    });
  }

}
