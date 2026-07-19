<script setup>
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import AppShell from '@/components/AppShell.vue'
import FilterBar from '@/components/FilterBar.vue'
import VideoCard from '@/components/VideoCard.vue'
import { assets } from '@/assets/baseline-assets'
import { fetchVideos } from '@/api/video'

const filters = reactive({ year: '全部年份', type: '全部类型', member: '全部' })
const videos = ref([])
const page = ref(1)
const loading = ref(false)

const fallback = Array.from({ length: 18 }, (_, index) => ({
  id: index + 20,
  title: ['731', '东极岛', '酱园弄', '长安的荔枝', '热烈', '飞驰人生'][index % 6],
  play_count: 1000 + index * 351,
  member_only: index % 4 === 0,
  cover_url: assets.covers[index % assets.covers.length]
}))

const params = () => ({
  page: page.value,
  member_only: filters.member === '会员' ? true : filters.member === '免费' ? false : undefined,
  keyword: filters.type === '全部类型' ? undefined : filters.type
})

const load = async (reset = false) => {
  if (loading.value) return
  loading.value = true
  if (reset) {
    page.value = 1
    videos.value = []
  }
  try {
    const result = await fetchVideos(params())
    videos.value = [...videos.value, ...(result.results || result)]
  } catch {
    videos.value = [...videos.value, ...fallback.map((item) => ({ ...item, id: `${item.id}-${page.value}` }))]
  } finally {
    loading.value = false
  }
}

const changeFilter = (patch) => {
  Object.assign(filters, patch)
  load(true)
}

const onScroll = () => {
  if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 240) {
    page.value += 1
    load()
  }
}

onMounted(() => {
  load(true)
  window.addEventListener('scroll', onScroll)
})
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<template>
  <AppShell>
    <section class="category-header">
      <h1>电影频道</h1>
      <p>多维筛选 · 无限滚动 · 高清正版内容</p>
    </section>
    <FilterBar :filters="filters" @change="changeFilter" />
    <section class="category-layout">
      <div class="category-main">
        <div class="video-grid">
          <VideoCard v-for="(video, index) in videos" :key="video.id" :video="video" :index="index" />
        </div>
        <div class="load-state">{{ loading ? '加载中...' : '继续下滑加载更多' }}</div>
      </div>
      <aside class="rank-sidebar">
        <h2>热播榜</h2>
        <ol>
          <li v-for="item in videos.slice(0, 8)" :key="`rank-${item.id}`">{{ item.title }}</li>
        </ol>
      </aside>
    </section>
  </AppShell>
</template>
