from django import forms
from django.forms import ModelForm

from .models import StudentSubmission

class QuestionForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea)
	solution = forms.FileField()
	deadline = forms.DateField()

class StudentSubmissionForm(ModelForm):
	class Meta:
		model = StudentSubmission 
		fields = ('submission',)

class SubmissionComparisonForm(forms.Form):
	def __init__(self, question_id, submission_id, *args, **kwargs):
		super(SubmissionComparisonForm, self).__init__(*args, **kwargs)
		self.fields['submissions'] = forms.ChoiceField(choices=[(sub.id, sub.student.user) for sub in StudentSubmission.objects.filter(question__id=question_id) if not sub.id==submission_id])