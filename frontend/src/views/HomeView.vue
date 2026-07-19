<script setup>
import { computed, onMounted, ref } from 'vue'
import AppShell from '@/components/AppShell.vue'
import { fetchHomeRecommend, fetchVideos } from '@/api/video'

const recommended = ref([])
const videos = ref([])
const loading = ref(false)
const error = ref('')

const heroVideo = computed(() => recommended.value[0] || videos.value[0] || null)
const heroCards = computed(() => (recommended.value.length ? recommended.value : videos.value).slice(0, 5))
const rows = computed(() => {
  const source = videos.value.length ? videos.value : recommended.value
  return [
    { title: '正在热播', items: source.slice(0, 6) },
    { title: '会员精选', items: source.filter((item) => item.member_only).slice(0, 6) },
    { title: '更多电影', items: source.slice(6, 18) }
  ].filter((row) => row.items.length)
})

const load = async () => {
  loading.value = true
  error.value = ''
  try {
    const [homeResult, listResult] = await Promise.all([fetchHomeRecommend(), fetchVideos({ page: 1 })])
    recommended.value = Array.isArray(homeResult) ? homeResult : homeResult.results || []
    videos.value = Array.isArray(listResult) ? listResult : listResult.results || []
  } catch {
    recommended.value = []
    videos.value = []
    error.value = '后端数据暂时无法加载'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <AppShell>
    <section class="yk-movie-hero">
      <template v-if="heroVideo">
        <img v-if="heroVideo.cover_url" class="movie-hero-bg" :src="heroVideo.cover_url" :alt="heroVideo.title" />
        <div v-else class="movie-hero-bg movie-hero-empty"></div>
        <div class="movie-hero-shade"></div>
        <div class="movie-hero-info">
          <h1>{{ heroVideo.title }}</h1>
          <div class="hero-meta"><span>{{ heroVideo.member_only ? 'VIP' : '高清' }}</span><span>{{ heroVideo.category?.name || '电影' }}</span></div>
          <p>播放量 {{ heroVideo.play_count || 0 }} · 时长 {{ Math.round((heroVideo.duration || 0) / 60) }} 分钟</p>
          <strong>{{ heroVideo.is_recommended ? '首页推荐' : '后端数据' }}</strong>
          <RouterLink :to="`/play/${heroVideo.id}`" class="hero-play">播放</RouterLink>
        </div>
        <div class="hero-poster-strip">
          <RouterLink v-for="(item, index) in heroCards" :key="item.id" :to="`/play/${item.id}`" class="hero-mini" :class="{ active: index === 0 }">
            <img v-if="item.cover_url" :src="item.cover_url" :alt="item.title" />
            <b>{{ item.is_recommended ? '推荐' : '电影' }}<small>{{ item.member_only ? 'VIP' : 'HD' }}</small></b>
            <em v-if="item.member_only">VIP</em>
            <span>{{ item.title }}</span>
          </RouterLink>
        </div>
      </template>
      <div v-else class="home-empty-state">
        <h1>{{ loading ? '正在加载后端数据' : '暂无后端视频数据' }}</h1>
        <p>{{ error || '请先在 Django 后台上传并发布视频资源' }}</p>
      </div>
    </section>

    <section class="movie-row" v-for="row in rows" :key="row.title">
      <h2>{{ row.title }}</h2>
      <div class="movie-card-grid">
        <RouterLink v-for="item in row.items" :key="item.id" :to="`/play/${item.id}`" class="movie-poster-card">
          <div class="poster-frame">
            <img v-if="item.cover_url" :src="item.cover_url" :alt="item.title" />
            <b>{{ item.category?.name || '电影' }}<small>{{ item.play_count || 0 }}</small></b>
            <em v-if="item.member_only">VIP</em>
          </div>
          <strong>{{ item.title }}</strong>
          <span>播放 {{ item.play_count || 0 }}</span>
        </RouterLink>
      </div>
    </section>
  </AppShell>
</template>
