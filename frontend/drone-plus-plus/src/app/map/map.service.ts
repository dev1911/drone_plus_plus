import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class MapService {
  apiUrl = 'https://api.tomtom.com/routing/1/calculateRoute/';
  constructor(private httpClient: HttpClient) { }
  findPath(srcLat, srcLong, destLat, destLong) {
    return this.httpClient.get(
      `${this.apiUrl}${srcLat},${srcLong}:${destLat},${destLong}/json?avoid=unpavedRoads&key=lJiiu1BLec33l0iGSETxeotI8qhJzde7`
    );
  }
}
