from django.core.urlresolvers import resolve
from django.urls import reverse

from .constants import *
from .models import User


def global_context(request):
    current_url = resolve(request.path_info).url_name

    context = {
        'current_url': current_url,
        'is_logged': False,
        'is_admin': False,
    }

    # Get user status context
    user_id = int(request.session.get(USER_ID, 0))
    if user_id:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass
        else:
            context['is_logged'] = True
            if user.super:
                context['is_admin'] = True

    # Build navigation bar
    nav_predefined = [
        {'name': 'time_line', 'url': ['', 'talked'], 'label': 'English time', 'admin': False},
        {'name': 'overview', 'url': ['overview'], 'label': 'Overview', 'admin': True},
        {'name': 'statistics', 'url': ['statistics'], 'label': 'Statistics', 'admin': False},
        {'name': 'my_subjects', 'url': ['my-subjects'], 'label': 'My subjects', 'admin': False},
        # {'name': 'time_line', 'url': ['my-profile'], 'label': 'My profile', 'admin': False}
    ]
    nav_items = []
    for item in nav_predefined:
        if context['is_admin'] or not item['admin']:
            url_name = 'talkShow:%s' % item['name']
            url = reverse(url_name)
            css_class = ''
            if current_url in item['url']:
                css_class = 'active'
            nav_items.append({'url': url, 'label': item['label'], 'class': css_class})

    context['nav_items'] = nav_items
    return context
