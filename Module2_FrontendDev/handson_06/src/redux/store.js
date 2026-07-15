import { configureStore } from "@reduxjs/toolkit";
import enrollReducer from "./enrollSlice";

export const store = configureStore({
reducer: { enrollment: enrollReducer }
});
