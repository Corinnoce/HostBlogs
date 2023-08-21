from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from blog import settings
import re


def sendmail_for_newsubscribe(email):
	content_html = render_to_string('mails/subscribe.html')
	text_content = strip_tags(content_html)
	subject = "Nous vous remercions pour avoir abonner à notre newsletters"
	from_mail = settings.EMAIL_HOST_USER
	email = EmailMultiAlternatives(subject,text_content,from_mail,[email])
	email.attach_alternative(content_html,"text/html")
	email.send()

def sendmail_for_newarticle(article,mailslist):
	link = f"https://corinnoce.pythonanywhere.com/{article.slug}"
	content_html = render_to_string('mails/article.html',{'article':article,'link':link})
	text_content = strip_tags(content_html)
	from_mail = settings.EMAIL_HOST_USER
	subject = "Nouveau article"
	email = EmailMultiAlternatives(subject,text_content,from_mail,mailslist)
	email.attach_alternative(content_html,"text/html")
	email.send()

def ismail(mail):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern,mail) is not None  
