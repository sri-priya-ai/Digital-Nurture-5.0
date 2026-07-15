import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { CourseCardComponent } from "./course-card.component";
import { CourseService } from "./course.service";

@Component({
selector: "app-course-list",
standalone: true,
imports: [CommonModule, FormsModule, CourseCardComponent],
template: `
<input [(ngModel)]="term" placeholder="Search...">
<p *ngIf="busy">Loading...</p>
<div *ngIf="!filtered().length && !busy">No courses found</div>
<app-course-card *ngFor="let c of filtered()" [title]="c.name" [tag]="c.code" [units]="c.credits"></app-course-card>
`
})
export class CourseListComponent implements OnInit {
list: any[] = [];
term = "";
busy = true;

constructor(private courseService: CourseService) {}

ngOnInit() {
this.courseService.fetchCourses().subscribe(data => {
this.list = data.map((p: any, i: number) => ({ name: p.title.slice(0, 20), code: `CS10${i}`, credits: 3 + (i % 2) }));
this.busy = false;
});
}

filtered() {
return this.list.filter(c => c.name.toLowerCase().includes(this.term.toLowerCase()));
}
}
