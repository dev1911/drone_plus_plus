import { Injectable } from '@angular/core';
import {LoginService} from './login.service';
import {CanActivate, Router} from '@angular/router';
import {error} from 'util';

@Injectable({
  providedIn: 'root'
})
export class AuthGuardService implements CanActivate {

  constructor(private loginService: LoginService, private router: Router) { }
  canActivate(): boolean {
    if (this.loginService.isLoggedIn()) {
      return true;
    }
    this.router.navigate(['login']).then(
      val => {
        // console.log(val);
      },
      e => {
        // console.log(e);
      }
    );
    return false;
  }
}
