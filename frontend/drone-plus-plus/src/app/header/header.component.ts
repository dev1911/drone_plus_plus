import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  userPresent: boolean ;
  user = String;
  constructor(private router: Router) {}

  ngOnInit() {
    if (localStorage.getItem('user-token') != null){
      this.userPresent = true;
    }
  }
  logout() {
    localStorage.removeItem('user-token');
    this.router.navigate(['']);
  }
}
