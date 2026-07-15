import client from "./apiClient";

export const getAllCourses = () => client.get("/posts?_limit=5");
export const getCourseById = id => client.get(`/posts/${id}`);
export const enrollStudent = (studentId, courseId) => client.post("/enrollments", { studentId, courseId });
