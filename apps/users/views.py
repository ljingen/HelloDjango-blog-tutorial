from django.shortcuts import render, redirect
from django.views.generic.base import View
from .forms import RegisterForm


# Create your views here.

class RegisterView(View):
    """
    user register
    """

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'users/register.html', {'form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            return redirect('blog:index')
        else:
            return render(request, 'users/register.html', {'form': register_form, 'msg': '用户已存在'})
        return render(request, 'users/register.html', context={'form': register_form})



