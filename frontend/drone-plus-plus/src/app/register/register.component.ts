import { Component, OnInit } from '@angular/core';
import { RegisterService } from './register.service';
// import { userInfo } from 'os';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  register;
  // password: string;
  // password2: string;
  // username: string;
  subError: string;
  providers: [RegisterService];
  constructor(private registerService: RegisterService) { }

  ngOnInit() {
    this.register = {username: '', password: '', password2: '', token: '',};

  }

  registerUser() {
    this.registerService.registerNewUser(this.register).subscribe(
      response => {
        alert('User ' + this.register.username + ' has been created!' );
        alert('Token' + this.register.token);
        // if (response && response.token) {
        //   localStorage.setItem('token', response.token);
        //   console.log("idhar aya");
        //   console.log(response.token);
        //  }
      },
      error => alert('error ' + error)
    );
    // TODO: set token in local storage/cookies
  }

}
