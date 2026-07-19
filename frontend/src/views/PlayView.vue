<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import AppShell from '@/components/AppShell.vue'
import MemberModal from '@/components/MemberModal.vue'
import { assets, posterPool } from '@/assets/baseline-assets'
import { checkMembership, fetchDanmaku, fetchMembershipPlans, fetchVideoDetail, playAuth, submitDanmaku, toggleFavorite } from '@/api/video'
import { useVideoStore } from '@/stores/video'

const route = useRoute()
const store = useVideoStore()
const modalOpen = ref(false)
const plans = ref([])
const danmakus = ref([])
const currentEpisode = ref(3)
const video = ref({
  id: route.params.id,
  title: '舍得智慧人物 第八季',
  video_id: 'XNjU0OTEwMDE0MA==',
  cover_url: assets.hero[0],
  member_only: true,
  play_count: 739
})

const poster = (index) => posterPool[index % posterPool.length] || assets.placeholder

const recommends = [
  '听你这么说', '言外之易', '和陌生人说话 第二季', '生命·成长 第四季', '我是医者', 'UP青年',
  '创造者 第一季', '圆桌派 第六季', '人生开卷题的答案', '四海中医', '龙中对 第二季', '双向镜',
  '风啊水啊一顶桥', '第一人称复数 第三季', '交友π', '我和我的小店', '京港生活', '潮流之下：我的新时代',
  '无双2026', '天地有大美', '人间财经', '时代引力', '开腔', '互联网上的一万种生活'
].map((title, index) => ({
  id: index + 1,
  title,
  cover: poster(index + 5),
  tag: index % 4 === 0 ? 'VIP' : index % 5 === 0 ? '独播' : '',
  meta: index % 3 === 0 ? '更新至07-16期' : index % 3 === 1 ? `${8 + index}期全` : '更新至25期'
}))

const episodes = [
  { title: '先导 因为热爱，所以舍得', image: poster(12), active: false },
  { title: '第1期 蔡澜 雄狮：成长没有标准答案', image: poster(13), active: false },
  { title: '第2期 黄健翔 马昕宇 潘采夫：热爱之外', image: poster(14), active: true }
]

const sideVideos = [
  '冲击世界杯任重道远，足球路遇瓶颈仍沉淀',
  '中国足球不缺好苗子，大众体育蓬勃带起体系',
  '昔日冠军人才断层，意大利足球的“整活”',
  '亚洲足坛迎来崛起，举国培养与对外交流双驱动',
  '九十分钟赛场硝烟，马明宇回忆世界杯',
  '状况没有标准答案，赵冬梅坦言儿子受益',
  '重新拾起书本开始学习，北大谈变成人生新知识改变命运',
  '学会换掉孩子，赵冬梅细心观察孩子的另一面',
  '把目光定得低一点，蔡澜建议看自我安慰的方法',
  '长寿哪一招优秀到底，动画“舍几子和学校”',
  '蔡澜继续坐镇解惑：成长，是一场取舍与奔赴'
]

const displayDanmaku = computed(() => danmakus.value.slice(0, 3))

const load = async () => {
  try {
    video.value = { ...video.value, ...(await fetchVideoDetail(route.params.id)) }
    await playAuth(route.params.id)
    danmakus.value = await fetchDanmaku(route.params.id)
    plans.value = await fetchMembershipPlans()
  } catch {
    danmakus.value = [
      { id: 1, content: '好喜欢这一季的访谈节奏' },
      { id: 2, content: '这一段值得反复看' },
      { id: 3, content: '人物纪录片的质感很足' }
    ]
  }
  store.remember(video.value)
}

const favorite = async () => {
  try {
    await toggleFavorite(route.params.id)
  } finally {
    store.saveFavorite(video.value)
  }
}

const sendDanmaku = async (content) => {
  if (!content.trim()) return
  try {
    const created = await submitDanmaku(route.params.id, { content, time_offset: 0, color: '#ffffff' })
    danmakus.value = [...danmakus.value, created]
  } catch {
    danmakus.value = [...danmakus.value, { id: Date.now(), content }]
  }
}

onMounted(async () => {
  await load()
  try {
    const membership = await checkMembership()
    modalOpen.value = video.value.member_only && !membership.active
  } catch {
    modalOpen.value = false
  }
})
</script>

<template>
  <AppShell>
    <div class="play-page">
      <main class="play-left">
        <section class="youku-member-player">
          <div class="video-player-container play-member-cover" :data-vid="video.video_id || 'VIDEO_ID'">
            <div class="member-player-copy">
              <h1>本片为会员专属内容</h1>
              <p>开通会员观看完整视频</p>
              <button type="button" @click="modalOpen = true">
                <span>首3月每月12元</span>
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
          </div>
        </section>

        <section class="play-recommend">
          <h2>为你推荐</h2>
          <div class="play-poster-grid">
            <article v-for="item in recommends" :key="item.id" class="play-poster-card">
              <div class="play-poster-frame">
                <img :src="item.cover" :alt="item.title" />
                <span v-if="item.tag" class="play-card-tag">{{ item.tag }}</span>
                <small>{{ item.meta }}</small>
              </div>
              <h3>{{ item.title }}</h3>
            </article>
          </div>
        </section>
      </main>

      <aside class="play-right">
        <div class="play-tabs">
          <button type="button" class="active">视频</button>
          <button type="button">讨论 1</button>
        </div>

        <section class="play-info">
          <h1>舍得智慧人物 第八季</h1>
          <div class="play-info-meta">赞 739　人称　访谈</div>
          <p>《舍得智慧人物》第八季重磅回归，时间的长河里，什么是人生最幸运的答案？本季节目给出自己的注解：因为热爱...</p>
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

        <section class="play-vip-card">
          <strong>会员特惠 首3月每月12元</strong>
          <p>热剧抢先看　广告特权　帧享影音</p>
          <button type="button" @click="modalOpen = true">立即开通</button>
        </section>

        <section class="play-side-section">
          <div class="side-heading">
            <h2>选集</h2>
            <a href="#">更新至07-16期 〉</a>
          </div>
          <article v-for="(item, index) in episodes" :key="item.title" class="episode-item" :class="{ active: index + 1 === currentEpisode }" @click="currentEpisode = index + 1">
            <img :src="item.image" :alt="item.title" />
            <p>{{ item.title }}</p>
          </article>
        </section>

        <section class="play-side-section">
          <h2>周边视频</h2>
          <article v-for="(item, index) in sideVideos" :key="item" class="around-item">
            <img :src="poster(index + 18)" :alt="item" />
            <div>
              <p>{{ item }}</p>
              <time>0{{ index % 2 }}:{{ ['39', '57', '27', '30', '03', '30', '26', '58', '38', '19', '40'][index] }}</time>
            </div>
          </article>
        </section>
      </aside>
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
