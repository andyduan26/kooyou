<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import AppShell from '@/components/AppShell.vue'
import MemberModal from '@/components/MemberModal.vue'
import { checkMembership, fetchDanmaku, fetchMembershipPlans, fetchVideoDetail, fetchVideos, playAuth, submitDanmaku, toggleFavorite } from '@/api/video'
import { useVideoStore } from '@/stores/video'

const route = useRoute()
const store = useVideoStore()
const modalOpen = ref(false)
const plans = ref([])
const danmakus = ref([])
const currentEpisode = ref(1)
const video = ref(null)
const related = ref([])
const allowed = ref(false)
const error = ref('')

const displayDanmaku = computed(() => danmakus.value.slice(0, 3))
const recommendVideos = computed(() => related.value.filter((item) => item.id !== video.value?.id).slice(0, 20))
const episodeItems = computed(() => {
  const count = video.value?.episode_count || 1
  return Array.from({ length: count }, (_, index) => ({
    id: index + 1,
    title: `${video.value?.title || '视频'} 第${index + 1}集`,
    image: video.value?.cover_url
  }))
})
const aroundVideos = computed(() => recommendVideos.value.slice(0, 10))

const load = async () => {
  error.value = ''
  allowed.value = false
  try {
    const detail = await fetchVideoDetail(route.params.id)
    video.value = detail
    try {
      const auth = await playAuth(route.params.id)
      allowed.value = Boolean(auth.allowed)
      video.value = { ...detail, play_url: auth.play_url || detail.play_url }
    } catch {
      allowed.value = !detail.member_only
    }
    const [danmakuResult, planResult, listResult] = await Promise.all([
      fetchDanmaku(route.params.id).catch(() => []),
      fetchMembershipPlans().catch(() => []),
      fetchVideos({ page: 1 }).catch(() => ({ results: [] }))
    ])
    danmakus.value = Array.isArray(danmakuResult) ? danmakuResult : []
    plans.value = Array.isArray(planResult) ? planResult : planResult.results || []
    related.value = Array.isArray(listResult) ? listResult : listResult.results || []
    store.remember(video.value)
  } catch {
    video.value = null
    related.value = []
    danmakus.value = []
    error.value = '后端视频详情暂时无法加载'
  }
}

const favorite = async () => {
  if (!video.value) return
  try {
    await toggleFavorite(route.params.id)
    store.saveFavorite(video.value)
  } catch {
    error.value = '收藏需要登录后操作'
  }
}

const sendDanmaku = async (content) => {
  if (!content.trim() || !video.value) return
  try {
    const created = await submitDanmaku(route.params.id, { content, time_offset: 0, color: '#ffffff' })
    danmakus.value = [...danmakus.value, created]
  } catch {
    error.value = '弹幕提交失败'
  }
}

onMounted(async () => {
  await load()
  try {
    const membership = await checkMembership()
    modalOpen.value = Boolean(video.value?.member_only && !membership.active)
  } catch {
    modalOpen.value = Boolean(video.value?.member_only && !allowed.value)
  }
})

watch(() => route.params.id, load)
</script>

<template>
  <AppShell>
    <div v-if="video" class="play-page">
      <main class="play-left">
        <section class="youku-member-player">
          <div class="video-player-container play-member-cover" :data-vid="video.video_id || 'VIDEO_ID'">
            <video v-if="allowed && video.play_url" class="native-player" controls :poster="video.cover_url">
              <source :src="video.play_url" type="video/mp4" />
            </video>
            <template v-else>
              <div class="member-player-copy">
                <h1>{{ video.member_only ? '本片为会员专属内容' : video.title }}</h1>
                <p>{{ video.member_only ? '开通会员观看完整视频' : '暂无可播放视频源' }}</p>
                <button v-if="video.member_only" type="button" @click="modalOpen = true">
                  <span>会员特惠</span>
                  立即开通
                </button>
              </div>
              <div class="member-player-chevron">〉</div>
              <div class="member-benefits">
                <span></span>
                <em>VIP会员专享以下特权</em>
                <span></span>
                <div class="benefit-row">
                  <div><i>免</i><b>贴片抢先看</b></div>
                  <div><i>AD</i><b>广告特权</b></div>
                  <div><i>冠</i><b>会员片库</b></div>
                  <div><i>HDR</i><b>蓝光HDR</b></div>
                  <div><i>券</i><b>权益下载</b></div>
                </div>
              </div>
            </template>
          </div>
        </section>

        <section class="play-recommend">
          <h2>为你推荐</h2>
          <div v-if="recommendVideos.length" class="play-poster-grid">
            <RouterLink v-for="item in recommendVideos" :key="item.id" :to="`/play/${item.id}`" class="play-poster-card">
              <div class="play-poster-frame">
                <img v-if="item.cover_url" :src="item.cover_url" :alt="item.title" />
                <span v-if="item.member_only" class="play-card-tag">VIP</span>
                <small>{{ item.category?.name || '电影' }}</small>
              </div>
              <h3>{{ item.title }}</h3>
            </RouterLink>
          </div>
          <p v-else class="load-state">暂无后端推荐数据</p>
        </section>
      </main>

      <aside class="play-right">
        <div class="play-tabs">
          <button type="button" class="active">视频</button>
          <button type="button">讨论 {{ danmakus.length }}</button>
        </div>

        <section class="play-info">
          <h1>{{ video.title }}</h1>
          <div class="play-info-meta">播放 {{ video.play_count || 0 }}　{{ video.category?.name || '电影' }}　{{ video.member_only ? '会员' : '免费' }}</div>
          <p>视频ID：{{ video.video_id }}。时长 {{ Math.round((video.duration || 0) / 60) }} 分钟，数据来自 Django 后端。</p>
          <div class="play-action-row">
            <button type="button">☷</button>
            <button type="button">↓</button>
            <button type="button">↗</button>
            <button type="button" @click="favorite">♡</button>
          </div>
          <div class="danmaku-mini">
            <span v-for="item in displayDanmaku" :key="item.id || item.content">{{ item.content }}</span>
            <form @submit.prevent="sendDanmaku($event.target.elements.danmaku.value); $event.target.reset()">
              <input name="danmaku" placeholder="发一条弹幕" />
            </form>
          </div>
        </section>

        <section v-if="video.member_only" class="play-vip-card">
          <strong>会员特惠</strong>
          <p>开通会员后观看 VIP 内容</p>
          <button type="button" @click="modalOpen = true">立即开通</button>
        </section>

        <section class="play-side-section">
          <div class="side-heading">
            <h2>选集</h2>
            <a href="#">共 {{ episodeItems.length }} 集 〉</a>
          </div>
          <article v-for="item in episodeItems" :key="item.id" class="episode-item" :class="{ active: item.id === currentEpisode }" @click="currentEpisode = item.id">
            <img v-if="item.image" :src="item.image" :alt="item.title" />
            <p>{{ item.title }}</p>
          </article>
        </section>

        <section class="play-side-section">
          <h2>周边视频</h2>
          <RouterLink v-for="item in aroundVideos" :key="item.id" :to="`/play/${item.id}`" class="around-item">
            <img v-if="item.cover_url" :src="item.cover_url" :alt="item.title" />
            <div>
              <p>{{ item.title }}</p>
              <time>播放 {{ item.play_count || 0 }}</time>
            </div>
          </RouterLink>
          <p v-if="!aroundVideos.length" class="load-state">暂无周边视频</p>
        </section>
      </aside>
    </div>

    <div v-else class="play-empty-state">
      <h1>{{ error || '暂无后端视频数据' }}</h1>
      <p>请先在 Django 后台上传并发布视频资源。</p>
    </div>

    <footer class="play-footer">
      <div>
        <h3>关于我们</h3>
        <p>关于我们　在线反馈　账号设备说明</p>
        <p>优酷热播云　优酷社会责任报告</p>
        <p>AI合成标识公告　Youku.tv</p>
      </div>
      <div>
        <h3>协议声明</h3>
        <p>用户协议　历史协议文本　知识产权声明</p>
        <p>隐私政策　反馈声明</p>
      </div>
      <div>
        <h3>服务合作</h3>
        <p>广告合作　优酷内容开放平台</p>
        <p>入驻优酷　娱奥</p>
      </div>
      <small>
        营业执照｜信息网络传播视听节目许可证：0108283号｜网络文化经营许可证｜京ICP备06028298号｜京公网安备11000002000017号
      </small>
    </footer>

    <MemberModal :open="modalOpen" :plans="plans" @close="modalOpen = false" />
  </AppShell>
</template>
