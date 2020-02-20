import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  pass: string;
  username: string;
  subError: string;
  constructor() { }

  ngOnInit() {
  }

  sub(username, pass) {
    // TODO: call API for login and set token in local storage/cookies
    console.log(username, pass);
  }


}
