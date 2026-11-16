import { Component, inject, OnInit, signal } from '@angular/core';
import { SidebarModule } from 'primeng/sidebar';
import { ButtonModule } from 'primeng/button';
import { MenubarModule } from 'primeng/menubar';
import { SignOut } from '@primeicons/angular/sign-out';
import { Bars } from '@primeicons/angular/bars';
import { MenuModule } from 'primeng/menu';
import { MenuItem } from 'primeng/api';
import { RouterLink, RouterOutlet } from '@angular/router';
import { Moon } from '@primeicons/angular/moon';
import { Sun } from '@primeicons/angular/sun';
import { AuthService } from '../services/auth_service/auth-service';
import {ActivatedRoute} from '@angular/router';


@Component({
  imports: [
    SidebarModule,
    MenuModule,
    ButtonModule,
    MenubarModule,
    SignOut,
    Bars,
    RouterLink,
    RouterOutlet,
    Moon,
    Sun,
],
  selector: 'app-layout',
  styleUrl: './layout.css',
  templateUrl: './layout.html',
})
export class Layout implements OnInit{
  items: MenuItem[] | undefined;
  isDarkMode: boolean = false;

  constructor(){
    // to do : make this gets the info from the system | from cashe or whatever
    this.isDarkMode=false;
  }

  ngOnInit() {

    this.items = [
        {
            separator: true
        },
        {
            label: 'Dashboard',
            icon: 'pi pi-th-large',
            routerLink: '/xyz',
            command: () => {
                // this.update();
            }
        },
        {
            label: 'Customers',
            icon: 'pi pi-users',

        },
        {
            label: 'Employees',
            icon: 'pi pi-briefcase',
            routerLink: '/employees',
        },
    ];
  }


// sidebar.menuButton.icon.size
  sidebardt = {
    menu: {
      menuButton: {
        icon: {
          size: 24,
          color: "blue",
        }
      }
    },
    main: {
      margin: 0,
      // background: 'blue',
    },
    aside: {
      padding: "none",
    }
  }
  menubardt = {
    root:{
      borderColor:'none',
      borderRadius:'none'
    }
  }
  sideBarMenudt = {
    root: {
      borderColor: 'none',
    },
    item: {
      icon: {
        size: "100px",
        color: "blue",
      }
    }
  }


  toggleDarkMode() {
      const element = document.querySelector('html');
      if(element)this.isDarkMode = !element.classList.contains('my-app-dark');
      // toggle : adds if missing, remove if present
      if(element)element.classList.toggle('my-app-dark');
      // <html may-app-dark>
  }
}