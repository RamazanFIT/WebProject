import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable, tap} from "rxjs";
import {Chat} from "./models/chat.model";
import {AuthToken} from "./models/token";
// @ts-ignore
import { CookieService } from 'ngx-cookie-service';
@Injectable({
  providedIn: 'root'
})
export class ApiService {

  BASE_URL = 'http://localhost:8000';
  httpHeaders = new HttpHeaders({ 'Content-Type': 'application/json' });

  constructor(private http: HttpClient, private cookieService: CookieService) { }

  getAllChats(): Observable<Chat[]> {
    const jwtToken = this.getJwtFromCookie(); // Получаем JWT токен из куки
    const headers = new HttpHeaders()
      .set('X-CSRFToken', 'J9CVAv52vGrMojuKpJxoTAkHkT6OyxiTZFboFWkxg0oqANlbLWetYGcqWiGV9YUs')
      .set('Cookie', `jwt=${jwtToken}`); // Устанавливаем куки с JWT токеном в заголовки запроса

    return this.http.get<Chat[]>(`${this.BASE_URL}/api/chatgpt/chats/`, { headers });
  }

  private getJwtFromCookie(): string {
    const jwtToken = this.getCookie('jwt');
    return jwtToken ? jwtToken : '';
  }


  private getCookie(name: string): string {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop()!.split('=')[1] : '';
  }


  login(username: string, password: string): Observable<any> {
    const headers = new HttpHeaders()
      .set('Content-Type', 'application/json')
      .set('X-CSRFToken', 'J9CVAv52vGrMojuKpJxoTAkHkT6OyxiTZFboFWkxg0oqANlbLWetYGcqWiGV9YUs');

    const body = {
      username: username,
      password: password
    };

    return this.http.post<any>(
      `${this.BASE_URL}/api/authorization/login/`,
      body,
      { headers: headers, withCredentials: true }
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
