import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class MapService {
  socket: WebSocket = null;
  locationChange = new EventEmitter();
  apiUrl = 'https://api.tomtom.com/routing/1/calculateRoute/';
  socketUrl = 'ws://192.168.99.103:30002/ws/drone/track/';
  gatewayUrl = 'http://192.168.99.103:30002/';
  logisticsUrl = 'http://192.168.99.103:30003';
  constructor(private httpClient: HttpClient) { }
  findPath(destLat, destLong, srcLatDef?, srcLongDef?) {
    const srcLat = srcLatDef || 0;
    const srcLong = srcLongDef || 0;
    return this.httpClient.post(`${this.gatewayUrl}path/`, {lat: destLat, long: destLong});
  }

  tomtom(srcLat, srcLong, destLat, destLong) {
    return this.httpClient.get(
      `${this.apiUrl}${srcLat},${srcLong}:${destLat},${destLong}/json?avoid=unpavedRoads&key=lJiiu1BLec33l0iGSETxeotI8qhJzde7` // 7
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

  getWarehouses() {
    return this.httpClient.get(this.gatewayUrl + 'warehouses/');
  }

}


/*
* drone svg  is taken from
* <div>Icons made by <a href="https://www.flaticon.com/authors/roundicons"
* title="Roundicons">Roundicons</a> from <a href="https://www.flaticon.com/"
* title="Flaticon">www.flaticon.com</a></div>
* */
