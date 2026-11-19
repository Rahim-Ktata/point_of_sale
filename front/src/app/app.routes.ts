import { Routes } from '@angular/router';
import { Notfound } from './not-found/not-found'
import { Employees } from './employee/employees/employees';
import { LoginForm } from './auth/login-form/login-form';
import { ForgetPswd } from './auth/forget-pswd/forget-pswd';
import { ResetPswd } from './auth/reset-pswd/reset-pswd';
import { ActivateAccount } from './auth/activate-account/activate-account';
import { adminGuard } from './guards/admin-guard';
import { AccessDenied } from './auth/access-denied/access-denied';
import { Dashboard } from './dashboard/dashboard';
import { Customers } from './customers/customers';
import { Layout } from './layout/layout';
import { SideBar } from './side-bar/side-bar';


export const routes: Routes = [
    // {
    // // path: 'team/:id',
    // path:'xyz',
    // },
    // {
    // // path: 'team/:id',
    // path:'',
    // component: Layout,
    // children: [{
    //     // path: 'user/:name',
    //     path: 'x',
    //     component: Test 
    // }]
    // }
    { 
        path: '', 
        redirectTo: () => {
             const token = localStorage.getItem('token');
            console.log(token);
            return token ? '/home/dashboard' : '/auth/login';
        }, 
        pathMatch: 'full' 
    },
    //   {path: users/:id', component: UserDetail}, // Dynamic


    {path: 'auth/login', component: LoginForm},
    {path: 'auth/forget_pswd', component: ForgetPswd},
    {path: 'auth/reset_pswd', component: ResetPswd},
    {path: 'auth/activate_account', component: ActivateAccount},
    {path: 'auth/access', component: AccessDenied},

    {path: 'side_bar', component: SideBar},

    {path: 'home', component: SideBar, 
        children: [
            {path: 'employees', component: Employees, canActivate:[adminGuard]},
            {path: 'dashboard', component: Dashboard},
            {path: 'customers', component: Customers},
        ]
    },
    // {path: 'login', component: Layout, 
    //     children: [
    //         {path: 'employees', component: Employees},
    //     ]
    // },

    // {path: 'employees', component: Employees,     canMatch: [authGuard]},
    // {path: '', component: },  // provide sth otherwise it goes to 404
    {path: '**', component: Notfound},  // should be last
    // {path: '', redirectTo: '/heroes-list', pathMatch: 'full'},
];
