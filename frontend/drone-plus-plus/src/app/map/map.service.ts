import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class MapService {
  apiUrl = 'https://api.tomtom.com/routing/1/calculateRoute/';
  logisticsUrl = 'http://127.0.0.1:8002';
  constructor(private httpClient: HttpClient) { }
  findPath(destLat, destLong) {
    const srcLat = 19.1136;
    const srcLong = 72.8697;
    // // calling Logistics API to find nearest warehouse
    // const res = this.httpClient.get(
    //   `${this.logisticsUrl}/warehouse/find/?destLat=${destLat}&destLong=${destLong}`
    // );
    // res.subscribe((data) => {
    //   srcLat = data['warehouses'][0]['srcLat'];
    //   srcLong = data['warehouses'][0]['srcLong'];
    // },
    //   (error) => {
    //     console.log('error ', error);
    //   });
    return this.httpClient.get(
      `${this.apiUrl}${srcLat},${srcLong}:${destLat},${destLong}/json?avoid=unpavedRoads&key=lJiiu1BLec33l0iGSETxeotI8qhJzde` //7
    );
  }
}
