import { useParams, useNavigate } from "react-router-dom";

export default function CourseDetailPage() {
const { courseId } = useParams();
const navigate = useNavigate();

return (
<div>
<h2>Course #{courseId}</h2>
<button onClick={() => navigate("/profile")}>Enroll & Go to Profile</button>
</div>
);
}
