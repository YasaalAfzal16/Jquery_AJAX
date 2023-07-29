from django.shortcuts import render
from .forms import StudentRegisteration
from .models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
# Create your views here.


def home(request):
    form = StudentRegisteration()
    stud = User.objects.all()
    return render(request, 'enroll/home.html', {'form': form, 'std': stud})


@csrf_protect
def save_data(request):
    if request.method == "POST":
        form = StudentRegisteration(request.POST)
        if form.is_valid():
            sid = request.POST.get('stuid')
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            print("In save_data func, sid:", sid)
            if (sid == ''):
                usr = User(name=name, email=email, password=password)
            else:
                usr = User(id=sid, name=name, email=email, password=password)
            usr.save()
            stud = User.objects.values()
            # print(stud)
            stud_data = list(stud)

            return JsonResponse({'status': 1, 'stud_data': stud_data})
        else:
            print(form.errors.as_data())
            return JsonResponse({'status': 0})


@csrf_protect
def delete_data(request):
    if request.method == "POST":
        id = request.POST.get('sid')
        # print(id)
        pi = User.objects.get(pk=id)
        pi.delete()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})


def edit_data(request):
    if (request.method == "POST"):
        id = request.POST.get('sid')
        # print(id)
        std = User.objects.get(pk=id)
        std_data = {"id": std.id, "name": std.name,
                    "email": std.email, "password": std.password}
        print("Editing Student ID:", std.id)
        return JsonResponse(std_data)
