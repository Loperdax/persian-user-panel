from django.contrib import admin
from django.urls import path
from user_manager_app import views

urlpatterns = [
    # Assign path '' to views.login _view
    path('' , views.login_view)
]
