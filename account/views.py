#encoding:utf-8
from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.template.context_processors import csrf

from housefinance.constants import LOGIN_URL

# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


def login(request):
    redirect_to = request.GET.get('next', '')
    # next_parameter = ''
    if redirect_to != '':
        next_parameter = '?next=' + redirect_to
    else:
        next_parameter = ''
        redirect_to = reverse('ffm:index')
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return HttpResponseRedirect(redirect_to)
                else:
                    return HttpResponseRedirect(LOGIN_URL+next_parameter)
            else:
                return HttpResponseRedirect(LOGIN_URL+next_parameter)
    else:
        uf = UserForm()
    context = {'uf': uf}
    context.update(csrf(request))
    context['next'] = redirect_to
    return render_to_response(template_name='account/login.html', context=context)


def logout(request):
    django_logout(request)
    return HttpResponseRedirect(LOGIN_URL)