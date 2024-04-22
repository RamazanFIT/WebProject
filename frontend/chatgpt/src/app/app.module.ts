import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import {ChatComponent} from "./components/chat/chat.component";
import {LoginComponent} from "./components/login/login.component";
import {FormsModule} from "@angular/forms";
import {CommonModule, NgOptimizedImage} from "@angular/common";
import {MainComponent} from "./components/main/main.component";

@NgModule({
  declarations: [
    AppComponent,
    ChatComponent,
    LoginComponent,
    MainComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    NgOptimizedImage,
    CommonModule,

  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
