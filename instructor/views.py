from django.shortcuts import render, Http404, HttpResponseRedirect
from django.contrib import messages
from django.template import RequestContext

from question.models import Question 
from userauth.models import RegUser

def instructor_home(request):
	context = {}
	if request.user.is_authenticated and RegUser.objects.get(user=request.user).instructor:
		instructor = RegUser.objects.get(user=request.user)
		questions = Question.objects.filter(createdby=instructor)
		context['questions'] = questions
		messages.success(request,"You are a instructor")
	else:
		raise Http404
	return render(request, "instructor/myquestions.html", context)

