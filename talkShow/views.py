from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import User, TalkShow, Subject, TalkShowSubject
from .tools import Tools
from .decorators import login_required
from .constants import *


# Create your views here.
def index(request):
    return HttpResponse("Really? You did it :D")


def login(request):
    # Handle login: POST
    if request.method == 'POST':
        try:
            email = request.POST['email'].strip()
            password = request.POST['password']
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
    user_id = int(request.session.get(USER_ID, 0))
    if user_id:
        return HttpResponseRedirect(reverse('talkShow:time_line'))
    else:
        return render(request, 'talkShow/login.html')


def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('talkShow:login'))


@login_required
def time_line(request, user_id):
    data = TalkShowSubject.objects.all()
    return render(request, 'talkShow/time_line.html', {'data': data})


@login_required
def my_subjects(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'talkShow/my_subjects.html', {'subjects': user.subject_set.all()})


