# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='oauthqquser',
            name='user',
            field=models.ForeignKey(verbose_name='用户', to=settings.AUTH_USER_MODEL),
        ),
    ]
