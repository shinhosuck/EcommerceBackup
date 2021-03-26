from django.contrib.auth.views import LoginView, LogoutView
from users.views import register, profile
from django.urls import path 


app_name = "users"


urlpatterns = [
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="users/logout.html"), name="logout"),

]