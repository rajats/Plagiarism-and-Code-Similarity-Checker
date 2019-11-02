from django.contrib import admin

from .models import Question, StudentSubmission

admin.site.register(Question)
admin.site.register(StudentSubmission)