# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-08-16 10:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0002_auto_20170815_1903'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.SmallIntegerField(choices=[(0, 'cmd'), (1, 'file_transfer')])),
                ('content', models.TextField(verbose_name='任务内容')),
                ('timeout', models.IntegerField(default=300, verbose_name='任务超时时间')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audit.Account')),
                ('host_user_binds', models.ManyToManyField(blank=True, to='audit.HostUserBind')),
            ],
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.SmallIntegerField(choices=[(0, '成功'), (1, '失败'), (2, '超时')])),
                ('host_user_bind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audit.HostUserBind')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audit.Task')),
            ],
        ),
        migrations.AlterField(
            model_name='token',
            name='val',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='token',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='tasklog',
            unique_together=set([('task', 'host_user_bind')]),
        ),
    ]
