from django.conf.urls import url
from . import views

app_name = 'diagnostic'

urlpatterns = [
    url('diagnostic/', views.diagnostic, name = 'diagnostic'),
]