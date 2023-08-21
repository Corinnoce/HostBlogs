from django.db import models
from django.utils.text import slugify
from django.core.paginator import Paginator
from .email import sendmail_for_newarticle

class Category(models.Model):
    name = models.CharField(max_length=254)
    picture = models.ImageField(upload_to='images/categories/',blank=True, null=True)
    cloudpicture = models.CharField(max_length=3000,blank=True)
    slug = models.SlugField(max_length=1000,blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
       self.slug = slugify(self.name)
       super(Category, self).save(*args, **kwargs) # Call the real save() method

class Newsletter(models.Model):
    email = models.CharField(max_length=500,unique=True)     

    def __str__(self):
        return self.email

def get_subscribe_emails():
    subscribers=Newsletter.objects.all()
    emails_list = [subscribe.email for subscribe in subscribers]
    return emails_list

class Author(models.Model):
    name = models.CharField(max_length=500)
    picture = models.ImageField(upload_to='images/authors/',blank=True, null=True)
    cloudpicture = models.CharField(max_length=10000,null=True,blank=True)
    description = models.TextField(blank=True)
    facebook = models.CharField(max_length=50000, blank=True, null=True)
    twitter = models.CharField(max_length=50000, blank=True, null=True)
    whatsapp = models.CharField(max_length=50000, blank=True, null=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='images/articles/',blank=True, null=True)
    cloudpicture = models.CharField(max_length=3000,blank=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=1000,blank=True, null=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    sendmail = models.BooleanField(default=True)
    published = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
       self.slug = slugify(self.title)
       super(Article, self).save(*args, **kwargs) 
       if self.sendmail and self.published :
        sendmail_for_newarticle(self,get_subscribe_emails())

class SousArticle(models.Model):
    """docstring for SousArticle"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    sub_title = models.CharField(max_length=300)
    picture = models.ImageField(upload_to='images/articles/',blank=True, null=True)
    cloudpicture = models.CharField(max_length=3000,blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.sub_title

class Tag(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=254,blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs) 

class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    username = models.CharField(max_length=254)
    content = models.TextField()
    created_at = models.DateField(auto_now=True, auto_now_add=False)


def paginate(request,objects,nbre):
    paginator = Paginator(objects,nbre)
    page = request.GET.get('page')
    return paginator.get_page(page)


def get_category():
    return Category.objects.all()

def get_category_blog(category):
    articles = Article.objects.filter(category=category,published=True)
    return articles
