import {Injectable} from '@angular/core';
import {map} from 'rxjs/operators';
import {Observable} from 'rxjs';
import {HttpRequest, HttpHandler, HttpEvent, HttpInterceptor, HttpResponse, HttpErrorResponse} from '@angular/common/http';

@Injectable()
export class AuthInterceptor implements  HttpInterceptor {
  constructor() {
  }
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token: string = localStorage.getItem('user-token');
    if (token) {
      req = req.clone({headers: req.headers.set('Authorization', `Token ${token}`)});
    }
    if (!req.headers.has('Content-Type')) {
      req = req.clone({headers: req.headers.set('Content-Type', 'application/json')});
    }
    req = req.clone({headers: req.headers.set('Accept', '*/*')});
    console.log('Apple', req);
    return next.handle(req).pipe(
      map((event: HttpEvent<any>) => {
        console.log(event);
        if(event instanceof  HttpResponse) {
          console.log(event);
        }
        return event;
      }),
    );
  }
}
