from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path("", views.index, name="index"),
    path("overview/", views.overview, name="overview"),
    path("validate/", views.validate_flag, name="validate_flag"),
]