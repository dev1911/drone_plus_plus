import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  pass: string;
  pass2: string;
  username: string;
  subError: string;
  constructor() { }

  ngOnInit() {
  }

  sub(username, pass, pass2) {
    // TODO: call API for register and set token in local storage/cookies
    console.log(username, pass, pass2);
  }

}
