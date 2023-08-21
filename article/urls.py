from django.urls import path
from .views import blog,detail,postcomment,subscribe,contact_us_on_email

urlpatterns = [
    path('',blog,name="blog"),
    path('<str:slug>/',detail,name="detail"),
    path('post/comments/',postcomment,name="postcomment"),
    path('newsletters/subscribe/',subscribe,name="subscribe"),
    path('message/mail/send/',contact_us_on_email,name="contact_us_on_email")
]
