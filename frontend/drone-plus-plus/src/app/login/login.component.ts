import { Component, OnInit } from '@angular/core';
import { LoginService } from './login.service';
import {Router} from '@angular/router';
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
  constructor(private loginService: LoginService, private router: Router) { }

  ngOnInit() {
    if (this.loginService.isLoggedIn()) {
      this.router.navigate(['']);
    }
    this.login = {username: '', password: ''};
  }

  loginUser() {
    this.loginService.loginNewUser(this.login).subscribe(data => {
      console.log('success');
      localStorage.setItem('user-token', data['token']);
      this.subError = '';
      this.router.navigate(['']);
      window.location.reload();
    },
    error => {
      console.log('error', error);
      this.subError = 'Invalid Credentials. Please try again!';
    }
    );
  }
  logout() {
    localStorage.removeItem('user-token');
  }

}
