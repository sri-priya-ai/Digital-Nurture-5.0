import { Routes } from "@angular/router";
import { CourseListComponent } from "./course-list.component";
import { StudentProfileComponent } from "./student-profile.component";

export const routes: Routes = [
{ path: "", component: CourseListComponent },
{ path: "profile", component: StudentProfileComponent }
];
