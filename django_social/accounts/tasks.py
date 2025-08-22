from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_otp(email,code):
    send_mail(
    subject="Otp Code" ,
    message= f"Your otp code is : {code}",
    from_email="matin.amani101013@email.com" , 
    recipient_list = [email,]
)