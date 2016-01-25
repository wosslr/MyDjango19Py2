# encoding:utf-8
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import re
import xmltodict
from django.utils import timezone

from housefinance.models import AccountingDocumentHeader, AccountingDocumentItem, User, Account


class WechatMessage:
    XMLEL_TO_USER = 'ToUserName'
    XMLEL_FROM_USER = 'FromUserName'
    XMLEL_CREATE_TIME = 'CreateTime'
    XMLEL_MSG_TYPE = 'MsgType'
    XMLEL_CONTENT = 'Content'
    XMLEL_MSG_ID = 'MsgId'

    sender = ''
    receiver = ''
    msg_content = ''
    msg_type = ''
    create_time = ''

    reply_tpl = '''<xml><ToUserName><![CDATA[{receiver}]]></ToUserName>
<FromUserName><![CDATA[{sender}]]></FromUserName>
<CreateTime>{create_time}</CreateTime>
<MsgType><![CDATA[{msg_type}]]></MsgType>
<Content><![CDATA[{content}]]></Content>
</xml>
    '''

    def __init__(self, p_raw_message):
        wechat_message = xmltodict.parse(p_raw_message)['xml']
        self.receiver = wechat_message[self.XMLEL_TO_USER]
        self.sender = wechat_message[self.XMLEL_FROM_USER]
        self.msg_type = wechat_message[self.XMLEL_MSG_TYPE]
        self.msg_content = wechat_message[self.XMLEL_CONTENT]
        self.create_time = wechat_message[self.XMLEL_CREATE_TIME]

    def reply(self, p_reply_message):
        return self.reply_tpl.format(
                receiver=self.sender,
                sender=self.receiver,
                create_time=self.create_time,
                msg_type=self.msg_type,
                content=p_reply_message
        )


class AccountingDocumentUtility:
    @staticmethod
    def create_acc_doc_by_msg(p_message):
        p_wechat_message = str(p_message)
        acc_doc_header = AccountingDocumentHeader()
        acc_doc_item_j = AccountingDocumentItem()
        acc_doc_item_d = AccountingDocumentItem()

        date_list = re.findall('^(.+?)天', p_wechat_message)
        if len(date_list) == 0:
            acc_doc_header.creation_date = timezone.now()
            comment_list = re.findall(r'^(.+?)[0-9].+?元', p_wechat_message)
        else:
            if date_list[0] == '今':
                acc_doc_header.creation_date = timezone.now()
            elif date_list[0] == '昨':
                acc_doc_header.creation_date = timezone.now().replace(day=-1)
            else:
                return date_list[0].encode() + '天?'
            comment_list = re.findall(r'天(.+?)[0-9].+?元', p_wechat_message)

        if len(comment_list) == 0:
            return '怎么花的钱?'.encode()
        else:
            acc_doc_header.comment = comment_list[0].encode()

        amount_list = re.findall(r'([0-9].+?)元', p_wechat_message)
        if len(amount_list) == 0:
            return '花了多少钱?'.encode()
        else:
            acc_doc_item_j.amount = int(amount_list[0])
            acc_doc_item_d.amount = int(amount_list[0])

        resource_list = re.findall(r'元(.+?)$', p_wechat_message)
        if len(resource_list) == 0:
            account_name_d = '现金'
        else:
            account_name_d = resource_list[0]

        account_name_j = '日常消费'

        account_list_j = Account.objects.filter(account_name=account_name_j)
        account_list_d = Account.objects.filter(account_name=account_name_d)

        if len(account_list_j) == 0 or len(account_list_d) == 0:
            return '科目还没设置好'
        else:
            acc_doc_item_j.account = account_list_j[0]
            acc_doc_item_d.account = account_list_d[0]

        acc_doc_header.creator = User.objects.first()
        acc_doc_item_j.dc_indicator = 'J'
        acc_doc_item_d.dc_indicator = 'D'

        acc_doc_header.save()
        acc_doc_item_j.document_header = acc_doc_header
        acc_doc_item_d.document_header = acc_doc_header
        acc_doc_item_j.save()
        acc_doc_item_d.save()

        return '凭证 ' + acc_doc_header.__str__() + ' 创建成功'
