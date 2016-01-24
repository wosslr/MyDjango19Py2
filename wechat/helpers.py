#encoding:utf-8
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

    def parse_message(self, p_raw_data):
        message = xmltodict.parse(p_raw_data)['xml']
        print(message)
        print(message[self.XMLEL_CONTENT])