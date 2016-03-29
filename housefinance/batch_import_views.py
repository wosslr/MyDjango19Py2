#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .constants import LOGIN_URL

from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf

import codecs


@login_required(login_url=LOGIN_URL)
def batch_import_zfb(request):
    if request.method == 'POST' and request.FILES:
        txtfile = request.FILES['txt_file']
        print(dir(txtfile))
        start_flag = False
        for line in txtfile:
            values = line.split(',')
            for value in values:
                value = value.strip()
                if value == '交易号':
                    start_flag = True
                    break
    elif request.method == 'GET':
        context = {}
        context.update(csrf(request))
        return render_to_response(template_name='housefinance/batch_import/batch_import_zfb.html', context=context)