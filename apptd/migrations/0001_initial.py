# Generated by Django 2.1.5 on 2020-03-06 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Uname', models.CharField(default='', max_length=20)),
                ('Upaswd', models.IntegerField(default=0)),
            ],
        ),
    ]
