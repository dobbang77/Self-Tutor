from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse
from main.camera import VideoCamera, TimeCount


# 자습모드 로딩
def loading_sel(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return render(request, 'main/Loading_sel.html')
        else:
            return render(request, 'user/signin.html')


# 자습모드 로딩
def loading_lec(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return render(request, 'main/Loading_lec.html')
        else:
            return render(request, 'user/signin.html')


def self_study(request):
    if request.method == 'GET':  # GET 메서드로 요청이 들어 올 경우
        user = request.user.is_authenticated
        if user:
            return render(request, 'main/Self.html')
        else:
            return render(request, 'user/signin.html')


def lecture_study(request):
    if request.method == 'GET':  # GET 메서드로 요청이 들어 올 경우
        user = request.user.is_authenticated
        if user:
            return render(request, 'main/Lecture.html')
        else:
            return render(request, 'user/signin.html')


def gen1(camera):
    while True:
        frame = camera.face_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def gen2(camera):
    while True:
        frame = camera.object_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def gen3(camera):
    while True:
        frame = camera.time_count()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# 인강모드
def video_feed_face(request):
    return StreamingHttpResponse(gen1(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')


# 자습모드
def video_feed_object(request):
    return StreamingHttpResponse(gen2(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')


def video_time_count(request):
    return StreamingHttpResponse(gen3(TimeCount()), content_type='multipart/x-mixed-replace; boundary=frame')
