from django.conf.urls import url
from . import views

app_name = 'insurance'

urlpatterns = [
    url('insurance/', views.insurance, name = 'insurance'),
]