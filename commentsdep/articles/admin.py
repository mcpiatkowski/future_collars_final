from django.contrib import admin
from .models import (
    Article, 
    Comment, 
    HoursWorked, 
    Profile, 
    Blacklist, 
    Payslip,
    )


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


class CommentAdmin(admin.ModelAdmin):
    fields = ['user', 'content', 'email', 'status']
    list_display = ('content', 'user', 'status')
    list_filter = ['status', 'article']
    search_fields = ['content']


class HoursWorkedAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user']}),
        ('Start & Finish', {'fields': ['start', 'finish']}),
        ('Salary', {'fields': ['salary']}),
    ]
    list_display = ('user', 'day', 'salary')
    list_filter = ['user']


class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'image', 'rate', 'logged']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(HoursWorked, HoursWorkedAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Blacklist)
admin.site.register(Payslip)