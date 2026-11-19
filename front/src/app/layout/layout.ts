// import { Component, inject, OnInit, signal } from '@angular/core';
// import { SidebarModule } from 'primeng/sidebar';
// import { ButtonModule } from 'primeng/button';
// import { MenubarModule } from 'primeng/menubar';
// import { SignOut } from '@primeicons/angular/sign-out';
// import { Bars } from '@primeicons/angular/bars';
// import { MenuModule } from 'primeng/menu';
// import { MenuItem } from 'primeng/api';
// import { RouterLink, RouterOutlet } from '@angular/router';
// import { Moon } from '@primeicons/angular/moon';
// import { Sun } from '@primeicons/angular/sun';
// import {ActivatedRoute} from '@angular/router';
// import { Dollar } from '@primeicons/angular/dollar';


// @Component({
//   imports: [
//     Dollar,
//     SidebarModule,
//     MenuModule,
//     ButtonModule,
//     MenubarModule,
//     SignOut,
//     Bars,
//     RouterLink,
//     RouterOutlet,
//     Moon,
//     Sun,
// ],
//   selector: 'app-layout',
//   styleUrl: './layout.css',
//   templateUrl: './layout.html',
// })
// export class Layout implements OnInit{
//   items: MenuItem[] | undefined;
//   isDarkMode: boolean = false;

//   constructor(){
//     // to do : make this gets the info from the system | from cashe or whatever
//     this.isDarkMode=false;
//   }

//   ngOnInit() {

//     this.items = [
//         // {
//         //     separator: true
//         // },
//         {
//             label: 'Dashboard',
//             icon: 'pi pi-th-large',
//             routerLink: '/home/dashboard',
//             command: () => {
//                 // this.update();
//             }
//         },
//         {
//             label: 'Customers',
//             icon: 'pi pi-users',
//             routerLink: '/home/customers',
//         },
//         {
//             label: 'Employees',
//             icon: 'pi pi-briefcase',
//             routerLink: '/home/employees',
//         },
//     ];
//   }


// // sidebar.menuButton.icon.size
//   sidebardt = {
//         menuButton: {
//           icon: {
//             size: 32,
//             color: "blue",
//           }
//         },
//     main: {
//       margin: 0,
//       // background: 'blue',
//     },
//     aside: {
//       padding: "none",
//     }
//   }
//   menubardt = {
//     root:{
//       borderColor:'none',
//       borderRadius:'none'
//     }
//   }
//   sideBarMenudt = {
//     root: {
//       borderColor: 'none',
//     },
//     item: {
//       icon: {
//         size: "100px",
//         color: "blue",
//       }
//     }
//   }


//   toggleDarkMode() {
//       const element = document.querySelector('html');
//       if(element)this.isDarkMode = !element.classList.contains('my-app-dark');
//       // toggle : adds if missing, remove if present
//       if(element)element.classList.toggle('my-app-dark');
//       // <html may-app-dark>
//   }
// }



import { Component, OnInit, signal } from '@angular/core';
import { AvatarModule } from 'primeng/avatar';
import { MenuModule } from 'primeng/menu';
import { SidebarModule } from 'primeng/sidebar';
import { ButtonModule } from 'primeng/button';
import { MenuItem } from 'primeng/api';
import { ChevronDown } from '@primeicons/angular/chevron-down';
import { Check } from '@primeicons/angular/check';
import { Home } from '@primeicons/angular/home';
import { Inbox } from '@primeicons/angular/inbox';
import { Search } from '@primeicons/angular/search';
import { Users } from '@primeicons/angular/users';
import { Bell } from '@primeicons/angular/bell';
import { Sidebar } from '@primeicons/angular/sidebar';

interface Company {
    name: string;
    logo: string;
    color: string;
}

@Component({

  selector: 'app-layout',
  styleUrl: './layout.css',
  templateUrl: './layout.html',
  imports: [AvatarModule, MenuModule, SidebarModule, ButtonModule, ChevronDown, Check, Home, Inbox, Search, Users, Bell, Sidebar]
})
export class Layout implements OnInit {
    isMobile = signal(false);

    open = signal(false);

    private mql?: MediaQueryList;

    private mqlListener?: (e: MediaQueryListEvent) => void;

    companies: Company[] = [
        { name: 'Acme Inc', logo: 'A', color: 'from-violet-500 to-indigo-600' },
        { name: 'Globex Corp', logo: 'G', color: 'from-emerald-500 to-teal-600' },
        { name: 'Initech', logo: 'I', color: 'from-orange-500 to-red-600' }
    ];

    activeCompany = this.companies[0];

    companyItems: MenuItem[] = [
        {
            label: 'Companies',
            items: [
                ...this.companies.map((c: any) => ({
                    label: c.name,
                    logo: c.logo,
                    color: c.color,
                    active: this.activeCompany.name === c.name,
                    command: () => {
                        this.activeCompany = c;
                        this.updateCompanyActive();
                    }
                })),
                { separator: true },
                { label: 'Add company', icon: 'pi pi-plus' }
            ]
        }
    ];

    userItems: MenuItem[] = [
        {
            label: 'john@acme.com',
            items: [{ label: 'Settings', icon: 'pi pi-cog' }, { label: 'Notifications', icon: 'pi pi-bell' }, { separator: true }, { label: 'Sign out', icon: 'pi pi-sign-out' }]
        }
    ];

    ngOnInit() {
        if (typeof window === 'undefined') return;
        this.mql = window.matchMedia('(max-width: 1023px)');
        this.isMobile.set(this.mql.matches);
        // this.open.set(!this.mql.matches);
        this.mqlListener = (e) => {
            this.isMobile.set(e.matches);
            this.open.set(!e.matches);
        };
        this.mql.addEventListener('change', this.mqlListener);
    }

    ngOnDestroy() {
        this.mql?.removeEventListener('change', this.mqlListener!);
    }

    updateCompanyActive(): void {
        const items = (this.companyItems[0] as any).items;
        
        items.forEach((item: any) => {
            if (item.logo) {
                item.active = this.activeCompany.name === item.label;
            }
        });
    }
}