# Generated by Django 4.0.3 on 2022-03-11 15:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_alter_game_cover_image_uri_alter_game_game_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='completion_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 11, 15, 6, 24, 252702, tzinfo=utc), verbose_name='Completion Date'),
            preserve_default=False,
        ),
    ]