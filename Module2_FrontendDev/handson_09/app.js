const roster = [
{ id: 1, title: "Data Structures", credits: 4 },
{ id: 2, title: "Web Basics", credits: 3 },
{ id: 3, title: "Database Systems", credits: 4 }
];

const gridBox = document.querySelector(".course-grid");
const filterBox = document.getElementById("filterBox");
const countBox = document.getElementById("resultCount");

const paint = list => {
gridBox.innerHTML = "";
list.forEach(item => {
const card = document.createElement("article");
card.className = "course-card";
card.tabIndex = 0;
card.textContent = `${item.title} — ${item.credits} credits`;
card.addEventListener("keydown", e => {
if (e.key === "Enter") alert(item.title);
});
gridBox.appendChild(card);
});
countBox.textContent = `${list.length} courses found`;
};

filterBox.addEventListener("input", e => {
const term = e.target.value.toLowerCase();
paint(roster.filter(r => r.title.toLowerCase().includes(term)));
});

paint(roster);
