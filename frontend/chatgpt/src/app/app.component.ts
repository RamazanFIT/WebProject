import { Component } from '@angular/core';
import {ApiService} from "./api.service";
// import {AppComponent} from './app.component';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  providers: [ApiService],
})
export class AppComponent {
  movies = [{name:'test'}, {name:'test2'}];

  constructor(private api: ApiService) {
    this.getChats();
  }

  getChats = ()=>{
    this.api.getAllChats().subscribe(
      data => {
        this.movies = data;
      }, error => console.log(error)
    )
  }
}
