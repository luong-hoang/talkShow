from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.urls import reverse
from django.utils import timezone
from django.template.loader import render_to_string

from django.db import IntegrityError, DatabaseError, connection
from django.db.models import Max, Count

from .models import User, TalkShow, Subject, TalkShowSubject
from .tools import Tools
from .decorators import login_required, admin_required
from .constants import *


# Create your views here.
def index(request):
    return HttpResponse("Really? You did it :D")


# todo: Check active user
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
    subjects = user.subject_set.all().order_by('date_modified')
    return render(request, 'talkShow/my_subjects.html',
                  {'subjects': subjects, 'allow_add_new': user.can_add_more_subject()})


@login_required
def edit_subject(request, user_id):
    if request.method == 'POST':
        # Validate
        subject_content = request.POST['subject'].strip()
        if subject_content == '':
            return JsonResponse({'status': False, 'msg': 'Subject is empty.'})
        user = User.objects.get(pk=user_id)

        # Check constrains
        try:
            subject_id = request.POST['id']
        except KeyError:
            # Add new subject, check if user can create a new one
            if not user.can_add_more_subject():
                return JsonResponse({'status': False, 'msg': 'You cannot add anymore subject.'})
            else:
                subject = Subject()
                subject.owner = user
                subject.date_added = timezone.now()
        else:
            # Edit exist subject
            try:
                subject = Subject.objects.get(pk=subject_id)
            except Subject.DoesNotExist:
                return JsonResponse({'status': False, 'msg': 'Subject not found, please try again.'})
            else:
                if subject.subject == subject_content:
                    return JsonResponse({'status': False, 'msg': 'Subject is not changed.'})
                if subject.owner.id != user_id:
                    return JsonResponse({'status': False, 'msg': 'You cannot change this subject.'})

        # Save the subject
        is_new = not bool(subject.id)
        subject.subject = subject_content
        try:
            subject.save()
            content = render_to_string('talkShow/partials/subject_item.html', {'subject': subject})
            return JsonResponse({'status': True, 'is_new': is_new, 'content': content})
        except (IntegrityError, DatabaseError) as e:
            return JsonResponse({'status': False, 'msg': str(e)})
    else:
        raise Http404


@login_required
def statistics(request, user_id):
    return render(request, 'talkShow/statistics.html', {'presenters': _hottest_presenter(), 'authors': _hottest_author()})


@admin_required
def subject_this_period(request, user):
    users = _get_user_current_subject()
    can_roll = _can_roll(users)
    return render(request, 'talkShow/admin/subject_this_period.html', {'users': users, 'can_roll': can_roll})


def _get_user_current_subject():
    users = []
    for user in User.objects.prefetch_related('subject_set').filter(active=True):
        subject = user.subject_set.order_by('-id')[:1]
        if len(subject) > 0 and not subject[0].talked():
            user.current_subject = subject[0]
        else:
            user.current_subject = False
        users.append(user)
    return users


def _can_roll(users):
    if not users:
        users = _get_user_current_subject()
    for user in users:
        if not user.current_subject:
            return False
    return True


def _hottest_presenter():
    user_ids = []
    # Get all users and frequency of each
    frequency = TalkShowSubject.objects.values('user').annotate(total=Count('user'))
    # Get max occupation in above set
    max_num = frequency.aggregate(max=Max('total'))['max']
    # Filter all max value from frequency set
    for user in frequency.filter(total=max_num):
        user_ids.append(user['user'])

    return User.objects.filter(pk__in=user_ids)


def _hottest_author():
    cursor = connection.cursor()
    join_query = 'SELECT tss.`id`, tss.`subject_id`, s.`owner_id` ' \
                      'FROM `talkShow_talkshowsubject` tss ' \
                      'LEFT JOIN `talkShow_subject` s ON (tss.`subject_id` = s.`id`)'

    frequency_query = 'SELECT `owner_id`, COUNT(`owner_id`) AS `total` ' \
                      'FROM (' + join_query + ') ' \
                      'GROUP BY `owner_id` ORDER BY `total` DESC'

    max_query = 'SELECT MAX(`owner_id`) FROM (' + frequency_query + ') AS `dummy`'

    # [(owner_id, frequency), ...]
    frequency_result = cursor.execute(frequency_query).fetchall()
    # [(max)]
    max_result = cursor.execute(max_query).fetchall()

    user_ids = []
    if len(max_result) > 0 and len(frequency_result) > 0:
        max_appear = max_result[0][0]
        for frequency in frequency_result:
            if frequency[1] == max_appear:
                user_ids.append(frequency[0])

    return User.objects.filter(pk__in=user_ids)

