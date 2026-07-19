<script setup>
const years = ['全部年份', '2026', '2025', '2024', '2023', '2022']
const types = ['全部类型', '动作', '喜剧', '悬疑', '爱情', '纪录']
const member = ['全部', '免费', '会员']

defineProps({
  filters: { type: Object, required: true }
})

defineEmits(['change'])
</script>

<template>
  <section class="filter-board">
    <div class="filter-row">
      <span>年份</span>
      <button v-for="item in years" :key="item" type="button" :class="{ active: filters.year === item }" @click="$emit('change', { year: item })">{{ item }}</button>
    </div>
    <div class="filter-row">
      <span>类型</span>
      <button v-for="item in types" :key="item" type="button" :class="{ active: filters.type === item }" @click="$emit('change', { type: item })">{{ item }}</button>
    </div>
    <div class="filter-row">
      <span>会员</span>
      <button v-for="item in member" :key="item" type="button" :class="{ active: filters.member === item }" @click="$emit('change', { member: item })">{{ item }}</button>
    </div>
  </section>
</template>
