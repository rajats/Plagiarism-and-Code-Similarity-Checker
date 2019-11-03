from datetime import datetime

from django.shortcuts import render
from django.shortcuts import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

from .models import Question, StudentSubmission
from .forms import QuestionForm, StudentSubmissionForm, SubmissionComparisonForm

from userauth.models import RegUser

def add_question(request):
	if request.user.is_authenticated and RegUser.objects.get(user=request.user).instructor:
		instructor = RegUser.objects.get(user=request.user)
		form = QuestionForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			content = form.cleaned_data['content']
			solution = form.cleaned_data['solution']
			deadline = form.cleaned_data['deadline']
			Question.objects.create(content=content, createdby=instructor, deadline=deadline, timestamp=timezone.now(), solution=solution)
			messages.success(request, 'Your question was added')
			#return HttpResponseRedirect(reverse('view_question', kwargs={'id': course.id})) 
			return HttpResponseRedirect('/instructor/')
		context = {'form': form}
		return render(request, "question/addquestion.html",context)
	else:
		raise Http404

def view_question(request, question_id):
	if request.user.is_authenticated:
		context = {}
		question = Question.objects.get(id=question_id)
		user = RegUser.objects.get(user=request.user)
		instructor = user.instructor
		context['instructor'] = instructor
		context['question'] = question
		if instructor:
			submissions = StudentSubmission.objects.filter(question=question)
			context['submissions'] = submissions
		else:
			my_submission = StudentSubmission.objects.filter(question=question, student=user)
			context['my_submission'] = my_submission
		return render(request, "question/viewquestion.html",context)
	else:
		raise Http404

def add_submission(request, question_id):
	if request.user.is_authenticated and not RegUser.objects.get(user=request.user).instructor:
		question = Question.objects.get(id=question_id)
		user = RegUser.objects.get(user=request.user)
		form = StudentSubmissionForm(request.POST or None, request.FILES or None)

		if form.is_valid():
			submission = form.cleaned_data['submission']
			try:
				obj = StudentSubmission.objects.get(question=question,student=user)
				obj.submission = submission
				obj.save
				messages.success(request, 'Your submission was updated')
			except StudentSubmission.DoesNotExist:
				StudentSubmission.objects.create(question=question, student=user, submission=submission, timestamp=timezone.now())
				messages.success(request, 'Your submission was added')
			return HttpResponseRedirect('/student/')
		context = {'form':form}
		return render(request, "question/addsubmission.html",context)
	else:
		raise Http404

def compare_submission(request, question_id, submission_id):
	if request.user.is_authenticated and RegUser.objects.get(user=request.user).instructor:
		context = {}
		form = SubmissionComparisonForm(question_id, submission_id, request.POST or None)
		if form.is_valid():
			pass
		context = {'form':form}
		return render(request, "question/comparesubmission.html",context)
	else:
		raise Http404


