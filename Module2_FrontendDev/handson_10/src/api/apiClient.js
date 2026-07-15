import axios from "axios";

const client = axios.create({
baseURL: "https://jsonplaceholder.typicode.com",
timeout: 5000,
headers: { "Content-Type": "application/json" }
});

client.interceptors.request.use(cfg => {
cfg.headers.Authorization = "Bearer mock-token";
return cfg;
});

client.interceptors.response.use(
res => res.data,
err => {
const wrapped = new Error(err.response?.data?.message || "Request failed");
wrapped.statusCode = err.response?.status || 500;
return Promise.reject(wrapped);
}
);

export default client;
