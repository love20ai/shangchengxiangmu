# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import django.utils.timezone
import django.contrib.auth.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('areas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', error_messages={'unique': 'A user with that username already exists.'}, unique=True)),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('mobile', models.CharField(max_length=11, verbose_name='手机号', unique=True)),
                ('email_active', models.BooleanField(verbose_name='邮箱验证状态', default=False)),
                ('default_address', models.ForeignKey(verbose_name='默认地址', to='areas.Address', related_name='users', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True)),
                ('groups', models.ManyToManyField(verbose_name='groups', to='auth.Group', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', blank=True)),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', to='auth.Permission', related_name='user_set', help_text='Specific permissions for this user.', related_query_name='user', blank=True)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'tb_users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
