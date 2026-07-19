<script setup>
import { ref } from 'vue'

defineProps({
  items: { type: Array, default: () => [] }
})

const emit = defineEmits(['submit'])
const content = ref('')

const submit = () => {
  if (!content.value.trim()) return
  emit('submit', { content: content.value.trim(), time_offset: 0, color: '#ffffff' })
  content.value = ''
}
</script>

<template>
  <div class="danmaku-panel">
    <div class="danmaku-track">
      <span v-for="item in items.slice(0, 10)" :key="item.id || item.content" class="danmaku-item">
        {{ item.content }}
      </span>
    </div>
    <form class="danmaku-form" @submit.prevent="submit">
      <input v-model="content" placeholder="发一条弹幕" />
      <button type="submit">发送</button>
    </form>
  </div>
</template>
