# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

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
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
        ('events', '__first__'),
        ('results', '__first__'),
        ('locations', '__first__'),
        ('cards', '0002_load_templates'),
    ]

    operations = [
        migrations.RunPython (makeAwesomePeople,),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('logged', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(to='events.Event')),
                ('location', models.ForeignKey(to='locations.Location')),
                ('result', models.ForeignKey(to='results.Result')),
            ],
            options={
                'ordering': ['logged'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('force', models.IntegerField(default=0)),
                ('dash', models.IntegerField(default=0)),
                ('resist', models.IntegerField(default=0)),
                ('charm', models.IntegerField(default=0)),
                ('wisdom', models.IntegerField(default=0)),
                ('power', models.IntegerField(default=0)),
                ('money', models.IntegerField(default=0)),
                ('active_event', models.ForeignKey(to='events.Event', blank=True, null=True)),
                ('active_location', models.ForeignKey(to='locations.Location', blank=True, null=True)),
                ('deck', models.OneToOneField(to='cards.Deck', blank=True, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='log',
            name='user',
            field=models.ForeignKey(to='accounts.Player'),
            preserve_default=True,
        ),
    ]
