from django.conf.urls import url
from . import views

app_name = 'preventative'

urlpatterns = [
    url('preventative/', views.preventative, name = 'preventative'),
]