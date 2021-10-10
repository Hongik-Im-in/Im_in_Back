from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from getImage import views

urlpatterns = [
    path('images/', views.image_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)
