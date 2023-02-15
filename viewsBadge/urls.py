# Django
from django.urls import path

# local Django
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("badge", views.badge, name="badge"),
    path("generate-badge", views.generateBadgeUrl, name="generate-badge")
]
