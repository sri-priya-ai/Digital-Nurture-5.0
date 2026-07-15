<template>
<article class="course-card">
<h3>{{ title }}</h3>
<p>{{ tag }}</p>
<span>{{ units }} credits</span>
</article>
</template>

<script setup>
defineProps({ title: String, tag: String, units: Number });
</script>

<style scoped>
.course-card { padding: 16px; border: 1px solid #ddd; border-radius: 8px; }
</style>
