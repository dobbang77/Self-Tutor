from django.shortcuts import render
from django.http import StreamingHttpResponse
from main.camera import VideoCamera


def study_view(request):
    if request.method == 'GET':  # GET 메서드로 요청이 들어 올 경우
        user = request.user.is_authenticated
        if user:
            return render(request, 'main/Recognize.html')
        else:
            return render(request, 'user/signin.html')


def index(request):
    if request.method == 'GET':  # GET 메서드로 요청이 들어 올 경우
        user = request.user.is_authenticated
        if user:
            return render(request, 'main/Streaming.html')
        else:
            return render(request, 'user/signin.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# 자습모드
def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')


# 인강모드
