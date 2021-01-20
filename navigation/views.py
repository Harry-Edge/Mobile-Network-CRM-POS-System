from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main.decorators import unauthenticated_user
from django.contrib import messages

from main.models import *
from main import process_upgrade


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        employee_id = request.POST.get('employeeid')
        password = request.POST.get('password')

        user = authenticate(request, username=employee_id, password=password)

        if user is not None:
            #messages.success(request, 'Successfully Logged out ')
            login(request, user)
            return redirect('menu')

        else:
            messages.error(request, 'Username or Password Incorrect')
            return render(request, 'navigation/login.html')

    return render(request, 'navigation/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def menu(request):

    employee = request.user

    compass_input_ctn = request.POST.get('ctn')

    if compass_input_ctn is not None:

        # Checks to see if the inputted number is valid before redirecting
        try:
             process_upgrade.get_account(compass_input_ctn)

             compass_ctn_url = str('/upgrade/dashboard/') + compass_input_ctn
             return redirect(compass_ctn_url)

        except MobileNumber.DoesNotExist:
            messages.error(request, 'Mobile Number is not Valid')


    context = {"employee": employee}

    return render(request, 'navigation/menu.html', context)



