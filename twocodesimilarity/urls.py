from django.urls import path
from .views import (
	check_two_codes_similarity
)

urlpatterns = [
    path('check-2-sim/', check_two_codes_similarity, name="check-2-sim"),
]