<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  video: { type: Object, required: true },
  index: { type: Number, default: 0 }
})

const image = computed(() => props.video.cover_url || '')
const label = computed(() => (props.video.member_only ? 'VIP' : '高清'))
</script>

<template>
  <div class="yk_card_368vl kooyou-card">
    <RouterLink :to="`/play/${video.id || video.video_id}`" class="kooyou-card-link" :aria-label="`${label} ${video.title}`">
      <div class="pack_wrap_2xjIs pack_vertical_ilL2U">
        <div class="pack_img_wrap_3sS_W">
          <img v-if="image" class="pack_img_YJm41" :src="image" :alt="video.title" />
          <div v-else class="pack_img_YJm41 card-cover-empty">{{ video.title }}</div>
        </div>
        <div class="pack_mark_1hLkl tag_YELLOW_3uzKD">
          <span>{{ label }}</span>
        </div>
        <div class="newSummaryLeft_2WuF0">
          <div class="newSummaryLeftText_22TVB">热度</div>
          <div class="newSummaryLeftSubTitle_3gXo1">{{ video.play_count || 0 }}</div>
        </div>
      </div>
      <div class="pack_title_vhB7u">{{ video.title }}</div>
    </RouterLink>
  </div>
</template>
