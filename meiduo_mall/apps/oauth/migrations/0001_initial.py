# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthQQUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('openid', models.CharField(max_length=64, verbose_name='openid', db_index=True)),
            ],
            options={
                'verbose_name': 'QQ登录用户数据',
                'verbose_name_plural': 'QQ登录用户数据',
                'db_table': 'tb_oauth_qq',
            },
        ),
    ]
