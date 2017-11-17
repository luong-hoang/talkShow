from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404

from .constants import *
from .models import User


# Force redirect to login if not logged
def login_required(view):
    def check(request, *args, **kwargs):
        user_id = int(request.session.get(USER_ID, 0))
        if user_id:
            return view(request, user_id, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('talkShow:login'))
    return check


def admin_required(view):
    def check(request, *args, **kwargs):
        user_id = int(request.session.get(USER_ID, 0))
        if user_id:
            user = get_object_or_404(User, pk=user_id)
            if user.super:
                return view(request, user, *args, **kwargs)
            else:
                return HttpResponse('Not authorized')
        else:
            return HttpResponseRedirect(reverse('talkShow:login'))
    return check
