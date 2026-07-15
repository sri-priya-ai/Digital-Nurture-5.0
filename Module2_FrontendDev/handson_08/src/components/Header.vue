<template>
<header>
<h2>Campus Hub</h2>
<RouterLink to="/">Home</RouterLink>
<RouterLink to="/courses">Courses</RouterLink>
<RouterLink to="/profile">Profile</RouterLink>
<span>{{ store.picked.length }} enrolled</span>
</header>
</template>

<script setup>
import { useEnrollStore } from "../stores/enrollment";
const store = useEnrollStore();
</script>
