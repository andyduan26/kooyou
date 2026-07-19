from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        abstract = True


class VideoCategory(TimeStampedModel):
    CHANNEL_MOVIE = "movie"
    CHANNEL_SERIES = "series"
    CHANNEL_ANIME = "anime"
    CHANNEL_VARIETY = "variety"
    CHANNEL_CHOICES = [
        (CHANNEL_MOVIE, "电影"),
        (CHANNEL_SERIES, "剧集"),
        (CHANNEL_ANIME, "动漫"),
        (CHANNEL_VARIETY, "综艺"),
    ]

    name = models.CharField("分类名称", max_length=50, unique=True)
    channel = models.CharField("频道分类", max_length=20, choices=CHANNEL_CHOICES, db_index=True)
    sort_order = models.PositiveIntegerField("排序", default=0)
    is_active = models.BooleanField("启用", default=True)

    class Meta:
        verbose_name = "视频分类"
        verbose_name_plural = "视频分类"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.name


class MembershipPlan(TimeStampedModel):
    name = models.CharField("套餐名称", max_length=80)
    price = models.DecimalField("价格", max_digits=8, decimal_places=2)
    duration_days = models.PositiveIntegerField("有效天数")
    description = models.TextField("套餐说明", blank=True)
    is_active = models.BooleanField("启用", default=True)

    class Meta:
        verbose_name = "会员套餐"
        verbose_name_plural = "会员套餐"
        ordering = ["price", "id"]

    def __str__(self):
        return self.name


class UserMembership(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="用户", on_delete=models.CASCADE)
    plan = models.ForeignKey(MembershipPlan, verbose_name="会员套餐", on_delete=models.PROTECT)
    started_at = models.DateTimeField("开始时间")
    expired_at = models.DateTimeField("到期时间", db_index=True)
    is_active = models.BooleanField("启用", default=True)

    class Meta:
        verbose_name = "用户会员"
        verbose_name_plural = "用户会员"
        ordering = ["-expired_at"]

    def __str__(self):
        return f"{self.user} - {self.plan}"


class Video(TimeStampedModel):
    video_id = models.CharField("视频ID", max_length=64, unique=True)
    title = models.CharField("标题", max_length=200)
    cover = models.ImageField("封面图", upload_to="covers/")
    video_file = models.FileField("视频文件", upload_to="videos/", blank=True, null=True)
    play_url = models.URLField("播放地址", blank=True)
    category = models.ForeignKey(VideoCategory, verbose_name="分类", on_delete=models.PROTECT, related_name="videos")
    duration = models.PositiveIntegerField("时长(秒)", default=0)
    play_count = models.PositiveIntegerField("播放量", default=0)
    member_only = models.BooleanField("会员限制", default=False)
    uploaded_at = models.DateTimeField("上传时间", auto_now_add=True)
    episode_count = models.PositiveIntegerField("选集集数", default=1)
    is_recommended = models.BooleanField("首页推荐", default=False)
    is_published = models.BooleanField("发布", default=True)

    class Meta:
        verbose_name = "视频资源"
        verbose_name_plural = "视频资源"
        ordering = ["-uploaded_at", "-id"]

    def __str__(self):
        return self.title

    @property
    def resolved_play_url(self):
        if self.video_file:
            return self.video_file.url
        return self.play_url


class UploadRecord(TimeStampedModel):
    video = models.ForeignKey(Video, verbose_name="视频", on_delete=models.CASCADE, related_name="upload_records")
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="上传人", on_delete=models.SET_NULL, null=True, blank=True)
    original_filename = models.CharField("原始文件名", max_length=255)
    file_size = models.PositiveBigIntegerField("文件大小", default=0)
    status = models.CharField("状态", max_length=30, default="completed")

    class Meta:
        verbose_name = "上传记录"
        verbose_name_plural = "上传记录"
        ordering = ["-created_at"]

    def __str__(self):
        return self.original_filename


class Comment(TimeStampedModel):
    video = models.ForeignKey(Video, verbose_name="视频", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="用户", on_delete=models.CASCADE)
    content = models.TextField("评论内容")
    is_visible = models.BooleanField("显示", default=True)

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = "用户评论"
        ordering = ["-created_at"]

    def __str__(self):
        return self.content[:30]


class Danmaku(TimeStampedModel):
    video = models.ForeignKey(Video, verbose_name="视频", on_delete=models.CASCADE, related_name="danmakus")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="用户", on_delete=models.SET_NULL, null=True, blank=True)
    content = models.CharField("弹幕内容", max_length=120)
    time_offset = models.DecimalField("出现时间(秒)", max_digits=8, decimal_places=2)
    color = models.CharField("颜色", max_length=20, default="#ffffff")
    is_visible = models.BooleanField("显示", default=True)

    class Meta:
        verbose_name = "弹幕"
        verbose_name_plural = "弹幕"
        ordering = ["time_offset", "created_at"]

    def __str__(self):
        return self.content


class Favorite(TimeStampedModel):
    video = models.ForeignKey(Video, verbose_name="视频", on_delete=models.CASCADE, related_name="favorites")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="用户", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "收藏记录"
        verbose_name_plural = "收藏记录"
        unique_together = ("video", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} 收藏 {self.video}"
