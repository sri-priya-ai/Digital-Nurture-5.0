const courseBox = document.querySelector(".course-grid");
const courseMsg = document.getElementById("courseStatus");
const notifyBox = document.querySelector(".notify-grid");
const notifyMsg = document.getElementById("notifyStatus");
const retryBtn = document.getElementById("retryBtn");

const delay = ms => new Promise(res => setTimeout(res, ms));

const loadCourses = async () => {
courseMsg.textContent = "Loading courses...";
await delay(1000);
const list = [
{ id: 1, name: "Data Structures", credits: 4 },
{ id: 2, name: "Web Basics", credits: 3 },
{ id: 3, name: "Database Systems", credits: 4 }
];
courseBox.innerHTML = list.map(c => `<article class="course-card"><h3>${c.name}</h3><span>${c.credits} credits</span></article>`).join("");
courseMsg.textContent = "";
};

const pullJson = async url => {
const res = await fetch(url);
if (!res.ok) throw new Error(`Request failed: ${res.status}`);
return res.json();
};

const loadNotifications = async () => {
notifyMsg.textContent = "Loading notifications...";
notifyBox.innerHTML = "";
retryBtn.hidden = true;
try {
const posts = await pullJson("https://jsonplaceholder.typicode.com/posts?_limit=5");
notifyBox.innerHTML = posts.map(p => `<div class="notify-card"><h4>${p.title}</h4></div>`).join("");
notifyMsg.textContent = "";
} catch (err) {
notifyMsg.innerHTML = `<span class="err-msg">Could not load notifications.</span>`;
retryBtn.hidden = false;
}
};

retryBtn.addEventListener("click", loadNotifications);

const dualFetch = async () => {
const [a, b] = await Promise.all([
axios.get("https://jsonplaceholder.typicode.com/users/1"),
axios.get("https://jsonplaceholder.typicode.com/users/2")
]);
console.log(a.data.name, b.data.name);
};

axios.interceptors.request.use(cfg => {
console.log("API call started:", cfg.url);
return cfg;
});

loadCourses();
loadNotifications();
dualFetch();
