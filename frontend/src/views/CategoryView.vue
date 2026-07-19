<script setup>
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import AppShell from '@/components/AppShell.vue'
import FilterBar from '@/components/FilterBar.vue'
import VideoCard from '@/components/VideoCard.vue'
import { fetchVideos } from '@/api/video'

const filters = reactive({ year: '全部年份', type: '全部类型', member: '全部' })
const videos = ref([])
const page = ref(1)
const loading = ref(false)
const error = ref('')
const hasNext = ref(true)

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
    const items = result.results || result
    videos.value = [...videos.value, ...(Array.isArray(items) ? items : [])]
    hasNext.value = Boolean(result.next)
  } catch {
    error.value = '后端数据暂时无法加载'
    hasNext.value = false
  } finally {
    loading.value = false
  }
}

const changeFilter = (patch) => {
  Object.assign(filters, patch)
  load(true)
}

const onScroll = () => {
  if (hasNext.value && window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 240) {
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
        <div v-if="!videos.length && !loading" class="load-state">{{ error || '暂无后端视频数据' }}</div>
        <div v-else class="load-state">{{ loading ? '加载中...' : hasNext ? '继续下滑加载更多' : '已加载全部后端数据' }}</div>
      </div>
      <aside class="rank-sidebar">
        <h2>热播榜</h2>
        <ol>
          <li v-for="item in videos.slice(0, 8)" :key="`rank-${item.id}`">{{ item.title }}</li>
        </ol>
        <p v-if="!videos.length">暂无排行数据</p>
      </aside>
    </section>
  </AppShell>
</template>
