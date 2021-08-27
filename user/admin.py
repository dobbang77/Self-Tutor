from django.contrib import admin  # 장고에서 어드민 툴을 사용하겠다
from .models import UserModel  # 우리가 생성한모델을 가져옴

# Register your models here.
admin.site.register(UserModel)  # 나의 UserModel 테이블을 Admin 에 추가합니다
