# coding=utf-8
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
mail_host = 'smtp.qq.com'
# receivers = '15305513057@189.cn'
receivers = ["13355661100@189.cn","13355661100@qq.cn"]
sender = '13355661100@qq.com'
passwd = 'wucimmhscslbbigb'
contents = '您有某某合同即将在某月某号到期（此邮件由系统自动发出，请不要回复）'

# 创建一个带附件的实例
message = MIMEMultipart()
message['From'] = Header("菜鸟教程", 'utf-8')
message['To'] = Header("测试", 'utf-8')
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')

# 邮件正文内容
message.attach(MIMEText('这是菜鸟教程Python 邮件发送测试……', 'plain', 'utf-8'))


# 构造邮件正文
msg=MIMEText(contents,'plain','utf-8')
# 构造邮件头部
msg['From']=sender
# msg['To'] = str(receivers)

msg['Subject'] = '合同到期预提醒，（此邮件由系统自动发出，请不要回复）'
try:
     server = smtplib.SMTP_SSL(mail_host, 465)
     server.login(sender, passwd)
     server.sendmail(sender, receivers, msg.as_string())
     print('发送成功')
except smtplib.SMTPException:
     print('无法发送')