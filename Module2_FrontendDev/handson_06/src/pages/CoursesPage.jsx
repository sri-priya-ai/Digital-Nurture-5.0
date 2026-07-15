import { Link } from "react-router-dom";
import { useDispatch } from "react-redux";
import { enroll } from "../redux/enrollSlice";

const list = [
{ id: 1, name: "Data Structures", credits: 4 },
{ id: 2, name: "Web Basics", credits: 3 },
{ id: 3, name: "Database Systems", credits: 4 }
];

export default function CoursesPage() {
const dispatch = useDispatch();

return (
<div>
<h2>Courses</h2>
{list.map(c => (
<div key={c.id}>
<Link to={`/courses/${c.id}`}>{c.name}</Link>
<button onClick={() => dispatch(enroll(c))}>Enroll</button>
</div>
))}
</div>
);
}
