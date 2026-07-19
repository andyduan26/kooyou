from django.db.models import F
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import VideoFilter
from .models import Comment, Danmaku, Favorite, MembershipPlan, UploadRecord, UserMembership, Video, VideoCategory
from .serializers import (
    ApiResponse,
    CommentSerializer,
    DanmakuSerializer,
    FavoriteSerializer,
    MembershipPlanSerializer,
    UploadRecordSerializer,
    VideoCategorySerializer,
    VideoDetailSerializer,
    VideoListSerializer,
    VideoUploadSerializer,
    user_has_active_membership,
)


class JsonResponseMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if isinstance(response.data, dict) and {"code", "message", "data"}.issubset(response.data.keys()):
            return response
        if response.exception:
            response.data = {"code": response.status_code, "message": "error", "data": response.data}
        else:
            response.data = ApiResponse.ok(response.data)
        return response


class CategoryViewSet(JsonResponseMixin, viewsets.ReadOnlyModelViewSet):
    queryset = VideoCategory.objects.filter(is_active=True)
    serializer_class = VideoCategorySerializer


class VideoViewSet(JsonResponseMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.filter(is_published=True).select_related("category")
    filterset_class = VideoFilter

    def get_serializer_class(self):
        return VideoDetailSerializer if self.action == "retrieve" else VideoListSerializer

    @action(detail=False, methods=["get"], url_path="home-recommend")
    def home_recommend(self, request):
        queryset = self.get_queryset().filter(is_recommended=True)[:24]
        serializer = VideoListSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny], url_path="play-auth")
    def play_auth(self, request, pk=None):
        video = self.get_object()
        allowed = bool(video.video_file) or not video.member_only or user_has_active_membership(request.user)
        if allowed:
            Video.objects.filter(pk=video.pk).update(play_count=F("play_count") + 1)
        return Response(
            {
                "video_id": video.video_id,
                "allowed": allowed,
                "member_only": video.member_only,
                "play_url": request.build_absolute_uri(video.video_file.url) if allowed and video.video_file else "",
                "has_video_file": bool(video.video_file),
            }
        )

    @action(detail=True, methods=["get", "post"], url_path="danmaku")
    def danmaku(self, request, pk=None):
        video = self.get_object()
        if request.method == "GET":
            serializer = DanmakuSerializer(video.danmakus.filter(is_visible=True), many=True)
            return Response(serializer.data)
        serializer = DanmakuSerializer(data={**request.data, "video": video.id})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user if request.user.is_authenticated else None)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get", "post"], permission_classes=[permissions.IsAuthenticatedOrReadOnly], url_path="comments")
    def comments(self, request, pk=None):
        video = self.get_object()
        if request.method == "GET":
            serializer = CommentSerializer(video.comments.filter(is_visible=True), many=True)
            return Response(serializer.data)
        serializer = CommentSerializer(data={**request.data, "video": video.id})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post", "delete"], permission_classes=[permissions.IsAuthenticated], url_path="favorite")
    def favorite(self, request, pk=None):
        video = self.get_object()
        if request.method == "DELETE":
            Favorite.objects.filter(video=video, user=request.user).delete()
            return Response({"favorited": False})
        favorite, _ = Favorite.objects.get_or_create(video=video, user=request.user)
        return Response(FavoriteSerializer(favorite).data)


class MembershipPlanViewSet(JsonResponseMixin, viewsets.ReadOnlyModelViewSet):
    queryset = MembershipPlan.objects.filter(is_active=True)
    serializer_class = MembershipPlanSerializer


class MembershipCheckView(JsonResponseMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        membership = (
            UserMembership.objects.filter(user=request.user, is_active=True, expired_at__gt=timezone.now())
            .select_related("plan")
            .order_by("-expired_at")
            .first()
        )
        return Response(
            {
                "active": bool(membership),
                "plan": membership.plan.name if membership else "",
                "expired_at": membership.expired_at if membership else None,
            }
        )


class AdminVideoUploadView(JsonResponseMixin, APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = VideoUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        video = serializer.save()
        upload = request.FILES.get("video_file")
        if upload:
            UploadRecord.objects.create(
                video=video,
                uploader=request.user,
                original_filename=upload.name,
                file_size=upload.size,
            )
        return Response(VideoUploadSerializer(video).data, status=status.HTTP_201_CREATED)


class UploadRecordViewSet(JsonResponseMixin, viewsets.ReadOnlyModelViewSet):
    queryset = UploadRecord.objects.select_related("video", "uploader")
    serializer_class = UploadRecordSerializer
    permission_classes = [permissions.IsAdminUser]
