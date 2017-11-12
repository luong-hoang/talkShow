from django.shortcuts import render
from django.http import HttpResponse
from .models import User, TalkShow, Subject, TalkShowSubject

USER_ID = 'user_id'


# Create your views here.
def index(request):
    return HttpResponse("Really? You did it :D")


def login(request):
    user_id = logged(request)
    if user_id:
        return HttpResponse('Logged')
    else:
        return render(request, 'talkShow/login.html')


def time_line(request):
    data = TalkShowSubject.objects.all()
    print(data)
    return render(request, 'talkShow/time_line.html', {'data': data})


def logged(request):
    return int(request.session.get(USER_ID, 0))
