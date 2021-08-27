from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse  # 화면에 글자를 띄울 때 사용
from django.contrib.auth import get_user_model  # 사용자가 데이터베이스 안에 있는지 검사하는 함수
from django.contrib import auth  # 사용자 auth 기능 암호화된 패스워드를 읽어올 수 있음.
from django.contrib.auth.decorators import login_required


# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':  # GET 메서드로 요청이 들어 올 경우
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':  # POST 메서드로 요청이 들어 올 경우
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        if password != password2:
            # 페스워드가 같지 않은 경우
            return render(request, 'user/signup.html', {'error':'패스워드를 확인해 주세요!'})
        else:
            if username == '' or password == '':
                # 사용자 저장을 위한 username과 password가 필수라는 것을 얘기 해 줍니다.
                return render(request, 'user/signup.html', {'error': '이름과 패스워드는 필수 입력정보 입니다!'})

            exist_user = get_user_model().objects.filter(username=username)

            if exist_user:
                return render(request, 'user/signup.html', {'error':'이미 존재하는 사용자입니다.'})
                # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password)  # 암호화된 비밀번호와 실제 비밀번호가 맞느지 확인해줌
        if me is not None:  # 사용자가 이미 존재한다면
            auth.login(request, me)
            return redirect('/')

        else:  # 오류화면을 출력하기 위해서는 render 함수를 사용해야함
            return render(request, 'user/signin.html',{'error':'ID 와 패스워드를 확인해 주세요!'} )

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')


@login_required # 사용자가 로그인이 되어야만 이용할 수 있는 함수
def logout(request):
    auth.logout(request)  # 인증 되어있는 정보를 없애기
    return redirect("/")


@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)  # 팔로우 하거나 팔로우를 취소할 유저
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')
