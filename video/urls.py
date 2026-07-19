from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdminVideoUploadView, CategoryViewSet, MembershipCheckView, MembershipPlanViewSet, UploadRecordViewSet, VideoViewSet


router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("videos", VideoViewSet, basename="video")
router.register("membership-plans", MembershipPlanViewSet, basename="membership-plan")
router.register("upload-records", UploadRecordViewSet, basename="upload-record")

urlpatterns = [
    path("", include(router.urls)),
    path("membership/check/", MembershipCheckView.as_view(), name="membership-check"),
    path("admin/videos/upload/", AdminVideoUploadView.as_view(), name="admin-video-upload"),
]
