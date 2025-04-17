from django.db import models

#User model class
class User(models.Model):
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    phonenumber = models.CharField(max_length=10)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #pies

#Pie model class
class Pie(models.Model):
    piename = models.CharField(max_length=25)
    users = models.ManyToManyField(User , related_name="pies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#This function will connection to DB and get all users in users table.
def get_users():
    return User.objects.all()

def create_user(post):
    return User.objects.create( firstname = post['firstname'], lastname= post['lastname'] , phonenumber = post['phonenumber'], address = post['address'] )

def create_pie(post):
    Pie.objects.create( piename = post['piename']  )

def get_pies():
    return Pie.objects.all()

def get_pie(id):
    return Pie.objects.get(id = id)

def update_pie(post):
    pie = Pie.objects.get( id  = post['pieid'] )
    pie.piename = post['piename']
    pie.save()

def vote_pie( user_id , pie_id):
    user = User.objects.get( id = user_id)
    pie = Pie.objects.get( id = pie_id)
    user.pies.add(pie)