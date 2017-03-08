# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-08 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('author_id', models.AutoField(primary_key=True, serialize=False)),
                ('author_name', models.CharField(max_length=100)),
                ('nationality', models.CharField(max_length=100, null=True)),
                ('author_summary', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.AutoField(primary_key=True, serialize=False)),
                ('book_name', models.CharField(max_length=100)),
                ('author_name', models.CharField(max_length=100)),
                ('press_house', models.CharField(max_length=100, null=True)),
                ('translator', models.CharField(max_length=100, null=True)),
                ('publication_date', models.CharField(max_length=100, null=True)),
                ('pages', models.CharField(max_length=100, null=True)),
                ('price', models.CharField(max_length=100, null=True)),
                ('package', models.CharField(max_length=10, null=True)),
                ('isbn', models.BigIntegerField(null=True)),
                ('score', models.DecimalField(decimal_places=1, max_digits=10, null=True)),
                ('evaluate_num', models.IntegerField(null=True)),
                ('collect_num', models.IntegerField(null=True)),
                ('content_summary', models.TextField(null=True)),
                ('title', models.CharField(max_length=100, null=True)),
                ('create_date', models.DateField(null=True)),
                ('author_id', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookEvaluate',
            fields=[
                ('op_id', models.AutoField(primary_key=True, serialize=False)),
                ('book_id', models.IntegerField()),
                ('user_name', models.CharField(max_length=100)),
                ('content', models.TextField(null=True)),
                ('create_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='BookNote',
            fields=[
                ('note_id', models.AutoField(primary_key=True, serialize=False)),
                ('book_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('user_name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100, null=True)),
                ('content', models.TextField(null=True)),
                ('create_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='BookScore',
            fields=[
                ('op_id', models.AutoField(primary_key=True, serialize=False)),
                ('book_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('score', models.IntegerField(null=True)),
                ('create_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='CollectionAuthor',
            fields=[
                ('op_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('author_id', models.IntegerField()),
                ('create_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='CollectionBook',
            fields=[
                ('op_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('book_id', models.IntegerField()),
                ('create_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('tel', models.BigIntegerField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('sex', models.IntegerField(null=True)),
                ('birthday', models.DateField(null=True)),
                ('age', models.IntegerField(null=True)),
                ('province', models.CharField(max_length=50, null=True)),
                ('city', models.CharField(max_length=50, null=True)),
                ('remark', models.CharField(max_length=500, null=True)),
                ('image', models.IntegerField(null=True)),
                ('create_date', models.DateField(null=True)),
            ],
        ),
    ]
