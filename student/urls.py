from django.urls import path
from .views import (
	student_home,
)

urlpatterns = [
    path('', student_home),
]