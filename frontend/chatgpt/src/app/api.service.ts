import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable, tap} from "rxjs";
import {Chat} from "./models/chat.model";
import {AuthToken} from "./models/token";
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  BASE_URL = 'http://localhost:8000';
  httpHeaders = new HttpHeaders({ 'Content-Type': 'application/json' });

  constructor(private http: HttpClient, private cookieService: CookieService) { }

  getAllChats(): Observable<Chat[]> {
    return this.http.get<Chat[]>(this.BASE_URL+'/api/chatgpt/chats');
  }

  login(username: string, password: string): Observable<AuthToken> {
    return this.http.post<AuthToken>(this.BASE_URL+'/api/authorization/login/', { username, password }).pipe(
      tap((authToken: AuthToken) => {
        // Store token in cookie
        this.cookieService.set('authToken', JSON.stringify(authToken));
      })
    );
  }

  logout(): void {
    // Remove token from local storage or session storage
    localStorage.removeItem('authToken');
  }

  getToken(): string | null {
    // Retrieve token from local storage or session storage
    const authTokenString = localStorage.getItem('authToken');
    if (authTokenString) {
      const authToken: AuthToken = JSON.parse(authTokenString);
      return authToken.token;
    }
    return null;
  }

  isLoggedIn(): boolean {
    // Check if token exists in local storage or session storage
    return !!this.getToken();
  }
}
