# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-09 13:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='用户名')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=64, unique=True, verbose_name='主机名')),
                ('addr', models.GenericIPAddressField(verbose_name='ip地址')),
                ('port', models.IntegerField(verbose_name='端口')),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='主机组名')),
            ],
        ),
        migrations.CreateModel(
            name='HostUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connection_type', models.SmallIntegerField(choices=[(1, 'SSH-Type'), (2, 'Account-Password')], verbose_name='连接主机的方式')),
                ('username', models.CharField(max_length=64, verbose_name='连接到主机的用户名')),
                ('password', models.CharField(max_length=64, verbose_name='连接到远程主机的密码')),
            ],
        ),
        migrations.CreateModel(
            name='HostUserBind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audit.Host')),
                ('host_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audit.HostUser')),
            ],
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='机房名称')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='hostuser',
            unique_together=set([('username', 'password')]),
        ),
        migrations.AddField(
            model_name='hostgroup',
            name='host_user_binds',
            field=models.ManyToManyField(to='audit.HostUserBind'),
        ),
        migrations.AddField(
            model_name='host',
            name='idc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audit.IDC', verbose_name='关联到机房'),
        ),
        migrations.AddField(
            model_name='account',
            name='host_group',
            field=models.ManyToManyField(blank=True, to='audit.HostGroup'),
        ),
        migrations.AddField(
            model_name='account',
            name='host_user_bind',
            field=models.ManyToManyField(blank=True, to='audit.HostUserBind'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='hostuserbind',
            unique_together=set([('host', 'host_user')]),
        ),
    ]
