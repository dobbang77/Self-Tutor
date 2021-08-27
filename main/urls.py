from django.conf.urls import url, include
from django.urls import path
from . import views

urlpatterns = [
    path('stream/', views.index, name='index'),
    path('study/', views.study_view, name='study'),
    path('video_feed/', views.video_feed, name='video_feed'),
    ]
