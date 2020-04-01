import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class MapService {
  socket: WebSocket = null;
  locationChange = new EventEmitter();
  apiUrl = 'https://api.tomtom.com/routing/1/calculateRoute/';
  socketUrl = 'ws://127.0.0.1:8000/ws/drone/track/';
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
        `${this.apiUrl}${srcLat},${srcLong}:${destLat},${destLong}/json?avoid=unpavedRoads&key=lJiiu1BLec33l0iGSETxeotI8qhJzde` // 7
    );
  }
  trackDrones(droneId) {
    if (this.socket) {
      this.socket.close();
    }
    if (droneId === undefined) {
      this.socket = new WebSocket(this.socketUrl);
      this.socket.onmessage = (e) => {
        // websocket opened for all drone tracking
        console.log('message', e);
      };
    } else {
      this.socket = new WebSocket(`${this.socketUrl}${droneId}/`);
      this.socket.onmessage = (e) => {
      // websocket opened for single drone tracking
        this.locationChange.emit(e.data);
      };
    }
  }
}


/*
* drone svg  is taken from
* <div>Icons made by <a href="https://www.flaticon.com/authors/roundicons"
* title="Roundicons">Roundicons</a> from <a href="https://www.flaticon.com/"
* title="Flaticon">www.flaticon.com</a></div>
* */
