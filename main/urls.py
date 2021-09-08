from django.conf.urls import url, include
from django.urls import path
from . import views

urlpatterns = [
    path('lecture_study/', views.lecture_study, name='lecture_study'),
    path('self_study/', views.self_study, name='self_study'),
    path('video_feed_face/', views.video_feed_face, name='video_feed_face'),
    path('video_feed_object/', views.video_feed_object, name='video_feed_object'),
    ]
