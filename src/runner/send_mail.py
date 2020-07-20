import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.common.constant import ENCODING
from src.config import setting
from src.config.setting import CONFIG
from src.runner.create_report import new_report


def send_mail(new_file):
    """
    发送邮件
    :param new_file: 邮件内容
    :return: 成功：打印邮件发送成功，失败：打印失败原因
    """
    f = open(new_file, "rb")
    mail_body = f.read()
    f.close()
    # 发送附件
    report = new_report(setting.TEST_REPORT)
    send_file = open(report, "rb").read()
    # --------- 读取config.ini配置文件,获取邮件发送参数 -----
    host = CONFIG.get("mail", "host_server")
    ssl_port = CONFIG.get("mail", "ssl_port")
    sender = CONFIG.get("mail", "from")
    receiver = CONFIG.get("mail", "to")
    user = CONFIG.get("mail", "user")
    pwd = CONFIG.get("mail", "password")
    subject = CONFIG.get("mail", "subject")

    attachment = MIMEText(send_file, "base64", ENCODING)
    attachment["Content-Type"] = "application/octet-stream"
    attachment.add_header("Content-Disposition", "attachment", filename=("gbk", "", report))

    msg = MIMEMultipart("related")
    msg.attach(attachment)
    msg_text = MIMEText(mail_body, "html", ENCODING)
    msg.attach(msg_text)
    msg["Subject"] = subject
    msg["from"] = sender
    msg["to"] = receiver

    try:
        server = smtplib.SMTP_SSL(host, port=ssl_port)
        server.login(user, pwd)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        print("邮件发送成功！")
    except Exception as e:
        print("邮件发送失败：" + str(e))
