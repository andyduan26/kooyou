from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from .models import Comment, Danmaku, Favorite, MembershipPlan, UploadRecord, UserMembership, Video, VideoCategory


User = get_user_model()


class ApiResponse:
    @staticmethod
    def ok(data=None, message="success"):
        return {"code": 0, "message": message, "data": data}


class UserSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "nickname"]

    def get_nickname(self, obj):
        return obj.get_full_name() or obj.username


class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = ["id", "name", "channel", "sort_order", "is_active", "created_at", "updated_at"]


class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = ["id", "name", "price", "duration_days", "description", "is_active", "created_at", "updated_at"]


class VideoListSerializer(serializers.ModelSerializer):
    category = VideoCategorySerializer(read_only=True)
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            "id",
            "video_id",
            "title",
            "cover_url",
            "category",
            "duration",
            "play_count",
            "member_only",
            "uploaded_at",
            "episode_count",
            "is_recommended",
        ]

    def get_cover_url(self, obj):
        request = self.context.get("request")
        url = obj.cover.url if obj.cover else ""
        return request.build_absolute_uri(url) if request and url else url


class VideoDetailSerializer(VideoListSerializer):
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
    favorites_count = serializers.IntegerField(source="favorites.count", read_only=True)
    play_url = serializers.SerializerMethodField()
    has_video_file = serializers.SerializerMethodField()

    class Meta(VideoListSerializer.Meta):
        fields = VideoListSerializer.Meta.fields + ["play_url", "has_video_file", "comments_count", "favorites_count", "created_at", "updated_at"]

    def get_play_url(self, obj):
        if not obj.video_file:
            return ""
        request = self.context.get("request")
        url = obj.video_file.url
        return request.build_absolute_uri(url) if request else url

    def get_has_video_file(self, obj):
        return bool(obj.video_file)


class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "id",
            "video_id",
            "title",
            "cover",
            "video_file",
            "play_url",
            "category",
            "duration",
            "member_only",
            "episode_count",
            "is_recommended",
            "is_published",
        ]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "video", "user", "content", "is_visible", "created_at", "updated_at"]
        read_only_fields = ["user", "is_visible"]


class DanmakuSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Danmaku
        fields = ["id", "video", "user", "content", "time_offset", "color", "is_visible", "created_at", "updated_at"]
        read_only_fields = ["user", "is_visible"]


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["id", "video", "user", "created_at", "updated_at"]
        read_only_fields = ["user"]


class UploadRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadRecord
        fields = ["id", "video", "uploader", "original_filename", "file_size", "status", "created_at", "updated_at"]
        read_only_fields = ["uploader"]


def user_has_active_membership(user):
    if not user or not user.is_authenticated:
        return False
    return UserMembership.objects.filter(user=user, is_active=True, expired_at__gt=timezone.now()).exists()
