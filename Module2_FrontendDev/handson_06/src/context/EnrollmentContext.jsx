import { createContext, useState } from "react";

export const EnrollmentContext = createContext();

export function EnrollmentProvider({ children }) {
const [picked, setPicked] = useState([]);

const addCourse = course => setPicked(prev => [...prev, course]);
const dropCourse = id => setPicked(prev => prev.filter(c => c.id !== id));

return (
<EnrollmentContext.Provider value={{ picked, addCourse, dropCourse }}>
{children}
</EnrollmentContext.Provider>
);
}
