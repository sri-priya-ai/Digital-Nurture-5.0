import { createSlice } from "@reduxjs/toolkit";

const enrollSlice = createSlice({
name: "enrollment",
initialState: { picked: [] },
reducers: {
enroll: (state, action) => { state.picked.push(action.payload); },
unenroll: (state, action) => { state.picked = state.picked.filter(c => c.id !== action.payload); }
}
});

export const { enroll, unenroll } = enrollSlice.actions;
export default enrollSlice.reducer;
