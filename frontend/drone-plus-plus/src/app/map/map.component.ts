import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {MapService} from './map.service';
declare let L;
declare let tomtom: any;

/**
 * This file is very badly written
 * Try to make it modular
 */

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})

export class MapComponent implements OnInit {
  @Output() locationChange = new EventEmitter();
  constructor(private mapService: MapService) { }
  lat = 18.983938;
  long = 72.8498176;
  destLat = 19.0178;
  destLong = 72.8478;
  droneIcon = new L.icon({
    iconUrl: '/assets/img/drone.svg',
    shadowUrl: '/assets/img/drone.svg',
    iconSize: [20, 20]
  });
  @Input() type: string;
  ngOnInit() {
    if (this.type === 'order') {
      navigator.geolocation.getCurrentPosition((position) => {
        // console.log('Got position', position.coords);
        this.lat = position.coords.latitude;
        this.long = position.coords.longitude;
      });
      const map = tomtom.L.map('map', {
        key: 'lJiiu1BLec33l0iGSETxeotI8qhJzde7',
        basePath: '/assets/sdk',
        center: [this.lat, this.long],
        zoom: 15,
        source: 'vector'
      });
      let path;
      const marker = new L.marker([this.lat, this.long]).addTo(map);
      map.on('click', (e) => {
        marker.setLatLng(e.latlng);
        this.lat = e.latlng.lat;
        this.long = e.latlng.lng;
        // console.log(this.lat, this.long);
        // update lat and long in new order component
        this.locationChange.emit({lat: this.lat, long: this.long});
        const response = this.mapService.findPath(this.lat, this.long);
        response.subscribe((data) => {
          const points = data['routes'][0].legs[0].points;
          const wayPoints = new Array();
          for(let i = 0; i < points.length; ++i) {
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
    } else if (this.type === 'track') {
        const token = localStorage.getItem('user-token');
        if (!this.type) {
          // TODO: this is for logistics person to track multiple drones
          this.mapService.trackDrones(undefined);
        } else {
          // TODO: this is for customers to track one single drone at a time
          const map = tomtom.L.map('map', {
            key: 'lJiiu1BLec33l0iGSETxeotI8qhJzde7',
            basePath: '/assets/sdk',
            center: [this.lat, this.long],
            zoom: 15,
            source: 'vector'
          });
          const marker = new L.marker([this.lat, this.long], {icon: this.droneIcon}).addTo(map);
          this.mapService.locationChange.subscribe(
            e => {
              const res = JSON.parse(e);
              console.log('Update position');
              marker.setLatLng([parseFloat(res.lat), parseFloat(res.long)]);
            }
          );
        }
    }

  }

}
