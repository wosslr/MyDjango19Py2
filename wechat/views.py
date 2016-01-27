#encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
import hashlib

from .helpers import WechatMessage, AccountingDocumentUtility
# Create your views here.


class IndexView(View):
    def get(self, request, *args, **kwargs):
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        token = 'wossffm03wechat'

        hashlist = [token, timestamp, nonce]
        hashlist.sort()

        hashstr = ''.join([s for s in hashlist])
        hashstr = hashlib.sha1(hashstr).hexdigest()

        if hashstr == signature:
            return HttpResponse(echostr)

        return HttpResponse('signature check failed')

    def post(self, request, *args, **kwargs):
        wechat = WechatMessage(request.body)
        reply_msg = AccountingDocumentUtility.create_acc_doc_by_msg(p_message=wechat.msg_content, p_userid=wechat.sender)
        return HttpResponse(wechat.reply(reply_msg))

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)
