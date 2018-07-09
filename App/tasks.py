from time import sleep

from celery import shared_task


@shared_task
def send_mail_asy(email):
    sleep(3)
    # print("send mail", email)
    return email

