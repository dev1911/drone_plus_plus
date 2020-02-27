import {Component, OnInit} from '@angular/core';
import {MapService} from './map.service';
declare let L;
declare let tomtom: any;

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})

export class MapComponent implements OnInit {

  constructor(private mapService: MapService) { }
  lat = 18.983938;
  long = 72.8498176;
  ngOnInit() {
    navigator.geolocation.getCurrentPosition((position) => {
      console.log('Got position', position.coords);
      this.lat = position.coords.latitude;
      this.long = position.coords.longitude;
      console.log(this.lat, this.long);
    });
    const map = tomtom.L.map('map', {
      key: 'lJiiu1BLec33l0iGSETxeotI8qhJzde7',
      basePath: '/assets/sdk',
      center: [this.lat, this.long],
      zoom: 15,
      source: 'vector'
    });
    let path;
    let marker = new L.marker([this.lat, this.long]).addTo(map);
    map.on('click', (e) => {
      marker.remove();
      marker = new L.marker(e.latlng).addTo(map);
      this.lat = e.latlng.lat;
      this.long = e.latlng.lng;
      const response = this.mapService.findPath(this.lat, this.long, 19.0178, 72.8478);
      response.subscribe((data) => {
        const points = data['routes'][0].legs[0].points;
        const wayPoints = new Array();
        for (let i = 0; i < points.length; ++i) {
          wayPoints.push(L.latLng(points[i].latitude, points[i].longitude));
        }
        if (path !== undefined) {
          path.remove();
        }
        path = L.polyline(wayPoints, {
          color: 'red',
          weight: 3
        }).addTo(map);
      });
    });

  }

}
