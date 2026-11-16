import { Routes } from '@angular/router';
import { Layout } from './layout/layout';
import { Test } from './test/test';
import { Notfound } from './not-found/not-found'
import { Employees } from './employee/employees/employees';
import { LoginForm } from './login-form/login-form';

export const routes: Routes = [
    {
    // path: 'team/:id',
    path:'xyz',
    component: Test,
    },
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
            return token ? '/home/employees' : '/auth/login';
        }, 
        pathMatch: 'full' 
    },
    //   {path: users/:id', component: UserDetail}, // Dynamic


    {path: 'home', component: Layout, 
        children: [
            {path: 'employees', component: Employees},
        ]
    },
    // {path: 'login', component: Layout, 
    //     children: [
    //         {path: 'employees', component: Employees},
    //     ]
    // },

    {path: 'auth/login', component: LoginForm},
    // {path: 'employees', component: Employees,     canMatch: [authGuard]},
    {path: '', component: Test},  // provide sth otherwise it goes to 404
    {path: '**', component: Notfound},  // should be last
    // {path: '', redirectTo: '/heroes-list', pathMatch: 'full'},
];
