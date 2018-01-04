from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import sys


class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = {}
        
        try:
            name = postData['name']
            username = postData['username']
            hire_date = postData['hire_date']
            password = postData['password']
            cpassword = postData['cpassword']

            if len(name) < 3:
                errors['inName'] = 'Name is too short; minimum 3 characters are required!'

            if len(username) < 3: 
                errors['inUsername'] = 'Userame is too short; minimum 3 characters are required!'
            
            if len(password) < 8:
                errors['inPassword'] = "Pasword must be minimum 8 characters long!"  
            elif password != cpassword:
                errors['inCPassword'] = 'Passwords do not match!'    

            if not errors:
                if User.objects.filter(username=username).exists():
                    errors['user_found'] = 'User already exists'
                else:
                    # if no errors and new user, add user to the database
                    hashpass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

                    user = User()
                    user.name = name
                    user.username = username
                    user.hire_date = hire_date
                    user.password = hashpass
                    user.save()

                    return user

        except:
            errors['userInput'] = 'An error has occured. Please fill the form again.'

        return errors    

    def validate_login(self, postData):
        errors = {}

        try:
            username = postData['username']
            password = postData['password']

            crt_user=User.objects.filter(username=username)
            if len(crt_user) == 1: 
                hashpassdb = crt_user[0].password
                if bcrypt.checkpw(password.encode(), hashpassdb.encode()):
                    return crt_user[0]
                else:
                    error['login'] = 'Username or password not valid '
                
            else:
                error['usernameInp'] = 'Wrong username or password'
        
        except: 
            errors['userInput'] = 'An error has occured. Please try again.'
        
        return errors            

class ItemManager(models.Manager):
    def validate_createItem(self, postData):
        errors = {}  
        print 'postData:', postData

        try:
            item_name = postData['item_name']
            user_id = int(postData['user_id'])

            if len(item_name) < 1: 
                errors['inItemEmpty'] = 'Field cannot be empty'
            elif len(item_name) <3:         
                errors['inItemLength'] = 'Minimum 3 characters are required for an item'
             
            if not errors:
 
                wisher=User.objects.get(id=user_id)

                item = Item.objects.create(item_name=item_name, wished_by=wisher)
                item.fav_by.add(wisher)

                '''
                item = Item()
                item.item_name = item_name
                item.wished_by = wisher
                print item.wished_by
                item.save()
                print item
                '''
                return item

        except:
            print sys.exc_info()
            errors['userInput'] = 'An error has occured. Please reintroduce item.'

        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    hire_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 
    objects = UserManager()       
    def __str__(self):
        return self.name 

class Item(models.Model):
    item_name = models.CharField(max_length=255)
    wished_by = models.ForeignKey(User, related_name="wisheditems")
    fav_by = models.ManyToManyField(User, related_name="favoriteitems")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)  
    objects = ItemManager()  
    def __str__(self):
        return self.item_name 