import { Component } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { RouterModule } from '@angular/router';



@Component({
  imports: [
    RouterModule,
    ButtonModule,
  ],
  selector: 'app-access-denied',
  styleUrl: './access-denied.css',
  templateUrl: './access-denied.html',
})
export class AccessDenied {}
