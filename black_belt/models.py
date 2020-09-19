from django.db import models
import bcrypt
import re


class UserManager(models.Manager):
    def register_validator(self, postData):
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9._+-]+@[a-zA-Z0-9._+-]+\.[a-zA-Z]+$')
        errors = {}
        if (len(postData['first-name']) or len(postData['last-name'])) < 2:
            errors['name'] = " First and/or last name must be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_password'] = "Email/Password error"
        if User.objects.filter(email=postData['email']).exists():
            errors['email_password'] = "Email/Password error"
        if len(postData['password']) < 8:
            errors['email_password'] = "Email/Password error"
        if postData['password'] != postData['confirm-pw']:
                errors['email_password'] = "Email/Password error"
        return errors

    def login_validator(self, postData):
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9._+-]+@[a-zA-Z0-9._+-]+\.[a-zA-Z]+$')
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_password'] = "Email/Password error"
        user = User.objects.filter(email=postData['email'])
        if not user:
            errors['email_password'] = "Login error"
        else:
            if user:
                logged_user = user[0]
                if bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()) == False:
                    errors['email_password'] = "Login error"
        return errors

class WishManager(models.Manager):
    def wish_validator(self, postData):
        errors = {}
        if len(postData['wish-item']) < 3:
            errors['wish_item'] = "Wish must be at least 3 characters"
        if len(postData['desc']) < 3:
            errors['desc'] = "Description must be at least 3 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wish(models.Model):
    wish_item = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(
        User, related_name='uploaded_wishes', on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name='liked_wishes')
    granted = models.BooleanField(False)
    objects = WishManager()
