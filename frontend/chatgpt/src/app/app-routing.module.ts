import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {ChatComponent} from "./components/chat/chat.component";
import {LoginComponent} from "./components/login/login.component";
import {MainComponent} from "./components/main/main.component";

const routes: Routes = [
  {path: 'chat', component: ChatComponent},
  {path: 'login', component: LoginComponent},
  {path: 'main', component: MainComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
