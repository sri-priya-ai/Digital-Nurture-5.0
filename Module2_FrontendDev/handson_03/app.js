import { subjects } from "./data.js";

const gridBox = document.querySelector(".course-grid");
const totalBox = document.getElementById("creditTotal");
const pickedBox = document.getElementById("pickedCourse");
const filterBox = document.getElementById("filterBox");
const sortBtn = document.getElementById("sortBtn");

let currentList = [...subjects];

const paintGrid = list => {
gridBox.innerHTML = "";
const frag = document.createDocumentFragment();
list.forEach(item => {
const card = document.createElement("article");
card.className = "course-card";
card.dataset.ref = item.ref;
card.innerHTML = `<h3>${item.title}</h3><p>${item.tag}</p><span>${item.units} credits</span>`;
frag.appendChild(card);
});
gridBox.appendChild(frag);
const sum = list.reduce((acc, cur) => acc + cur.units, 0);
totalBox.textContent = `Total credits: ${sum}`;
};

filterBox.addEventListener("input", e => {
const term = e.target.value.toLowerCase();
currentList = subjects.filter(s => s.title.toLowerCase().includes(term));
paintGrid(currentList);
});

sortBtn.addEventListener("click", () => {
currentList = [...currentList].sort((a, b) => b.units - a.units);
paintGrid(currentList);
});

gridBox.addEventListener("click", e => {
const card = e.target.closest(".course-card");
if (!card) return;
const match = subjects.find(s => s.ref == card.dataset.ref);
pickedBox.textContent = `${match.title} — Grade: ${match.mark}`;
});

paintGrid(currentList);
