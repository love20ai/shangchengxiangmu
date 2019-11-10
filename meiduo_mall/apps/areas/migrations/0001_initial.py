# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('title', models.CharField(max_length=20, verbose_name='地址名称')),
                ('receiver', models.CharField(max_length=20, verbose_name='收货人')),
                ('place', models.CharField(max_length=50, verbose_name='地址')),
                ('mobile', models.CharField(max_length=11, verbose_name='手机')),
                ('tel', models.CharField(max_length=20, verbose_name='固定电话', default='', null=True, blank=True)),
                ('email', models.CharField(max_length=30, verbose_name='电子邮箱', default='', null=True, blank=True)),
                ('is_deleted', models.BooleanField(verbose_name='逻辑删除', default=False)),
            ],
            options={
                'verbose_name': '用户地址',
                'verbose_name_plural': '用户地址',
                'db_table': 'tb_address',
                'ordering': ['-update_time'],
            },
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('parent', models.ForeignKey(verbose_name='上级行政区划', to='areas.Area', related_name='subs', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True)),
            ],
            options={
                'verbose_name': '省市区',
                'verbose_name_plural': '省市区',
                'db_table': 'tb_areas',
            },
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(verbose_name='市', to='areas.Area', related_name='city_addresses', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='address',
            name='district',
            field=models.ForeignKey(verbose_name='区', to='areas.Area', related_name='district_addresses', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='address',
            name='province',
            field=models.ForeignKey(verbose_name='省', to='areas.Area', related_name='province_addresses', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
