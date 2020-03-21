import {Component, ElementRef, Input, OnInit, ViewChild} from '@angular/core';


@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {

  @ViewChild('sidebar', {static: true}) sidebar: ElementRef;
  constructor() { }

  @Input() orders: object;

  ngOnInit() {

  }

}
