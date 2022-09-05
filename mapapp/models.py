from django.db import models

# Create your models here.


class User(models.Model):
    first_name = models.CharField('First Name', max_length=60)
    last_name = models.CharField('Last Name', max_length=60)
    email = models.EmailField('Email', max_length=100)
    password = models.CharField('Password', max_length=120)

    # Below allows this model to appear in admin page
    def __str__(self):
        return self.first_name + ' ' + self.last_name


class UserLoginTokens(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    access_token = models.CharField('Access Token', max_length=400)
    refresh_token = models.CharField('Refresh Token', max_length=400)


class UserAddress(models.Model):
    first_line = models.CharField('First Line', default=None, max_length=400)
    second_line = models.CharField('Second Line', default=True, max_length=400)
    town_city = models.CharField('Town/City', default=True, max_length=100)
    postcode = models.CharField('Postcode', default=True, max_length=50)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
