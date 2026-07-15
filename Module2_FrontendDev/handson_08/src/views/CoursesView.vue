<template>
<input v-model="term" placeholder="Search...">
<div class="course-grid">
<CourseCard v-for="c in filteredCourses" :key="c.id" :title="c.name" :tag="c.code" :units="c.credits" />
<button v-for="c in list" :key="'btn'+c.id" @click="store.enroll(c)">Enroll {{ c.name }}</button>
</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import CourseCard from "../components/CourseCard.vue";
import { useEnrollStore } from "../stores/enrollment";

const store = useEnrollStore();
const list = ref([]);
const term = ref("");

onMounted(() => {
list.value = [
{ id: 1, name: "Data Structures", code: "CS101", credits: 4 },
{ id: 2, name: "Web Basics", code: "CS102", credits: 3 },
{ id: 3, name: "Database Systems", code: "CS201", credits: 4 }
];
});

const filteredCourses = computed(() => list.value.filter(c => c.name.toLowerCase().includes(term.value.toLowerCase())));
</script>
