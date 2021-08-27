#user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class UserModel(AbstractUser):  # class B(A) 처럼 UserModel 에서 model.Model 클래스를 상속하겠다는 뜻
    class Meta:
        db_table = "my_user"  # 테이블의 이름

    bio = models.CharField(max_length=256, default='')
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')


