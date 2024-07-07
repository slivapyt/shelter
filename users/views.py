import random
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth import logout
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.core.mail import send_mail
from config import settings
from users.forms import UserRegisterForm, UserForm
from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache

from users.services import send_new_password





class LoginView(BaseLoginView):
    template_name = 'users/login.html'



def my_logout_view(request):
    logout(request)
    return redirect('/')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        new_user = form.save()
        send_mail(
            subject='поздравляем с регистрацией',
            message='Вы зарегистрировались на нашей платформе, добро пожаловать!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list = [new_user.email]
                )   
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm
    
    def get_object(self, queryset=None):
        return self.request.user




@login_required
def generate_new_password(request):
    new_password = User.objects.make_random_password()
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    print(new_password)
    return redirect(reverse('dogs:index'))
    