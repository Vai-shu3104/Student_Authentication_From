from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student
from django.contrib.auth.hashers import check_password, make_password


def register(request):
    if request.method == "POST":
        fullname = request.POST['fullname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Password does not match")
            return redirect('register')

        if Student.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        Student.objects.create(
            fullname=fullname,
            email=email,
            mobile=mobile,
            password=make_password(password)
        )

        messages.success(request, "Registration successful")
        return redirect('login')

    return render(request, "registration/register.html")


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            student = Student.objects.get(email=email)

            if check_password(password, student.password):
                # ✅ SESSION STORE (IMPORTANT)
                request.session['student_id'] = student.id
                request.session['student_name'] = student.fullname
                request.session['student_email'] = student.email

                return redirect('dashboard')
            else:
                messages.error(request, "Invalid Password")

        except Student.DoesNotExist:
            messages.error(request, "Invalid Email")

    return render(request, "registration/login.html")


def dashboard(request):
    # ✅ LOGIN CHECK
    if 'student_id' not in request.session:
        return redirect('login')

    context = {
        'name': request.session['student_name'],
        'email': request.session['student_email']
    }

    return render(request, "registration/dashboard.html", context)


def logout(request):
    request.session.flush()
    return redirect('login')
