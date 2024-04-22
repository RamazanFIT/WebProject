import { Component } from '@angular/core';
import {ApiService} from "../../api.service";
import {Chat} from "../../models/chat.model";
import { NgOptimizedImage } from '@angular/common'

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.css'
})
export class ChatComponent {
  chats: Chat[] = [];
  chatLabels: string = '';

  constructor(private chatService: ApiService) {}

  ngOnInit(): void {
    this.getChats();
  }

  getChats(): void {
    this.chatService.getAllChats().subscribe(
      chats => {
        this.chats = chats;
        if (Array.isArray(this.chats)) {
          this.chatLabels = this.chats.map(chat => chat.label).join(', ');
        }
        else {
          console.error('Chats data is not an array:', this.chats);

        }
      },
      error => {
        console.error('Error fetching chats:', error);
      }
    );
  }
}
