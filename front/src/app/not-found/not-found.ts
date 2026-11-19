import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { RippleModule } from 'primeng/ripple';

@Component({
    selector: 'app-notfound',
    standalone: true,
    imports: [
        RouterModule, 
        ButtonModule,
        RippleModule,
    ],
    styleUrl: './not-found.css',
    templateUrl: './not-found.html',
})
export class Notfound {}
