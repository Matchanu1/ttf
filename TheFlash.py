# -*- coding: utf-8 -*-

from linepy import *
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse
from gtts import gTTS
from googletrans import Translator
#==============================================================================#
botStart = time.time()

nadya = LINE()
#nadya = LINE("TOKEN KAMU")
#nadya = LINE("Email","Password")
nadya.log("Auth Token : " + str(nadya.authToken))
channelToken = nadya.getChannelResult()
nadya.log("Channel Token : " + str(channelToken))

nadyaMID = nadya.profile.mid
nadyaProfile = nadya.getProfile()
lineSettings = nadya.getSettings()
oepoll = OEPoll(nadya)
Rfu = [nadya]
RfuBot=[nadyaMID]
admin=['uf1d4103373d5a161edf2d9d9e2d48837','ua11927d673a2ae7bab9c737e4bd206d2',nadyaMID]
Family=["uf1d4103373d5a161edf2d9d9e2d48837","ua11927d673a2ae7bab9c737e4bd206d2",nadyaMID]
RfuFamily = RfuBot + Family
#==============================================================================#
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")

read = json.load(readOpen)
settings = json.load(settingsOpen)

wait = {
   'acommentOn':False,
   'bcommentOn':False,
   'autoLeave':False,
   'autoJoin':True,
}

myProfile = {
	"displayName": "",
	"statusMessage": "",
	"pictureStatus": ""
}

myProfile["displayName"] = nadyaProfile.displayName
myProfile["statusMessage"] = nadyaProfile.statusMessage
myProfile["pictureStatus"] = nadyaProfile.pictureStatus
#==============================================================================#
def restartBot():
    print ("[ INFO ] BOT RESETTED")
    backupData()
#    time.sleep(3)
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False    
    
def logError(text):
    nadya.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
        
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        nadya.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
        
def helpmessage():
    helpMessage =  "╔═══════════════" + "\n" + \
                  "╠สปีด➥เช็คความเร็วบอท" + "\n " \
                  "╠แทค➥แทคสมาชิกในกลุ่ม" + "\n " \
                  "╠เชคค่า➥เช็คการตั้งค่าบอท" + "\n " \
                  "╠เชคแอด➥เช็คคนสร้างกลุ่ม" + "\n " \
                  "╠ชื่อกลุ่ม➥แสดงชื่อกลุ่ม" + "\n " \
                  "╠รูปกลุ่ม➥แสดงรูปกลุ่ม" + "\n " \
                  "╠ไอดีกลุ่ม➥เช็คไอดีกลุ่ม" + "\n " \
                  "╠รายชื่อสมาชิก➥รายชื่อสมาชิกกลุ่ม" + "\n " \
                  "╠รายชื่อกลุ่ม➥รายชื่อกลุ่มทั้งหมดของบอท" + "\n " \
                  "╠ทีมงาน➥คนทำบอทและพัฒนา" + "\n " \
                  "╚═══════════════"
    return helpMessage
    
def helptexttospeech():
    helpTextToSpeech =   "╔═══════════════" + "\n" + \
                         "║" + "\n " \
                         "╠.ข้างหน้าคำสั่งทั้งหมด" + "\n " \
                         "║" + "\n " \
                         "╠เตะ @" + "\n" + \
                         "╠ตอนรับเข้า" + "\n " \
                         "╠ตอนรับออก" + "\n " \
                         "╠ตั้งเข้า:" + "\n " \
                         "╠ตั้งออก:" + "\n " \
                         "╠ออก" + "\n " \
                         "╠ยกเลิก" + "\n" + \
                         "╠โทร(เลข)" + "\n" + \
                         "║"+ "\n " \
                         "╠**คำสั่งเฉพาะแอดมิน**"+ "\n " \
                         "╚═══════════════"
    return helpTextToSpeech
#==============================================================================#
def lineBot(op):
    try:
        if op.type == 0:
            print ("[ 0 ] END OF OPERATION")
            return

        if op.type == 5:
            print ("[ 5 ] NOTIFIED AUTOBLOCK")
            if settings["autoAdd"] == True:
            	nadya.blockContact(op.param1)
                #nadya.sendMessage(op.param1, "Halo {} terimakasih telah menambahkan saya sebagai teman :D".format(str(nadya.getContact(op.param1).displayName)))

        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE GROUP")
            group = nadya.getGroup(op.param1)
            if settings["autoJoin"] == True:
                nadya.acceptGroupInvitation(op.param1)

        if op.type == 15:
            if wait["bcommentOn"] and "bcomment" in wait:
            	h = nadya.getContact(op.param2)
                nadya.sendMessage(op.param1,nadya.getContact(op.param2).displayName + "\n\n" + str(wait["bcomment"]))
                nadya.sendImageWithUrl(op.param1, "http://dl.profile.line-cdn.net/" + h.pictureStatus)

        if op.type == 17:
            if wait["acommentOn"] and "acomment" in wait:
                ginfo = nadya.getGroup(op.param1)
                cnt = nadya.getContact(op.param2)
                image = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
                nadya.sendMessage(op.param1,cnt.displayName + "\n\n" + str(wait["acomment"]))
                c = Message(to=op.param1, from_=None, text=None, contentType=13)
                c.contentMetadata={'mid':op.param2}
                nadya.sendMessage(c)  
                nadya.sendImageWithUrl(op.param1,image)

        if op.type == 24:
            print ("[ 24 ] NOTIFIED LEAVE ROOM")
            if settings["autoLeave"] == True:
                nadya.leaveRoom(op.param1)

        if op.type == 25:
            print ("[ 25 ] SEND MESSAGE")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != nadya.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
#==============================================================================#

#==============================================================================#
        if op.type == 26:
            print ("[ 26 ] RECEIVE MESSAGE")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != nadya.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if settings["autoRead"] == True:
                    nadya.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
                    text = msg.text
                    if text is not None:
                        nadya.sendMessage(msg.to,text)
#==============================================================================#
                if msg.text in ["คำสั่ง","Help","help"]:
                    helpMessage = helpmessage()
                    nadya.sendMessage(to, str(helpMessage))
                if text.lower() == 'คำสั่ง2':
                	if msg.from_ in admin:
                            helpTextToSpeech = helptexttospeech()
                            nadya.sendMessage(to, str(helpTextToSpeech))
#==============================================================================#
                if msg.text.lower().startswith("เตะ "):
                	if msg.from_ in admin:
                            targets = []
                            key = eval(msg.contentMetadata["MENTION"])
                            key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            nadya.kickoutFromGroup(msg.to,[target])
                        except:
                            nadya.sendText(msg.to,"Error")
                if text.lower() == 'เชคค่า':
                    try:
                        ret_ = "╔════════════"
                        if settings["autoJoin"] == True: ret_ += "\n║ ระบบเข้ากลุ่มออโต้ ✔"
                        else: ret_ += "\n║ ระบบเข้ากลุ่มออโต้ ✘"
                        if settings["autoLeave"] == True: ret_ += "\n║ ระบบออกกลุ่มออโต้  ✔"
                        else: ret_ += "\n║ ระบบออกกลุ่มออโต้ ✘"
                        if wait["acommentOn"] == True: ret_ += "\n║ ระบบตอนรับคนเข้ากลุ่ม ✔"
                        else: ret_ += "\n║ ระบบตอนรับคนเข้ากลุ่ม ✘"
                        if wait["bcommentOn"] == True: ret_ += "\n║ ระบบตอนรับคนออกกลุ่ม ✔"
                        else: ret_ += "\n║ ระบบตอนรับคนออกกลุ่ม ✘"
                        ret_ += "\n╚════════════"
                        nadya.sendMessage(to, str(ret_))
                    except Exception as e:
                        nadya.sendMessage(msg.to, str(e))

                if ".ยกเลิก" == msg.text.lower():
                	if msg.from_ in admin:
                    if msg.toType == 2:
                        group = nadya.getGroup(msg.to)
                        gMembMids = [contact.mid for contact in group.invitee]
                        for _mid in gMembMids:
                            nadya.cancelGroupInvitation(msg.to,[_mid])
                        nadya.sendMessage(to,"ยกเลิกค้างเชิญเสร็จสิ้น(。-`ω´-)")

                if ".โทร" in msg.text.lower():
                	if msg.from_ in admin:
                     if msg.toType == 2:
                            sep = text.split(" ")
                            strnum = text.replace(sep[0] + " ","")
                            num = int(strnum)
                            nadya.sendMessage(to, "เชิญเข้าร่วมการโทร(。-`ω´-)")
                            for var in range(0,num):
                                group = nadya.getGroup(to)
                                members = [mem.mid for mem in group.members]
                                nadya.acquireGroupCallRoute(to)
                                nadya.inviteIntoGroupCall(to, contactIds=members)

                if text.lower() == '.ออก':
                	if msg.from_ in admin:
                    if msg.toType == 2:
                        ginfo = cl.getGroup(to)
                        try:
                            cl.sendMessage(to, "บอทออกเรียบร้อย(。-`ω´-)")
                            cl.leaveGroup(to)
                        except:
                            pass

                if ".ทีมงาน" == msg.text.lower():
                    msg.contentType = 13
                    nadya.sendMessage(to, "✍️  ᴛ⃢​ᴇ⃢​ᴀ⃢​ᴍ⃢   🔝ͲᎻᎬᖴ͙͛Ꮮ͙͛ᗩ͙͛ᔑ͙͛Ꮋ͙  ̾⚡")
                    nadya.sendContact(to, "u07fb5496b409998a4f1f0af307d2c6e9")
                    nadya.sendContact(to, "ua11927d673a2ae7bab9c737e4bd206d2")

                if msg.text in ["Speed","speed","Sp","sp",".Sp",".sp",".Speed",".speed","\Sp","\sp","\speed","\Speed","สปีด"]:
                	start = time.time()
                    nadya.sendMessage(to, "การตอบสนองของบอท(。-`ω´-)")
                    elapsed_time = time.time() - start
                    nadya.sendMessage(msg.to, "[ %s Seconds ]\n[ " % (elapsed_time) + str(int(round((time.time() - start) * 1000)))+" ms ]")

                if msg.text in ["ออน",".ออน","\ออน",".uptime",".Uptime"]:
                	timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    nadya.sendMessage(to, "ระยะเวลาการทำงานของบอท(。-`ω´-)\n{}".format(str(runtime)))

                if msg.text in ["Tag","tagall","แทค","แทก","Tagall","tag"]:
                	group = nadya.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//100
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*100 : (a+1)*100]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Alin \n'
                        nadya.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        nadya.sendMessage(to, "จำนวนสมาชิก {} คน(。-`ω´-)".format(str(len(nama))))
#==============================================================================#
                if text.lower() == 'เชคแอด':
                    group = nadya.getGroup(to)
                    GS = group.creator.mid
                    nadya.sendContact(to, GS)
                if text.lower() == 'ไอดีกลุ่ม':
                    gid = nadya.getGroup(to)
                    nadya.sendMessage(to, "\n" + gid.id)
                if text.lower() == 'รูปกลุ่ม':
                    group = nadya.getGroup(to)
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    nadya.sendImageWithURL(to, path)
                if text.lower() == 'ชื่อกลุ่ม':
                    gid = nadya.getGroup(to)
                    nadya.sendMessage(to, "\n" + gid.name)
                if text.lower() == 'รายชื่อสมาชิก':
                    if msg.toType == 2:
                        group = nadya.getGroup(to)
                        ret_ = "╔══[ รายชื่อสมชิกกลุ่ม ]"
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n╠ {}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\n╚══[ จำนวนสมาชิก {} คน(。-`ω´-) ]".format(str(len(group.members)))
                        nadya.sendMessage(to, str(ret_))
                if text.lower() == 'รายชื่อกลุ่ม':
                        groups = nadya.groups
                        ret_ = "╔══[ รายชื่อกลุ่ม ]"
                        no = 0 + 1
                        for gid in groups:
                            group = nadya.getGroup(gid)
                            ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n╚══[ จำนวนกลุ่ม {} กลุ่ม(。-`ω´-)]".format(str(len(groups)))
                        nadya.sendMessage(to, str(ret_))
#=================THEFLASH====================================================#
                if text.lower() == '.เข้ากลุ่ม on':
                	if msg.from_ in admin:
                            settings["autoJoin"] = True
                            nadya.sendMessage(to, "เปิดระบบเข้ากลุ่มออโต้(。-`ω´-)")
                if text.lower() == '.เข้ากลุ่ม off':
                	if msg.from_ in admin:
                            settings["autoJoin"] = False
                            nadya.sendMessage(to, "ปิดระบบเข้ากลุ่มออโต้(。-`ω´-)")

                if text.lower() == '.ออกกลุ่ม on':
                	if msg.from_ in admin:
                            settings["autoLeave"] = True
                            nadya.sendMessage(to, "เปิดระบบออกกลุ่มออโต้(。-`ω´-)")
                if text.lower() == '.ออกกลุ่ม off':
                	if msg.from_ in admin:
                            settings["autoLeave"] = False
                            nadya.sendMessage(to, "ปิดระบบออกกลุ่มออโต้(。-`ω´-)")

                if msg.text.lower() ==  '.ตอนรับเข้า on':
                	if msg.from_ in admin:
                            wait['acommentOn'] = True
                            nadya.sendMessage(msg.to,"เปิดระบบตอนรับสมาชิกเข้ากลุ่ม(。-`ω´-)")
                if msg.text.lower() ==  '.ตอนรับเข้า off':
                	if msg.from_ in admin:
                            wait['acommentOn'] = False
                            nadya.sendMessage(msg.to,"ปิดระบบตอนรับสมาชิกเข้ากลุ่ม(。-`ω´-)")

                if msg.text.lower() == '.ตอนรับออก on':
                	if msg.from_ in admin:
                            wait["bcommentOn"] = True
                            nadya.sendMessage(msg.to,"เปิดระบบตอนรับสมาชิกออกกลุ่ม(。-`ω´-)")
                if msg.text.lower() == '.ตอนรับออก off':
                	if msg.from_ in admin:
                            wait['bcommentOn'] = False
                            nadya.sendMessage(msg.to,"ปิดระบบตอนรับสมาชิกออกกลุ่ม(。-`ω´-)")

                if ".ตั้งเข้า:" in msg.text.lower():
                	if msg.from_ in admin:
                            c = msg.text.replace(".ตั้งเข้า:","")
                    if c in [""," ","\n",None]:
                        nadya.sendMessage(msg.to,"เกิดข้อผิดพลาด(。-`ω´-)")
                    else:
                        wait["acomment"] = c
                        nadya.sendMessage(msg.to,"ตั้งค่าข้อความตอนรับเสร็จสิ้น(。-`ω´-)")

                if ".ตั้งออก:" in msg.text.lower():
                	if msg.from_ in admin:
                            c = msg.text.replace(".ตั้งออก:","")
                    if c in [""," ","\n",None]:
                        nadya.sendMessage(msg.to,"เกิดข้อผิดพลาด(。-`ω´-)")
                    else:
                        wait["bcomment"] = c
                        nadya.sendMessage(msg.to,"ตั้งค่าข้อความตอนรับออกเสร็จสิ้น(。-`ω´-)")
#=================THEFLASH====================================================#
#==============================================================================#
                if msg.text.lower().startswith(".พูด "):
                       sep = text.split(" ")
                       say = text.replace(sep[0] + " ","")
                       lang = 'th'
                       tts = gTTS(text=say, lang=lang)
                       tts.save("hasil.mp3")
                       nadya.sendAudio(msg.to,"hasil.mp3")
#==============================================================================#
        if op.type == 55:
            print ("[ 55 ] NOTIFIED READ MESSAGE")
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                   pass
            except:
                pass
    except Exception as error:
        logError(error)
#==============================================================================#
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
