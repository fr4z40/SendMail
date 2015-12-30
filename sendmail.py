#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Eduardo Frazão
#   * http://github.com/fr4z40
#   * https://bitbucket.org/fr4z40

import smtplib
from getpass import getpass
from sys import version_info

if version_info[0] == 2:
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email.mime.text import MIMEText
    from email import Encoders
else:
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email import encoders as Encoders
    raw_input = input


def main():
    smtp_server = ((raw_input("SMTP Server: ")).strip())
    smtp_port = int((raw_input("Port: ")).strip())
    mail_to = ((raw_input("Email To: ")).strip())
    subject = ((raw_input("subject: ")).strip())
    mail_from = ((raw_input("Email From: ")).strip())

    msg = MIMEMultipart()

    while 1:
        body_msg = []
        try:
            if (({'y':1, 'n':0})[(((raw_input("Write Message?  y/n : ")).strip()).lower())]) == 0:
                break
            else:

                try:
                    if (({'h':'h', 'p':'p'})[(((raw_input("(H)TML or (P)lain Text?  H/P : ")).strip()).lower())]) == 'h':
                        type_msg = 'html'
                    else:
                        type_msg = 'plain'
                except:
                    print("Wrong Key!, plain text selected by default")

                print("\nWhen you end, press CTRL+C\n\nBody Message\t[Type: %s]\n%s" % (type_msg,'='*65))
                while 1:
                    try:
                        body_msg.append(raw_input(">"))
                    except:
                        break
                print('%s\n\n' % ('='*62))
                body_msg = (('\n'.join(body_msg)).strip())
                msg.attach(MIMEText(body_msg, type_msg))
                break
        except:
            if len(body_msg) >= 1:
                break
            else:
                print('Something goes wrong!')


    while 1:
        try:
            if (({'y':1, 'n':0})[(((raw_input("Attach a file?  y/n : ")).strip()).lower())]) == 0:
                break
            else:
                file_path = ((raw_input("File Path: ")).strip())
                file_attach = MIMEBase('application', "octet-stream")
                file_attach.set_payload(open(("%s" % file_path), "rb").read())
                Encoders.encode_base64(file_attach)
                file_name = (((file_path.split('/'))[-1]).strip())
                file_attach.add_header('Content-Disposition', 'attachment; filename="%s"' % file_name)
                msg.attach(file_attach)
                break
        except:
            print('Incorrect Key, try again with "y" or "n"')

    password = ((getpass("Password: ")).strip())

    msg['Subject'] = subject
    #server = smtplib.SMTP('smtp.live.com', 587) # live.com, by example
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(mail_from, password)
    server.sendmail(mail_from, mail_to, msg.as_string())
    server.quit()

if __name__ == '__main__':
    main()
