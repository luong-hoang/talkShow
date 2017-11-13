from django.http import HttpResponseRedirect
from django.urls import reverse

from .constants import *


# Force redirect to login if not logged
def login_required(view):
    def check(request, *args, **kwargs):
        user_id = int(request.session.get(USER_ID, 0))
        if user_id:
            return view(request, user_id, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('talkShow:login'))
    return check
