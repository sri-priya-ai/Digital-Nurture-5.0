import { Component } from "@angular/core";
import { ReactiveFormsModule, FormGroup, FormControl, Validators } from "@angular/forms";

@Component({
selector: "app-student-profile",
standalone: true,
imports: [ReactiveFormsModule],
template: `
<form [formGroup]="profileForm">
<input formControlName="name" placeholder="Name">
<span *ngIf="profileForm.get('name')?.invalid && profileForm.get('name')?.touched">Name is required</span>
<input formControlName="email" placeholder="Email">
<span *ngIf="profileForm.get('email')?.invalid && profileForm.get('email')?.touched">Enter a valid email</span>
<input formControlName="semester" placeholder="Semester">
<button [disabled]="profileForm.invalid" (click)="submit()">Submit</button>
</form>
`
})
export class StudentProfileComponent {
profileForm = new FormGroup({
name: new FormControl("", Validators.required),
email: new FormControl("", [Validators.required, Validators.email]),
semester: new FormControl("", [Validators.required, Validators.min(1), Validators.max(8)])
});

submit() {
console.log(this.profileForm.value);
}
}
