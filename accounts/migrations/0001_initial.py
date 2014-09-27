# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import os
from sys import path
from django.core import serializers

def makeAwesomePeople (apps, schema_editor):
    User = apps.get_model ('auth', 'User')
    db_alias = schema_editor.connection.alias
        
    User.objects.using (db_alias).bulk_create([
        User (date_joined = "2014-09-24T06:03:56.267Z", last_login = "2014-09-24T06:04:04.863Z", first_name = "Justin", last_name = "Brown", is_staff = True, username = "justinbrown", is_active = True, email = "brown.justin.michael@gmail.com", password = "pbkdf2_sha256$12000$JgAopSkAH1aN$jFKrm6ma6yVZ2+Ua1dImHOIXu6Ols/bdfUns7DpRJDI=", is_superuser = True),
        User (date_joined = "2014-09-23T04:29:44Z", last_login = "2014-09-23T04:29:44Z", first_name = "Nathan", last_name = "Brown", is_staff = True, username = "NathanBrown", is_active = True, email = "Brown.Nathan.Andrew@gmail.com", password = "pbkdf2_sha256$12000$RJubOgT7a0Kp$pq2n0N9+HUq49f80Bk75nky2NBlWX+lZAa00ixW+l+A=", is_superuser = True),
        User (date_joined = "2014-09-23T04:31:32Z", last_login = "2014-09-23T04:31:32Z", first_name = "Richard", last_name = "Thomas", is_staff = True, username = "RichardThomas", is_active = True, email = "Allattos@gmail.com", password = "pbkdf2_sha256$12000$BK8XF5EbsDeY$o7vwY2vNkNcc2JJEe/d0vwGXqpj2OFpwsaQrTea15Ow=", is_superuser = True),
    ])

class Migration(migrations.Migration):  

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.RunPython (makeAwesomePeople,),
    ]