from django.contrib import admin
from .models import Article, Comment, HoursWorked, Profile
# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    fields = ['user', 'content', 'email', 'status']
    list_display = ('content', 'user', 'status')
    list_filter = ['status', 'article']
    search_fields = ['content']


class HoursWorkedAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user']}),
        ('Start & Finish', {'fields': ['start', 'finish']}),
    ]
    list_display = ('user', 'day')
    list_filter = ['user']


class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'image', 'rate']


admin.site.register(Article)
admin.site.register(Comment, CommentAdmin)
admin.site.register(HoursWorked, HoursWorkedAdmin)
admin.site.register(Profile, ProfileAdmin)
