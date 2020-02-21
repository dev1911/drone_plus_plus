import { Component, OnInit } from '@angular/core';
import { LoginService } from './login.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  login;
  // password: string;
  // username: string;
  subError: string;
  providers: [LoginService];
  constructor(private loginService: LoginService) { }

  ngOnInit() {
    this.login = {username: '', password: ''};
  }

  loginUser() {
    this.loginService.loginNewUser(this.login).subscribe(
      response => {
        alert('User ' + this.login.username + ' has been logged!' );
      },
      error => console.log('error', error)
    );
    // TODO: set token in local storage/cookies
  }

}
