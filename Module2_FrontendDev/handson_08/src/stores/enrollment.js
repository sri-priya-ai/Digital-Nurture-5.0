import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useEnrollStore = defineStore("enrollment", () => {
const picked = ref([]);

const totalUnits = computed(() => picked.value.reduce((sum, c) => sum + c.credits, 0));

const enroll = course => picked.value.push(course);
const unenroll = id => { picked.value = picked.value.filter(c => c.id !== id); };

return { picked, totalUnits, enroll, unenroll };
});
