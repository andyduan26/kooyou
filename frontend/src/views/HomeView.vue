<script setup>
import { onMounted, ref } from 'vue'
import AppShell from '@/components/AppShell.vue'
import VideoCard from '@/components/VideoCard.vue'
import { assets } from '@/assets/baseline-assets'
import { fetchHomeRecommend, fetchVideos } from '@/api/video'

const recommended = ref([])
const feed = ref([])
const page = ref(1)

const fallback = ['藏海传', '以法之名', '凡人修仙传', '长安的荔枝', '姐姐当家', '捕风追影', '重案无罪', '勇者无疆'].map((title, index) => ({
  id: index + 1,
  video_id: `VIDEO_${index + 1}`,
  title,
  play_count: 6000 + index * 918,
  member_only: index % 3 === 0,
  cover_url: assets.covers[index % assets.covers.length]
}))

const load = async () => {
  try {
    recommended.value = await fetchHomeRecommend()
    const result = await fetchVideos({ page: page.value })
    feed.value = result.results || result
  } catch {
    recommended.value = fallback.slice(0, 5)
    feed.value = fallback
  }
}

const loadMore = async () => {
  page.value += 1
  try {
    const result = await fetchVideos({ page: page.value })
    feed.value = [...feed.value, ...(result.results || result)]
  } catch {
    feed.value = [...feed.value, ...fallback.map((item) => ({ ...item, id: `${item.id}-${page.value}` }))]
  }
}

onMounted(load)
</script>

<template>
  <AppShell>
    <section class="home-hero">
      <div class="hero-track">
        <article v-for="(item, index) in (recommended.length ? recommended.slice(0, 3) : fallback.slice(0, 3))" :key="item.id" class="hero-slide">
          <img :src="assets.hero[index % assets.hero.length]" :alt="item.title" />
          <div class="img_top_shadow_2Php6"></div>
          <div class="img_left_shadow_2fEQ_"></div>
          <div class="img_bottom_shadow_FR1ZY"></div>
          <div class="hero-copy">
            <h1>{{ item.title }}</h1>
            <p>全网热播 · 高清正版 · 为好内容全力以赴</p>
            <RouterLink :to="`/play/${item.id}`">立即观看</RouterLink>
          </div>
        </article>
      </div>
    </section>

    <section class="content-band">
      <div class="section-head">
        <h2>热门推荐</h2>
        <button type="button" @click="loadMore">换一换</button>
      </div>
      <div class="video-grid">
        <VideoCard v-for="(video, index) in feed" :key="video.id" :video="video" :index="index" />
      </div>
    </section>

    <section class="content-band">
      <div class="section-head">
        <h2>频道精选</h2>
        <RouterLink to="/category">查看全部</RouterLink>
      </div>
      <div class="channel-strip">
        <RouterLink v-for="item in ['电影', '剧集', '动漫', '综艺']" :key="item" :to="{ path: '/category', query: { channel: item } }">{{ item }}</RouterLink>
      </div>
    </section>
  </AppShell>
</template>
