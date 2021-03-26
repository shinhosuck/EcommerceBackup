from users.forms import UserRegisterForm, UpdateUserInfoForm, UpdateProfileInfoForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from users.models import Profile




def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"{username}, you have successfully registered!")
            # new user profile
            new_user = Profile.objects.get(user=form.instance)
            new_user.first_name = form.instance.first_name
            new_user.last_name = form.instance.last_name
            new_user.email = form.instance.email
            new_user.save()
        return redirect("users:login")
    else:
         form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    user = request.user 
    if request.method == "POST":
        user_form = UpdateUserInfoForm(request.POST, instance=user)
        profile_form = UpdateProfileInfoForm(request.POST, request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"{user.username}, your user information has been updated")
            return redirect("users:profile")
    else:
        user_form = UpdateUserInfoForm(instance=user)
        profile_form = UpdateProfileInfoForm(instance=user.profile)
        context = {
            "user_form": user_form,
            "profile_form": profile_form
        }
    return render(request, "users/profile.html", context)
