from django.db import models

# Create your models here.
class User(models.Model):
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    phonenumber = models.CharField(max_length=10)
    address = models.TextField()


#This function will connection to DB and get all users in users table.
def get_users():
    return models.User.objects.all()