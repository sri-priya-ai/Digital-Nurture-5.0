import { Component, Input } from "@angular/core";

@Component({
selector: "app-course-card",
standalone: true,
template: `
<article class="course-card">
<h3>{{ title }}</h3>
<p>{{ tag }}</p>
<span>{{ units }} credits</span>
</article>
`
})
export class CourseCardComponent {
@Input() title = "";
@Input() tag = "";
@Input() units = 0;
}
