'''
 2019年1月28日18:45:37

    微信接口 -- itchat 使用

'''

import itchat
import datetime
from datetime import date, datetime, timedelta

from itchat.content import TEXT

from DbHelper import DbHelper


class IT_CHAT:

    # login in
    def lc(self):
        print("Finish Login")

    # exit
    def ec(self):
        print("exit")

    # get friends list
    def get_friends_list():
        friends = itchat.get_friends(update=True)[0:]
        return friends

    # send message
    def send_msg(msg, toUser):
        return itchat.send_msg(msg=msg, toUserName=toUser)

    def send_img(url, toUser):
        return itchat.send_image(url, toUser)

    def send_file(url, toUser):
        return itchat.send_file(url, toUser)

    # lisiten message   -- 文本信息   好友信息   群组信息   公众号信息
    @itchat.msg_register([
        itchat.content.TEXT,
        itchat.content.PICTURE,
        itchat.content.MAP,
        itchat.content.RECORDING,
        itchat.content.ATTACHMENT,
        itchat.content.VIDEO],
        isFriendChat=True,
        isGroupChat=False,
        isMpChat=False)
    def lisiten_msg(recv_msg):
        # print(recv_msg['MsgType'])  # 1:文本    3:图片      34:语音     47:表情     49:红包     62:视频     10000:系统信息
        # print(recv_msg['User'])
        # print(recv_msg['User']['MemberList'])
        # print(recv_msg['User']['NickName'])
        # print(recv_msg['Text'])
        # print(recv_msg)

        dbhelper = DbHelper()
        sql = """ INSERT INTO ITCHAT_MSGINFO (MSG_ID,
                FR_USERNAME,
                TO_USERNAME,
                MSG_TYPE,
                CONTENT,
                STATUS,
                IMG_STATUS,
                CREATE_TIME,
                VOICE_LENGTH,
                PLAY_LENGTH,
                FILE_NAME,
                FILE_SIZE,
                MEDIAL_ID,
                URL,
                APP_MSG_TYPE,
                STATUSNOTIFYCODE,
                STATUSNOTIFYUSERNAME,
                REC_USERNAME,
                REC_NICKNAME,
                REC_QQNUM,
                REC_PROVINCE,
                REC_CITY,
                REC_CONTENT,
                REC_SIGNATURE,
                REC_ALIAS,
                REC_SCENE,
                REC_VERIFYFLAG,
                REC_ATTRSTATUS,
                REC_SEX,
                REC_TICKET,
                REC_OPCODE,
                FORWARDFLAG,
                APP_ID,
                APP_TYPE,
                HASPRODUCTID,
                TICKET,
                IMGHEIGHT,
                IMGWIDTH,
                SUBMSGTYPE,
                NEWMSGID,
                ORICONTENT,
                ENCRYFILENAME,
                -- USER_MEMBERLIST,
                USER_UIN,
                USER_USERNAME,
                USER_NICKNAME,
                USER_HEADIMGURL,
                USER_CONTACTFLAG,
                USER_MEMBERCOUNT,
                USER_REMARKNAME,
                USER_HIDEINPUTBARFLAG,
                USER_SEX,
                USER_SIGNATURE,
                USER_VERIFYFLAG,
                USER_OWNERUIN,
                USER_PYINITIAL,
                USER_PYQUANPIN,
                USER_REMARKPYINITIAL,
                USER_REMARKPYQUANPIN,
                USER_STARFRIEND,
                USER_APPACCOUNTFLAG,
                USER_STATUES,
                USER_ATTRSTATUS,
                USER_PROVINCE,
                USER_CITY,
                USER_ALIAS,
                USER_SNSFLAG,
                USER_UNIFRIEND,
                USER_DISPLAYNAME,
                USER_CHATROOMID,
                USER_KEYWORD,
                USER_ENCRYCHATROOMID,
                USER_ISOWNER,
                TYPE,
                TEXT,
                ISFRIENDCHAT,
                ISGROUPCHAT,
                ISMPCHAT) VALUES
                (:MSG_ID,
                :FR_USERNAME,
                :TO_USERNAME,
                :MSG_TYPE,
                :CONTENT,
                :STATUS,
                :IMG_STATUS,
                :CREATE_TIME,
                :VOICE_LENGTH,
                :PLAY_LENGTH,
                :FILE_NAME,
                :FILE_SIZE,
                :MEDIAL_ID,
                :URL,
                :APP_MSG_TYPE,
                :STATUSNOTIFYCODE,
                :STATUSNOTIFYUSERNAME,
                :REC_USERNAME,
                :REC_NICKNAME,
                :REC_QQNUM,
                :REC_PROVINCE,
                :REC_CITY,
                :REC_CONTENT,
                :REC_SIGNATURE,
                :REC_ALIAS,
                :REC_SCENE,
                :REC_VERIFYFLAG,
                :REC_ATTRSTATUS,
                :REC_SEX,
                :REC_TICKET,
                :REC_OPCODE,
                :FORWARDFLAG,
                :APP_ID,
                :APP_TYPE,
                :HASPRODUCTID,
                :TICKET,
                :IMGHEIGHT,
                :IMGWIDTH,
                :SUBMSGTYPE,
                :NEWMSGID,
                :ORICONTENT,
                :ENCRYFILENAME,
                -- :USER_MEMBERLIST,
                :USER_UIN,
                :USER_USERNAME,
                :USER_NICKNAME,
                :USER_HEADIMGURL,
                :USER_CONTACTFLAG,
                :USER_MEMBERCOUNT,
                :USER_REMARKNAME,
                :USER_HIDEINPUTBARFLAG,
                :USER_SEX,
                :USER_SIGNATURE,
                :USER_VERIFYFLAG,
                :USER_OWNERUIN,
                :USER_PYINITIAL,
                :USER_PYQUANPIN,
                :USER_REMARKPYINITIAL,
                :USER_REMARKPYQUANPIN,
                :USER_STARFRIEND,
                :USER_APPACCOUNTFLAG,
                :USER_STATUES,
                :USER_ATTRSTATUS,
                :USER_PROVINCE,
                :USER_CITY,
                :USER_ALIAS,
                :USER_SNSFLAG,
                :USER_UNIFRIEND,
                :USER_DISPLAYNAME,
                :USER_CHATROOMID,
                :USER_KEYWORD,
                :USER_ENCRYCHATROOMID,
                :USER_ISOWNER,
                :TYPE,
                :TEXT,
                :ISFRIENDCHAT,
                :ISGROUPCHAT,
                :ISMPCHAT) """
        params = {
            'MSG_ID': recv_msg['MsgId'],
            'FR_USERNAME': recv_msg['FromUserName'],
            'TO_USERNAME': recv_msg['ToUserName'],
            'MSG_TYPE': recv_msg['MsgType'],
            'CONTENT': recv_msg['Content'],
            'STATUS':recv_msg['Status'],
            'IMG_STATUS':recv_msg['ImgStatus'],
            'CREATE_TIME': datetime.fromtimestamp((recv_msg['CreateTime'])),
            'VOICE_LENGTH':recv_msg['VoiceLength'],
            'PLAY_LENGTH':recv_msg['PlayLength'],
            'FILE_NAME':recv_msg['FileName'],
            'FILE_SIZE':recv_msg['FileSize'],
            'MEDIAL_ID':recv_msg['MediaId'],
            'URL':recv_msg['Url'],
            'APP_MSG_TYPE':recv_msg['AppMsgType'],
            'STATUSNOTIFYCODE':recv_msg['StatusNotifyCode'],
            'STATUSNOTIFYUSERNAME':recv_msg['StatusNotifyUserName'],
            'REC_USERNAME':recv_msg['RecommendInfo']['UserName'],
            'REC_NICKNAME':recv_msg['RecommendInfo']['NickName'],
            'REC_QQNUM':recv_msg['RecommendInfo']['QQNum'],
            'REC_PROVINCE':recv_msg['RecommendInfo']['Province'],
            'REC_CITY':recv_msg['RecommendInfo']['City'],
            'REC_CONTENT':recv_msg['RecommendInfo']['Content'],
            'REC_SIGNATURE':recv_msg['RecommendInfo']['Signature'],
            'REC_ALIAS':recv_msg['RecommendInfo']['Alias'],
            'REC_SCENE':recv_msg['RecommendInfo']['Scene'],
            'REC_VERIFYFLAG':recv_msg['RecommendInfo']['VerifyFlag'],
            'REC_ATTRSTATUS':recv_msg['RecommendInfo']['AttrStatus'],
            'REC_SEX':recv_msg['RecommendInfo']['Sex'],
            'REC_TICKET':recv_msg['RecommendInfo']['Ticket'],
            'REC_OPCODE':recv_msg['RecommendInfo']['OpCode'],
            'FORWARDFLAG':recv_msg['ForwardFlag'],
            'APP_ID':recv_msg['AppInfo']['AppID'],
            'APP_TYPE':recv_msg['AppInfo']['Type'],
            'HASPRODUCTID':recv_msg['HasProductId'],
            'TICKET':recv_msg['Ticket'],
            'IMGHEIGHT':recv_msg['ImgHeight'],
            'IMGWIDTH':recv_msg['ImgWidth'],
            'SUBMSGTYPE':recv_msg['SubMsgType'],
            'NEWMSGID':recv_msg['NewMsgId'],
            'ORICONTENT':recv_msg['OriContent'],
            'ENCRYFILENAME':recv_msg['EncryFileName'],
            # 'USER_MEMBERLIST':recv_msg['User']['MemberList'],
            'USER_UIN':recv_msg['User']['Uin'],
            'USER_USERNAME':recv_msg['User']['UserName'],
            'USER_NICKNAME':recv_msg['User']['NickName'],
            'USER_HEADIMGURL':recv_msg['User']['HeadImgUrl'],
            'USER_CONTACTFLAG':recv_msg['User']['ContactFlag'],
            'USER_MEMBERCOUNT':recv_msg['User']['MemberCount'],
            'USER_REMARKNAME':recv_msg['User']['RemarkName'],
            'USER_HIDEINPUTBARFLAG':recv_msg['User']['HideInputBarFlag'],
            'USER_SEX':recv_msg['User']['Sex'],
            'USER_SIGNATURE':recv_msg['User']['Signature'],
            'USER_VERIFYFLAG':recv_msg['User']['VerifyFlag'],
            'USER_OWNERUIN':recv_msg['User']['OwnerUin'],
            'USER_PYINITIAL':recv_msg['User']['PYInitial'],
            'USER_PYQUANPIN':recv_msg['User']['PYQuanPin'],
            'USER_REMARKPYINITIAL':recv_msg['User']['RemarkPYInitial'],
            'USER_REMARKPYQUANPIN':recv_msg['User']['RemarkPYQuanPin'],
            'USER_STARFRIEND':recv_msg['User']['StarFriend'],
            'USER_APPACCOUNTFLAG':recv_msg['User']['AppAccountFlag'],
            'USER_STATUES':recv_msg['User']['Statues'],
            'USER_ATTRSTATUS':recv_msg['User']['AttrStatus'],
            'USER_PROVINCE':recv_msg['User']['Province'],
            'USER_CITY':recv_msg['User']['City'],
            'USER_ALIAS':recv_msg['User']['Alias'],
            'USER_SNSFLAG':recv_msg['User']['SnsFlag'],
            'USER_UNIFRIEND':recv_msg['User']['UniFriend'],
            'USER_DISPLAYNAME':recv_msg['User']['DisplayName'],
            'USER_CHATROOMID':recv_msg['User']['ChatRoomId'],
            'USER_KEYWORD':recv_msg['User']['KeyWord'],
            'USER_ENCRYCHATROOMID':recv_msg['User']['EncryChatRoomId'],
            'USER_ISOWNER':recv_msg['User']['IsOwner'],
            'TYPE':recv_msg['Type'],
            'TEXT':recv_msg['Text'],
            'ISFRIENDCHAT':'1',
            'ISGROUPCHAT':'0',
            'ISMPCHAT':'0'
        }

        if dbhelper.Execute(sql, params):
            ...

        # insert error log


if __name__ == '__main__':

    # create new object
    ic = IT_CHAT()

    # login in
    itchat.auto_login(loginCallback=ic.lc, exitCallback=ic.ec, hotReload=True)

    # flag = send_msg('Hello', 'filehelper')
    # print(flag)

    # start listening
    itchat.run()

    # logout
    itchat.logout()