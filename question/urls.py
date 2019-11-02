from django.urls import path
from .views import (
	add_question,
	view_question,
	add_submission,
)

urlpatterns = [
    path('add-question/', add_question, name="add-question"),
    path('<int:id>/view-question', view_question, name="view-question"),
    path('<int:id>/add-submission', add_submission, name="add-submission"),
]