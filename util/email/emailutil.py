# 163:PCBBQCVVANWCHVDL

# qq:ilegxhawxgchbfcc

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.errors import MessageDefect

from email.utils import parseaddr, formataddr
import smtplib
from setting.globalsettings import getconfig


class Email():
    def __init__(self,toaddr):
        self.__smtpserver = getconfig('SMTPSERVER')
        self.__fromaddr = getconfig('EMAIL')
        self.__toaddr = toaddr
        self.__password = 'ilegxhawxgchbfcc'


    def sendemail(self,subject,content):
        msg = MIMEText(content,'html','utf-8')
        msg['From'] = self.__fromaddr
        msg['To'] = self.__toaddr
        subject = '[Tornado考勤系统] ' + subject
        msg['Subject'] = Header(subject,'utf-8').encode()
        server = smtplib.SMTP(self.__smtpserver, 25)
        server.login(self.__fromaddr, self.__password)
        try:
            server.sendmail(self.__fromaddr, [self.__toaddr], msg.as_string())
        except Exception as e:
            print(e)
        finally:
            server.quit()


def sendapprovemail(username,usergroup,email):
    approvemail = Email(email)
    subject = '[Tornado考勤系统] 用户批准'
    content = '''
    <html>
    <body>
    <p>Dear %s:</p>
    <p>您的注册已被批准,用户组为%s</p>
    </body>
    </html>
    ''' % (username,usergroup)
    approvemail.sendemail(subject,content)