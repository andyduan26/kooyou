# Kooyou Django Backend

优酷视频点播项目 Django REST 后端仓库，负责视频资源管理、分类筛选、播放鉴权、会员套餐、弹幕、评论、收藏、上传记录和 SimpleUI 中文后台。页面渲染全部交给独立 Vue 前端，Django 不提供模板页面。

## 技术栈

- Python 3.12
- Django 最新 LTS
- Django REST Framework
- django-simpleui
- django-cors-headers
- django-filter
- Pillow
- gunicorn
- python-multipart
- SQLite 开发数据库
- PostgreSQL 生产数据库
- Railway 部署

## 项目结构

```text
.
├── manage.py
├── requirements.txt
├── railway.json
├── Procfile
├── kooyou_backend/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── video/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   ├── tests.py
│   └── migrations/
├── scripts/
│   └── create_superuser.py
├── media/
├── staticfiles/
└── frontend/
```

如果后续拆分为独立后端仓库，可以移除 `frontend/`，但不得移除 Django 后端、API、SimpleUI 后台、部署配置和管理员初始化脚本。

## 本地虚拟环境搭建步骤

进入项目根目录：

```bash
cd /Users/andyduan26/Documents/优酷2.0
```

安装 Python 3.12：

```bash
brew install python@3.12
```

创建虚拟环境：

```bash
python3.12 -m venv .venv
```

激活虚拟环境：

```bash
source .venv/bin/activate
```

升级 pip：

```bash
python -m pip install --upgrade pip
```

安装依赖：

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

启动开发服务器：

```bash
python manage.py runserver 127.0.0.1:8000
```

后端检查：

```bash
python manage.py check
python manage.py test
```

## SimpleUI 中文后台

后台地址：

```text
http://127.0.0.1:8000/admin/
```

后台 UI：

- 使用 django-simpleui。
- 默认语言为简体中文。
- 用于管理视频资源、视频分类、会员套餐、评论、弹幕、收藏和上传记录。

固定管理员账号：

```text
用户名：andyduan26
密码：Ay281988
邮箱：andyduanxiaoga@163.com
后台显示昵称：钱多多
```

管理员使用说明：

- 本账号是项目固定超级管理员账号。
- 初始化脚本为 `scripts/create_superuser.py`。
- AI 辅助开发不得擅自修改、删除、禁用该账号。
- 生产上线后如需修改密码，必须由项目所有者明确要求。

## 后台视频上传操作指南

1. 启动后端服务：

```bash
python manage.py runserver 127.0.0.1:8000
```

2. 打开后台：

```text
http://127.0.0.1:8000/admin/
```

3. 使用固定管理员登录：

```text
andyduan26 / Ay281988
```

4. 进入视频分类管理，先创建分类：

- 电影
- 剧集
- 动漫
- 综艺

5. 进入视频资源管理，新增视频：

- 填写视频标题。
- 上传封面图。
- 填写播放地址或上传视频文件。
- 选择分类。
- 填写时长。
- 设置播放量。
- 设置是否会员限制。
- 设置选集集数。
- 保存。

6. 如需管理评论、弹幕、收藏记录、上传记录，在对应后台模型中搜索、筛选、排序、分页查看。

7. 视频文件和封面图会进入 `media/` 目录，开发环境不要把真实大视频文件提交到 Git。

## REST API

基础地址：

```text
http://127.0.0.1:8000/api/
```

常用接口：

- 首页推荐：`GET /api/videos/recommendations/`
- 分类筛选：`GET /api/videos/`
- 视频详情：`GET /api/videos/{id}/`
- 播放鉴权：`GET /api/videos/{id}/play-auth/`
- 弹幕列表：`GET /api/videos/{id}/danmaku/`
- 弹幕提交：`POST /api/videos/{id}/danmaku/`
- 收藏切换：`POST /api/videos/{id}/favorite/`
- 会员校验：`GET /api/membership/check/`
- 会员套餐：`GET /api/membership/plans/`
- 后台视频上传：`POST /api/admin/videos/upload/`

前端通过环境变量 `VITE_API_BASE_URL` 指向本后端。

## CORS 配置

开发环境允许：

```text
http://127.0.0.1:5174
http://localhost:5174
```

生产环境必须配置 Vercel 前端域名：

```text
https://your-vercel-frontend.vercel.app
```

禁止生产环境无理由开放全部来源。

## Railway 部署教程

### 1. 准备 GitHub 仓库

确保代码已推送到 GitHub：

```bash
git status --short
git push origin main
```

### 2. Railway 创建项目

1. 登录 Railway。
2. 点击 `New Project`。
3. 选择 `Deploy from GitHub repo`。
4. 选择后端仓库。
5. 添加 PostgreSQL 服务。

### 3. 配置环境变量

Railway 后端服务需要配置：

```env
DJANGO_SECRET_KEY=your-production-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-backend.up.railway.app
DATABASE_URL=postgresql://...
CORS_ALLOWED_ORIGINS=https://your-vercel-frontend.vercel.app
```

### 4. 部署配置

`Procfile`：

```text
web: gunicorn kooyou_backend.wsgi:application
```

`railway.json`：

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn kooyou_backend.wsgi:application",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 5. 执行线上迁移

在 Railway 控制台执行：

```bash
python manage.py migrate
```

### 6. 创建线上管理员

在 Railway 控制台执行：

```bash
python scripts/create_superuser.py
```

创建后使用：

```text
用户名：andyduan26
密码：Ay281988
```

登录：

```text
https://your-backend.up.railway.app/admin/
```

### 7. 前端接入后端

在 Vercel 前端项目中配置：

```env
VITE_API_BASE_URL=https://your-backend.up.railway.app
```

重新部署 Vercel 前端。

## .gitignore 过滤范围

后端仓库 `.gitignore` 必须过滤：

- Mac 系统隐藏文件。
- 编辑器缓存。
- Python 虚拟环境。
- Python 编译缓存。
- SQLite 数据库文件。
- Django `media/` 上传内容。
- Django `staticfiles/` 收集产物。
- 视频上传缓存。
- 日志文件。
- 前端 `node_modules/` 和 `dist/`。
- Vercel、Railway、Netlify 本地缓存。

## 开发提交前检查

后端修改：

```bash
python manage.py check
python manage.py test
```

文档修改：

```bash
git diff --check
```

提交：

```bash
git add .
git commit -m "docs: update backend repository docs"
git push origin main
```
