from django.urls import path
from .views import (
    KeyDetailView, KeyView, KeepaliveView
)

urlpatterns = [
    path('keys/', KeyView.as_view()),
    path('keys/<str:key_id>/', KeyDetailView.as_view()),
    path('keepalive/<str:key_id>/', KeepaliveView.as_view())
]
