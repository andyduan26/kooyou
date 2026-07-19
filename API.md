# API

所有接口返回统一 JSON：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

## 视频

- `GET /api/videos/home-recommend/` 首页推荐
- `GET /api/videos/?channel=movie&category=1&keyword=龙&member_only=false` 分类筛选
- `GET /api/videos/{id}/` 视频详情
- `POST /api/videos/{id}/play-auth/` 视频播放鉴权，登录后调用

## 弹幕与评论

- `GET /api/videos/{id}/danmaku/` 弹幕列表
- `POST /api/videos/{id}/danmaku/` 提交弹幕
- `GET /api/videos/{id}/comments/` 评论列表
- `POST /api/videos/{id}/comments/` 提交评论，登录后调用

## 收藏

- `POST /api/videos/{id}/favorite/` 收藏视频，登录后调用
- `DELETE /api/videos/{id}/favorite/` 取消收藏，登录后调用

## 会员

- `GET /api/membership-plans/` 会员套餐
- `GET /api/membership/check/` 会员校验，登录后调用

## 后台上传

- `POST /api/admin/videos/upload/` 后台视频上传，仅管理员可用，`multipart/form-data`

字段：

- `video_id`
- `title`
- `cover`
- `video_file`
- `play_url`
- `category`
- `duration`
- `member_only`
- `episode_count`
- `is_recommended`
- `is_published`
