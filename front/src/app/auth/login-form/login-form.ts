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
import { OAuth2PasswordRequestForm } from '../../../models/interfaces/auth';


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
  selector: 'app-login-form',
  styleUrl: './login-form.css',
  templateUrl: './login-form.html',
  providers: [MessageService]
})
export class LoginForm {
  mask : boolean = true;
  private messageService = inject(MessageService);
  private router = inject(Router);


  constructor(
    private authService: AuthService,
  ){}

  loginModel = signal<OAuth2PasswordRequestForm>({
    username : '',
    password : '',
  });

  loginForm = form(this.loginModel,
    (schemaPath) => {
      required(schemaPath.username, {message: 'Email is required'});
      email(schemaPath.username, {message: 'Enter a valid email address'});
      required(schemaPath.password, {message: 'Password is required'});
      maxLength(schemaPath.password, 20, {message: 'Password is too long'});
      minLength(schemaPath.password, 8, {message: 'Password is too short'});
    }
  );


  public login(){
      this.messageService.add({
          severity: 'secondary',
          summary: 'Please wait...',
          detail: 'Verifying credentials.',
          icon: 'pi pi-spinner pi-spin',
          key: 'promise',
          sticky: true
      });

      this.authService.getToken(
        this.loginModel()
      )
        .subscribe({

          next:(data)=>{
            this.messageService.clear('promise');
            // a toast
            if(data.status_code == 200){
              this.messageService.add({ severity: 'success', summary: 'Saved successfully', detail: data.detail });
              this.authService.saveToken(data.access_token)
              // redirect
              this.router.navigate(['/home/employees']);
            }
            else{
              this.messageService.add({ severity: 'error', summary: 'Something went wrong', detail: data.detail });
            }
            console.log(data)
          },
          error:(err)=>{
            console.log(err)
            this.messageService.clear('promise');

            if(err.error.detail){
              this.messageService.add({ severity: 'error', summary: 'Something went wrong', detail: err.error.detail });
            }
            else
              this.messageService.add({ severity: 'error', summary: 'Something went wrong', detail: "We couldn’t complete the action." });
          },
      })
  }
}

