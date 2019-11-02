from django.shortcuts import render, Http404, HttpResponseRedirect
from django.contrib import messages
from django.template import RequestContext

from question.models import Question, StudentSubmission 
from userauth.models import RegUser

def student_home(request):
	context = {}
	if request.user.is_authenticated and not RegUser.objects.get(user=request.user).instructor:
		student = RegUser.objects.get(user=request.user)
		questions = Question.objects.all()
		my_submissions = StudentSubmission.objects.filter(student=student)
		context['questions'] = questions
		context['my_submissions'] = my_submissions
		messages.success(request,"You are a student")
	else:
		raise Http404
	return render(request, "student/studenthome.html", context)


