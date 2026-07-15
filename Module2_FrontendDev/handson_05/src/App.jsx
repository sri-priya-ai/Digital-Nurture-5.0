import { useState, useEffect } from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";
import CourseCard from "./components/CourseCard";
import StudentProfile from "./components/StudentProfile";

export default function App() {
const [courses, setCourses] = useState([]);
const [query, setQuery] = useState("");
const [enrolled, setEnrolled] = useState([]);
const [busy, setBusy] = useState(true);
const [errMsg, setErrMsg] = useState("");

useEffect(() => {
fetch("https://jsonplaceholder.typicode.com/posts?_limit=5")
.then(res => res.json())
.then(data => {
setCourses(data.map((p, i) => ({ id: p.id, name: p.title.slice(0, 20), code: `CS10${i}`, credits: 3 + (i % 2), grade: "A" })));
setBusy(false);
})
.catch(() => {
setErrMsg("Failed to load courses");
setBusy(false);
});
}, []);

useEffect(() => {
console.log("Courses updated");
}, [courses]);

const visibleCourses = courses.filter(c => c.name.toLowerCase().includes(query.toLowerCase()));

const handleEnroll = course => {
setEnrolled(prev => [...prev, course]);
};

return (
<>
<Header siteName="Campus Hub" enrolledCount={enrolled.length} />
<main>
<input placeholder="Search..." value={query} onChange={e => setQuery(e.target.value)} />
{busy && <p>Loading...</p>}
{errMsg && <p>{errMsg}</p>}
<div className="course-grid">
{visibleCourses.map(c => (
<CourseCard key={c.id} {...c} onEnroll={() => handleEnroll(c)} />
))}
</div>
<StudentProfile />
</main>
<Footer />
</>
);
}
