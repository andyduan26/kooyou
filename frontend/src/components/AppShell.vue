<script setup>
import { RouterLink } from 'vue-router'
import { assets } from '@/assets/baseline-assets'

const channels = ['首页', '电视剧', '动漫', '电影', '综艺', '短剧', '会员中心', '少儿', '纪录片', '体育', '人文', '直播', '游戏', '乐学']
</script>

<template>
  <div class="youku-shell">
    <aside class="leftnav_left_box leftnav_left_box_z leftnav_light_on shell-side">
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
              :key="item"
              :to="item === '首页' ? '/' : { path: '/category', query: { channel: item } }"
              class="leftnav_link_item leftnav_link_item_new"
              active-class="leftnav_current_item"
            >
              <span class="leftnav_nav_mark"><span>{{ item }}</span></span>
            </RouterLink>
          </div>
        </div>
      </nav>
    </aside>
    <header class="topheader_top_header_box topheader_top_filter_no shell-top">
      <div class="topheader_left_box"></div>
      <div class="topheader_right_box topheader_left_box_margin topheader_channel">
        <div class="search_search_box">
          <div class="search_search_box_wrap">
            <div class="search_search_input_box">
              <div class="search_search_input_content">
                <input class="search_search_input" placeholder="藏海传" />
              </div>
              <span class="iconfontheader icon-search search_search_icon"></span>
            </div>
          </div>
        </div>
        <RouterLink class="shell-vip" to="/profile">会员特惠</RouterLink>
        <RouterLink class="shell-link" to="/profile">历史</RouterLink>
        <RouterLink class="shell-link" to="/profile">个人中心</RouterLink>
      </div>
    </header>
    <main class="shell-main">
      <slot />
    </main>
  </div>
</template>
