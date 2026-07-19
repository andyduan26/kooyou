# 优酷视频点播项目 AI 开发约束文档

本文档是本项目后续所有 AI 辅助开发、代码迭代、功能新增、页面修改、接口扩展、部署维护的最高约束。任何代码生成、重构、修复、样式调整、接口变更、数据库迁移都必须先阅读并遵守本文档。

## 1. 项目整体架构说明

本项目是基于优酷视频站点视觉基准搭建的前后端分离视频点播系统。

整体架构固定为：

- 前端：Vue3 + Vite + Vue Router + Pinia + Axios。
- 前端部署：Vercel 静态站点部署。
- 后端：Django 最新 LTS + Django REST Framework。
- 后端部署：Railway。
- 开发数据库：SQLite。
- 生产数据库：PostgreSQL。
- 后台管理：Django Admin + django-simpleui，后台语言为简体中文。
- 页面渲染：全部交给独立 Vue 前端，Django 禁止承担模板页面渲染职责。
- 接口通信：Vue 前端通过 Axios 请求 Django REST API。
- 视频资源：后端负责视频、封面、分类、会员、弹幕、收藏、评论等业务数据管理；前端负责播放器容器、播放鉴权状态展示和交互。

当前仓库包含：

- 根目录静态视觉基准：`index.html`、`category.html`、`play.html`、`style.css`、`base.js`、`assets/`、`assets清单.txt`。
- Django 后端：`manage.py`、`kooyou_backend/`、`video/`、`requirements.txt`、`railway.json`、`Procfile`。
- Vue 前端：`frontend/`。
- 项目文档：`README.md`、`INSTALL.md`、`API.md`、`CHANGELOG.md`、`design-qa.md`。

任何阶段都不得随意改变技术栈，不得将前后端合并为 Django 模板项目，不得将 Vue 页面逻辑迁移到后端模板。

## 2. 视觉复刻强制规范

本项目的视觉目标是 1:1 对齐原始优酷页面和已清洗 HTML 基准。所有页面修改必须以原始优酷视觉为最高标准。

强制要求：

- 首页、分类页、播放页必须对齐原始优酷 HTML 基准和截图基准。
- 禁止擅自重构原始布局层级。
- 禁止擅自删减页面模块。
- 禁止擅自美化、改色、改圆角、改间距、改卡片比例、改字体层级。
- 禁止把优酷暗色视觉改成其他品牌风格。
- 禁止为了实现方便而简化播放器、会员弹窗、弹幕、选集、推荐列表、筛选栏、分页、卡片 hover 等模块。
- 禁止把图片资源改回 base64。
- 禁止使用 `[REMOVED_BASE64_IMG]`、`[BASE64_ASSET]`、`data:image`、内嵌 base64 图片。
- 所有图片、图标、封面、背景图必须存放在外部资源目录。

视觉基准文件：

- 首页基准：根目录 `index.html`、`style.css`、`assets/`，以及对应截图基准。
- 分类页基准：根目录 `category.html`、`style.css`、`assets/`，以及对应截图基准。
- 播放页基准：根目录 `play.html`、`style.css`、`assets/`，以及对应截图基准。
- 视觉 QA 记录：`design-qa.md`。

全站公共 UI 约束：

- Header 必须全站共用同一个组件。
- 导航、底部、视频卡片、会员按钮、播放按钮、弹幕区域、选集区域、推荐视频卡片必须保持统一 class 语义和统一视觉参数。
- 页面之间不得出现不同的卡片宽高、圆角、阴影、字体大小、颜色值和 hover 效果，除非原始优酷页面基准明确不同。
- 当前全站公共 Header 位于 `frontend/src/components/AppShell.vue`，样式位于 `frontend/src/styles/global.css`。

播放器占位标准：

```html
<div class="video-player-container" data-vid="VIDEO_ID"></div>
```

如需绑定真实视频，允许由 Vue 组件动态设置 `data-vid`，但不得删除 `video-player-container` 语义。

视觉修改流程：

1. 先查看原始 HTML 基准和截图基准。
2. 再查看现有 Vue 页面和公共样式。
3. 只做与需求相关的最小修改。
4. 修改后必须本地打开页面检查。
5. 必须运行 `npm run build`。
6. 必须更新 `design-qa.md` 记录本次视觉检查结果。

## 3. 前端 Vue 编码规范

前端目录固定为 `frontend/`。

技术栈固定：

- Vue3。
- Vite。
- Vue Router。
- Pinia。
- Axios。
- Composition API。
- `<script setup>`。

目录职责：

- `frontend/src/main.js`：Vue 应用入口。
- `frontend/src/App.vue`：根应用组件。
- `frontend/src/router/index.js`：路由配置。
- `frontend/src/stores/`：Pinia 状态管理。
- `frontend/src/api/`：Axios 实例和 API 请求封装。
- `frontend/src/components/`：可复用业务组件。
- `frontend/src/views/`：页面级组件。
- `frontend/src/assets/`：前端静态资源。
- `frontend/src/assets/youku/`：从优酷 HTML 基准提取或复刻使用的图片、图标、字体等资源。
- `frontend/src/styles/global.css`：全站公共样式。
- `frontend/src/styles/baseline.css`：基准样式承接文件。

组件命名规范：

- 页面组件使用 `XxxView.vue`，例如 `HomeView.vue`、`CategoryView.vue`、`PlayView.vue`、`ProfileView.vue`。
- 业务组件使用 PascalCase，例如 `AppShell.vue`、`VideoCard.vue`、`PlayerBox.vue`、`DanmakuLayer.vue`、`MemberModal.vue`、`FilterBar.vue`。
- 组件名必须表达业务含义，禁止使用 `Box1.vue`、`NewComponent.vue`、`Test.vue` 等临时命名。

静态资源规范：

- 所有图片必须放入 `frontend/src/assets/` 或其子目录。
- 优酷视觉复刻相关图片统一放入 `frontend/src/assets/youku/`。
- 禁止在 Vue 文件、CSS 文件、JS 文件中写入 base64 图片。
- 禁止使用远程不稳定图片链接作为核心视觉资产。
- `frontend/src/assets/baseline-assets.js` 用于集中导入和导出基准图片资源。
- 新增封面图、背景图、图标后，应同步维护资源清单或说明。

路由规范：

- 首页路由：`/`。
- 分类页路由：`/category`。
- 播放页路由：`/play/:id`。
- 个人中心路由：`/profile`。
- 所有页面必须通过 Vue Router 管理。
- 禁止直接使用多份独立 HTML 替代 Vue Router 页面。

接口请求规范：

- 所有 HTTP 请求必须通过 `frontend/src/api/http.js` 中的 Axios 实例。
- 所有视频业务请求必须封装在 `frontend/src/api/video.js` 或同级业务 API 文件。
- API 基础地址必须读取环境变量：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

- 禁止在组件中散落硬编码完整后端地址。
- 组件中只调用封装后的 API 方法。
- API 错误必须有前端兜底数据或可理解的空状态，避免页面白屏。

播放器组件规范：

- 播放器核心组件必须保留 `video-player-container` 容器。
- 会员限制视频必须展示会员拦截态。
- 已鉴权视频可以使用原生 `<video>` 或后续接入正式播放器 SDK。
- 播放器区域不得因为接口失败而消失。
- 播放页必须保留相关推荐、选集、会员开通入口、点赞收藏入口。

弹幕组件规范：

- 弹幕组件必须独立封装。
- 弹幕列表通过接口加载。
- 弹幕提交通过接口提交。
- 接口失败时允许本地临时追加弹幕，但不得破坏页面。
- 弹幕输入、弹幕轨道、弹幕展示区域必须保留。

会员弹窗规范：

- 会员弹窗必须独立封装。
- 播放鉴权失败或用户非会员访问会员视频时必须可触发。
- 弹窗必须展示会员套餐信息。
- 弹窗关闭、开通按钮、会员权益信息必须保留。

视频卡片规范：

- 视频卡片必须组件化。
- 卡片必须支持封面图、标题、播放量、会员标识。
- 卡片比例、圆角、文字颜色、hover 效果必须与优酷基准一致。
- 不得在不同页面复制出多套视觉不一致的视频卡片。

## 4. 后端 Django 编码规范

后端目录固定在仓库根目录 Django 项目内。

技术栈固定：

- Django 最新 LTS。
- Django REST Framework。
- django-simpleui。
- django-cors-headers。
- django-filter。
- Pillow。
- gunicorn。
- python-multipart。
- SQLite 开发环境。
- PostgreSQL 生产环境。

Django 主项目：

- `kooyou_backend/`。

视频业务 APP：

- `video/`。

数据模型必须完整覆盖以下业务：

- 视频资源。
- 视频分类。
- 用户。
- 会员套餐。
- 用户评论。
- 弹幕。
- 收藏记录。
- 上传记录。

所有业务模型必须包含：

- `id` 主键，使用 `AutoField`。
- `created_at`。
- `updated_at`。

视频表必须包含：

- 视频 ID。
- 标题。
- 封面图。
- 播放地址。
- 分类 ID。
- 时长。
- 播放量。
- 会员限制。
- 上传时间。
- 选集集数。

视频分类表必须支持：

- 电影。
- 剧集。
- 动漫。
- 综艺。
- 后续扩展频道。

REST API 命名规范：

- 首页推荐：`GET /api/videos/recommendations/`。
- 分类筛选：`GET /api/videos/`。
- 视频详情：`GET /api/videos/{id}/`。
- 视频播放鉴权：`GET /api/videos/{id}/play-auth/`。
- 弹幕列表：`GET /api/videos/{id}/danmaku/`。
- 弹幕提交：`POST /api/videos/{id}/danmaku/`。
- 收藏切换：`POST /api/videos/{id}/favorite/`。
- 会员校验：`GET /api/membership/check/`。
- 会员套餐：`GET /api/membership/plans/`。
- 后台视频上传接口：`POST /api/admin/videos/upload/` 或当前后端既有等价接口。

接口返回规范：

- 返回 JSON。
- RESTful 方法语义清晰。
- 列表接口支持分页。
- 分类接口支持筛选。
- 错误响应必须包含可读错误信息。
- 不得让接口直接返回 HTML 模板。

SimpleUI 后台规范：

- 必须启用 django-simpleui。
- 后台语言必须为简体中文。
- 视频资源、视频分类、会员套餐、用户评论、弹幕、上传记录必须注册后台。
- 后台列表必须支持搜索、分页、排序、过滤。
- 视频资源后台必须支持封面图和视频文件上传。
- 常用字段必须支持批量编辑。
- 管理后台不允许移除超级管理员入口。

固定超级管理员规范：

- 用户名：`andyduan26`。
- 密码：`Ay281988`。
- 邮箱：`andyduanxiaoga@163.com`。
- 后台显示昵称：`钱多多`。

后续初始化脚本不得更改以上账号信息，除非用户明确要求。

视频上传处理规则：

- 封面图必须使用 ImageField 或等价处理方式。
- 视频文件必须使用 FileField 或等价处理方式。
- 上传路径必须按业务分类清晰管理。
- 不得把大视频文件提交进 Git 仓库。
- 开发环境媒体文件存放在 `media/`。
- 生产环境应使用 Railway 持久化方案或对象存储方案。

## 5. 本地完整启动流程

### 5.1 后端 Django 启动

进入项目根目录：

```bash
cd /Users/andyduan26/Documents/优酷2.0
```

创建 Python 虚拟环境：

```bash
python3.12 -m venv .venv
```

如果本机没有 Python 3.12，先安装兼容版本：

```bash
brew install python@3.12
```

激活虚拟环境：

```bash
source .venv/bin/activate
```

升级 pip：

```bash
python -m pip install --upgrade pip
```

安装后端依赖：

```bash
pip install -r requirements.txt
```

执行数据库迁移：

```bash
python manage.py migrate
```

创建固定超级管理员：

```bash
python scripts/create_superuser.py
```

启动后端：

```bash
python manage.py runserver 127.0.0.1:8000
```

检查后端：

```bash
python manage.py check
python manage.py test
```

后台地址：

```text
http://127.0.0.1:8000/admin/
```

API 地址：

```text
http://127.0.0.1:8000/api/
```

### 5.2 前端 Vue 启动

进入前端目录：

```bash
cd /Users/andyduan26/Documents/优酷2.0/frontend
```

安装依赖：

```bash
npm install
```

配置本地环境变量：

```bash
cp .env.example .env.local
```

如果不存在 `.env.example`，手动创建 `.env.local`：

```bash
echo "VITE_API_BASE_URL=http://127.0.0.1:8000" > .env.local
```

启动前端：

```bash
npm run dev
```

本地访问：

```text
http://127.0.0.1:5174/
```

前端构建检查：

```bash
npm run build
```

### 5.3 联调顺序

推荐顺序：

1. 启动 Django 后端 `127.0.0.1:8000`。
2. 启动 Vue 前端 `127.0.0.1:5174`。
3. 打开首页 `/`。
4. 打开分类页 `/category`。
5. 打开播放页 `/play/1`。
6. 检查播放鉴权、弹幕提交、收藏、会员弹窗。

## 6. Git & GitHub 仓库规范

当前 GitHub 仓库：

```text
git@github.com:andyduan26/kooyou.git
```

远程仓库页面：

```text
https://github.com/andyduan26/kooyou.git
```

分仓规范：

- 目标架构允许前后端分仓管理。
- 当前阶段为同一仓库内前后端分目录管理。
- 如果后续拆分仓库，前端仓库只保留 `frontend/` 相关代码，后端仓库只保留 Django 相关代码。
- 拆分前必须保证部署配置、环境变量和 README 同步更新。

提交规范：

- 每完成一个独立功能必须提交。
- 每次提交前必须检查 `git status --short`。
- 每次提交前必须运行对应测试或构建。
- 每次提交后必须推送到 GitHub。

Commit Message 规范：

- 新功能：`feat: 描述`
- 修复：`fix: 描述`
- 文档：`docs: 描述`
- 重构：`refactor: 描述`
- 样式调整：`fix: 描述` 或 `refactor: 描述`
- 部署配置：`docs:` 或 `feat:`，按实际内容选择。

示例：

```bash
git add .
git commit -m "docs: add ai development constraints"
git push origin main
```

分支规范：

- 默认稳定分支：`main`。
- AI 开发临时分支建议使用 `codex/` 前缀。
- 示例：`codex/video-upload-api`、`codex/play-page-polish`。
- 未经用户要求，不得强制重置 `main`。
- 禁止使用 `git reset --hard`、`git checkout -- .` 删除用户改动，除非用户明确要求。
- 发现非本人改动时，必须保留并基于现状增量开发。

## 7. 上线部署标准

### 7.1 Vercel 前端部署

前端部署目录：

```text
frontend/
```

Vercel 构建命令：

```bash
npm run build
```

Vercel 输出目录：

```text
frontend/dist
```

前端环境变量：

```env
VITE_API_BASE_URL=https://你的-railway-后端域名
```

Vercel 路由要求：

- 必须保留 SPA history fallback。
- 刷新 `/category`、`/play/:id`、`/profile` 不得 404。
- 静态资源应配置缓存。
- 配置文件：`frontend/vercel.json`。

部署前检查：

```bash
cd frontend
npm install
npm run build
```

### 7.2 Railway 后端部署

Railway 配置文件：

- `railway.json`。
- `Procfile`。
- `requirements.txt`。

Railway 启动命令应通过 gunicorn 启动 Django：

```bash
gunicorn kooyou_backend.wsgi:application
```

生产环境变量必须包含：

```env
DJANGO_SECRET_KEY=生产密钥
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=你的-railway-后端域名
DATABASE_URL=Railway PostgreSQL 地址
CORS_ALLOWED_ORIGINS=https://你的-vercel-前端域名
```

生产部署步骤：

1. Railway 连接 GitHub 仓库。
2. 配置 PostgreSQL。
3. 配置环境变量。
4. 部署 Django 服务。
5. 执行数据库迁移。
6. 创建线上超级管理员。
7. 配置 Vercel `VITE_API_BASE_URL` 指向 Railway 后端。
8. 重新部署 Vercel 前端。

线上迁移命令：

```bash
python manage.py migrate
```

线上创建管理员：

```bash
python scripts/create_superuser.py
```

线上管理员使用规范：

- 固定账号：`andyduan26`。
- 固定邮箱：`andyduanxiaoga@163.com`。
- 后台昵称：`钱多多`。
- 初始密码：`Ay281988`。
- 生产上线后如需改密，只能由项目所有者明确要求执行。
- AI 不得擅自修改、删除、禁用该管理员账号。

### 7.3 CORS 标准

后端必须允许 Vercel 前端域名跨域访问 API。

开发环境可允许：

```text
http://127.0.0.1:5174
http://localhost:5174
```

生产环境必须配置：

```text
https://你的-vercel-前端域名
```

禁止生产环境无限制开放所有来源，除非用户明确要求临时排查问题。

## 8. AI 辅助开发硬性约束

所有 AI 辅助开发必须遵守以下硬性规则。

### 8.1 修改前必须做的事

任何代码修改前必须：

1. 阅读本 `agent.md`。
2. 查看当前 `git status --short`。
3. 查看相关文件现状。
4. 明确本次修改范围。
5. 确认不会破坏既有页面、接口、后台和部署配置。

### 8.2 禁止事项

AI 严禁：

- 删除已经正常工作的代码。
- 重建项目。
- 更换技术栈。
- 把 Vue 前端改成 Django 模板。
- 把 Django 后端改成其他框架。
- 删除视频播放模块。
- 删除会员模块。
- 删除弹幕模块。
- 删除收藏模块。
- 删除分类筛选模块。
- 删除 SimpleUI 后台。
- 删除超级管理员创建脚本。
- 删除部署配置。
- 删除优酷静态视觉基准文件。
- 擅自修改全站视觉风格。
- 擅自改变页面布局。
- 擅自替换为营销落地页、企业官网风格、卡通风格、渐变风格、玻璃风格或其他非优酷风格。
- 使用 base64 内嵌图片。
- 把大体积视频文件提交到 Git。
- 使用破坏性 Git 命令覆盖用户改动。

### 8.3 必须保留的核心业务模块

前端必须保留：

- 首页推荐。
- 分类筛选。
- 播放页播放器容器。
- 播放鉴权。
- 会员弹窗。
- 弹幕列表。
- 弹幕提交。
- 收藏。
- 点赞入口。
- 选集切换。
- 相关推荐。
- 个人中心。

后端必须保留：

- 视频资源模型。
- 视频分类模型。
- 会员套餐模型。
- 评论模型。
- 弹幕模型。
- 收藏模型。
- 上传记录模型。
- REST API。
- SimpleUI 后台。
- CORS 配置。
- Railway 部署配置。

### 8.4 开发完成标准

每次阶段完成前必须执行：

前端相关修改：

```bash
cd frontend
npm run build
```

后端相关修改：

```bash
python manage.py check
python manage.py test
```

文档相关修改：

```bash
git diff --check
```

视觉相关修改：

- 本地打开对应页面。
- 对照优酷基准截图或 HTML。
- 更新 `design-qa.md`。

### 8.5 输出与交付规范

每个阶段完成后必须向用户说明：

- 完成内容。
- 修改文件。
- 新增文件。
- 验证命令。
- Commit 内容。
- GitHub 推送状态。

如果某项验证无法执行，必须明确说明原因，不得假装通过。

### 8.6 增量开发原则

后续所有需求都按阶段完成：

- 一次只完成一个明确阶段。
- 优先保证项目可运行。
- 优先复用现有组件、样式、接口、模型。
- 不做无关重构。
- 不做大范围格式化。
- 不改无关文件。
- 不覆盖用户未提交改动。

本项目的长期目标是维护一个可持续迭代的商业级优酷风格视频点播系统，而不是一次性生成演示代码。
