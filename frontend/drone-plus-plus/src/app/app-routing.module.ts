import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {LoginComponent} from './login/login.component';
import {RegisterComponent} from './register/register.component';
import {NeworderComponent} from './neworder/neworder.component';
import {TrackorderComponent} from './trackorder/trackorder.component';
import {AuthGuardService} from './login/auth-guard.service';
import {HomeComponent} from './home/home.component';

const routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'login', component: LoginComponent},
  {path: 'register', component: RegisterComponent},
  {path: 'order/new', component: NeworderComponent, canActivate: [AuthGuardService]},
  {path: 'order/track', component: TrackorderComponent, canActivate: [AuthGuardService]}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
