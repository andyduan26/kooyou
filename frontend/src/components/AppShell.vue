<script setup>
import { RouterLink } from 'vue-router'
import { assets } from '@/assets/baseline-assets'

const channels = [
  { name: '首页', to: '/' },
  { name: '电视剧', to: { path: '/category', query: { channel: '电视剧' } } },
  { name: '电影', to: { path: '/category', query: { channel: '电影' } } },
  { name: '综艺', to: { path: '/category', query: { channel: '综艺' } } },
  { name: '分类⌄', to: '/category' }
]
</script>

<template>
  <div class="youku-shell play-shell">
    <header class="site-header play-topbar">
      <RouterLink to="/" class="site-header-logo play-topbar-logo">
        <img :src="assets.logo" alt="优酷" />
      </RouterLink>
      <nav class="site-header-nav">
        <RouterLink v-for="item in channels" :key="item.name" class="play-topbar-link" :to="item.to">
          {{ item.name }}
        </RouterLink>
      </nav>
      <div class="site-header-spacer"></div>
      <div class="play-topbar-search">
        <input placeholder="当我飞奔向你" />
        <span>⌕</span>
      </div>
      <RouterLink class="play-topbar-vip" to="/profile">会员特惠</RouterLink>
      <RouterLink class="play-topbar-icon" to="/profile">◷<span>历史</span></RouterLink>
      <RouterLink class="play-topbar-icon" to="/profile">▱<span>客户端</span></RouterLink>
      <RouterLink class="play-topbar-login" to="/profile">登录</RouterLink>
    </header>
    <main class="shell-main">
      <slot />
    </main>
  </div>
</template>
