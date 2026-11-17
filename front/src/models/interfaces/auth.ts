

import { Response } from "./common"

export interface AccountActivation{
    token : string
    password : string
    confirm_password : string
}

export interface AccountActivationOut extends Response{}

export interface OAuth2PasswordRequestForm{
    username : string
    password : string
}

export interface Token extends Response{
    access_token: string
    token_type: string
}


export interface TokenData{
    email: string
}


export interface ForgetPasswordOut extends Response{}
export interface ForgetPasswordEntry {
    email: string
}

export interface ResetPasswordEntry{
    token : string
    password : string
    confirm_password : string
}

export interface ResetPasswordOut extends Response{}