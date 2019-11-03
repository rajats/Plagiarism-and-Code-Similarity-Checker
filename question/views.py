import pygments
import pygments.lexers

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
				obj.save()
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
		code1 = StudentSubmission.objects.get(id=submission_id).submission.read().decode("utf-8") 
		form = SubmissionComparisonForm(question_id, submission_id, request.POST or None)
		if form.is_valid():
			chosen_sub_id = form.cleaned_data['choose_submissions']
			code2 = StudentSubmission.objects.get(id=chosen_sub_id).submission.read().decode("utf-8") 
			###################Plagiarism logic###############
			tkns, sc_idx = tokenize_code(code1)
			clean_code= clean(tkns)
			k_grams1 = get_k_grams(clean_code, sc_idx)
			fp1 = winnowing(k_grams1)

			tkns, sc_idx = tokenize_code(code2)
			clean_code= clean(tkns)
			k_grams2 = get_k_grams(clean_code, sc_idx)
			fp2 = winnowing(k_grams2)

			suspicious_part_code1 = ""
			start_set = False
			for f1 in fp1:
			    for f2 in fp2:
			        if f1[0] == f2[0]:
			            if not start_set:
			                start_set = True
			                start = k_grams1[f1[1]][1]
			                end = k_grams1[f1[1]][2]
			            else:
			                if k_grams1[f1[1]][1] < end:
			                    end = k_grams1[f1[1]][2]
			                else:
			                    suspicious_part_code1 += code1[start:end]
			                    start = k_grams1[f1[1]][1]
			                    end = k_grams1[f1[1]][2]
			suspicious_part_code1 += code1[start:end]
			#print (suspicious_part_code1)
			#print ("------------------------------------------------------------------------------")            
			suspicious_part_code2 = ""
			start_set = False
			for f1 in fp1:
			    for f2 in fp2:
			        if f1[0] == f2[0]:
			            if not start_set:
			                start_set = True
			                start = k_grams2[f2[1]][1]
			                end = k_grams2[f2[1]][2]
			            else:
			                if k_grams2[f2[1]][1] < end:
			                    end = k_grams2[f2[1]][2]
			                else:
			                    suspicious_part_code2 += code2[start:end]
			                    start = k_grams2[f2[1]][1]
			                    end = k_grams2[f2[1]][2]
			suspicious_part_code2 += code2[start:end]
			#print (suspicious_part_code2)
			suspicious_part_code1 = suspicious_part_code1.replace("\t", "----")
			suspicious_part_code2 = suspicious_part_code2.replace("\t", "----")
			context['suspicious_part_code1'] = suspicious_part_code1.split("\n")
			context['suspicious_part_code2'] = suspicious_part_code2.split("\n")

			##################################################

		context['form'] = form
		return render(request, "question/comparesubmission.html",context)
	else:
		raise Http404


def get_k_grams(text, sc_idx, k=20):
    k_grams = [(text[:k], sc_idx[0], sc_idx[k])]
    for i in range(1, len(text)-k+1):
        k_grams.append((text[i:i+k], sc_idx[i], sc_idx[i+k-1]))
    return k_grams

def right_min(window):
    return min(range(len(window)), key=lambda i: (window[i][0], -i))

def winnowing(k_grams, w=4):
    fingerprints = []
    hash_k_grams = [(hash(k_grams[i][0]),i) for i in range(len(k_grams))]
    #hash_k_grams = hashes = [(77,0),(74,1),(42,1),(17,3),(98,4),(50,5),(17,6),(98,7),(8,8),(88,9),(67,10),(39,11),(77,12),(74,13),(42,14),(17,15),(98,16)]
    curr_window = hash_k_grams[:w]
    right_min_idx = right_min(curr_window)
    last_min = curr_window[right_min_idx]
    fingerprints.append(last_min)
    right = w
    while(right!=len(hash_k_grams)):    #until right window reaches last hash of k_grams
        curr_window = hash_k_grams[right-w+1:right+1]
        #print right, right_min_idx
        if not (hash_k_grams[right] > last_min and (right-right_min_idx) < w):
            if right-right_min_idx < w:
                right_min_idx = right
                last_min = hash_k_grams[right_min_idx]
            else:
                right_min_idx = right_min(curr_window)
                #print right_min_idx
                last_min = curr_window[right_min_idx]
                right_min_idx = last_min[1]
            fingerprints.append(last_min)
        right += 1
    return fingerprints

def tokenize_code(code):
    tokens, sc_idx = [], []
    idx = 0
    for token in pygments.lex(code, pygments.lexers.PythonLexer()):
        #print token,token[0],len(token[0])
        if token[0] in pygments.token.Comment or token[0] == pygments.token.Text:
            idx += len(token[1])
            continue
        if token[0] == pygments.token.Name:
            tokens.append(("V",idx,idx+len(token[1])))
            sc_idx.append(idx)
        elif token[0] == pygments.token.Name.Function:
            tokens.append(("F",idx,idx+len(token[1])))
            sc_idx.append(idx)
        elif token[0] in pygments.token.Literal.String: #print statements does not matter
            tokens.append(("S",idx,idx+len(token[1])))
            sc_idx.append(idx)
        else:
            tokens.append((token[1],idx,idx+len(token[1])))
            for i in range(len(token[1])):
                sc_idx.append(idx+i)
        idx += len(token[1])
    return tokens, sc_idx

def clean(tk_code):
    return ''.join(str(x[0]) for x in tk_code)