import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {MapService} from './map.service';
import {TrackorderService} from '../trackorder/trackorder.service';
import {typeIsOrHasBaseType} from 'tslint/lib/language/typeUtils';
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
  constructor(private mapService: MapService, private trackorderService: TrackorderService) { }
  lat = 18.983938;
  long = 72.8498176;
  destLat = 19.0178;
  destLong = 72.8478;
  droneIcon = new L.icon({
    iconUrl: '/assets/img/drone.svg',
    shadowUrl: '/assets/img/drone.svg',
    iconSize: [20, 20]
  });
  warehouseIcon = new L.icon({
    iconUrl: '/assets/img/wh.svg',
    iconSize: [20, 20]
  });
  map = undefined;
  dronePath = undefined;
  warehouses = [];
  @Input() type: string;
  ngOnInit() {
    if (this.type === 'order') {
      navigator.geolocation.getCurrentPosition((position) => {
        this.lat = position.coords.latitude;
        this.long = position.coords.longitude;
      });
      this.map = tomtom.L.map('map', {
        key: 'lJiiu1BLec33l0iGSETxeotI8qhJzde7',
        basePath: '/assets/sdk',
        center: [this.lat, this.long],
        zoom: 15,
        source: 'vector'
      });
      let path;
      const marker = new L.marker([this.lat, this.long]).addTo(this.map);
      this.map.on('click', (e) => {
        marker.setLatLng(e.latlng);
        this.lat = e.latlng.lat;
        this.long = e.latlng.lng;
        // console.log(this.lat, this.long);
        // update lat and long in new order component
        this.locationChange.emit({lat: this.lat, long: this.long});
        const response = this.mapService.findPath(this.lat, this.long);
        response.subscribe(data => {
          console.log(data);
          const srcLat = data['lat'];
          const srcLong = data['long'];
          this.mapService.tomtom(srcLat, srcLong, this.lat, this.long).subscribe((data) => {
            console.log(data);
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
            }).addTo(this.map);
          });
        }, error => {
          console.error(error);
        });
      });
    } else if (this.type === 'track') {
        const token = localStorage.getItem('user-token');
        if (!this.type) {
          // TODO: this is for logistics person to track multiple drones
          this.mapService.trackDrones(undefined);
        } else {
          this.map = tomtom.L.map('map', {
            key: 'lJiiu1BLec33l0iGSETxeotI8qhJzde7',
            basePath: '/assets/sdk',
            center: [this.lat, this.long],
            zoom: 15,
            source: 'vector'
          });
          const marker = new L.marker([this.lat, this.long], {icon: this.droneIcon})
            .bindTooltip('Drone with Order', {permanent: false, direction: 'top'})
            .addTo(this.map);
          this.mapService.locationChange.subscribe(
            e => {
              const res = JSON.parse(e);
              console.log('Update position');
              marker.setLatLng([parseFloat(res.lat), parseFloat(res.long)]);
            }
          );
        }
    }

    if (this.trackorderService.getShowWarehouses()) {
      this.showWarehouses();
    }
  }

  showWarehouses() {
    this.mapService.getWarehouses().subscribe( data => {
      console.log(data);
      data['warehouse'].forEach(w => {
        const marker = new L.marker([w.latitude, w.longitude], {icon: this.warehouseIcon})
          .bindTooltip(w.name, {permanent: false, direction: 'top'})
          .addTo(this.map);
        this.warehouses.push(marker);
      });
    });
  }

  hideWarehouses() {
    this.warehouses.forEach( warehouse => {
      this.map.removeLayer(warehouse);
    });
  }

  showDronePath(droneId, destLat, destLong) {
    if (this.dronePath !== undefined) {
      this.map.removeLayer(this.dronePath);
    }
    this.mapService.findPath(destLat, destLong).subscribe(d => {
      const srcLat = d['lat'];
      const srcLong = d['long']
      this.mapService.tomtom(destLat, destLong, srcLat, srcLong).subscribe((data) => {
        console.log(data);
        const points = data['routes'][0].legs[0].points;
        const wayPoints = new Array();
        for(let i = 0; i < points.length; ++i) {
          wayPoints.push(L.latLng(points[i].latitude, points[i].longitude));
        }
        if (this.dronePath !== undefined) {
          this.dronePath.remove();
        }
        this.dronePath = L.polyline(wayPoints, {
          color: 'red',
          weight: 3
        }).addTo(this.map);
      });
    });
  }
}
