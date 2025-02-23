from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, my_logout_view, RegisterView, UserUpdateView, generate_new_password

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name = 'login'),
    path('logout/', my_logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),

]
