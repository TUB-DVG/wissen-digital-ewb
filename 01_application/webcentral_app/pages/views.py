from django.shortcuts import render, redirect 
#from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index(request):
	
	return render(request, 'pages/index.html')

def Datenschutzhinweis(request):
	return render(request, 'pages/Datenschutzhinweis.html')

def about(request):
    return render(request, 'pages/about.html')

def data(request):
    return render(request, 'pages/data.html')
	
def coming(request):
    return render(request, 'pages/coming.html')


from django.contrib.auth.models import User
class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('index')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'pages/register.html', context)

def loginPage(request):
	"""
	if not User.objects.filter(username="ptj").exists():
		user=User.objects.create_user(username="ptj",password="BF_Ptj_2022")
	"""
	if request.user.is_authenticated:
		return redirect('index')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('index')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'pages/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')
