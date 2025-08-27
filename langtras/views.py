
from django.shortcuts import render
from lang.models import Lang
from django.contrib.auth.forms import UserCreationForm
from lang.forms import CreateUserForm

def home(request):
    # lang = Lang.objects.all()
    form = CreateUserForm()
    return render(request, 'register.html', {'form':form})


    