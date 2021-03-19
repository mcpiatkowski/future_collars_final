from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from math import floor

PUBLICATION_STATUSES = (
    ('pending', 'Oczekuje'),
    ('accepted', 'Zaakceptowano'),
    ('rejected', 'Odrzucono'),
    )
# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    snippet = models.TextField(verbose_name='Snippet')
    publication_datetime = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"{self.id}/"
    

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


class HoursWorked(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    day = models.DateField(auto_now_add=True)
    start = models.DateTimeField()
    finish = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-day', '-start']

    def clean(self):
        print('lipton')
    

    def get_absolute_url(self):
        return f"my_site/{self.id}"


    def duration_seconds(self):
        pass


    #@property
    def duration(self):
        if self.finish:
            counted_seconds = (self.finish - self.start).total_seconds()
            seconds = floor(counted_seconds/100)
            #counted_seconds = floor(counted)
            minutes = floor(counted_seconds/60)
            hours = floor(minutes/3600)
            return "{}:{}:{}".format(hours, minutes, seconds)
        return 'ciężką pracą ludzie się bogacą'


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    rate = models.FloatField(null=True)
    logged = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'


    def payout(self):
        total_hours = self.user.hoursworked_set.all()