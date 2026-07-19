from django.contrib import admin

from .models import Comment, Danmaku, Favorite, MembershipPlan, UploadRecord, UserMembership, Video, VideoCategory


@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "channel", "sort_order", "is_active", "created_at")
    list_editable = ("sort_order", "is_active")
    list_filter = ("channel", "is_active")
    search_fields = ("name",)
    ordering = ("sort_order", "id")
    list_per_page = 20
    actions = ["export_selected"]

    @admin.action(description="导出所选分类")
    def export_selected(self, request, queryset):
        self.message_user(request, f"已选择 {queryset.count()} 条分类，可接入 CSV 导出。")


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "video_id", "title", "category", "duration", "play_count", "member_only", "episode_count", "is_recommended", "is_published", "uploaded_at")
    list_editable = ("member_only", "episode_count", "is_recommended", "is_published")
    list_filter = ("category__channel", "category", "member_only", "is_recommended", "is_published")
    search_fields = ("video_id", "title", "play_url")
    readonly_fields = ("uploaded_at", "created_at", "updated_at")
    ordering = ("-uploaded_at",)
    list_per_page = 20
    actions = ["mark_recommended", "mark_unrecommended", "export_selected"]

    @admin.action(description="批量设为首页推荐")
    def mark_recommended(self, request, queryset):
        queryset.update(is_recommended=True)

    @admin.action(description="批量取消首页推荐")
    def mark_unrecommended(self, request, queryset):
        queryset.update(is_recommended=False)

    @admin.action(description="导出所选视频")
    def export_selected(self, request, queryset):
        self.message_user(request, f"已选择 {queryset.count()} 条视频，可接入 CSV 导出。")


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "duration_days", "is_active", "created_at")
    list_editable = ("price", "duration_days", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    list_per_page = 20


@admin.register(UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "plan", "started_at", "expired_at", "is_active")
    list_editable = ("is_active",)
    list_filter = ("plan", "is_active", "expired_at")
    search_fields = ("user__username", "user__email", "plan__name")
    list_per_page = 20


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "video", "user", "content", "is_visible", "created_at")
    list_editable = ("is_visible",)
    list_filter = ("is_visible", "created_at")
    search_fields = ("content", "video__title", "user__username")
    list_per_page = 20


@admin.register(Danmaku)
class DanmakuAdmin(admin.ModelAdmin):
    list_display = ("id", "video", "user", "content", "time_offset", "color", "is_visible", "created_at")
    list_editable = ("color", "is_visible")
    list_filter = ("is_visible", "video")
    search_fields = ("content", "video__title", "user__username")
    list_per_page = 20


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "video", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("video__title", "user__username")
    list_per_page = 20


@admin.register(UploadRecord)
class UploadRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "video", "uploader", "original_filename", "file_size", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("original_filename", "video__title", "uploader__username")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
