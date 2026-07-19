from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Video, VideoCategory


class VideoApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = VideoCategory.objects.create(name="电影", channel=VideoCategory.CHANNEL_MOVIE)
        self.video = Video.objects.create(
            video_id="VIDEO_ID",
            title="测试影片",
            cover=SimpleUploadedFile("cover.jpg", b"file", content_type="image/jpeg"),
            play_url="https://cdn.example.com/video.mp4",
            category=self.category,
            is_recommended=True,
        )
        self.user = get_user_model().objects.create_user(username="viewer", password="pass12345")

    def test_home_recommend_returns_unified_json(self):
        response = self.client.get("/api/videos/home-recommend/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["code"], 0)
        self.assertEqual(response.json()["data"][0]["video_id"], "VIDEO_ID")

    def test_member_only_play_requires_membership(self):
        self.video.member_only = True
        self.video.save(update_fields=["member_only"])
        self.client.force_authenticate(self.user)
        response = self.client.post(f"/api/videos/{self.video.id}/play-auth/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["data"]["allowed"])
