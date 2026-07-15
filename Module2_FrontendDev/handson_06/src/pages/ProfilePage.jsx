import { useSelector, useDispatch } from "react-redux";
import { unenroll } from "../redux/enrollSlice";

export default function ProfilePage() {
const picked = useSelector(state => state.enrollment.picked);
const dispatch = useDispatch();

return (
<div>
<h2>Profile</h2>
<ul>
{picked.map(c => (
<li key={c.id}>
{c.name} <button onClick={() => dispatch(unenroll(c.id))}>Remove</button>
</li>
))}
</ul>
</div>
);
}
