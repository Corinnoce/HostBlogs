from django.shortcuts import render,get_object_or_404,redirect
from article.models import *
from accounts.models import Accounts
from django.urls import reverse
from django.db.models import Q
from .email import ismail,sendmail_for_newsubscribe
from django.contrib import messages

def index(request):
    context={}
    #Accounts.objects.create_user(username="Corinnoce",password="forget",is_staff=True,is_superuser=True)
    articles = Article.objects.filter(published=True)
    context['portfolio'] = Article.objects.filter(published=True,picture__isnull=False).order_by('-created_at')[:4]
    context['articles'] = paginate(request,articles,3)
    
    return render(request,'index.html',context)

def blog(request):
    articles = Article.objects.filter(published=True)
    if category:=request.GET.get('category'):
        articles = Article.objects.filter(published=True,category=get_object_or_404(Category,slug=category))
    if tag:=request.GET.get('tag'):
        articles = Article.objects.filter(Q(title__icontains=tag)|Q(description__icontains=tag),published=True)
    if article:=request.GET.get('article'):
        articles = Article.objects.filter(Q(title__icontains=article)|Q(description__icontains=article),published=True)

    articles = paginate(request,articles,3)
    return render(request,'articles/index.html',{'articles':articles,'categorys':get_category()})

def detail(request,slug):
    context={}
    context['article'] = get_object_or_404(Article,slug=slug,published=True)
    context['categorys'] = get_category()
    context['recent_post'] = get_category_blog(context['article'].category)
    context['tags'] = Tag.objects.filter(category=context['article'].category)
    context['comments'] = Comment.objects.filter(article=context['article'])
    context['s_articles'] = SousArticle.objects.filter(article=context['article'])

    return render(request,'articles/detail.html',context)

def add_newsletter(request,email):
    if ismail(email):
        get,created=Newsletter.objects.get_or_create(email=email)
        if created:
            sendmail_for_newsubscribe(email)
            return render(request,'index.html',{'succes':"Vous êtes maintenant abonnée à notre newsletter :) "})

def postcomment(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        content = request.POST.get('content')
        email = request.POST.get('email')
        slug = request.POST.get('slug')
        if ismail(email):
            if username!='' and content!='' and slug!='':
                add_newsletter(request,email)
                blog = get_object_or_404(Article,slug=slug,published=True)
                Comment.objects.create(username=username,content=content,article=blog)
            else:
                messages.error(request,"Veuillez remplir le formulaire ")
        else:
            messages.error(request,"Email invalide ")
        return redirect(reverse('detail',kwargs={'slug':slug}))

def subscribe(request):
    if request.method == 'POST':
        if ismail(request.POST.get('email')):
            add_newsletter(request,request.POST.get('email'))
        else:
            messages.error(request,"Email save already ")
    return redirect('index')

def contact_us_on_email(request):
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        name = request.POST.get('name')
        message = request.POST.get('message')

        if ismail(email):
            if subject!='' and email!='' and name!='' and message!='':
                pass
            else:
                messages.error(request,"Veuillez remplir le formulaire")
        else:
            messages.error(request,"Email invalide")
    return redirect('index')