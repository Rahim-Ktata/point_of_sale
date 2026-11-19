import { HttpClient, HttpHeaders } from '@angular/common/http';
import { inject, Service, signal } from '@angular/core';
import { DeleteEmployeeResponse, EditEmployeeEntry, EditEmployeeOut, EmployeeCreate, EmployeePublic, EmployeeUploadResponse, GetAllEmployees, MatchyUploadEntry } from '../../../models/interfaces/employee';
import { back_base_url } from '../../utils';
import { AccountActivation, AccountActivationOut, ForgetPasswordEntry, ForgetPasswordOut, OAuth2PasswordRequestForm, ResetPasswordEntry, ResetPasswordOut, Token } from '../../../models/interfaces/auth';
import { Router } from '@angular/router';

@Service()
export class AuthService {

    private router = inject(Router);
    private http = inject(HttpClient);
    isAuthenticated = signal<boolean>(localStorage.getItem('token')?true:false);

//   getEmployees(skip:number, limit:number, filter: string){
//     // the <GetAllEmp> is useless, no verif or err, see Critical in docs
//     return this.http.get<GetAllEmployees>(back_base_url + 'employee/get_all_employees', 
//         {
//             params: {skip: skip, limit: limit, filter: filter},
//         }
//     );
//   }

//   editEmployee(id: number,data:EditEmployeeEntry){
//     return this.http.patch<EditEmployeeOut>(back_base_url + `employee/edit_employee/${id}`,data);
//   }
    // constructor(){
    //     this.updateAuthStauts();
    // }

    // isAuthenticated(){
    //     const token = localStorage.getItem('token');
    //     // if (token){this.isAuthenticated.set(true);}
    //     // else {this.isAuthenticated.set(false);}
    //     return token? true: false;
    // }
    getAuthToken(){
        const authToken = localStorage.getItem('token');
        if(!authToken) return '';
        else return authToken;
    }
    getToken(entry: OAuth2PasswordRequestForm){
        const formData = new FormData();
        formData.append('username', entry.username);
        formData.append('password', entry.password);

        const headers = new HttpHeaders({ 'enctype': 'multipart/form-data' });

        return this.http.post<Token>(back_base_url + "token", formData, {headers: headers})
    }
    saveToken(token:string){
        localStorage.setItem('token',token);
    }

    sendForgetPswdEmail(entry: ForgetPasswordEntry){
        return this.http.get<ForgetPasswordOut>(back_base_url + "forget_password", 
            {params:{
                email:entry.email
            }}
        )
    }

    resetPswd(entry: ResetPasswordEntry){
        return this.http.post<ResetPasswordOut>(back_base_url + "reset_password",entry)
    }

    activateAccount(entry: AccountActivation){
        return this.http.patch<AccountActivationOut>(back_base_url + "employee/confirm_account",entry)
    }

    hasRole(role:string){
        // return true;
        const payload = localStorage.getItem('token')?.split('.')[1];
        if(!payload){
            this.router.navigate(['/auth/login'])
            return false;
        }
        const payload_decoded = atob(payload)
        const payload_json = JSON.parse(payload_decoded);
        let roles;
        if(payload_json['roles'].includes(',')){
            roles = payload_json['roles'].split[','];
        }
        else{
            roles = payload_json['roles'];
        }
        if(!roles) {
            this.router.navigate(['/auth/login'])
            return false;
        }
        if(roles.includes(role)){
            return true;
        }
        else {
            this.router.navigate(['/auth/access'])
            return false;
        }
    }
}


// @Service()
// export class EmployeeService {
//   addEmployee(entry:EmployeeCreate){
//     return this.http.post<EmployeePublic>(back_base_url + 'employee/add_employee',entry)
//   }

//   deleteEmployee(id:number){
//     return this.http.delete<DeleteEmployeeResponse>(back_base_url + `employee/delete_employee/${id}`)
//   }

//   bulkUploadEmployees(entry:MatchyUploadEntry){
//     return this.http.post<EmployeeUploadResponse>(back_base_url + "employees_bulk_upload",entry)
//   }
// }

