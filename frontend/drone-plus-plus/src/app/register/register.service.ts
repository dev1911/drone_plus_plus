import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class RegisterService {

  constructor(private http: HttpClient) { }
  registerNewUser(userData): Observable<any> {
    return this.http.post('http://127.0.0.1:8000/accounts/register/', userData); }
}
