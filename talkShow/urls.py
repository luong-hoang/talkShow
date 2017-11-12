from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^test', views.index, name='test'),
    url(r'^$', views.login, name='login'),
    url(r'^talked', views.time_line, name='time_line'),
]