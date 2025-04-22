from django.db import models
from django.db.models import Count
import bcrypt
import re

class UserManager(models.Manager):
    def basic_validator_login(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email'])
        # add keys and values to errors dictionary for each invalid field
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Wrong email address!"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"    
        if len(postData['email']) == 0 :   
            errors["emailrequired"] = "Email is required!"  
        if len(postData['password']) == 0 :   
            errors["passwordrequired"] = "Password is required!"    
        #if len(user) and not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
        #    errors["passwordwronge"] = "Password or email does not exist!"   
        if not len(user):
            errors['emailnewuser'] = "Email is not registered" 
        return errors

    def basic_validator_reg(self, postData):
        errors = {}
        new_user = User.objects.filter(email = postData['email'])
        # add keys and values to errors dictionary for each invalid field       
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"  
        if len(postData['confirmpassword']) < 8:
            errors["confirmpassword"] = "Confirm Password should be at least 8 characters" 
        if len(postData['lastname']) < 3:
            errors["lastname"] = "Last name should be at least 3 characters" 
        if len(postData['firstname']) < 3:
            errors["firstname"] = "First Name should be at least 3 characters" 
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Wrong email address!"
        if postData['password'] != postData['confirmpassword']:
            errors['password_confirm'] = "Password Dosent Match!"
        if len(postData['email']) == 0 :   
            errors["emailrequired"] = "Email is required!"  
        if len(postData['password']) == 0 :   
            errors["passwordrequired"] = "Password is required!"
        if len(postData['confirmpassword']) == 0 :   
            errors["confirmpasswordrequired"] = "Confrim password is required!"
        if len(postData['lastname']) == 0 :   
            errors["lastnamerequired"] = "Last name is required!"
        if len(postData['firstname']) == 0 :   
            errors["firstnamerequired"] = "First name is required!"   
        if len(new_user):
            errors['emailnewuser'] = "Email already exist" 
        return errors

class PieManager(models.Manager):
    def basic_validator_save_Pie(self, postData):
        errors = {}
        if len(postData['piename']) == 0 :   
            errors["piename"] = "Pie name is required!"  
        if len(postData['filling']) == 0 :   
            errors["piefilling"] = "Pie filling is required!" 
        if len(postData['crust']) == 0 :   
            errors["piecrust"] = "Pie crust is required!"  
        return errors

#User model class
class User(models.Model):
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    phonenumber = models.CharField(max_length=10)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #pies
    #address
    #mypie
    objects = UserManager() 

#Pie model class
class Pie(models.Model):
    piename = models.CharField(max_length=25)
    users = models.ManyToManyField(User , related_name="pies")
    filling =  models.CharField(max_length=25, default='Cheese')
    crust =  models.CharField(max_length=25, default='Vanilla')
    created_by = models.ForeignKey(User, related_name="mypie", default=1,on_delete = models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PieManager() 

#Address model class
class Address(models.Model):
    country = models.CharField(max_length=25)
    state = models.CharField(max_length=40)
    city = models.CharField(max_length=25)
    street= models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name="address" , on_delete= models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


#This function will connection to DB and get all users in users table.
def get_users():
    return User.objects.all()

def get_user(id):
    return User.objects.get(id = id)

def create_user(post):
    user_password = post['password']
    hash1 = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt()).decode()
    return User.objects.create( firstname = post['firstname'], lastname= post['lastname'] , phonenumber = post['phonenumber'], email =  post['email'], password = hash1)

def create_pie(post):
    id = post.session['user_id'] 
    user = User.objects.get( id = id )
    Pie.objects.create( piename = post.POST['piename'] , filling = post.POST['filling'], crust= post.POST['crust'], created_by = user   )

def get_pies():
    return Pie.objects.all()

def get_pie(id):
    return Pie.objects.get(id = id)

def update_pie(post):
    pie = Pie.objects.get( id  = post['pieid'] )
    pie.piename = post['piename']
    pie.filling = post['filling']
    pie.crust = post['crust']
    pie.save()

def vote_pie( user_id , pie_id):
    user = User.objects.get( id = user_id)
    pie = Pie.objects.get( id = pie_id)
    user.pies.add(pie)

def unvote_pie( user_id , pie_id):
    print("test")
    user = User.objects.get( id = user_id)
    pie = Pie.objects.get( id = pie_id)
    pie.users.remove(user)
    #user.pies.remove(pie)

def check_vote(user_id , pie_id):
    user = User.objects.get(id = user_id)
    pie = Pie.objects.get( id = pie_id)
    # or user.pies.filter(id=pie.id).exists()
    if (pie.users.filter(id=user.id).exists()):
        return True
    else:
        return False

def login_user(post):
    user_exist = User.objects.filter(email=post.POST['email'])
    if user_exist:
        logged_user = user_exist[0] 
        if bcrypt.checkpw(post.POST['password'].encode(), logged_user.password.encode()):
            post.session['user_id'] = logged_user.id
            return True
            #messages.success(formvalue, "User successfully Logged")
        else:
            print("Failed password")    
            return False            
    else:
        return False      
    
def delete_pie(pie_id):
    pie = Pie.objects.get( id = pie_id)
    pie.delete()

#This method will get all associated records in the intermediary table between User and Pie and 
# return the count of votes for each pie in a descending order
def vote_count():
    return Pie.objects.annotate(num_votes=Count('users')).order_by('-num_votes')