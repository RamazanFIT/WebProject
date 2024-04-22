// login.component.ts
import { Component } from '@angular/core';
import {ApiService} from "../../api.service";
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  errorMessage: string = '';

  constructor(private authService: ApiService, private cookieService: CookieService) {}


  login(): void {
    this.authService.login(this.username, this.password).subscribe(
      response => {
        const token = response.token;
        // Сохранение токена в куках
        this.cookieService.set('jwt', token);

        if (this.authService.isLoggedIn()) {
          console.log('Success');
          // Навигация на страницу dashboard или другую необходимую страницу после успешного входа
          // Пример: this.router.navigate(['/dashboard']);
        } else {
          console.error('User is not logged in after successful login');
        }
      },
      error => {
        this.errorMessage = 'Invalid username or password.';
        console.error('Login error:', error);
      }
    );
  }

}
