import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchAllCourses, selectCourses, selectCoursesLoading, selectCoursesError } from "../redux/courseSlice";

export default function CoursesPage() {
const dispatch = useDispatch();
const list = useSelector(selectCourses);
const busy = useSelector(selectCoursesLoading);
const errMsg = useSelector(selectCoursesError);

useEffect(() => {
dispatch(fetchAllCourses());
}, [dispatch]);

if (busy) return <p>Loading...</p>;
if (errMsg) return <p>{errMsg}</p>;

return (
<ul>
{list.map(c => <li key={c.id}>{c.title}</li>)}
</ul>
);
}
