from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from math import floor
from django.core.exceptions import ValidationError 

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
            raise ValidationError("Pusty Komentarz")

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
    salary = models.FloatField(null=True, default=0.0)
    objects = HoursWorkedManager()


    class Meta:
        ordering = ['-day', '-start']


    def get_absolute_url(self):
        return f"my_site/{self.id}"


    #@property
    def duration(self):
        if self.finish:
            return str(self.finish - self.start).split('.')[0]
        return 'ciężką pracą ludzie się bogacą'

    
    def get_duration(self):
        if self.finish:
            total_time = (self.finish - self.start).total_seconds()
            total_time = floor((total_time/3600)*100)/100
            return total_time
        return 0


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg')
    rate = models.FloatField(null=True)
    logged = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'


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
        if payslip and payslip.month == obj.day.month:
            payslip.month_hours += obj.get_duration()
            payslip.month_salary += obj.salary
            payslip.save()
        else:
            Payslip.objects.create(
                user=obj.user, 
                month=obj.day.month, 
                month_hours= obj.get_duration(),
                month_salary=obj.salary
                )


class Payslip(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    month = models.IntegerField()
    month_hours = models.FloatField()
    month_salary = models.FloatField(null=True)
    objects = PayslipManager()

    class Meta:
        ordering = ['-month']