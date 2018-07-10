from time import sleep

from celery import shared_task

from App.viewhelper import send_mail_to


@shared_task
def send_mail_asy(email):
    sleep(3)
    # print("send mail", email)
    return email


@shared_task
def send_mail_to_asy(u_username, active_url, u_email):
    send_mail_to(u_username, active_url, u_email)
    return u_username + u_email
