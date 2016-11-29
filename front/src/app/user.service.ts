import { Injectable } from "@angular/core";
import {Response, Http } from "@angular/http";
import { Observable } from "rxjs/Observable";
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/do';
import 'rxjs/add/operator/catch';

import  { IUser } from "./user";


@Injectable()
export class UserService{
    private _userUrl = 'http://127.0.0.1:8000/api/v1.0/auth/register/';
    constructor(private _http:Http){ }
    registerUser(): Observable<IUser[]>{
        return this._http.post(this._userUrl, '')
           .map((response: Response) => <IUser[]> response.json())
           .do(data=>console.log('Response ' + JSON .stringify(data))) 
           .catch(this.handleError);

}
    private handleError(error:Response){
        console.log(error);
        return Observable.throw(error.json().error || 'Server Error');
    }

}