# Generated by Django 2.2 on 2020-03-27 16:03

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(error_messages={'unique': 'A user with this already exists.'}, help_text='Please enter a user name', max_length=30, unique=True, verbose_name='用户名')),
                ('password', models.CharField(help_text='Please enter a password', max_length=20, verbose_name='密码')),
                ('register_time', models.DateTimeField(auto_now_add=True, verbose_name='注册日期')),
                ('sex', models.CharField(choices=[('f', '女'), ('m', '男')], help_text='Please enter user', max_length=1, verbose_name='性别')),
                ('head_image', models.ImageField(help_text='Please upload your portrait', upload_to='head', verbose_name='头像')),
                ('email', models.EmailField(blank=True, error_messages={'unique': 'A email with this already exists.'}, help_text='Please write your email', max_length=254, unique=True, verbose_name='邮箱')),
                ('telephone', models.CharField(error_messages={'unique': 'A telephone number with this already exists.'}, help_text='Please write your cell-phone number', max_length=11, unique=True, verbose_name='手机号')),
            ],
            options={
                'verbose_name': '消费者',
                'verbose_name_plural': '消费者',
            },
            managers=[
                ('user_', django.db.models.manager.Manager()),
            ],
        ),
    ]
