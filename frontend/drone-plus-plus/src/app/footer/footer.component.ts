import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.css']
})
export class FooterComponent implements OnInit {

  email: string;

  constructor() { }

  sub(){
    console.log(this.email);
  }

  ngOnInit() {
  }

}
