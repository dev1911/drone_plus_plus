import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {LoginService} from '../login/login.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  authenticated: boolean ;
  user: string;
  constructor(private router: Router, private loginService: LoginService) {}

  ngOnInit() {
    if (localStorage.getItem('user-token') != null) {
      this.authenticated = this.loginService.isLoggedIn();
      if (this.authenticated) {
        this.user = this.loginService.getUserInfo();
      }
    }
  }
  logout() {
    localStorage.removeItem('user-token');
    this.router.navigate(['']);
  }
}
