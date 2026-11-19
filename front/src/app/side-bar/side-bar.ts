import { Component, inject, signal } from '@angular/core';
import { SidebarModule } from 'primeng/sidebar';
import { ThLarge, Users, Briefcase } from '@primeicons/angular';
import { ActivatedRoute, isActive, Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { TooltipModule } from 'primeng/tooltip';
import { ButtonDirective } from 'primeng/button';

@Component({
  imports: [
  RouterLinkActive,
    TooltipModule,
    ThLarge,
    Briefcase,
    Users,
    SidebarModule,
    RouterLink,
    ButtonDirective,
    RouterOutlet
],
  selector: 'app-side-bar',
  styleUrl: './side-bar.css',
  templateUrl: './side-bar.html',
})
export class SideBar {
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  activeRoute = signal<any[]>([]);

  constructor(){
    const snapshot = this.route.snapshot;
    this.activeRoute.set(snapshot.url)
    // console.log(this.activeRoute())
  }
  isDashboardActive = isActive('/home/dashboard',this.router)
  isCustomersActive = isActive('/home/customers',this.router)
  isEmployeesActive = isActive('/home/employees',this.router)
  isactive(path:string){
    console.log(this.isDashboardActive())
     return isActive(path,this.router)()
  }

  isSettingsActive = isActive('/settings', this.router, {
    paths: 'subset',
    queryParams: 'ignored',
    fragment: 'ignored',
    matrixParams: 'ignored',
  });

  sidebardt = {
    menuButton: {
      icon: {
        size: 40,
      }
    },
  }

}
