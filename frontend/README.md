# Kooyou Vue Frontend

优酷视频点播项目前端仓库，使用 Vue3 + Vite + Vue Router + Pinia + Axios 搭建。前端只负责页面渲染、交互、播放器容器、弹幕 UI、会员拦截展示和 REST API 调用；视频数据、会员鉴权、弹幕保存、收藏记录等业务由 Django REST 后端提供。

## 技术栈

- Vue3
- Vite
- Vue Router
- Pinia
- Axios
- Vercel

## 视觉规范

所有页面必须严格对齐项目中的优酷原始 HTML 视觉基准和截图基准。

禁止事项：

- 禁止擅自修改优酷原版布局、间距、颜色、圆角、卡片比例和交互层级。
- 禁止删除首页推荐、分类筛选、播放页播放器、会员弹窗、弹幕、收藏、选集、相关推荐等核心模块。
- 禁止使用 base64 或 `data:image` 内嵌图片。
- 禁止把页面改造成营销页、企业官网风格或其他非优酷风格。

核心公共组件：

- `src/components/AppShell.vue`：全站公共 Header 和页面外壳。
- `src/components/VideoCard.vue`：视频卡片。
- `src/components/PlayerBox.vue`：播放器容器。
- `src/components/DanmakuLayer.vue`：弹幕组件。
- `src/components/MemberModal.vue`：会员弹窗。
- `src/components/FilterBar.vue`：分类筛选栏。

## 目录结构

```text
frontend/
├── index.html
├── package.json
├── package-lock.json
├── vercel.json
├── vite.config.js
├── .env.example
├── .gitignore
└── src/
    ├── App.vue
    ├── main.js
    ├── api/
    │   ├── http.js
    │   └── video.js
    ├── assets/
    │   ├── baseline-assets.js
    │   └── youku/
    ├── components/
    ├── router/
    ├── stores/
    ├── styles/
    └── views/
```

## 本地启动教程

进入前端目录：

```bash
cd frontend
```

安装依赖：

```bash
npm install
```

创建本地环境变量：

```bash
cp .env.example .env.local
```

如果 `.env.example` 不存在，手动创建：

```bash
echo "VITE_API_BASE_URL=http://127.0.0.1:8000" > .env.local
```

启动开发服务：

```bash
npm run dev
```

本地访问：

```text
http://127.0.0.1:5174/
```

生产构建检查：

```bash
npm run build
```

## 页面功能说明

### 首页 `/`

- 全站公共 Header。
- 优酷电影频道 Hero 推荐。
- 横向轮播推荐卡片。
- 热门视频分区。
- 新片即将上线。
- 预约按钮。
- VIP 和票房标签。

### 分类页 `/category`

- 全站公共 Header。
- 频道分类筛选。
- 年份、类型、会员条件筛选。
- 视频列表。
- 无限滚动分页加载。
- 侧边热播榜。

### 播放页 `/play/:id`

- 全站公共 Header。
- 播放器容器：

```html
<div class="video-player-container" data-vid="VIDEO_ID"></div>
```

- 会员观看拦截。
- 会员开通卡片。
- 选集切换。
- 弹幕加载和提交。
- 点赞、收藏入口。
- 相关推荐。
- 周边视频。

### 个人中心 `/profile`

- 观看历史。
- 我的收藏。
- 会员中心。
- 本地兜底数据展示。

## 对接后端 API 修改方法

API 基础地址统一由环境变量控制：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

本地开发时指向 Django 本地服务：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

线上部署时指向 Railway 后端：

```env
VITE_API_BASE_URL=https://your-railway-backend.up.railway.app
```

Axios 实例文件：

```text
src/api/http.js
```

视频业务接口封装：

```text
src/api/video.js
```

组件中禁止直接硬编码完整接口地址，必须调用 `src/api/video.js` 导出的请求方法。

常用接口：

- 首页推荐：`fetchRecommendations()`
- 视频列表：`fetchVideos(params)`
- 视频详情：`fetchVideoDetail(id)`
- 播放鉴权：`playAuth(id)`
- 弹幕列表：`fetchDanmaku(id)`
- 弹幕提交：`submitDanmaku(id, payload)`
- 收藏切换：`toggleFavorite(id)`
- 会员校验：`checkMembership()`
- 会员套餐：`fetchMembershipPlans()`

## Vercel 一键部署步骤

1. 将前端仓库推送到 GitHub。
2. 登录 Vercel。
3. 点击 `Add New Project`。
4. 选择前端 GitHub 仓库。
5. 设置项目根目录为前端目录。
6. 设置构建命令：

```bash
npm run build
```

7. 设置输出目录：

```text
dist
```

8. 添加环境变量：

```env
VITE_API_BASE_URL=https://your-railway-backend.up.railway.app
```

9. 点击 Deploy。

`vercel.json` 已配置 SPA 路由回退和静态资源缓存，刷新 `/category`、`/play/:id`、`/profile` 不应出现 404。

## 开发提交前检查

```bash
npm run build
git status --short
```

视觉相关修改还必须更新根目录 `design-qa.md`。
