from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name="login"),
    path('register/', views.register, name="register"),
    path('verify-user/<auth_token>', views.verify, name="verify-email"),
    path('error', views.errors, name="error"),
    path('logout/', views.signout, name="signout")
]
