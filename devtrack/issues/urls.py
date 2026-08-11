from django.urls import path
from .views import api_root, issues_view, reporters_view

urlpatterns = [
    path('', api_root),
    path('reporters/', reporters_view),
    path('issues/', issues_view),
]
