# Kooyou

基于优酷视频站视觉基准的前后端分离视频点播项目。本阶段后端只提供 Django REST API 与 SimpleUI 管理后台，页面渲染全部交给独立 Vue 前端。

## 后端能力

- 视频资源、视频分类、会员套餐、用户会员、评论、弹幕、收藏、上传记录模型
- SimpleUI 中文后台，支持封面图和视频文件上传、搜索、筛选、排序、分页、批量编辑
- RESTful API： 首页推荐、分类筛选、视频详情、播放鉴权、弹幕提交、收藏、会员校验、后台上传
- CORS 支持本地 Vite 与 Vercel 前端域名

## 前端能力

- Vue3 + Vite + Vue Router + Pinia + Axios 独立前端
- 基于第一阶段优酷静态 HTML 视觉基准复刻首页、分类页、播放页和个人中心
- 对接 Django REST API，使用 `VITE_API_BASE_URL` 管理后端地址
- Vercel 静态部署配置已放在 `frontend/vercel.json`

## 快速启动

```bash
pyenv install 3.12.4
pyenv local 3.12.4
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python scripts/create_superuser.py
python manage.py runserver
```

后台地址：`http://127.0.0.1:8000/admin/`

固定管理员：

- 用户名：`andyduan26`
- 密码：`Ay281988`
- 邮箱：`andyduanxiaoga@163.com`
- 昵称：`钱多多`
