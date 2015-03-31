# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('dev_id', models.CharField(unique=True, verbose_name='Device ID', max_length=50)),
                ('reg_id', models.CharField(unique=True, verbose_name='Registration ID', max_length=255)),
                ('name', models.CharField(null=True, blank=True, verbose_name='Name', max_length=255)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('modified_date', models.DateTimeField(verbose_name='Modified date', auto_now=True)),
                ('is_active', models.BooleanField(verbose_name='Is active?', default=False)),
            ],
            options={
                'ordering': ['-modified_date'],
                'verbose_name_plural': 'Devices',
                'abstract': False,
                'verbose_name': 'Device',
            },
            bases=(models.Model,),
        ),
    ]
