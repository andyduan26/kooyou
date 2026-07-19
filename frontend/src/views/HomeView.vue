<script setup>
import AppShell from '@/components/AppShell.vue'
import { assets } from '@/assets/baseline-assets'

const heroCards = [
  ['新上线', '10间敢死队', '预告'],
  ['', '香港奇案', 'VIP'],
  ['新上线', '喜羊羊与灰太狼', '首播'],
  ['', '连城诀经典荧幕', ''],
  ['新上线', '荒蛮异形', '首播']
]

const rowTitles = [
  '正在热播',
  '“影”领一夏！好片看不停',
  '新片·即将上线',
  '浴血奋战·国产战争片',
  '高票房喜剧电影',
  '院线最新预告首发',
  '神秘东南亚·犯罪电影',
  '含泪呐喊！我要我的祖国'
]

const names = [
  ['哈利·波特与魔法石', '鬼吹灯之南海归墟', '龙在少林', '致胜王牌', '新喜剧之王', '默杀'],
  ['第二十条', '飞驰人生2', '长安的荔枝', '封神第一部：朝歌风云', '镖人：风起大漠', '蛟龙行动'],
  ['开往悬崖的火车', '断魂剑', '功夫女足', '想你了', '给阿嬷的情书', '小康路上'],
  ['东溪突击', '铁道英雄', '八佰', '红巴山', '绝地重生', '勇士连'],
  ['热辣滚烫', '前任4：英年早婚', '年会不能停！', '这个杀手不太冷静', '独行月球', '人生路不熟'],
  ['《群星闪耀时》预告', '侏罗纪世界重生', '周深献唱片尾曲', '蜘蛛侠全新预告', '捕风追影预告', '奇遇预告'],
  ['消失的她', '孤注一掷', '烈探', '误杀2', '默杀', '再见吧'],
  ['苍狼之浴血绝杀', '坚守1200秒', '烽火地雷战', '浴血狙击', '雪豹之虎啸军魂', '赤焰']
]

const subtitles = [
  ['', '', '', '', '', ''],
  ['', '', '', '', '', ''],
  ['今天16:00上线', '明天10:00上线', '敬请期待', '敬请期待', '敬请期待', ''],
  ['', '', '', '', '', ''],
  ['', '', '', '', '', ''],
  ['0:25', '0:30', '4:22', '1:22', '', ''],
  ['', '', '', '', '', ''],
  ['', '', '', '', '', '']
]

const posterAt = (index) => assets.posters[index % assets.posters.length]
</script>

<template>
  <AppShell>
    <section class="yk-movie-hero">
      <img class="movie-hero-bg" :src="assets.hero[1]" alt="10间敢死队" />
      <div class="movie-hero-shade"></div>
      <div class="movie-hero-info">
        <h1>10间敢死队</h1>
        <div class="hero-meta"><span>首播</span><span>电影</span></div>
        <p>素金·宋朝｜霸气男团勇敢救家族，该他们帮小兵遇上拼命求生的他们，展开生死大厮！</p>
        <strong>NEW 新上线</strong>
        <RouterLink to="/play/1" class="hero-play">播放</RouterLink>
      </div>
      <div class="hero-poster-strip">
        <RouterLink v-for="(item, index) in heroCards" :key="item[1]" :to="`/play/${index + 1}`" class="hero-mini" :class="{ active: index === 0 }">
          <img :src="posterAt(index)" :alt="item[1]" />
          <b v-if="item[0]">{{ item[0] }}<small>NEW</small></b>
          <em v-if="item[2]">{{ item[2] }}</em>
          <span>{{ item[1] }}</span>
        </RouterLink>
      </div>
    </section>

    <section class="movie-row" v-for="(title, rowIndex) in rowTitles" :key="title">
      <h2>{{ title }}</h2>
      <div class="movie-card-grid" :class="{ trailers: rowIndex === 5 }">
        <RouterLink
          v-for="(name, index) in names[rowIndex]"
          :key="`${title}-${name}`"
          :to="`/play/${rowIndex}-${index}`"
          class="movie-poster-card"
        >
          <div class="poster-frame">
            <img :src="posterAt(rowIndex * 6 + index + 5)" :alt="name" />
            <b v-if="rowIndex !== 5">{{ index % 3 === 0 ? '票房破' : index % 3 === 1 ? '豆瓣' : '全独播' }}<small>{{ index % 2 ? '33亿' : '9.2分' }}</small></b>
            <em v-if="index % 2 === 0">VIP</em>
            <i v-if="rowIndex === 5">{{ subtitles[rowIndex][index] }}</i>
          </div>
          <strong>{{ name }}</strong>
          <span v-if="subtitles[rowIndex][index]">{{ subtitles[rowIndex][index] }}</span>
          <button v-if="rowIndex === 2" type="button">预约｜{{ ['5102人', '6236人', '19.1万人', '5.0万人', '73.8万人', ''][index] }}</button>
        </RouterLink>
      </div>
    </section>
  </AppShell>
</template>
