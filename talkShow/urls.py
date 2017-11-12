from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^index', views.index, name='login'),
    url(r'^$', views.time_line, name='time_line'),
]