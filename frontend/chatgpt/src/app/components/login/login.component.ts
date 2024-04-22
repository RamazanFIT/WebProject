// login.component.ts
import { Component } from '@angular/core';
import {ApiService} from "../../api.service";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  errorMessage: string = '';

  constructor(private authService: ApiService) {}

  login(): void {
    this.authService.login(this.username, this.password).subscribe(
      () => {
        if (this.authService.isLoggedIn()) {
          console.log('Success')
        } else {
          // Handle the case where the user is not logged in (unlikely after successful login)
          console.error('User is not logged in after successful login');
        }
        // Navigate to dashboard or desired route after successful login
        // Example: this.router.navigate(['/dashboard']);
      },
      error => {
        this.errorMessage = 'Invalid username or password.';
        console.error('Login error:', error);
      }
    );
  }
}
