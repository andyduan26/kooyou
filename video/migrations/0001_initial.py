import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MembershipPlan",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("name", models.CharField(max_length=80, verbose_name="套餐名称")),
                ("price", models.DecimalField(decimal_places=2, max_digits=8, verbose_name="价格")),
                ("duration_days", models.PositiveIntegerField(verbose_name="有效天数")),
                ("description", models.TextField(blank=True, verbose_name="套餐说明")),
                ("is_active", models.BooleanField(default=True, verbose_name="启用")),
            ],
            options={"verbose_name": "会员套餐", "verbose_name_plural": "会员套餐", "ordering": ["price", "id"]},
        ),
        migrations.CreateModel(
            name="VideoCategory",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="分类名称")),
                ("channel", models.CharField(choices=[("movie", "电影"), ("series", "剧集"), ("anime", "动漫"), ("variety", "综艺")], db_index=True, max_length=20, verbose_name="频道分类")),
                ("sort_order", models.PositiveIntegerField(default=0, verbose_name="排序")),
                ("is_active", models.BooleanField(default=True, verbose_name="启用")),
            ],
            options={"verbose_name": "视频分类", "verbose_name_plural": "视频分类", "ordering": ["sort_order", "id"]},
        ),
        migrations.CreateModel(
            name="UserMembership",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("started_at", models.DateTimeField(verbose_name="开始时间")),
                ("expired_at", models.DateTimeField(db_index=True, verbose_name="到期时间")),
                ("is_active", models.BooleanField(default=True, verbose_name="启用")),
                ("plan", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="video.membershipplan", verbose_name="会员套餐")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="用户")),
            ],
            options={"verbose_name": "用户会员", "verbose_name_plural": "用户会员", "ordering": ["-expired_at"]},
        ),
        migrations.CreateModel(
            name="Video",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("video_id", models.CharField(max_length=64, unique=True, verbose_name="视频ID")),
                ("title", models.CharField(max_length=200, verbose_name="标题")),
                ("cover", models.ImageField(upload_to="covers/", verbose_name="封面图")),
                ("video_file", models.FileField(blank=True, null=True, upload_to="videos/", verbose_name="视频文件")),
                ("play_url", models.URLField(blank=True, verbose_name="播放地址")),
                ("duration", models.PositiveIntegerField(default=0, verbose_name="时长(秒)")),
                ("play_count", models.PositiveIntegerField(default=0, verbose_name="播放量")),
                ("member_only", models.BooleanField(default=False, verbose_name="会员限制")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True, verbose_name="上传时间")),
                ("episode_count", models.PositiveIntegerField(default=1, verbose_name="选集集数")),
                ("is_recommended", models.BooleanField(default=False, verbose_name="首页推荐")),
                ("is_published", models.BooleanField(default=True, verbose_name="发布")),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="videos", to="video.videocategory", verbose_name="分类")),
            ],
            options={"verbose_name": "视频资源", "verbose_name_plural": "视频资源", "ordering": ["-uploaded_at", "-id"]},
        ),
        migrations.CreateModel(
            name="UploadRecord",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("original_filename", models.CharField(max_length=255, verbose_name="原始文件名")),
                ("file_size", models.PositiveBigIntegerField(default=0, verbose_name="文件大小")),
                ("status", models.CharField(default="completed", max_length=30, verbose_name="状态")),
                ("uploader", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name="上传人")),
                ("video", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="upload_records", to="video.video", verbose_name="视频")),
            ],
            options={"verbose_name": "上传记录", "verbose_name_plural": "上传记录", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="用户")),
                ("video", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorites", to="video.video", verbose_name="视频")),
            ],
            options={"verbose_name": "收藏记录", "verbose_name_plural": "收藏记录", "ordering": ["-created_at"], "unique_together": {("video", "user")}},
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("content", models.TextField(verbose_name="评论内容")),
                ("is_visible", models.BooleanField(default=True, verbose_name="显示")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="用户")),
                ("video", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="video.video", verbose_name="视频")),
            ],
            options={"verbose_name": "用户评论", "verbose_name_plural": "用户评论", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Danmaku",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("content", models.CharField(max_length=120, verbose_name="弹幕内容")),
                ("time_offset", models.DecimalField(decimal_places=2, max_digits=8, verbose_name="出现时间(秒)")),
                ("color", models.CharField(default="#ffffff", max_length=20, verbose_name="颜色")),
                ("is_visible", models.BooleanField(default=True, verbose_name="显示")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name="用户")),
                ("video", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="danmakus", to="video.video", verbose_name="视频")),
            ],
            options={"verbose_name": "弹幕", "verbose_name_plural": "弹幕", "ordering": ["time_offset", "created_at"]},
        ),
    ]
