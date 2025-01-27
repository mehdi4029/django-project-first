from django.db import models
from django.contrib.auth.models import User
from jdatetime import datetime
import jdatetime
from django.utils import timezone



# methods -------------------------------------------------------------------------------------------------------
def createUniquePath(instance,fileName):
       return f'static/media/images/user_{instance.author.id}/{fileName}'





# Create your models here.
class Category(models.Model) :
    name = models.CharField(max_length=100)

class Post(models.Model) :
    statusChoices = [
        ('draft' , 'Draft') ,
        ('published' , 'Published' ,)
    ]
    title = models.CharField(max_length=100)
    body = models.TextField()
    image = models.FileField(upload_to=createUniquePath)
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) # will update after instanciation
    updated_at = models.DateTimeField(auto_now=True ) #will update in every .save()
    poststatus = models.CharField(max_length=100 , choices = statusChoices , default="draft")
    publish_date = models.DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M") )
    is_important = models.BooleanField(default=False)

    @property
    def description(self):
        return self.body[:200] if len(self.body) > 200 else self.body
    @property
    def getJdateTime(self):
        return self.publish_date.strftime("%Y-%m-%d %H:%M")[0:len(self.publish_date.strftime("%Y-%m-%d %H:%M"))-5].replace("-" , "/")

    # converting created_at to jalali --->  jdatetime.date.fromgregorian(date=x.created_at)



class Comment(models.Model) :
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    related_to_post = models.ForeignKey(Post , on_delete=models.CASCADE)

    @property
    def getJdateTime(self):
        return str(jdatetime.datetime.fromgregorian(datetime=self.created_at))[:10].replace('-' , '/')