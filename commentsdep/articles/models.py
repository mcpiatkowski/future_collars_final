from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from math import floor
import decimal

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
        default='pending',
        #editable=False,
        )
    
    def __str__(self):
        return self.content


class HoursWorkedManager(models.Manager):

    def total_salary(self, obj):
        obj.salary = obj.get_duration * obj.user.profile.rate
        obj.save()


class HoursWorked(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    day = models.DateField(auto_now_add=True)
    start = models.DateTimeField()
    finish = models.DateTimeField(null=True)
    salary = models.DecimalField(max_digits=4, decimal_places=2, null=True, default=0)
    objects = HoursWorkedManager


    class Meta:
        ordering = ['-day', '-start']

    
    def clean(self):
        print("USER: ", self.user)


    def get_absolute_url(self):
        return f"my_site/{self.id}"


    #@property
    def duration(self):
        if self.finish:
            counted_seconds = (self.finish - self.start).total_seconds()
            seconds = floor(counted_seconds/100)
            #counted_seconds = floor(counted)
            minutes = floor(counted_seconds/60)
            hours = floor(minutes/3600)
            return "{}h {} m".format(hours, minutes)
        return 'ciężką pracą ludzie się bogacą'

    
    def get_duration(self):
        if self.finish:
            total_time = (self.finish - self.start).total_seconds()
            print("GET DURATION: ", total_time)
            print("GET DURATION TYPE: ", type(total_time))
            total_time = total_time/3600
            #total_time = floor(total_time *100)/100
            print("GET DURATION AFTER FLOOR: ", total_time)
            return decimal.Decimal(total_time)
        return 0


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    rate = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    logged = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'


class Blacklist(models.Model):
    word = models.CharField('word', max_length=16)

    def __str__(self):
        return self.word
