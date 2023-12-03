from email import message
from django.core.mail import send_mail
import random
from . models import *

from django.conf  import settings


def share_blog(email_f,title,email_to,comment, blog_token,name):
    try:
        subject = f'{name }Shared a new blog {title}'
        message = f'Title : {title}   commnet : {comment} \n Please click on the link below to reset your password,\n https://django-blog-application.onrender.com/view-blog/{blog_token}' 
        email_from = settings.EMAIL_HOST
        send_mail(subject, message, email_from, [email_to])
    except Exception as e:
        print(e)