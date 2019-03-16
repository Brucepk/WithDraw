# -*- coding:utf-8 -*-
import os
import re
import shutil
import time
import itchat
from itchat.content import *

'''
作者：pk哥
公众号：Python知识圈
日期：2018/09/25
代码解析详见公众号「Python知识圈」。
'''


# 说明：可以撤回的有文本文字、微信自带&收藏的表情、图片、语音、位置、名片、分享、附件、视频
msg_dict = {}    # 定义字典储存消息
rev_tmp_dir = "E:\\wechat\\withdraw\\"   # 定义文件存储临时目录
if not os.path.exists(rev_tmp_dir):
    os.mkdir(rev_tmp_dir)
face_bug = None    # 处理表情解决方法


@itchat.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO, FRIENDS],
                     isFriendChat=True, isGroupChat=True)
def handler_receive_msg(msg):    # 将接收到的消息存放在字典中，不接受不具有撤回功能的信息
    global face_bug     # 全局变量
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())   # 格式化本地时间戳 e: 2018-09-04 22:02:08
    msg_id = msg['MsgId']   # 消息ID
    msg_time = msg['CreateTime']    # 消息时间
    if 'ActualNickName' in msg:     # 判断是否为群消息
        from_user = msg['ActualUserName']    # 群消息的发送者,用户的唯一标识
        msg_from = msg['ActualNickName']
        friends = itchat.get_friends(update=True)    # 获取所有好友
        for friend in friends:
            if from_user == friend['UserName']:      # 判断群里撤回消息的是否为自己好友
                if friend['RemarkName']:             # 优先使用好友的备注名称，没有则使用昵称
                    msg_from = friend['RemarkName']
                else:
                    msg_from = friend['NickName']
                break

        groups = itchat.get_chatrooms(update=True)        # 获取所有的群
        for group in groups:
            if msg['FromUserName'] == group['UserName']:  # 根据群消息的FromUserName匹配是哪个群
                group_name = group['NickName']
                group_members = group['MemberCount']
                break
        group_name = group_name + '(' + str(group_members) + ')'

    else:    # 否则输入个人消息
        if itchat.search_friends(userName=msg['FromUserName'])['RemarkName']:   # 优先使用备注名称
            msg_from = itchat.search_friends(userName=msg['FromUserName'])['RemarkName']
        else:
            msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName']
        group_name = ''

    msg_content = None    # 消息内容
    msg_share_url = None     # 分享的链接

    if msg['Type'] in ('Text', 'Friends'):
        msg_content = msg['Text']    # 如果发送的消息是文本或者好友推荐
    elif msg['Type'] in ('Recording', 'Attachment', 'Video', 'Picture'):
        msg_content = r"" + msg['FileName']     # 如果发送的消息是附件、视频、图片、语音
        msg['Text'](rev_tmp_dir + msg['FileName'])   # 保存文件
    elif msg['Type'] == 'Card':
        msg_content = msg['RecommendInfo']['NickName'] + r" 的名片"
    elif msg['Type'] == 'Map':
        x, y, location = re.search(
            "<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
        if location is None:
            msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()      # 内容为详细的地址
        else:
            msg_content = r"" + location
    elif msg['Type'] == 'Sharing':      # 如果消息为分享的音乐或者文章，详细的内容为文章的标题或者是分享的名字
        msg_content = msg['Text']
        msg_share_url = msg['Url']      # 分享链接
    face_bug = msg_content
    # 更新字典
    msg_dict.update({msg_id: {"msg_from": msg_from,
                              "msg_time": msg_time,
                              "msg_time_rec": msg_time_rec,
                              "msg_type": msg["Type"],
                              "msg_content": msg_content,
                              "msg_share_url": msg_share_url,
                              "group_name": group_name}})


@itchat.msg_register(NOTE, isFriendChat=True, isGroupChat=True, isMpChat=True)
# 收到note通知类消息，判断是不是撤回并进行相应操作
def send_msg_helper(msg):
    global face_bug
    if re.search(r"\<\!\[CDATA\[.*撤回了一条消息\]\]\>", msg['Content']) is not None:
        # 获取消息的id
        old_msg_id = re.search(
            "\<msgid\>(.*?)\<\/msgid\>",
            msg['Content']).group(1)   # 在返回的content查找撤回的消息的id
        old_msg = msg_dict.get(old_msg_id, {})
        if len(old_msg_id) < 11:
            itchat.send_file(rev_tmp_dir + face_bug, toUserName='filehelper')
            os.remove(rev_tmp_dir + face_bug)
        else:
            msg_body = "快来看啊，有人撤回消息啦！" + "\n" \
                       + old_msg.get('msg_from') + " 撤回了 " + old_msg.get("msg_type") + " 消息" + "\n" \
                       + old_msg.get('msg_time_rec') + "\n" \
                       + "撤回了什么 ⇣" + "\n" \
                       + r"" + old_msg.get('msg_content')
            # 如果是分享存在链接
            if old_msg['msg_type'] == "Sharing":
                msg_body += "\n就是这个链接➣ " + old_msg.get('msg_share_url')
            itchat.send(msg_body, toUserName='filehelper')    # 将撤回消息发送到文件助手
            if old_msg["msg_type"] in (
                    "Picture", "Recording", "Video", "Attachment"):
                file = '@fil@%s' % (rev_tmp_dir + old_msg['msg_content'])
                itchat.send(msg=file, toUserName='filehelper')
                os.remove(rev_tmp_dir + old_msg['msg_content'])
            msg_dict.pop(old_msg_id)        # 删除字典旧消息


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()
