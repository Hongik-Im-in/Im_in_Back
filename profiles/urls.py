from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from profiles import views

urlpatterns = [
    path('profiles/', views.profile_list),
    path('profiles/<int:pk>', views.profile_detail),
    #path('profiles/<int:studentId>', views.profile_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
