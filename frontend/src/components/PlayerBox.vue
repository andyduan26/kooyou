<script setup>
defineProps({
  video: { type: Object, default: () => ({}) },
  allowed: { type: Boolean, default: true }
})
</script>

<template>
  <section class="play-stage">
    <div class="video-player-container" :data-vid="video.video_id || 'VIDEO_ID'">
      <video v-if="allowed && video.play_url" class="native-player" controls :poster="video.cover_url">
        <source :src="video.play_url" type="video/mp4" />
      </video>
      <div v-else class="player-cover">
        <strong>{{ video.title || '正在加载视频' }}</strong>
        <span>{{ allowed ? '原生播放器容器' : '会员内容，开通后观看' }}</span>
      </div>
      <slot />
    </div>
  </section>
</template>
