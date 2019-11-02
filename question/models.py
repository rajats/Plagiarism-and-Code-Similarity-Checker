from django.db import models

from userauth.models import RegUser

class Question(models.Model):
	content = models.TextField()
	createdby = models.ForeignKey(RegUser, null=True, on_delete=models.SET_NULL)
	deadline = models.DateField(null=True, blank=True)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True)
	solution = models.FileField(upload_to="question/files/")

	def file_link(self):
		if self.solution:
			return self.solution.url
		else:
			return "No attachment"

class StudentSubmission(models.Model):
	question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL) 
	student = models.ForeignKey(RegUser, null=True, blank=True, on_delete=models.SET_NULL)
	submission = models.FileField(upload_to="studentsubmission/files/")
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True)

	def file_link(self):
		if self.submission:
			return self.submission.url
		else:
			return "No attachment"




