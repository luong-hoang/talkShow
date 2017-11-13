from django.conf.urls import url
from . import views

app_name = 'talkShow'
urlpatterns = [
    url(r'^test', views.index, name='test'),
    url(r'^$', views.time_line, name='time_line'),
    url(r'^talked', views.time_line, name='time_line'),
    url(r'^login', views.login, name='login'),
]