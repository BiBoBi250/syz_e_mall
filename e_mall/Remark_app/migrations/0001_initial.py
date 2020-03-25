# Generated by Django 2.2 on 2020-03-25 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Shop_app', '0001_initial'),
        ('Shopper_app', '0001_initial'),
        ('User_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(choices=[('1', '一星好评'), ('2', '二星好评'), ('3', '三星好评'), ('4', '四星好评'), ('5', '五星好评')], help_text='Please rate the goods', max_length=1, verbose_name='评分')),
                ('reward_content', models.TextField(help_text='Please enter a comment', verbose_name='评论内容')),
                ('reward_time', models.DateTimeField(auto_now_add=True)),
                ('commodity', models.ForeignKey(help_text='您所评分的商品', on_delete=django.db.models.deletion.CASCADE, related_name='remark', to='Shop_app.Commodity', verbose_name='商品')),
                ('consumer', models.ForeignKey(help_text='您所评分的商家', on_delete=django.db.models.deletion.CASCADE, related_name='remark', to='User_app.Consumer', verbose_name='消费者')),
                ('shopper', models.ForeignKey(help_text='评论的商家', on_delete=django.db.models.deletion.CASCADE, related_name='remark', to='Shopper_app.Shoppers', verbose_name='商家')),
            ],
            options={
                'verbose_name': '评论表',
                'verbose_name_plural': '评论表',
            },
        ),
        migrations.CreateModel(
            name='Remark_reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_content', models.TextField(help_text='Please enter a comment', verbose_name='评论内容')),
                ('reply_time', models.DateTimeField(auto_now_add=True)),
                ('remark', models.ForeignKey(help_text='请填写对评论的回复', on_delete=django.db.models.deletion.CASCADE, related_name='remark_reply', to='Remark_app.Remark', verbose_name='评论')),
                ('shopper', models.OneToOneField(help_text='商家', on_delete=django.db.models.deletion.CASCADE, related_name='remark_reply', to=settings.AUTH_USER_MODEL, verbose_name='商家')),
            ],
            options={
                'verbose_name': '评论回复表',
                'verbose_name_plural': '评论回复表',
            },
        ),
    ]
