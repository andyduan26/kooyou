<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { assets } from '@/assets/baseline-assets'

const route = useRoute()
const isPlayPage = computed(() => route.name === 'play')

const channels = [
  { name: '首页', icon: assets.navPublic },
  { name: '光阴之外', icon: assets.navLive },
  { name: '电视剧', icon: assets.navMovie },
  { name: '动漫', icon: assets.navPublic },
  { name: '电影', icon: assets.navMovie },
  { name: '综艺', icon: assets.navLive },
  { name: '短剧', icon: assets.navPublic },
  { name: '会员中心', icon: assets.navMovie },
  { name: '少儿', icon: assets.navPublic },
  { name: '纪录片', icon: assets.navLive },
  { name: '体育', icon: assets.navSport, hot: true },
  { name: '人文', icon: assets.navPublic }
]
</script>

<template>
  <div class="youku-shell" :class="{ 'play-shell': isPlayPage }">
    <header v-if="isPlayPage" class="play-topbar">
      <RouterLink to="/" class="play-topbar-logo">
        <img :src="assets.logo" alt="优酷" />
      </RouterLink>
      <RouterLink class="play-topbar-link" to="/">首页</RouterLink>
      <RouterLink class="play-topbar-link" to="/category">分类⌄</RouterLink>
      <div class="play-topbar-search">
        <input placeholder="神奇动物在哪里" />
        <span>⌕</span>
      </div>
      <RouterLink class="play-topbar-vip" to="/profile">会员特惠</RouterLink>
      <RouterLink class="play-topbar-icon" to="/profile">◷<span>历史</span></RouterLink>
      <RouterLink class="play-topbar-icon" to="/profile">▱<span>客户端</span></RouterLink>
      <RouterLink class="play-topbar-login" to="/profile">登录</RouterLink>
    </header>
    <aside v-if="!isPlayPage" class="leftnav_left_box leftnav_left_box_z leftnav_light_on shell-side movie-shell-side">
      <div class="leftnav_left_logo">
        <RouterLink to="/" class="logo_logo_box logo_logo_hover">
          <img class="logo_logo_img" :src="assets.logo" alt="Kooyou" />
        </RouterLink>
      </div>
      <nav class="leftnav_nav_box">
        <div class="leftnav_nav_content">
          <div class="leftnav_nav_inner">
            <RouterLink
              v-for="item in channels"
              :key="item.name"
              :to="item.name === '首页' ? '/' : { path: '/category', query: { channel: item.name } }"
              class="leftnav_link_item leftnav_link_item_new"
              active-class="leftnav_current_item"
            >
              <img class="movie-nav-icon" :src="item.icon" alt="" />
              <span class="leftnav_nav_mark">
                <span>{{ item.name }}</span>
                <em v-if="item.hot">世界杯</em>
              </span>
            </RouterLink>
          </div>
        </div>
      </nav>
    </aside>
    <header v-if="!isPlayPage" class="topheader_top_header_box topheader_top_filter_no shell-top movie-shell-top">
      <div class="topheader_left_box"></div>
      <div class="topheader_right_box topheader_left_box_margin topheader_channel">
        <div class="search_search_box">
          <div class="search_search_box_wrap">
            <div class="search_search_input_box">
              <div class="search_search_input_content">
                <input class="search_search_input" placeholder="王鹤棣" />
              </div>
              <span class="iconfontheader icon-search search_search_icon"></span>
            </div>
          </div>
        </div>
        <RouterLink class="shell-vip" to="/profile">会员特惠</RouterLink>
        <RouterLink class="shell-link" to="/category">筛选</RouterLink>
        <RouterLink class="shell-link" to="/profile">历史</RouterLink>
        <RouterLink class="shell-link" to="/profile">客户端</RouterLink>
        <RouterLink class="shell-login" to="/profile">登录</RouterLink>
      </div>
    </header>
    <main class="shell-main">
      <slot />
    </main>
  </div>
</template>
