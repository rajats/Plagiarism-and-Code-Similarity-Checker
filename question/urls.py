from django.urls import path
from .views import (
	add_question,
	view_question,
	add_submission,
	compare_submission,
)

urlpatterns = [
    path('add-question/', add_question, name="add-question"),
    path('<int:question_id>/view-question', view_question, name="view-question"),
    path('<int:question_id>/add-submission', add_submission, name="add-submission"),
    path('<int:question_id>/<int:submission_id>/compare-submission', compare_submission, name="compare-submission"),
]