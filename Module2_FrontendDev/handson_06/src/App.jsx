import { Routes, Route, Link } from "react-router-dom";
import HomePage from "./pages/HomePage";
import CoursesPage from "./pages/CoursesPage";
import CourseDetailPage from "./pages/CourseDetailPage";
import ProfilePage from "./pages/ProfilePage";

export default function App() {
return (
<>
<nav>
<Link to="/">Home</Link>
<Link to="/courses">Courses</Link>
<Link to="/profile">Profile</Link>
</nav>
<Routes>
<Route path="/" element={<HomePage />} />
<Route path="/courses" element={<CoursesPage />} />
<Route path="/courses/:courseId" element={<CourseDetailPage />} />
<Route path="/profile" element={<ProfilePage />} />
</Routes>
</>
);
}
