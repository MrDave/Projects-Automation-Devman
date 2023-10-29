from django.shortcuts import render, redirect
from .models import DevmanUser
from .forms import DevmanUserForm, ProjectManagerForm

def index(request):
    return render(request, 'index.html')


def students(request):
    error = ''
    if request.method == 'POST':
        form = DevmanUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма была неверной'

    form = DevmanUserForm()
    data = {
        'form': form,
        'error': error

    }
    return render(request, 'students.html', data)


def pms(request):
    error = ''
    if request.method == 'POST':
        form = ProjectManagerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма была неверной'

    form = ProjectManagerForm()
    data = {
        'form': form,
        'error': error

    }
    return render(request, 'pms.html', data)

def info_pro(request):
    students_all = DevmanUser.objects.all()
    return render(request, 'info_pro.html', {'students_all': students_all})