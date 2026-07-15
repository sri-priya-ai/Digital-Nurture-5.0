export default function Header({ siteName, enrolledCount }) {
return (
<header>
<h2>{siteName}</h2>
<span>Enrolled: {enrolledCount}</span>
<nav>
<a href="#">Home</a>
<a href="#">Courses</a>
<a href="#">Profile</a>
</nav>
</header>
);
}
