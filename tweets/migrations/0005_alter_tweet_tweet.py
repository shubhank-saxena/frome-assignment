# Generated by Django 5.0.4 on 2024-04-04 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0004_delete_tweethashtag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='tweet',
            field=models.TextField(),
        ),
    ]
