from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render

from .forms import EmailForm, RegistrationForm


def register(request):
    """
    Handles RegistrationForm, login the new user,
    and redirects to home page
    """
    if request.user.is_authenticated():
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form':form})


@login_required
def account_settings(request):
    """
    Displays EmailForm and PasswordChangeForm
    """
    email_form = EmailForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)

    return render(request,
                  'account-settings.html',
                  {'email_form':email_form,
                   'password_form':password_form})


@login_required
def change_email(request):
    """
    Handles EmailForm and responds to user using messages
    """
    if request.method == 'POST':
        form = EmailForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Email was updated successfully!')
        else:
            messages.error(request, 'Please enter valid data.')
    return redirect('account_settings')


@login_required
def change_password(request):
    """
    Handles PasswordChangeForm and responds to user using messages
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.error(request, 'Please enter valid data')
    return redirect('account_settings')
