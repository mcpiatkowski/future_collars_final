from django.apps import apps
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from math import floor, ceil
from django.core.exceptions import ValidationError
from django.template.defaultfilters import date
from django.utils import timezone

import pytz
import datetime


PUBLICATION_STATUSES = (
    ('pending', 'Oczekuje'),
    ('accepted', 'Zaakceptowano'),
    ('rejected', 'Odrzucono'),
    )


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=256, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    snippet = models.CharField(max_length=120, verbose_name='Snippet')
    publication_datetime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-publication_datetime']
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:article-detail', args=[self.id])
    

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField(verbose_name='comment')
    email = models.EmailField(max_length=256, verbose_name='e-mail', default='')
    publication_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=8, 
        choices=PUBLICATION_STATUSES, 
        default='accepted',
        #editable=False,
        )
    
    def __str__(self):
        return self.content

    def clean(self):
        if not self.content:
            raise ValidationError("Pusty komentarz")

    def get_absolute_url(self):
        return reverse('articles:article-detail', args=[self.article.id])


class HoursWorkedManager(models.Manager):

    def total_salary(self, obj):
        obj.salary = floor(obj.get_duration() * obj.user.profile.rate*100)/100
        obj.save()


class HoursWorked(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    day = models.DateField(auto_now_add=True)
    start = models.DateTimeField()
    finish = models.DateTimeField(null=True)
    salary = models.FloatField(null=True)
    objects = HoursWorkedManager()


    class Meta:
        ordering = ['-day', '-start']


    def get_absolute_url(self):
        return f"my_site/{self.id}"

    def get_time(self):
        tzname = 'Europe/Warsaw'
        timezone.activate(pytz.timezone(tzname))
        now = timezone.now()
        return str(now - self.start).split('.')[0]

    #@property
    def duration(self):
        if self.finish:
            return str(self.finish - self.start).split('.')[0]
        return ''
    
    def get_duration(self):
        if self.finish:
            total_time = (self.finish - self.start).total_seconds()
            total_time = ceil((total_time/3600)*100)/100
            return total_time
        return 0

    def get_current_salary(self):
        rate = self.user.profile.rate
        duration = (timezone.now() - self.start).total_seconds()
        salary = floor((duration/3600)*100*rate)/100
        return str(salary) + ' PLN'

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    rate = models.FloatField(null=True)
    logged = models.BooleanField(default=False)

#    def __str__(self):
#        return f'{self.user.username} Profile'

    def get_last_pending_hours_worked(self):
        obj = apps.get_model('articles.HoursWorked').objects.filter(user__profile=self, start__isnull=False, finish__isnull=True).last()
        if obj:
            return obj.get_time(), obj.get_current_salary()
        obj = apps.get_model('articles.HoursWorked').objects.first()
        return obj.duration(), str(obj.salary) + ' PLN'

    def get_absolute_url(self):
        return reverse('articles:my-site')

    def time_elapsed(self):
        if self.start:
            return datetime.datetime.now() - self.start
        return None


class BlacklistManager(models.Manager):

    def validate_words(self, obj):
        blacklist = Blacklist.objects.all().values_list('word', flat=True)
        print("BLACKLIST: ", blacklist)
        for word in obj:
            if word in blacklist:
                return True
           # for blacklist_obj in Blacklist.objects.all():
            ##       return True
        return False


class Blacklist(models.Model):
    word = models.CharField('word', max_length=16)
    objects = BlacklistManager()

    def __str__(self):
        return self.word


class PayslipManager(models.Manager):
    
    def update(self, obj):
        payslip = Payslip.objects.all().last()
        if payslip:
            p_month = payslip.month.strftime('%b')
            h_month = obj.day.strftime('%b')
            if p_month == h_month:
                payslip.month_hours += obj.get_duration()
                payslip.month_salary += obj.salary
                payslip.save()
        else:
            Payslip.objects.create(
                user=obj.user, 
                month=obj.day, 
                month_hours= obj.get_duration(),
                month_salary=obj.salary
                )


class Payslip(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    month = models.DateField()
    month_hours = models.FloatField()
    month_salary = models.FloatField(null=True)
    objects = PayslipManager()

    class Meta:
        ordering = ['-month']

    
    def get_month_str(self):
        return date(self.month, 'F')
        