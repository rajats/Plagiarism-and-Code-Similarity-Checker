from django.shortcuts import render, render_to_response, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from .forms import LoginForm
from .models import RegUser

def signin(request):
	if request.user.is_superuser:
		raise Http404
	if request.user.is_authenticated:
		if RegUser.objects.get(user=request.user).instructor:
			return HttpResponseRedirect('/instructor/')
		else:
			return HttpResponseRedirect('/student/')
	form = LoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username = username, password = password)
		if user is not None:
			login(request, user)
			if RegUser.objects.get(user=request.user).instructor:
				return HttpResponseRedirect('/instructor/')
			else:
				return HttpResponseRedirect('/student/')
		else:
			messages.error(request, 'username or password does not match')
	context = {'form': form}
	return render(request, "userauth/login.html",context)

def signout(request):
	logout(request)
	messages.success(request,"You have logged out")
	return HttpResponseRedirect(reverse("signin"))
