<template>
<h2>Profile</h2>
<p>Total credits: {{ store.totalUnits }}</p>
<ul>
<li v-for="c in store.picked" :key="c.id">
{{ c.name }} <button @click="store.unenroll(c.id)">Remove</button>
</li>
</ul>
</template>

<script setup>
import { storeToRefs } from "pinia";
import { useEnrollStore } from "../stores/enrollment";

const store = useEnrollStore();
const { picked } = storeToRefs(store);
</script>
