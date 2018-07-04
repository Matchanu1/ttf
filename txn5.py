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
   'autoAdd':False,
   'autoJoin':True,
   'addmsg':"🎉ข้อความออโต้🎉\nขอบคุณที่แอดมาคับ😀",
   'acomment':"สวัสดี",
   'bcomment':"เจอกันคับ",
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
        
"╔═══════════════" + "\n" + \
                  "║สปีด➥เช็คความเร็วบอท" + "\n" \
                  "║แทค➥แทคสมาชิกในกลุ่ม" + "\n" \
                  "║เชคค่า➥เช็คการตั้งค่าบอท" + "\n" \
                  "║เชคแอด➥เช็คคนสร้างกลุ่ม" + "\n" \
                  "║ชื่อกลุ่ม➥แสดงชื่อกลุ่ม" + "\n" \
                  "║รูปกลุ่ม➥แสดงรูปกลุ่ม" + "\n" \
                  "║ไอดีกลุ่ม➥เช็คไอดีกลุ่ม" + "\n" \
                  "║รายชื่อสมาชิก➥ชื่อสมาชิกกลุ่ม" + "\n" \
                  "║ทีมงาน➥คนพัฒนา" + "\n" \
                  "║คท @➥ส่งคอนแท็กคนที่แท็ก" + "\n" \
                  "║มิด @➥ส่งMIDคนที่แท็ก" + "\n" \
                  "║ชื่อ @➥ส่งชื่อคนที่แท็ก" + "\n" \
                  "║ตัส @➥ส่งตัสคนที่แท็ก" + "\n" \
                  "║ดิส @➥ส่งดิสคนที่แท็ก" + "\n" \
                  "║ดิสวีดีโอ @➥ส่งวีดีโอคนที่แท็ก" + "\n" \
                  "║ดิสปก @➥ส่งปกคนที่แท็ก" + "\n" \
                  "║!แทค➥แท็กคนใส่ชื่อร่องหน" + "\n" \
                  "║!มิด➥หามิดคนใส่ชื่อร่องหน" + "\n" \
                  "║!คท➥ส่งคอนแท็กคนใส่ร่องหน" + "\n" \
                  "║ตั้งเวลา➥เปิดหาคนซุ่ม" + "\n" \
                  "║อ่าน➥แสดงชื่อคนซุ่ม" + "\n" \
                  "║google (ข้อความ)➥ค้นหาต่างๆ" + "\n" \
                  "║ลิ้งกลุ่ม on/off➥เปิด/ปิดลิ้งกลุ่ม" + "\n" \
                  "║ขอลิ้งกลุ่ม➥ขอลิ้งกลุ่ม" + "\n" \
                  "╚═══════════════"
    return helpMessage
    
def helptexttospeech():
    helpTextToSpeech =   ".ข้างหน้าแทน-ทั้งหมด" + "\n " \
                         " " + "\n " \
                         "-เตะ @" + "\n" + \
                         "-ออก" + "\n" \
                         "-ยกเลิก" + "\n" + \
                         "-ลบรัน" + "\n" + \
                         "-โทร(เลข)" + "\n" + \
                         "-รายชื่อกลุ่ม" + "\n" + \
                         " " + "\n " + \
                         "-เข้ากลุ่ม on\off" + "\n" + \
                         "-ออกกลุ่ม on\off" + "\n" + \
                         "-ตอนรับเข้า on\off" + "\n" + \
                         "-ตอนรับออก on\off" + "\n" + \
                         "-แอดออโต้ on\off" + "\n" + \
                         "-ตั้งเข้า:" + "\n" + \
                         "-ตั้งออก:" + "\n" + \
                         "-ตั้งแอด:" + "\n" + \
                         "-เชคตั้งเข้า" + "\n" + \
                         "-เชคตั้งออก" + "\n" + \
                         "-เชคตั้งแอด" + "\n" + \
                         " " + "\n " + \
                         "**คำสั่งเฉพาะแอดมิน**"
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
                nadya.findAndAddContactsByMid(op.param1)
                if(settings["addmsg"]in[""," ","\n",None]):
                  pass
                else:
                  nadya.sendMessage(op.param1,nadya.getContact(op.param2).displayName + str(settings["addmsg"]))

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
                cnt = nadya. getContact(op.param2)
                h = nadya.getContact(op.param2)
                nadya.sendMessage(op.param1,cnt.displayName + "\n\n" + str(wait["acomment"]))
                nadya.sendImageWithUrl(op.param1, "http://dl.profile.line-cdn.net/" + h.pictureStatus)

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
                  if msg._from in admin:
                         helpTextToSpeech = helptexttospeech()
                         nadya.sendMessage(to, str(helpTextToSpeech))
#==============================================================================#
                if msg.text.lower().startswith(".เตะ "):
                  if msg._from in admin:
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
                        if settings["autoAdd"] == True: ret_ += "\n║ ระบบแอดออโต้ ✔"
                        else: ret_ += "\n║ ระบบแอดออโต้ ✘"
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
                  if msg._from in admin:
                         if msg.toType == 2:
                             group = nadya.getGroup(msg.to)
                             gMembMids = [contact.mid for contact in group.invitee]
                         for _mid in gMembMids:
                             nadya.cancelGroupInvitation(msg.to,[_mid])
                             nadya.sendMessage(to,"ยกเลิกค้างเชิญเสร็จสิ้น(。-`ω´-)")

                if "google " in msg.text.lower():
                    spl = re.split("google ",msg.text,flags=re.IGNORECASE)
                    if spl[0] == "":
                        if spl[1] != "":
                                try:
                                    if msg.toType != 0:
                                        cl.sendText(msg.to,"กำลังรับข้อมูล กรุณารอสักครู่..")
                                    else:
                                        cl.sendText(msg.from_,"กำลังรับข้อมูล กรุณารอสักครู่..")
                                    resp = BeautifulSoup(requests.get("https://www.google.co.th/search",params={"q":spl[1],"gl":"th"}).content,"html.parser")
                                    text = "ผลการค้นหาจาก Google:\n\n"
                                    for el in resp.findAll("h3",attrs={"class":"r"}):
                                        try:
                                                tmp = el.a["class"]
                                                continue
                                        except:
                                                pass
                                        try:
                                                if el.a["href"].startswith("/search?q="):
                                                    continue
                                        except:
                                                continue
                                        text += el.a.text+"\n"
                                        text += str(el.a["href"][7:]).split("&sa=U")[0]+"\n\n"
                                    text = text[:-2]
                                    if msg.toType != 0:
                                        cl.sendText(msg.to,str(text))
                                    else:
                                        cl.sendText(msg.from_,str(text))
                                except Exception as e:
                                    print(e)

                if text.lower() == '.ลบรัน':
                  if msg._from in admin:
                      gid = nadya.getGroupIdsInvited()
                      start = time.time()
                      for i in gid:
                          nadya.rejectGroupInvitation(i)
                      elapsed_time = time.time() - start
                      nadya.sendMessage(to, "กำลังดำเนินการ(。-`ω´-)")
                      nadya.sendMessage(to, "เวลาที่ใช้: %sวินาที(。-`ω´-)" % (elapsed_time))

                if ".โทร" in msg.text.lower():
                  if msg._from in admin:
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
                  if msg._from in admin:
                      if msg.toType == 2:
                          ginfo = nadya.getGroup(to)
                          try:
                              nadya.sendMessage(to, "บอทออกเรียบร้อย(。-`ω´-)")
                              nadya.leaveGroup(to)
                          except:
                             pass

                if "ทีมงาน" == msg.text.lower():
                    msg.contentType = 13
                    nadya.sendMessage(to, "✍️  ᴛ⃢​ᴇ⃢​ᴀ⃢​ᴍ⃢   🔝ͲᎻᎬᖴ͙͛Ꮮ͙͛ᗩ͙͛ᔑ͙͛Ꮋ͙  ̾⚡")
                    nadya.sendContact(to, "uf1d4103373d5a161edf2d9d9e2d48837")
                    nadya.sendContact(to, "ua11927d673a2ae7bab9c737e4bd206d2")

                if msg.text in ["Me","me","คท","!me","!Me",".me",".Me",".คท"]:
                    nadya.sendMessage(receiver, None, contentMetadata={'mid': sender}, contentType=13)

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

                if msg.text.lower().startswith("คท "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = nadya.getContact(ls)
                            mi_d = contact.mid
                            nadya.sendContact(msg.to, mi_d)

                if msg.text.lower().startswith("มิด "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = ""
                        for ls in lists:
                            ret_ += ls
                        nadya.sendMessage(msg.to, str(ret_))

                if msg.text.lower().startswith("ชื่อ "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = nadya.getContact(ls)
                            nadya.sendMessage(msg.to, contact.displayName)

                if msg.text.lower().startswith("ตัส "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = nadya.getContact(ls)
                            nadya.sendMessage(msg.to, contact.statusMessage)

                if msg.text.lower().startswith("ดิส "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line-cdn.net/" + nadya.getContact(ls).pictureStatus
                            nadya.sendImageWithURL(msg.to, str(path))

                if msg.text.lower().startswith("ดิสวีดีโอ "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line-cdn.net/" + nadya.getContact(ls).pictureStatus + "/vp"
                            nadya.sendImageWithURL(msg.to, str(path))

                if msg.text.lower().startswith("ดิสปก "):
                    if line != None:
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = "http://dl.profile.line-cdn.net/" + nadya.getProfileCoverURL(ls)
                                nadya.sendImageWithURL(msg.to, str(path))

                if text.lower() == '!แทค':
                    gs = nadya.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        nadya.sendMessage(to, "ไม่มีคนใส่ชื่อร่องหน(。-`ω´-)")
                    else:
                        mc = ""
                        for target in targets:
                            mc += sendMessageWithMention(to,target) + "\n"
                        nadya.sendMessage(to, mc)

                if text.lower() == '!มิด':
                    gs = nadya.getGroup(to)
                    lists = []
                    for g in gs.members:
                        if g.displayName in "":
                            lists.append(g.mid)
                    if lists == []:
                        nadya.sendMessage(to, "ไม่มีคนใส่ชื่อร่องหน(。-`ω´-)")
                    else:
                        mc = ""
                        for mi_d in lists:
                            mc += "->" + mi_d + "\n"
                        nadya.sendMessage(to,mc)

                if text.lower() == '!คท':
                    gs = nadya.getGroup(to)
                    lists = []
                    for g in gs.members:
                        if g.displayName in "":
                            lists.append(g.mid)
                    if lists == []:
                        nadya.sendMessage(to, "ไม่มีคนใส่ชื่อร่องหน(。-`ω´-)")
                    else:
                        for ls in lists:
                            contact = nadya.getContact(ls)
                            mi_d = contact.mid
                            nadya.sendContact(to, mi_d)

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
                if text.lower() == '.รายชื่อกลุ่ม':
                  if msg._from in admin:
                      groups = nadya.groups
                      ret_ = "╔══[ รายชื่อกลุ่ม ]"
                      no = 0 + 1
                      for gid in groups:
                         group = nadya.getGroup(gid)
                         ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                         no += 1
                      ret_ += "\n╚══[ จำนวนกลุ่ม {} กลุ่ม(。-`ω´-)]".format(str(len(groups)))
                      nadya.sendMessage(to, str(ret_))

                if text.lower() == 'ขอลิ้งกลุ่ม':
                    if msg.toType == 2:
                        group = nadya.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            ticket = nadya.reissueGroupTicket(to)
                            nadya.sendMessage(to, "https://line.me/R/ti/g/{}".format(str(ticket)))
                        else:
                            nadya.sendMessage(to, "กรุณาเปิดลิ้งกลุ่มก่อนลงคำสั่งนี้ด้วยครับ(。-`ω´-)".format(str(settings["keyCommand"])))

                if text.lower() == 'ลิ้งกลุ่ม on':
                    if msg.toType == 2:
                        group = nadya.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            nadya.sendMessage(to, "ลิ้งกลุ่มเปิดอยู่แล้ว(。-`ω´-)")
                        else:
                            group.preventedJoinByTicket = False
                            nadya.updateGroup(group)
                            nadya.sendMessage(to, "เปิดลิ้งกลุ่มเรียบร้อย(。-`ω´-)")

                if text.lower() == 'ลิ้งกลุ่ม off':
                    if msg.toType == 2:
                        group = nadya.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            nadya.sendMessage(to, "ลิ้งกลุ่มปิดอยู่แล้ว(。-`ω´-)")
                        else:
                            group.preventedJoinByTicket = True
                            nadya.updateGroup(group)
                            nadya.sendMessage(to, "ลิ้งกลุ่มปิดเรียบร้อย(。-`ω´-)")
#=================THEFLASH====================================================#
                if text.lower() == '.แอดออโต้ on':
                  if msg._from in admin:
                      settings["autoAdd"] = True
                      nadya.sendMessage(to, "เปิดระบบออโต้บล็อค(。-`ω´-)")
                if text.lower() == '.แอดออโต้ off':
                  if msg._from in admin:
                      settings["autoAdd"] = False
                      nadya.sendMessage(to, "ปิดระบบออโต้บล็อค(。-`ω´-)")

                if text.lower() == '.เข้ากลุ่ม on':
                  if msg._from in admin:
                      settings["autoJoin"] = True
                      nadya.sendMessage(to, "เปิดระบบเข้ากลุ่มออโต้(。-`ω´-)")
                if text.lower() == '.เข้ากลุ่ม off':
                  if msg._from in admin:
                      settings["autoJoin"] = False
                      nadya.sendMessage(to, "ปิดระบบเข้ากลุ่มออโต้(。-`ω´-)")

                if text.lower() == '.ออกกลุ่ม on':
                  if msg._from in admin:
                      settings["autoLeave"] = True
                      nadya.sendMessage(to, "เปิดระบบออกกลุ่มออโต้(。-`ω´-)")
                if text.lower() == '.ออกกลุ่ม off':
                  if msg._from in admin:
                      settings["autoLeave"] = False
                      nadya.sendMessage(to, "ปิดระบบออกกลุ่มออโต้(。-`ω´-)")

                if msg.text.lower() ==  '.ตอนรับเข้า on':
                  if msg._from in admin:
                      wait['acommentOn'] = True
                      nadya.sendMessage(msg.to,"เปิดระบบตอนรับสมาชิกเข้ากลุ่ม(。-`ω´-)")
                if msg.text.lower() ==  '.ตอนรับเข้า off':
                  if msg._from in admin:
                      wait['acommentOn'] = False
                      nadya.sendMessage(msg.to,"ปิดระบบตอนรับสมาชิกเข้ากลุ่ม(。-`ω´-)")

                if msg.text.lower() == '.ตอนรับออก on':
                  if msg._from in admin:
                      wait["bcommentOn"] = True
                      nadya.sendMessage(msg.to,"เปิดระบบตอนรับสมาชิกออกกลุ่ม(。-`ω´-)")
                if msg.text.lower() == '.ตอนรับออก off':
                  if msg._from in admin:
                      wait['bcommentOn'] = False
                      nadya.sendMessage(msg.to,"ปิดระบบตอนรับสมาชิกออกกลุ่ม(。-`ω´-)")

                if ".ตั้งเข้า:" in msg.text.lower():
                  if msg._from in admin:
                      c = msg.text.replace(".ตั้งเข้า:","")
                      if c in [""," ","\n",None]:
                         nadya.sendMessage(msg.to,"เกิดข้อผิดพลาด(。-`ω´-)")
                      else:
                         wait["acomment"] = c
                         nadya.sendMessage(msg.to,"ตั้งค่าข้อความตอนรับเสร็จสิ้น(。-`ω´-)")

                if ".ตั้งแอด: " in msg.text:
                  if msg._from in admin:
                      settings["addmsg"] = msg.text.replace(".ตั้งแอด: ","")
                      nadya.sendMessage(msg.to,"ตั้งค่าข้อความแอดเสร็จสิ้น(。-`ω´-)")

                if ".ตั้งออก:" in msg.text.lower():
                  if msg._from in admin:
                      c = msg.text.replace(".ตั้งออก:","")
                      if c in [""," ","\n",None]:
                          nadya.sendMessage(msg.to,"เกิดข้อผิดพลาด(。-`ω´-)")
                      else:
                         wait["bcomment"] = c
                         nadya.sendMessage(msg.to,"ตั้งค่าข้อความตอนรับออกเสร็จสิ้น(。-`ω´-)")

                if msg.text in [".เชคตั้งเข้า"]:
                  if msg._from in admin:
                      nadya.sendMessage(msg.to,"เช็คข้อความตอนรับล่าสุด(。-`ω´-)" + "\n\n➤" + str(wait["acomment"]))
                if msg.text in [".เชคตั้งออก"]:
                  if msg._from in admin:
                      nadya.sendMessage(msg.to,"เช็คข้อความตอนรับออกล่าสุด(。-`ω´-)" + "\n\n➤" + str(wait["bcomment"]))
                if msg.text in [".เชคตั้งแอด"]:
                  if msg._from in admin:
                      nadya.sendMessage(msg.to,"เช็คข้อความแอดล่าสุด(。-`ω´-)" + "\n\n➤" + str(settings["addmsg"]))
#=================THEFLASH====================================================#
#==============================================================================#
                if msg.text.lower().startswith("พูด "):
                       sep = text.split(" ")
                       say = text.replace(sep[0] + " ","")
                       lang = 'th'
                       tts = gTTS(text=say, lang=lang)
                       tts.save("hasil.mp3")
                       nadya.sendAudio(msg.to,"hasil.mp3")
#==============================================================================#
                if text.lower() == 'ตั้งเวลา':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read['readPoint']:
                            try:
                                del read['readPoint'][msg.to]
                                del read['readMember'][msg.to]
                                del read['readTime'][msg.to]
                            except:
                                pass
                            read['readPoint'][msg.to] = msg.id
                            read['readMember'][msg.to] = ""
                            read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                            read['ROM'][msg.to] = {}
                            with open('read.json', 'w') as fp:
                                json.dump(read, fp, sort_keys=True, indent=4)
                                nadya.sendMessage(msg.to,"เปิดหาคนซุ่ม(。-`ω´-)")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                            pass
                        read['readPoint'][msg.to] = msg.id
                        read['readMember'][msg.to] = ""
                        read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                        read['ROM'][msg.to] = {}
                        with open('read.json', 'w') as fp:
                            json.dump(read, fp, sort_keys=True, indent=4)
                            nadya.sendMessage(msg.to, "Set reading point:\n" + readTime)
                  
                if text.lower() == 'อ่าน':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if receiver in read['readPoint']:
                        if read["ROM"][receiver].items() == []:
                            nadya.sendMessage(receiver,"[ Reader ]:\nNone")
                        else:
                            chiya = []
                            for rom in read["ROM"][receiver].items():
                                chiya.append(rom[1])
                            cmem = nadya.getContacts(chiya) 
                            zx = ""
                            zxc = ""
                            zx2 = []
                            xpesan = '[ Reader ]:\n'
                        for x in range(len(cmem)):
                            xname = str(cmem[x].displayName)
                            pesan = ''
                            pesan2 = pesan+"@c\n"
                            xlen = str(len(zxc)+len(xpesan))
                            xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                            zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                            zx2.append(zx)
                            zxc += pesan2
                        text = xpesan+ zxc + "\n[ Lurking time ]: \n" + readTime
                        try:
                            nadya.sendMessage(receiver, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
                        except Exception as error:
                            print (error)
                        pass
                    else:
                        nadya.sendMessage(receiver,"กรุณาพิม [ตั้งเวลา] ก่อนลงคำสั่งนี้คับ(。-`ω´-)")
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
