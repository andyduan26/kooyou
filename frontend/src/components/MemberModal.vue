<script setup>
defineProps({
  open: { type: Boolean, default: false },
  plans: { type: Array, default: () => [] }
})

defineEmits(['close'])
</script>

<template>
  <div v-if="open" class="member-mask">
    <section class="member-dialog">
      <button class="member-close" type="button" @click="$emit('close')">×</button>
      <h2>开通优酷会员</h2>
      <p>会员专享内容，开通后可继续观看完整影片。</p>
      <div class="member-plans">
        <button v-for="plan in plans" :key="plan.id" type="button">
          <strong>{{ plan.name }}</strong>
          <span>¥{{ plan.price }} / {{ plan.duration_days }}天</span>
        </button>
        <button v-if="!plans.length" type="button">
          <strong>连续包月</strong>
          <span>¥19.9 / 30天</span>
        </button>
      </div>
    </section>
  </div>
</template>
