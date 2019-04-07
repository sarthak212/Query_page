from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# Create your models here.
class user_info(models.Model):
    user_p=models.ForeignKey(User,on_delete=models.CASCADE,related_name="userinf")
    studies=models.CharField(max_length=100,blank=True,null=True)
    home=models.CharField(max_length=300,blank=True,null=True)
    work=models.CharField(max_length=200,blank=True,null=True)
    image_field=models.ImageField(upload_to='profile_pic',blank=True)
class question(models.Model):
    author=models.ForeignKey(user_info,on_delete=models.CASCADE)
    question_title=models.CharField(max_length=100)
    published=models.BooleanField(default=False)
    publish_date=models.DateField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('cloneapp:question_detail',kwargs={'pk':self.pk})
    def publish(self):
        self.published=True
        self.publish_date=timezone.now()

class answerclass(models.Model):
    question_answer=models.ForeignKey(question,on_delete=models.CASCADE,related_name='question_ans')
    author_ans=models.ForeignKey(user_info,on_delete=models.CASCADE,related_name='user_information')
    title_ans=models.CharField(max_length=400)
