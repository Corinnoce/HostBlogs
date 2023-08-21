from django.contrib import admin
from .models import Article,Category,Author,Tag,Newsletter,SousArticle
from django.utils.translation import gettext_lazy as _

class ArticleView(admin.ModelAdmin):
    list_display=('title','category','published')

class SousArticleView(admin.ModelAdmin):
    list_display=('sub_title','article')

class CategorieView(admin.ModelAdmin):
    list_display=('name','slug')

class AuthorView(admin.ModelAdmin):
    list_display=('name','description')

class TagView(admin.ModelAdmin):
    list_display=('name','category')   

admin.site.register(SousArticle,SousArticleView)
admin.site.register(Tag,TagView)
admin.site.register(Newsletter)
admin.site.register(Category,CategorieView)
admin.site.register(Author,AuthorView)
admin.site.register(Article,ArticleView)


admin.site.site_title = _("CRYPTOEARN")
admin.site.site_header = _("CRYPTOEARN")
admin.site.index_title = _("CRYPTOEARN")
