import {Component, ElementRef, EventEmitter, Input, OnInit, Output, ViewChild} from '@angular/core';


@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {

  @ViewChild('sidebar', {static: true}) sidebar: ElementRef;
  @Output() track = new EventEmitter();
  constructor() { }

  @Input() orders: object;

  ngOnInit() {
  }
  trackOrder(droneId: number) {
    this.track.emit(droneId);
  }

}
