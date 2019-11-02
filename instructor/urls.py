from django.urls import path
from .views import (
	instructor_home,
)

urlpatterns = [
    path('', instructor_home),
]