<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import AppShell from '@/components/AppShell.vue'
import DanmakuLayer from '@/components/DanmakuLayer.vue'
import MemberModal from '@/components/MemberModal.vue'
import PlayerBox from '@/components/PlayerBox.vue'
import VideoCard from '@/components/VideoCard.vue'
import { assets } from '@/assets/baseline-assets'
import { checkMembership, fetchDanmaku, fetchMembershipPlans, fetchVideoDetail, fetchVideos, playAuth, submitDanmaku, toggleFavorite } from '@/api/video'
import { useVideoStore } from '@/stores/video'

const route = useRoute()
const store = useVideoStore()
const video = ref({ id: route.params.id, title: '龙在少林', video_id: 'XNTIwMDU4NzU2MA==', cover_url: assets.hero[0], member_only: true })
const related = ref([])
const danmakus = ref([])
const plans = ref([])
const allowed = ref(true)
const modalOpen = ref(false)
const currentEpisode = ref(1)

const fallbackRelated = ['龙的传人', '我是谁', '逃学威龙', '飞鹰计划', '富贵列车', '举起手来'].map((title, index) => ({
  id: index + 100,
  title,
  cover_url: assets.covers[index % assets.covers.length],
  play_count: 2000 + index * 513,
  member_only: index % 2 === 0
}))

const load = async () => {
  try {
    video.value = await fetchVideoDetail(route.params.id)
    const auth = await playAuth(route.params.id)
    allowed.value = auth.allowed
    video.value.play_url = auth.play_url
    modalOpen.value = !auth.allowed
    danmakus.value = await fetchDanmaku(route.params.id)
    const list = await fetchVideos({ page: 1 })
    related.value = list.results || list
    plans.value = await fetchMembershipPlans()
  } catch {
    related.value = fallbackRelated
    danmakus.value = [{ id: 1, content: '经典港片回忆杀' }, { id: 2, content: '这个画面太熟悉了' }]
  }
  store.remember(video.value)
}

const sendDanmaku = async (payload) => {
  try {
    const created = await submitDanmaku(route.params.id, payload)
    danmakus.value = [...danmakus.value, created]
  } catch {
    danmakus.value = [...danmakus.value, { id: Date.now(), ...payload }]
  }
}

const favorite = async () => {
  try {
    await toggleFavorite(route.params.id)
  } finally {
    store.saveFavorite(video.value)
  }
}

onMounted(async () => {
  await load()
  try {
    const membership = await checkMembership()
    if (video.value.member_only && !membership.active) modalOpen.value = true
  } catch {
    if (video.value.member_only) modalOpen.value = true
  }
})
</script>

<template>
  <AppShell>
    <PlayerBox :video="video" :allowed="allowed">
      <DanmakuLayer :items="danmakus" @submit="sendDanmaku" />
    </PlayerBox>
    <section class="play-layout">
      <div class="play-main">
        <div class="play-title-row">
          <div>
            <h1>{{ video.title }}</h1>
            <p>播放 {{ video.play_count || 0 }} · {{ video.member_only ? '会员' : '免费' }}</p>
          </div>
          <div class="action-cluster">
            <button type="button" @click="favorite">收藏</button>
            <button type="button">点赞</button>
          </div>
        </div>
        <div class="episode-panel">
          <button v-for="episode in 12" :key="episode" type="button" :class="{ active: currentEpisode === episode }" @click="currentEpisode = episode">
            {{ episode }}
          </button>
        </div>
      </div>
      <aside class="related-panel">
        <h2>相关推荐</h2>
        <VideoCard v-for="(item, index) in related.slice(0, 6)" :key="item.id" :video="item" :index="index" />
      </aside>
    </section>
    <MemberModal :open="modalOpen" :plans="plans" @close="modalOpen = false" />
  </AppShell>
</template>
