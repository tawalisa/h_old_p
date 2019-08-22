'''
Created on 2018-11-1

@author: tawalisa@163.com
'''
import smtplib
import ConfigParser
import time
import os
import re
import sys
import Queue
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
dateformat = '%Y%m%d %H%M%S%f'
pattern = re.compile(r"(\d{8} \d{9})")

def  getLastTime(output):
    temp = None
    for match in pattern.finditer(output):
        t = match.group(1)
        a = datetime.datetime.strptime(t,dateformat)
        temp = a
    return temp 

def closeFile(filePath):
    if filePath:
        filePath.close()
        
r"""add total_seconds in version 2.6
"""      
def total_seconds(deltatime):
    return (deltatime.microseconds + (deltatime.seconds + deltatime.days*24*3600) * 1e6) / 1e6


def changeConfig(hostname,servertype):
    tracecommand = "imconfcontrol -install -key \"/"+hostname+"/"+servertype+"/traceOutputLevel\"=\"add=9,connection=5,backend=5,entrycache=5,modify=5,modrdn=2,delete=2,consrepl=9,chglog=9\"" 
    oplogcommand = "imconfcontrol -install -key \"/"+hostname+"/"+servertype+"/opLogOutputLevel\"=\"bind=1,add=2,modify=2, modrdn=2,delete=2, unbind=1\"" 
    print tracecommand
    print oplogcommand
    os.popen(tracecommand)
    os.popen(oplogcommand)
    pass

pstackfileformat = '%Y%m%d%H%M%S%f'
def dopstack(pid):
    command = 'pstack '+ pid+ " > 'pstack/"+datetime.datetime.now().strftime(pstackfileformat)+"'"
    os.popen(command)
    print command
    pass

def sendEmail(hostname):
    print("start sending email")
    me = "sender@lijia.com"
    you = "lijia@lijia.com"
    msg = MIMEMultipart('alternative')
    msg['Subject'] = " The automonitor was triggered on "+ hostname
    msg['From'] = me
    msg['To'] = you
    
    html = """\
    <html>
      <head></head>
      <body>
        <p>Hi Team!<br>
           The Action has been triggered<br>
           Please check!!!
        </p>
      </body>
    </html>
    """
    
    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    s = smtplib.SMTP('mail.lijia.com',25)
    s.sendmail(me, you, msg.as_string())
    s.quit()
    print("end sending email")

def undoConfig(hostname,servertype):
    tracecommand = "imconfcontrol -install -key \"/"+hostname+"/"+servertype+"/traceOutputLevel\"=\"\"" 
    oplogcommand = "imconfcontrol -install -key \"/"+hostname+"/"+servertype+"/opLogOutputLevel\"=\"bind=1,add=1,modify=1,delete=1,unbind=1\"" 
    print tracecommand
    print oplogcommand
    os.popen(tracecommand)
    os.popen(oplogcommand)
    pass


def doMonitorResouce(out_file):
    f = os.popen('sudo iotop -bo -n2')
    output = f.read()
    out_file.write("\n\n--------iotop---"+datetime.datetime.now().strftime(pstackfileformat)+"----\n")
    out_file.write(output)
    print('sudo iotop -bo -n2')
    
    f = os.popen('iostat -x')
    output = f.read()
    out_file.write("\n\n--------iostat---"+datetime.datetime.now().strftime(pstackfileformat)+"----\n")
    out_file.write(output)
    print('iostat -x')
    
    f = os.popen('top -b -n 2')
    output = f.read()
    out_file.write("\n\n--------top---"+datetime.datetime.now().strftime(pstackfileformat)+"----\n")
    out_file.write(output)
    print('top -b -n 2')


def startMonitor(resumetime,hostname,servertype,pstackInterval):
    sendEmail(hostname)
    pid = getpid(servertype)
    changeConfig(hostname,servertype)
    start_time = datetime.datetime.now()
    out_file = open("reourceMonitor.log","w")
    while 1:
        if total_seconds(datetime.datetime.now() - start_time) > resumetime:
            undoConfig(hostname,servertype);
            out_file.close()
            break;
        else:
            dopstack(pid)
            doMonitorResouce(out_file)
            time.sleep(float(pstackInterval))
    
def triggerThreshold(line,que,checkingInterval,resumetime,hostname,servertype,pstackInterval):
    if line.find("LDAPThresholdSrchTimeExceeded")>-1:
        logtime = getLastTime(line)
        if que.full():
            lastQue = que.get()
            now_time = datetime.datetime.now()
#             print(now_time)
#             print(lastQue)
            t = total_seconds(now_time - lastQue)
#             print(t)
            if t < checkingInterval:
                startMonitor(resumetime,hostname,servertype,pstackInterval)
                return True
            else:
                que.put(logtime)
            
        else:
            que.put(logtime) 
    return False

def detectLog(logPath,que,checkingInterval,resumetime,hostname,servertype,pstackInterval):
    curlogfile,curino = None,None
    while 1:
        if os.stat(logPath).st_ino != curino:
            new = open(logPath,"r")
            closeFile(curlogfile)
            curlogfile = new
            curino = os.fstat(curlogfile.fileno()).st_ino
        where = curlogfile.tell()
        line = curlogfile.readline()
        if not line:
            time.sleep(0.1)
            curlogfile.seek(where)
        else:
            if triggerThreshold(line,que,checkingInterval,resumetime,hostname,servertype,pstackInterval): 
                print "stop process"
                sys.exit()
            else:
                print line
    
def getpid(servertype): 
    f = os.popen('cat /home/imail/tmp/'+servertype+'.pid')
    imdirservpid = f.read()
    return "".join(imdirservpid.split())

def createpstackfolder():
    command = "mkdir pstack"
    os.popen(command)
    print command

createpstackfolder()
settings = ConfigParser.ConfigParser()
settings.read('shaw/settings.ini')
logPath = settings.get("settings", "logpath")
threshold = settings.getint("settings", "threshold")
checkingInterval = settings.getint("settings", "checkingInterval")
resumetime = settings.getint("settings", "resumetime")
que = Queue.Queue(threshold-1)
hostname = settings.get("settings", "hostname")
servertype = settings.get("settings", "servertype")
pstackInterval = settings.get("settings", "pstackInterval")

detectLog(logPath,que,checkingInterval,resumetime,hostname,servertype,pstackInterval)
