<script setup>
import AppShell from '@/components/AppShell.vue'
import VideoCard from '@/components/VideoCard.vue'
import { useVideoStore } from '@/stores/video'

const store = useVideoStore()
</script>

<template>
  <AppShell>
    <section class="profile-header">
      <h1>个人中心</h1>
      <p>观看历史、我的收藏与会员中心</p>
    </section>
    <section class="profile-grid">
      <div class="profile-section">
        <h2>观看历史</h2>
        <div class="video-grid compact">
          <VideoCard v-for="(item, index) in store.history" :key="`history-${item.id}`" :video="item" :index="index" />
        </div>
        <p v-if="!store.history.length">暂无观看记录</p>
      </div>
      <div class="profile-section">
        <h2>我的收藏</h2>
        <div class="video-grid compact">
          <VideoCard v-for="(item, index) in store.favorites" :key="`favorite-${item.id}`" :video="item" :index="index" />
        </div>
        <p v-if="!store.favorites.length">暂无收藏</p>
      </div>
      <div class="profile-section membership-center">
        <h2>会员中心</h2>
        <p>开通会员后可观看 VIP 内容、高清影片和独家剧集。</p>
        <button type="button">立即开通</button>
      </div>
    </section>
  </AppShell>
</template>
