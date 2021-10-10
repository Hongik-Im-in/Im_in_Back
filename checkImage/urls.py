from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from checkImage import views

urlpatterns = [
    path('check/', views.check_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)

