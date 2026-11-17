import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { CheckboxModule } from 'primeng/checkbox';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { RippleModule } from 'primeng/ripple';
import { pattern, minLength, maxLength, email, form, FormField, required, minDate, maxDate, validate } from '@angular/forms/signals';
import { InputPasswordModule } from 'primeng/inputpassword';
import { Eye } from '@primeicons/angular/eye';
import { EyeSlash } from '@primeicons/angular/eye-slash';
import { IconFieldModule } from 'primeng/iconfield';
import { InputIconModule } from 'primeng/inputicon';
import { MessageService } from 'primeng/api';
import { MessageModule } from 'primeng/message';
import { Spinner } from '@primeicons/angular/spinner';
import { ToastModule } from 'primeng/toast';
import {Router} from '@angular/router';
import { AuthService } from '../../services/auth_service/auth-service';
import { ForgetPasswordEntry, OAuth2PasswordRequestForm } from '../../../models/interfaces/auth';

@Component({
  imports: [
    ToastModule,
    MessageModule,
    Eye,
    EyeSlash,
    IconFieldModule,
    InputIconModule,
    InputPasswordModule,
    FormField,
    ButtonModule, CheckboxModule, InputTextModule, PasswordModule, FormsModule, RouterModule, RippleModule],
  selector: 'app-forget-pswd',
  styleUrl: './forget-pswd.css',
  templateUrl: './forget-pswd.html',
  providers: [MessageService]
})
export class ForgetPswd {

  private messageService = inject(MessageService);
  private router = inject(Router);

  constructor(
    private authService: AuthService,
  ){}

  forgetPswdModel = signal<ForgetPasswordEntry>({
    email : '',
  });

  forgetPswdForm = form(this.forgetPswdModel,
    (schemaPath) => {
      required(schemaPath.email, {message: 'Email is required'});
      email(schemaPath.email, {message: 'Enter a valid email address'});
    }
  );

  public forgetPswd(){

    this.messageService.add({
        severity: 'secondary',
        summary: 'Please wait...',
        detail: 'Sending reset password email.',
        icon: 'pi pi-spinner pi-spin',
        key: 'promise',
        sticky: true
    });

    this.authService.sendForgetPswdEmail(this.forgetPswdModel())
      .subscribe({
        next:(data)=>{
          this.messageService.clear('promise');

          if(data.status_code == 200){
            this.messageService.add({ severity: 'success', summary: 'Saved successfully', detail: data.detail });
            // redirect
            // this.router.navigate(['/home/employees']);
          }
          else{
            this.messageService.add({ severity: 'error', summary: 'Something went wrong', detail: data.detail });
          }
        },
        error:(err)=>{
          this.messageService.clear('promise');
          console.log(err)
          if(err.name=="HttpErrorResponse"){
            this.messageService.add({ severity: 'error', summary: 'Something went wrong', detail: err.statusText });
          }
          else if(err.error.detail){
            this.messageService.add({ severity: 'error', summary: 'Something went wrong', detail: err.error.detail });
          }
          else
            this.messageService.add({ severity: 'error', summary: 'Something went wrong', detail: "We couldn’t complete the action." });

        }
      })
  }


  // public login(){
  //     this.messageService.add({
  //         severity: 'secondary',
  //         summary: 'Please wait...',
  //         detail: 'Verifying credentials.',
  //         icon: 'pi pi-spinner pi-spin',
  //         key: 'promise',
  //         sticky: true
  //     });

  //     this.authService.getToken(
  //       this.loginModel()
  //     )
  //       .subscribe({

  //         next:(data)=>{
  //           this.messageService.clear('promise');
  //           // a toast
  //           console.log(data)
  //         },
  //         error:(err)=>{
  //           console.log(err)
  //     })
  // }
}

