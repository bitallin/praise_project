# encoding = utf8
import itchat, time, re
from itchat.content import *
import tf_idf_sim
import random


# 如果对方发的是文字，则我们给对方回复以下的东西
@itchat.msg_register([TEXT])
def txt_reply(msg):
    text = msg['Text']
    random_index = random.randint(0, 5)
    print(text)
    res_txt = tf_idf_sim.find_sim_sentence(text)
    itchat.send((res_txt[random_index]), msg['FromUserName'])


# 如果对方发送的是图片，音频，视频和分享的东西我们都做出以下回复。
@itchat.msg_register([PICTURE, RECORDING, VIDEO, SHARING])
def other_reply(msg):
    itchat.send(('那我就祝你猪年大吉大利，事事顺心'), msg['FromUserName'])


@itchat.msg_register(msgType=TEXT, isFriendChat=False, isGroupChat=True, isMpChat=False)
def group_reply(msg):
    print(msg)
    if msg.User["NickName"] == '夸夸群':  # 指定群聊的名称
        txt = msg['Text']
        random_index = random.randint(0, 5)
        print(txt)
        res_txt = tf_idf_sim.find_sim_sentence(txt)
        itchat.send((res_txt[random_index]), msg['FromUserName'])


itchat.auto_login(hotReload=True)

itchat.run()
