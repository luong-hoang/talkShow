from django.conf.urls import url
from . import views

app_name = 'talkShow'
urlpatterns = [
    url(r'^test', views.index, name='test'),
    url(r'^$', views.time_line, name='time_line'),
    url(r'^talked', views.time_line, name='time_line'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^my-subjects', views.my_subjects, name='my_subjects'),
    url(r'^edit-subject', views.edit_subject, name='edit_subject'),
    url(r'^statistics', views.statistics, name='statistics'),
    # Admin
    url(r'^overview', views.subject_this_period, name='overview'),
]