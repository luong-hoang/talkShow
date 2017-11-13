from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import User, TalkShow, Subject, TalkShowSubject
from .tools import Tools

USER_ID = 'user_id'
EMAIL = 'email'
PASSWORD = 'password'


# Create your views here.
def index(request):
    return HttpResponse("Really? You did it :D")


def login(request):
    # Handle login: POST
    if request.method == 'POST':
        try:
            email = request.POST[EMAIL].strip()
            password = request.POST[PASSWORD]
            if email == '' or password.strip() == '':
                return render(request, 'talkShow/login.html', {'error': 'Please fill in all fields.'})
            user = User.objects.get(email=email)
        except KeyError:
            return render(request, 'talkShow/login.html', {'error': 'Please fill in all fields.'})
        except User.DoesNotExist:
            return render(request, 'talkShow/login.html', {'error': 'User not found.'})
        else:
            if Tools.md5(password) != user.password:
                return render(request, 'talkShow/login.html', {'error': 'Wrong password.'})
            else:
                # Store session
                request.session[USER_ID] = user.id
                return HttpResponseRedirect(reverse('talkShow:time_line'))

    # Handle get page: GET
    user_id = logged(request)
    if user_id:
        return HttpResponseRedirect(reverse('talkShow:time_line'))
    else:
        return render(request, 'talkShow/login.html')


def time_line(request):
    user_id = logged(request)
    if user_id:
        data = TalkShowSubject.objects.all()
        return render(request, 'talkShow/time_line.html', {'data': data})
    else:
        return HttpResponseRedirect(reverse('talkShow:login'))


# Check session if user is logged
def logged(request):
    return int(request.session.get(USER_ID, 0))
