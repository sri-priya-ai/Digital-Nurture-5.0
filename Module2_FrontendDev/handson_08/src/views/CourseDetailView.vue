<template>
<h2>Course #{{ route.params.id }}</h2>
<button @click="goEnroll">Enroll & Go to Profile</button>
</template>

<script setup>
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const goEnroll = () => router.push("/profile");
</script>
