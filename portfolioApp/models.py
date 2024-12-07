from django.db import models

# Create your models here.
class Blog(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    authorName=models.CharField(max_length=150)
    image=models.ImageField(upload_to='blog',blank=True,null=True)
    timeStamp=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=12)
    description=models.TextField(max_length=200)

    def __str__(self):
        return self.name


class Skills(models.Model):
    skill=models.CharField(max_length=150)
    experience=models.IntegerField()

    def __str__(self):
        return self.skill