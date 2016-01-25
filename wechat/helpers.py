# encoding:utf-8
import xmltodict


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
        self.create_time  =wechat_message[self.XMLEL_CREATE_TIME]

    def reply(self, p_reply_message):
        return self.reply_tpl.format(
            receiver = self.sender,
            sender = self.receiver,
            create_time = self.create_time,
            msg_type = self.msg_type,
            content = p_reply_message
        )
    # def parse_message(self, p_raw_data):
    #     wechat_message = xmltodict.parse(p_raw_data)['xml']
    #     print(wechat_message)
    #     print(wechat_message[self.XMLEL_CONTENT])
    #     self.receiver = wechat_message[self.XMLEL_TO_USER]
    #     self.sender = wechat_message[self.XMLEL_FROM_USER]
    #     self.msg_type = wechat_message[self.XMLEL_MSG_TYPE]
