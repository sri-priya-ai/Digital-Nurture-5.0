export default function CourseCard({ name, code, credits, grade, onEnroll }) {
return (
<article className="course-card">
<h3>{name}</h3>
<p>{code}</p>
<span>{credits} credits</span>
<p>Grade: {grade}</p>
<button onClick={onEnroll}>Enroll</button>
</article>
);
}
