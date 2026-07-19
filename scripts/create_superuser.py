import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kooyou_backend.settings")
django.setup()

from django.contrib.auth import get_user_model


User = get_user_model()
user, created = User.objects.update_or_create(
    username="andyduan26",
    defaults={
        "email": "andyduanxiaoga@163.com",
        "first_name": "钱多多",
        "is_staff": True,
        "is_superuser": True,
        "is_active": True,
    },
)
user.set_password("Ay281988")
user.save()

print(("created" if created else "updated") + ": andyduan26")
