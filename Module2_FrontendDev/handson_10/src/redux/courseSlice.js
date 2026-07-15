import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { getAllCourses } from "../api/courseApi";

export const fetchAllCourses = createAsyncThunk("courses/fetchAll", async () => {
return await getAllCourses();
});

const courseSlice = createSlice({
name: "courses",
initialState: { list: [], loading: false, error: null },
reducers: {},
extraReducers: builder => {
builder
.addCase(fetchAllCourses.pending, state => { state.loading = true; state.error = null; })
.addCase(fetchAllCourses.fulfilled, (state, action) => { state.list = action.payload; state.loading = false; })
.addCase(fetchAllCourses.rejected, (state, action) => { state.error = action.error.message; state.loading = false; });
}
});

export const selectCourses = state => state.courses.list;
export const selectCoursesLoading = state => state.courses.loading;
export const selectCoursesError = state => state.courses.error;

export default courseSlice.reducer;
