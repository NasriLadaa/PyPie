from django.db import models
import bcrypt

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

#Pie model class
class Pie(models.Model):
    piename = models.CharField(max_length=25)
    users = models.ManyToManyField(User , related_name="pies")
    filling =  models.CharField(max_length=25, default='Cheese')
    crust =  models.CharField(max_length=25, default='Vanilla')
    created_by = models.ForeignKey(User, related_name="mypie", default=1,on_delete = models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    
