from django.shortcuts import render, redirect
from .models import Student
from .forms import DevmanUserForm

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
    return render(request, 'pms.html')

def info_pro(request):
    students_all = Student.objects.all()
    return render(request, 'info_pro.html', {'students_all': students_all})