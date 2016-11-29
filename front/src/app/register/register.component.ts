import { Component, OnInit } from '@angular/core';

import { IUser} from '../user'

import {UserService} from '../user.service'

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  errorMessage : string;
  user : IUser[];
  constructor(public _userService: UserService ) { 
  }
 
   ngOnInit(): void{
      this._userService.registerUser().
      subscribe(user => this.user = user, 
      error => this.errorMessage = <any>error );
    }
}
 

