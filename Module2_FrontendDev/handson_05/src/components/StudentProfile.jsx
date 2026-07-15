import { useState } from "react";

export default function StudentProfile() {
const [form, setForm] = useState({ name: "", email: "", semester: "" });

const updateField = e => {
setForm({ ...form, [e.target.name]: e.target.value });
};

return (
<div>
<h2>Profile</h2>
<input name="name" placeholder="Name" value={form.name} onChange={updateField} />
<input name="email" placeholder="Email" value={form.email} onChange={updateField} />
<input name="semester" placeholder="Semester" value={form.semester} onChange={updateField} />
</div>
);
}
