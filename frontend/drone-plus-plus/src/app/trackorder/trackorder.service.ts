import { Injectable } from '@angular/core';
import {LoginService} from '../login/login.service';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class TrackorderService {
  gatewayUrl = 'http://127.0.0.1:8000/all_order/';
  constructor(private httpClient: HttpClient) { }
  getOrders() {
    return this.httpClient.get(this.gatewayUrl);
  }
  getShowWarehouses(): boolean {
    if (localStorage.getItem('show-warehouses') != null) {
      return localStorage.getItem('show-warehouses') === 'true';
    }
    return false;
  }

  getShowPaths(): boolean {
    if (localStorage.getItem('show-paths') != null) {
      return localStorage.getItem('show-paths') === 'true';
    }
    return false;
  }

  getShowDrones(): boolean {
    if (localStorage.getItem('show-drones') != null) {
      return localStorage.getItem('show-drones') === 'true';
    }
    return false;
  }
  setShowWarehouses(show: boolean) {
    localStorage.setItem('show-warehouses', show ? 'true' : 'false');
  }

  setShowDrones(show: boolean) {
    localStorage.setItem('show-drones', show ? 'true' : 'false');
  }

  setShowPaths(show: boolean) {
    localStorage.setItem('show-paths', show ? 'true' : 'false');
  }
}

