from django import forms
from django.forms import ModelForm

from .models import Question, StudentSubmission

class QuestionForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea)
	solution = forms.FileField()
	deadline = forms.DateField()

class StudentSubmissionForm(ModelForm):
	class Meta:
		model = StudentSubmission 
		fields = ('submission',)