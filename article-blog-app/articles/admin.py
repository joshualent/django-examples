from django.contrib import admin

from .models import Article, Comment

# Register your models here.


class CommentInline(admin.TabularInline):
    """Comment Stacked Inline"""

    model = Comment


class ArticleAdmin(admin.ModelAdmin):
    """Admin for Article Model"""

    inlines = [
        CommentInline,
    ]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
