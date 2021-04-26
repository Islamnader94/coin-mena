from django.contrib.auth import views
from django.urls import path
from .views import QuotesView

urlpatterns = [
    path('v1/quotes', QuotesView.as_view(), name='v1-quotes'),
]