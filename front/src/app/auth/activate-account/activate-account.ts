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
import { AccountActivation, ResetPasswordEntry } from '../../../models/interfaces/auth';
import {ActivatedRoute} from '@angular/router';

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
  selector: 'app-activate-account',
  styleUrl: './activate-account.css',
  templateUrl: './activate-account.html',
  providers: [MessageService]
})
export class ActivateAccount {

  mask : boolean = true;
  private messageService = inject(MessageService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  constructor(
    private authService: AuthService,
  ){}

  ActivateAccountModel = signal<AccountActivation>({
    token: '',
    password : '', 
    confirm_password : ''
  });

  accountActivationForm = form(this.ActivateAccountModel,
    (schemaPath) => {
      required(schemaPath.password, {message: 'Field required'});
      required(schemaPath.confirm_password, {message: 'Field required'});
      maxLength(schemaPath.password, 20, {message: 'Password is too long'});
      minLength(schemaPath.password, 8, {message: 'Password is too short'});
      validate(schemaPath.confirm_password, ({value}) => {
        if (value() != this.ActivateAccountModel().password ) {
          return {
            kind: 'https',
            message: "Password doesn't match",
          };
        }
        return null;
      });
    }
  );

  public activateAccount(){
    this.messageService.add({
        severity: 'secondary',
        summary: 'Please wait...',
        detail: 'Verifying account.',
        icon: 'pi pi-spinner pi-spin',
        key: 'promise',
        sticky: true
    });

    const token = this.route.snapshot.queryParams['token'];
    if(token){
      this.ActivateAccountModel().token = token;
    }

    this.authService.activateAccount(
      this.ActivateAccountModel()
    )
      .subscribe({

        next:(data)=>{
          this.messageService.clear('promise');
          // a toast
          if(data.status_code == 200){
            // this.messageService.add({ severity: 'success', summary: 'Saved successfully', detail: data.detail });
            // redirect
            this.router.navigate(['/home/employees']);
          }
          else{
            this.messageService.add({ severity: 'error', summary: 'Something went wrong', detail: data.detail });
          }
        },
        error:(err)=>{
          this.messageService.clear('promise');

          if(err.error.detail){
            if(err.error.detail== "token expired"){
              this.messageService.add({ severity: 'error', summary: 'Something went wrong', detail: "The reset link expired please try again." });
            }
            else{
              this.messageService.add({ severity: 'error', summary: 'Something went wrong', detail: err.error.detail });
            }
          }
          else
            this.messageService.add({ severity: 'error', summary: 'Something went wrong', detail: "We couldn’t complete the action." });
        },
      })
  }

}

